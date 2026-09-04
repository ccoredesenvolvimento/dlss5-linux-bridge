#pragma once

#include <algorithm>
#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <limits>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

namespace dlssnr {

class WeightFormatError : public std::runtime_error {
 public:
  explicit WeightFormatError(const std::string& message) : std::runtime_error(message) {}
};

enum class OffsetBasis { Relative, Absolute };

struct WeightEntry {
  std::string name;
  std::uint64_t stored_offset = 0;
  std::uint64_t size = 0;
  std::uint64_t file_offset = 0;
};

class WeightContainer {
 public:
  static constexpr std::array<char, 8> kMagic{{'D', 'L', 'S', 'S', 'N', 'R', 'W', '1'}};
  static constexpr std::uint64_t kHeaderSize = 16;

  static WeightContainer Open(const std::filesystem::path& path,
                              bool require_dense = true) {
    std::ifstream input(path, std::ios::binary);
    if (!input) {
      throw WeightFormatError("cannot open weight container: " + path.string());
    }
    input.seekg(0, std::ios::end);
    const auto end_position = input.tellg();
    if (end_position < 0) {
      throw WeightFormatError("cannot determine weight-container size");
    }
    const auto file_size = static_cast<std::uint64_t>(end_position);
    if (file_size < kHeaderSize) {
      throw WeightFormatError("weight container is smaller than its 16-byte header");
    }
    input.seekg(0, std::ios::beg);

    std::array<char, 8> magic{};
    ReadExact(input, magic.data(), magic.size(), "magic");
    if (magic != kMagic) {
      throw WeightFormatError("invalid DLSSNRW1 magic");
    }
    const std::uint32_t count = ReadU32(input, "tensor count");
    const std::uint32_t data_offset_32 = ReadU32(input, "data offset");
    const std::uint64_t data_offset = data_offset_32;
    if (data_offset < kHeaderSize || data_offset > file_size) {
      throw WeightFormatError("data offset is outside the file");
    }
    if (count > (data_offset - kHeaderSize) / 18U) {
      throw WeightFormatError("tensor count cannot fit in the index region");
    }

    struct RawEntry {
      std::string name;
      std::uint64_t offset;
      std::uint64_t size;
    };
    std::vector<RawEntry> raw;
    raw.reserve(count);
    std::unordered_set<std::string> names;
    for (std::uint32_t index = 0; index < count; ++index) {
      const std::uint8_t name_size = ReadU8(input, "name size");
      if (name_size == 0) {
        throw WeightFormatError("empty tensor name at record " + std::to_string(index));
      }
      std::string name(name_size, '\0');
      ReadExact(input, name.data(), name.size(), "tensor name");
      if (!IsValidUtf8(name)) {
        throw WeightFormatError("invalid UTF-8 tensor name at record " +
                                std::to_string(index));
      }
      if (!names.insert(name).second) {
        throw WeightFormatError("duplicate tensor name: " + name);
      }
      raw.push_back(RawEntry{name, ReadU64(input, "tensor offset"),
                             ReadU64(input, "tensor size")});
    }
    const auto index_end_position = input.tellg();
    if (index_end_position < 0 ||
        static_cast<std::uint64_t>(index_end_position) != data_offset) {
      throw WeightFormatError("index records do not end at the declared data offset");
    }

    auto convert = [&](OffsetBasis basis) -> std::vector<WeightEntry> {
      std::vector<WeightEntry> entries;
      entries.reserve(raw.size());
      for (const auto& item : raw) {
        if (basis == OffsetBasis::Relative &&
            item.offset > std::numeric_limits<std::uint64_t>::max() - data_offset) {
          return {};
        }
        const std::uint64_t file_offset =
            basis == OffsetBasis::Relative ? data_offset + item.offset : item.offset;
        if (file_offset < data_offset || file_offset > file_size ||
            item.size > file_size - file_offset) {
          return {};
        }
        entries.push_back(WeightEntry{item.name, item.offset, item.size, file_offset});
      }
      if (require_dense) {
        std::uint64_t cursor = data_offset;
        for (const auto& item : entries) {
          if (item.file_offset != cursor || item.size > file_size - cursor) {
            return {};
          }
          cursor += item.size;
        }
        if (cursor != file_size) {
          return {};
        }
      }
      return entries;
    };

    auto relative = convert(OffsetBasis::Relative);
    auto absolute = convert(OffsetBasis::Absolute);
    if (relative.empty() && absolute.empty() && count != 0) {
      throw WeightFormatError("tensor offsets do not describe a valid data section");
    }
    OffsetBasis basis = OffsetBasis::Relative;
    std::vector<WeightEntry> entries;
    if (!relative.empty() || (count == 0 && data_offset == file_size)) {
      entries = std::move(relative);
    } else {
      basis = OffsetBasis::Absolute;
      entries = std::move(absolute);
    }

    return WeightContainer(path, file_size, data_offset, basis, std::move(entries));
  }

  const std::filesystem::path& path() const noexcept { return path_; }
  std::uint64_t file_size() const noexcept { return file_size_; }
  std::uint64_t data_offset() const noexcept { return data_offset_; }
  OffsetBasis offset_basis() const noexcept { return offset_basis_; }
  const std::vector<WeightEntry>& entries() const noexcept { return entries_; }

