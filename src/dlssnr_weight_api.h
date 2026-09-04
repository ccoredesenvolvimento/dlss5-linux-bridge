#pragma once

#include <stddef.h>
#include <stdint.h>

#if defined(_WIN32)
#define DLSSNR_API extern "C" __declspec(dllexport)
#else
#define DLSSNR_API extern "C"
#endif

typedef void* DLSSNR_WeightHandle;

typedef enum DLSSNR_WeightStatus {
  DLSSNR_WEIGHT_OK = 0,
  DLSSNR_WEIGHT_INVALID_ARGUMENT = 1,
  DLSSNR_WEIGHT_FORMAT_OR_IO_ERROR = 2,
  DLSSNR_WEIGHT_NOT_FOUND = 3,
  DLSSNR_WEIGHT_BUFFER_TOO_SMALL = 4,
  DLSSNR_WEIGHT_OUT_OF_RANGE = 5,
  DLSSNR_WEIGHT_INTERNAL_ERROR = 6
} DLSSNR_WeightStatus;

// Opens a DLSSNRW1 file from a UTF-8 path. The caller owns *out_handle and must
// release it with DLSSNR_Weights_Close.
DLSSNR_API DLSSNR_WeightStatus DLSSNR_Weights_OpenUtf8(
    const char* path, DLSSNR_WeightHandle* out_handle);

#if defined(_WIN32)
// Native Windows path variant for game directories containing non-ASCII text.
DLSSNR_API DLSSNR_WeightStatus DLSSNR_Weights_OpenWide(
    const wchar_t* path, DLSSNR_WeightHandle* out_handle);
#endif

DLSSNR_API void DLSSNR_Weights_Close(DLSSNR_WeightHandle handle);

DLSSNR_API DLSSNR_WeightStatus DLSSNR_Weights_Count(
    DLSSNR_WeightHandle handle, uint32_t* out_count);

// Returns metadata for an entry. required_name_bytes includes the terminating
// NUL. Passing name_buffer=nullptr/name_capacity=0 is a valid size query.
DLSSNR_API DLSSNR_WeightStatus DLSSNR_Weights_GetEntry(
    DLSSNR_WeightHandle handle,
    uint32_t index,
    char* name_buffer,
    size_t name_capacity,
    size_t* required_name_bytes,
    uint64_t* file_offset,
    uint64_t* byte_size);

// Reads a complete tensor by logical name. required_bytes is always populated
// on success or BUFFER_TOO_SMALL. A null destination is a valid size query.
DLSSNR_API DLSSNR_WeightStatus DLSSNR_Weights_Read(
    DLSSNR_WeightHandle handle,
    const char* name,
    void* destination,
    uint64_t destination_capacity,
    uint64_t* required_bytes);

// Thread-local diagnostic text for the most recent API failure.
DLSSNR_API const char* DLSSNR_Weights_LastError(void);
