#include "../src/dlssnr_weights.hpp"

#include <array>
#include <cassert>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <string>
#include <vector>

namespace {

void WriteU32(std::ofstream& output, std::uint32_t value) {
  for (unsigned int shift = 0; shift < 32; shift += 8) {
    output.put(static_cast<char>((value >> shift) & 0xffU));
  }
}

void WriteU64(std::ofstream& output, std::uint64_t value) {
  for (unsigned int shift = 0; shift < 64; shift += 8) {
    output.put(static_cast<char>((value >> shift) & 0xffU));
  }
}

std::filesystem::path MakeContainer(dlssnr::OffsetBasis basis) {
  const auto path = std::filesystem::temp_directory_path() /
                    (basis == dlssnr::OffsetBasis::Relative
                         ? "dlssnrw1-relative-test.bin"
                         : "dlssnrw1-absolute-test.bin");
  const std::array<std::string, 3> names{"front.weight", "block24.layer0", "tail.bias"};
  const std::array<std::vector<std::uint8_t>, 3> payloads{
      std::vector<std::uint8_t>{1, 2, 3},
      std::vector<std::uint8_t>{4, 5, 6, 7, 8},
      std::vector<std::uint8_t>{9},
  };
  std::uint32_t index_size = 0;
  for (const auto& name : names) index_size += 1U + static_cast<std::uint32_t>(name.size()) + 16U;
  const std::uint32_t data_offset = 16U + index_size;

  std::ofstream output(path, std::ios::binary | std::ios::trunc);
  output.write(dlssnr::WeightContainer::kMagic.data(), 8);
  WriteU32(output, static_cast<std::uint32_t>(names.size()));
  WriteU32(output, data_offset);
  std::uint64_t cursor = 0;
  for (std::size_t index = 0; index < names.size(); ++index) {
    output.put(static_cast<char>(names[index].size()));
    output.write(names[index].data(), static_cast<std::streamsize>(names[index].size()));
    WriteU64(output, basis == dlssnr::OffsetBasis::Relative ? cursor : data_offset + cursor);
    WriteU64(output, payloads[index].size());
    cursor += payloads[index].size();
  }
  for (const auto& payload : payloads) {
    output.write(reinterpret_cast<const char*>(payload.data()),
                 static_cast<std::streamsize>(payload.size()));
  }
  output.close();
  return path;
}

}  // namespace

int main() {
  for (const auto basis : {dlssnr::OffsetBasis::Relative, dlssnr::OffsetBasis::Absolute}) {
    const auto path = MakeContainer(basis);
    const auto container = dlssnr::WeightContainer::Open(path);
    assert(container.entries().size() == 3);
    assert(container.offset_basis() == basis);
    assert(container.Find("block24.layer0") != nullptr);
    assert((container.Read("block24.layer0") == std::vector<std::uint8_t>{4, 5, 6, 7, 8}));
    assert(container.Find("missing") == nullptr);
    std::filesystem::remove(path);
  }

  const auto bad = std::filesystem::temp_directory_path() / "dlssnrw1-bad-test.bin";
  {
    std::ofstream output(bad, std::ios::binary | std::ios::trunc);
    output << "not-a-container";
  }
  bool rejected = false;
  try {
    (void)dlssnr::WeightContainer::Open(bad);
  } catch (const dlssnr::WeightFormatError&) {
    rejected = true;
  }
  assert(rejected);
  std::filesystem::remove(bad);
  return 0;
}