  const WeightEntry* Find(const std::string& name) const noexcept {
    const auto iterator = std::find_if(entries_.begin(), entries_.end(),
                                       [&](const WeightEntry& item) {
                                         return item.name == name;
                                       });
    return iterator == entries_.end() ? nullptr : &*iterator;
  }

  std::vector<std::uint8_t> Read(const WeightEntry& entry) const {
    if (entry.size > static_cast<std::uint64_t>(
                         std::numeric_limits<std::size_t>::max())) {
      throw WeightFormatError("tensor is too large for this process");
    }
    std::ifstream input(path_, std::ios::binary);
    if (!input) {
      throw WeightFormatError("cannot reopen weight container");
    }
    input.seekg(static_cast<std::streamoff>(entry.file_offset), std::ios::beg);
    if (!input) {
      throw WeightFormatError("cannot seek to tensor: " + entry.name);
    }
    std::vector<std::uint8_t> bytes(static_cast<std::size_t>(entry.size));
    if (!bytes.empty()) {
      ReadExact(input, reinterpret_cast<char*>(bytes.data()), bytes.size(),
                "tensor payload");
    }
    return bytes;
  }

  std::vector<std::uint8_t> Read(const std::string& name) const {
    const auto* entry = Find(name);
    if (entry == nullptr) {
      throw WeightFormatError("tensor not found: " + name);
    }
    return Read(*entry);
  }

 private:
  WeightContainer(std::filesystem::path path, std::uint64_t file_size,
                  std::uint64_t data_offset, OffsetBasis basis,
                  std::vector<WeightEntry> entries)
      : path_(std::move(path)),
        file_size_(file_size),
        data_offset_(data_offset),
        offset_basis_(basis),
        entries_(std::move(entries)) {}

  static void ReadExact(std::istream& input, char* destination, std::size_t size,
                        const char* label) {
    if (size == 0) return;
    input.read(destination, static_cast<std::streamsize>(size));
    if (input.gcount() != static_cast<std::streamsize>(size)) {
      throw WeightFormatError(std::string("truncated ") + label);
    }
  }

  static std::uint8_t ReadU8(std::istream& input, const char* label) {
    char byte = 0;
    ReadExact(input, &byte, 1, label);
    return static_cast<std::uint8_t>(static_cast<unsigned char>(byte));
  }

  static std::uint32_t ReadU32(std::istream& input, const char* label) {
    std::array<unsigned char, 4> bytes{};
    ReadExact(input, reinterpret_cast<char*>(bytes.data()), bytes.size(), label);
    return static_cast<std::uint32_t>(bytes[0]) |
           (static_cast<std::uint32_t>(bytes[1]) << 8U) |
           (static_cast<std::uint32_t>(bytes[2]) << 16U) |
           (static_cast<std::uint32_t>(bytes[3]) << 24U);
  }

  static std::uint64_t ReadU64(std::istream& input, const char* label) {
    std::array<unsigned char, 8> bytes{};
    ReadExact(input, reinterpret_cast<char*>(bytes.data()), bytes.size(), label);
    std::uint64_t value = 0;
    for (unsigned int index = 0; index < 8; ++index) {
      value |= static_cast<std::uint64_t>(bytes[index]) << (8U * index);
    }
    return value;
  }

  static bool IsValidUtf8(const std::string& value) noexcept {
    const auto* bytes = reinterpret_cast<const unsigned char*>(value.data());
    std::size_t index = 0;
    while (index < value.size()) {
      const unsigned char lead = bytes[index++];
      if (lead <= 0x7fU) continue;
      unsigned int continuation_count = 0;
      std::uint32_t code_point = 0;
      if ((lead & 0xe0U) == 0xc0U) {
        continuation_count = 1;
        code_point = lead & 0x1fU;
        if (code_point < 2U) return false;
      } else if ((lead & 0xf0U) == 0xe0U) {
        continuation_count = 2;
        code_point = lead & 0x0fU;
      } else if ((lead & 0xf8U) == 0xf0U) {
        continuation_count = 3;
        code_point = lead & 0x07U;
      } else {
        return false;
      }
      if (continuation_count > value.size() - index) return false;
      for (unsigned int offset = 0; offset < continuation_count; ++offset) {
        const unsigned char continuation = bytes[index++];
        if ((continuation & 0xc0U) != 0x80U) return false;
        code_point = (code_point << 6U) | (continuation & 0x3fU);
      }
      if ((continuation_count == 2 && code_point < 0x800U) ||
          (continuation_count == 3 && code_point < 0x10000U) ||
          (code_point >= 0xd800U && code_point <= 0xdfffU) ||
          code_point > 0x10ffffU) {
        return false;
      }
    }
    return true;
  }

  std::filesystem::path path_;
  std::uint64_t file_size_ = 0;
  std::uint64_t data_offset_ = 0;
  OffsetBasis offset_basis_ = OffsetBasis::Relative;
  std::vector<WeightEntry> entries_;
};

}  // namespace dlssnr
