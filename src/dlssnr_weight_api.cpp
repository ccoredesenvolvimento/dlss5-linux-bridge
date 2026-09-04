#include "dlssnr_weight_api.h"
#include "dlssnr_weights.hpp"

#include <algorithm>
#include <cstring>
#include <filesystem>
#include <limits>
#include <memory>
#include <new>
#include <string>

namespace {

struct WeightHandleImpl {
  explicit WeightHandleImpl(dlssnr::WeightContainer value)
      : container(std::move(value)) {}
  dlssnr::WeightContainer container;
};

thread_local std::string last_error;

void ClearError() { last_error.clear(); }

DLSSNR_WeightStatus Fail(DLSSNR_WeightStatus status, const std::string& message) {
  last_error = message;
  return status;
}

WeightHandleImpl* AsHandle(DLSSNR_WeightHandle handle) {
  return static_cast<WeightHandleImpl*>(handle);
}

template <typename Function>
DLSSNR_WeightStatus Guard(Function&& function) noexcept {
  try {
    ClearError();
    return function();
  } catch (const dlssnr::WeightFormatError& error) {
    return Fail(DLSSNR_WEIGHT_FORMAT_OR_IO_ERROR, error.what());
  } catch (const std::filesystem::filesystem_error& error) {
    return Fail(DLSSNR_WEIGHT_FORMAT_OR_IO_ERROR, error.what());
  } catch (const std::bad_alloc&) {
    return Fail(DLSSNR_WEIGHT_INTERNAL_ERROR, "memory allocation failed");
  } catch (const std::exception& error) {
    return Fail(DLSSNR_WEIGHT_INTERNAL_ERROR, error.what());
  } catch (...) {
    return Fail(DLSSNR_WEIGHT_INTERNAL_ERROR, "unknown C++ exception");
  }
}

template <typename Path>
DLSSNR_WeightStatus OpenPath(const Path& path, DLSSNR_WeightHandle* out_handle) {
  if (out_handle == nullptr) {
    return Fail(DLSSNR_WEIGHT_INVALID_ARGUMENT, "out_handle is null");
  }
  *out_handle = nullptr;
  auto container = dlssnr::WeightContainer::Open(std::filesystem::path(path));
  auto handle = std::make_unique<WeightHandleImpl>(std::move(container));
  *out_handle = handle.release();
  return DLSSNR_WEIGHT_OK;
}

}  // namespace

DLSSNR_WeightStatus DLSSNR_Weights_OpenUtf8(const char* path,
                                             DLSSNR_WeightHandle* out_handle) {
  return Guard([&]() {
    if (path == nullptr || *path == '\0') {
      if (out_handle != nullptr) *out_handle = nullptr;
      return Fail(DLSSNR_WEIGHT_INVALID_ARGUMENT, "path is empty");
    }
#if defined(_WIN32)
    return OpenPath(std::filesystem::u8path(path), out_handle);
#else
    return OpenPath(path, out_handle);
#endif
  });
}

#if defined(_WIN32)
DLSSNR_WeightStatus DLSSNR_Weights_OpenWide(const wchar_t* path,
                                             DLSSNR_WeightHandle* out_handle) {
  return Guard([&]() {
    if (path == nullptr || *path == L'\0') {
      if (out_handle != nullptr) *out_handle = nullptr;
      return Fail(DLSSNR_WEIGHT_INVALID_ARGUMENT, "path is empty");
    }
    return OpenPath(path, out_handle);
  });
}
#endif

void DLSSNR_Weights_Close(DLSSNR_WeightHandle handle) {
  delete AsHandle(handle);
}

DLSSNR_WeightStatus DLSSNR_Weights_Count(DLSSNR_WeightHandle handle,
                                          uint32_t* out_count) {
  return Guard([&]() {
    if (handle == nullptr || out_count == nullptr) {
      return Fail(DLSSNR_WEIGHT_INVALID_ARGUMENT, "handle/out_count is null");
    }
    const auto count = AsHandle(handle)->container.entries().size();
    if (count > std::numeric_limits<uint32_t>::max()) {
      return Fail(DLSSNR_WEIGHT_INTERNAL_ERROR, "entry count exceeds uint32");
    }
    *out_count = static_cast<uint32_t>(count);
    return DLSSNR_WEIGHT_OK;
  });
}

DLSSNR_WeightStatus DLSSNR_Weights_GetEntry(
    DLSSNR_WeightHandle handle,
    uint32_t index,
    char* name_buffer,
    size_t name_capacity,
    size_t* required_name_bytes,
    uint64_t* file_offset,
    uint64_t* byte_size) {
  return Guard([&]() {
    if (handle == nullptr || required_name_bytes == nullptr ||
        file_offset == nullptr || byte_size == nullptr) {
      return Fail(DLSSNR_WEIGHT_INVALID_ARGUMENT, "required output argument is null");
    }
    const auto& entries = AsHandle(handle)->container.entries();
    if (index >= entries.size()) {
      return Fail(DLSSNR_WEIGHT_OUT_OF_RANGE, "entry index is out of range");
    }
    const auto& entry = entries[index];
    const size_t required = entry.name.size() + 1;
    *required_name_bytes = required;
    *file_offset = entry.file_offset;
    *byte_size = entry.size;
    if (name_buffer == nullptr || name_capacity < required) {
      return Fail(DLSSNR_WEIGHT_BUFFER_TOO_SMALL, "name buffer is too small");
    }
    std::memcpy(name_buffer, entry.name.data(), entry.name.size());
    name_buffer[entry.name.size()] = '\0';
    return DLSSNR_WEIGHT_OK;
  });
}

DLSSNR_WeightStatus DLSSNR_Weights_Read(
    DLSSNR_WeightHandle handle,
    const char* name,
    void* destination,
    uint64_t destination_capacity,
    uint64_t* required_bytes) {
  return Guard([&]() {
    if (handle == nullptr || name == nullptr || *name == '\0' ||
        required_bytes == nullptr) {
      return Fail(DLSSNR_WEIGHT_INVALID_ARGUMENT, "handle/name/required_bytes is invalid");
    }
    const auto* entry = AsHandle(handle)->container.Find(name);
    if (entry == nullptr) {
      *required_bytes = 0;
      return Fail(DLSSNR_WEIGHT_NOT_FOUND, std::string("tensor not found: ") + name);
    }
    *required_bytes = entry->size;
    if (destination == nullptr || destination_capacity < entry->size) {
      return Fail(DLSSNR_WEIGHT_BUFFER_TOO_SMALL, "tensor destination is too small");
    }
    const auto bytes = AsHandle(handle)->container.Read(*entry);
    if (!bytes.empty()) {
      std::memcpy(destination, bytes.data(), bytes.size());
    }
    return DLSSNR_WEIGHT_OK;
  });
}

const char* DLSSNR_Weights_LastError(void) { return last_error.c_str(); }
