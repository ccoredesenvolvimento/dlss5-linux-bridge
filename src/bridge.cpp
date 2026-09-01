// Independent interoperability research prototype.
// This source does not contain or redistribute NVIDIA binaries.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <d3d12.h>

#include <nvsdk_ngx.h>

namespace {

HMODULE GetNeuralModule() {
  static HMODULE module = LoadLibraryW(L"nvngx_dlssnr.dll");
  return module;
}

template <typename T>
T ResolveNeural(const char* name) {
  HMODULE module = GetNeuralModule();
  return module == nullptr ? nullptr : reinterpret_cast<T>(GetProcAddress(module, name));
}

HMODULE GetDlssModule() {
  static HMODULE module = LoadLibraryW(L"nvngx_dlss_real.dll");
  return module;
}

template <typename T>
T ResolveDlss(const char* name) {
  HMODULE module = GetDlssModule();
  return module == nullptr ? nullptr : reinterpret_cast<T>(GetProcAddress(module, name));
}

using Init = NVSDK_NGX_Result (*)(unsigned long long, const wchar_t*, ID3D12Device*,
                                 NVSDK_NGX_Version, const NVSDK_NGX_Parameter*);
using Create = NVSDK_NGX_Result (*)(ID3D12GraphicsCommandList*, NVSDK_NGX_Feature,
                                   const NVSDK_NGX_Parameter*, NVSDK_NGX_Handle**);
using Evaluate = NVSDK_NGX_Result (*)(ID3D12GraphicsCommandList*, const NVSDK_NGX_Handle*,
                                     const NVSDK_NGX_Parameter*,
                                     PFN_NVSDK_NGX_ProgressCallback);
using Release = NVSDK_NGX_Result (*)(NVSDK_NGX_Handle*);
using Shutdown = NVSDK_NGX_Result (*)(ID3D12Device*);

}  // namespace

extern "C" __declspec(dllexport) __declspec(noinline) NVSDK_NGX_Result Bridge_Init(
    unsigned long long application_id, const wchar_t* data_path, ID3D12Device* device,
    NVSDK_NGX_Version api_version, const NVSDK_NGX_Parameter* feature_info) {
  auto function = ResolveNeural<Init>("NVSDK_NGX_D3D12_Init_Ext");
  if (function == nullptr) return NVSDK_NGX_Result_FAIL_PlatformError;
  volatile NVSDK_NGX_Result result =
      function(application_id, data_path, device, api_version, feature_info);
  return result;
}

extern "C" __declspec(dllexport) __declspec(noinline) NVSDK_NGX_Result Bridge_Create(
    ID3D12GraphicsCommandList* commands, NVSDK_NGX_Feature feature_id,
    const NVSDK_NGX_Parameter* parameters, NVSDK_NGX_Handle** handle) {
  auto function = ResolveNeural<Create>("NVSDK_NGX_D3D12_CreateFeature");
  if (function == nullptr) return NVSDK_NGX_Result_FAIL_PlatformError;
  volatile NVSDK_NGX_Result result = function(commands, feature_id, parameters, handle);
  return result;
}

extern "C" __declspec(dllexport) __declspec(noinline) NVSDK_NGX_Result Bridge_Evaluate(
    ID3D12GraphicsCommandList* commands, const NVSDK_NGX_Handle* handle,
    const NVSDK_NGX_Parameter* parameters, PFN_NVSDK_NGX_ProgressCallback callback) {
  auto function = ResolveNeural<Evaluate>("NVSDK_NGX_D3D12_EvaluateFeature");
  if (function == nullptr) return NVSDK_NGX_Result_FAIL_PlatformError;
  volatile NVSDK_NGX_Result result = function(commands, handle, parameters, callback);
  return result;
}

extern "C" __declspec(dllexport) __declspec(noinline) NVSDK_NGX_Result Bridge_Release(
    NVSDK_NGX_Handle* handle) {
  auto function = ResolveNeural<Release>("NVSDK_NGX_D3D12_ReleaseFeature");
  if (function == nullptr) return NVSDK_NGX_Result_FAIL_PlatformError;
  volatile NVSDK_NGX_Result result = function(handle);
  return result;
}

extern "C" __declspec(dllexport) __declspec(noinline) NVSDK_NGX_Result Bridge_Shutdown(
    ID3D12Device* device) {
  auto function = ResolveNeural<Shutdown>("NVSDK_NGX_D3D12_Shutdown1");
  if (function == nullptr) return NVSDK_NGX_Result_FAIL_PlatformError;
  volatile NVSDK_NGX_Result result = function(device);
  return result;
}

extern "C" __declspec(dllexport) __declspec(noinline) NVSDK_NGX_Result Bridge_DLSS_Init(
    unsigned long long application_id, const wchar_t* data_path, ID3D12Device* device,
    NVSDK_NGX_Version api_version, const NVSDK_NGX_Parameter* feature_info) {
  auto function = ResolveDlss<Init>("NVSDK_NGX_D3D12_Init_Ext");
  if (function == nullptr) return NVSDK_NGX_Result_FAIL_PlatformError;
  volatile NVSDK_NGX_Result result =
      function(application_id, data_path, device, api_version, feature_info);
  return result;
}

extern "C" __declspec(dllexport) __declspec(noinline) NVSDK_NGX_Result Bridge_DLSS_Create(
    ID3D12GraphicsCommandList* commands, NVSDK_NGX_Feature feature_id,
    const NVSDK_NGX_Parameter* parameters, NVSDK_NGX_Handle** handle) {
  auto function = ResolveDlss<Create>("NVSDK_NGX_D3D12_CreateFeature");
  if (function == nullptr) return NVSDK_NGX_Result_FAIL_PlatformError;
  volatile NVSDK_NGX_Result result = function(commands, feature_id, parameters, handle);
  return result;
}

extern "C" __declspec(dllexport) __declspec(noinline) NVSDK_NGX_Result Bridge_DLSS_Evaluate(
    ID3D12GraphicsCommandList* commands, const NVSDK_NGX_Handle* handle,
    const NVSDK_NGX_Parameter* parameters, PFN_NVSDK_NGX_ProgressCallback callback) {
  auto function = ResolveDlss<Evaluate>("NVSDK_NGX_D3D12_EvaluateFeature");
  if (function == nullptr) return NVSDK_NGX_Result_FAIL_PlatformError;
  volatile NVSDK_NGX_Result result = function(commands, handle, parameters, callback);
  return result;
}

extern "C" __declspec(dllexport) __declspec(noinline) NVSDK_NGX_Result Bridge_DLSS_Release(
    NVSDK_NGX_Handle* handle) {
  auto function = ResolveDlss<Release>("NVSDK_NGX_D3D12_ReleaseFeature");
  if (function == nullptr) return NVSDK_NGX_Result_FAIL_PlatformError;
  volatile NVSDK_NGX_Result result = function(handle);
  return result;
}

extern "C" __declspec(dllexport) __declspec(noinline) NVSDK_NGX_Result Bridge_DLSS_Shutdown(
    ID3D12Device* device) {
  auto function = ResolveDlss<Shutdown>("NVSDK_NGX_D3D12_Shutdown1");
  if (function == nullptr) return NVSDK_NGX_Result_FAIL_PlatformError;
  volatile NVSDK_NGX_Result result = function(device);
  return result;
}
