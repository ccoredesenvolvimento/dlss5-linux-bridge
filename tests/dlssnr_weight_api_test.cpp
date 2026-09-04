#include "../src/dlssnr_weight_api.h"
#include "../src/dlssnr_weights.hpp"

#include <array>
#include <cassert>
#include <cstdint>
#include <cstring>
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

std::filesystem::path MakeContainer() {
  const auto path = std::filesystem::temp_directory_path() / "dlssnrw1-api-test.bin";
  const std::array<std::string, 2> names{"block24.layer0.layer", "tail.bias"};
  const std::array<std::vector<std::uint8_t>, 2> payloads{
      std::vector<std::uint8_t>{1, 3, 5, 7},
      std::vector<std::uint8_t>{2, 4},
  };
  std::uint32_t index_size = 0;
  for (const auto& name : names) {
    index_size += 1U + static_cast<std::uint32_t>(name.size()) + 16U;
  }
  const std::uint32_t data_offset = 16U + index_size;
  std::ofstream output(path, std::ios::binary | std::ios::trunc);
  output.write(dlssnr::WeightContainer::kMagic.data(), 8);
  WriteU32(output, 2);
  WriteU32(output, data_offset);
  std::uint64_t cursor = 0;
  for (std::size_t index = 0; index < names.size(); ++index) {
    output.put(static_cast<char>(names[index].size()));
    output.write(names[index].data(), static_cast<std::streamsize>(names[index].size()));
    WriteU64(output, cursor);
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
  const auto path = MakeContainer();
  DLSSNR_WeightHandle handle = nullptr;
  assert(DLSSNR_Weights_OpenUtf8(path.string().c_str(), &handle) == DLSSNR_WEIGHT_OK);
  assert(handle != nullptr);

  std::uint32_t count = 0;
  assert(DLSSNR_Weights_Count(handle, &count) == DLSSNR_WEIGHT_OK);
  assert(count == 2);

  std::size_t required_name = 0;
  std::uint64_t file_offset = 0;
  std::uint64_t byte_size = 0;
  assert(DLSSNR_Weights_GetEntry(handle, 0, nullptr, 0, &required_name,
                                 &file_offset, &byte_size) ==
         DLSSNR_WEIGHT_BUFFER_TOO_SMALL);
  assert(required_name == std::strlen("block24.layer0.layer") + 1);
  assert(byte_size == 4);
  std::vector<char> name(required_name);
  assert(DLSSNR_Weights_GetEntry(handle, 0, name.data(), name.size(),
                                 &required_name, &file_offset, &byte_size) ==
         DLSSNR_WEIGHT_OK);
  assert(std::string(name.data()) == "block24.layer0.layer");

  std::uint64_t required_bytes = 0;
  assert(DLSSNR_Weights_Read(handle, name.data(), nullptr, 0, &required_bytes) ==
         DLSSNR_WEIGHT_BUFFER_TOO_SMALL);
  assert(required_bytes == 4);
  std::vector<std::uint8_t> bytes(required_bytes);
  assert(DLSSNR_Weights_Read(handle, name.data(), bytes.data(), bytes.size(),
                             &required_bytes) == DLSSNR_WEIGHT_OK);
  assert((bytes == std::vector<std::uint8_t>{1, 3, 5, 7}));

  assert(DLSSNR_Weights_Read(handle, "missing", nullptr, 0, &required_bytes) ==
         DLSSNR_WEIGHT_NOT_FOUND);
  assert(std::strlen(DLSSNR_Weights_LastError()) > 0);
  assert(DLSSNR_Weights_GetEntry(handle, 9, nullptr, 0, &required_name,
                                 &file_offset, &byte_size) ==
         DLSSNR_WEIGHT_OUT_OF_RANGE);

  DLSSNR_Weights_Close(handle);
  std::filesystem::remove(path);

  handle = reinterpret_cast<void*>(1);
  assert(DLSSNR_Weights_OpenUtf8("/definitely/missing/dlssnr.bin", &handle) ==
         DLSSNR_WEIGHT_FORMAT_OR_IO_ERROR);
  assert(handle == nullptr);
  assert(std::strlen(DLSSNR_Weights_LastError()) > 0);
  return 0;
}
