// Independent interoperability research prototype.
// This source does not contain or redistribute NVIDIA binaries.
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <d3d12.h>
#include <wrl/client.h>

#include <cstdarg>
#include <cstdint>
#include <cstdio>
#include <mutex>
#include <unordered_map>

#include <nvsdk_ngx.h>

using Microsoft::WRL::ComPtr;

namespace {

using Init = NVSDK_NGX_Result (*)(unsigned long long, const wchar_t*, ID3D12Device*,
                                 NVSDK_NGX_Version, const NVSDK_NGX_Parameter*);
using CoreInit = NVSDK_NGX_Result (*)(unsigned long long, const wchar_t*, ID3D12Device*,
                                     NVSDK_NGX_Version);
using CoreInitExt = NVSDK_NGX_Result (*)(unsigned long long, const wchar_t*, ID3D12Device*,
                                        NVSDK_NGX_Version, const NVSDK_NGX_Parameter*);
using GetFeatureRequirements = NVSDK_NGX_Result (*)(
    IDXGIAdapter*, const NVSDK_NGX_FeatureDiscoveryInfo*,
    NVSDK_NGX_FeatureRequirement*);
using Create = NVSDK_NGX_Result (*)(ID3D12GraphicsCommandList*, NVSDK_NGX_Feature,
                                   const NVSDK_NGX_Parameter*, NVSDK_NGX_Handle**);
using Evaluate = NVSDK_NGX_Result (*)(ID3D12GraphicsCommandList*, const NVSDK_NGX_Handle*,
                                     const NVSDK_NGX_Parameter*,
                                     PFN_NVSDK_NGX_ProgressCallback);
using Release = NVSDK_NGX_Result (*)(NVSDK_NGX_Handle*);
using Shutdown = NVSDK_NGX_Result (*)(ID3D12Device*);

struct FeatureState {
  NVSDK_NGX_Handle* neural_handle = nullptr;
  unsigned int input_width = 0;
  unsigned int input_height = 0;
  unsigned int output_width = 0;
  unsigned int output_height = 0;
  ComPtr<ID3D12Resource> private_output;
  ID3D12Resource* observed_output = nullptr;
  unsigned long long evaluations = 0;
};

std::mutex state_mutex;
std::unordered_map<const NVSDK_NGX_Handle*, FeatureState> features;
ComPtr<ID3D12Device> device;
HMODULE bridge = nullptr;
HMODULE core_module = nullptr;
CoreInit core_init = nullptr;
CoreInitExt core_init_ext = nullptr;
GetFeatureRequirements core_get_feature_requirements = nullptr;
Create core_create = nullptr;
Evaluate core_evaluate = nullptr;
Release core_release = nullptr;
Init dlss_init = nullptr;
Create dlss_create = nullptr;
Evaluate dlss_evaluate = nullptr;
Release dlss_release = nullptr;
Init nr_init = nullptr;
Create nr_create = nullptr;
Evaluate nr_evaluate = nullptr;
Release nr_release = nullptr;
Shutdown nr_shutdown = nullptr;
bool neural_ready = false;
bool standard_ready = false;
bool snippets_initialized = false;

void Log(const char* format, ...) {
  FILE* file = std::fopen("dlssnr-proxy.log", "a");
  if (file == nullptr) return;
  SYSTEMTIME time{};
  GetLocalTime(&time);
  std::fprintf(file, "%02u:%02u:%02u.%03u ", time.wHour, time.wMinute,
               time.wSecond, time.wMilliseconds);
  va_list arguments;
  va_start(arguments, format);
  std::vfprintf(file, format, arguments);
  va_end(arguments);
  std::fputc('\n', file);
  std::fclose(file);
}

template <typename T>
T Resolve(HMODULE module, const char* name) {
  return module == nullptr ? nullptr : reinterpret_cast<T>(GetProcAddress(module, name));
}

bool EnsureRuntime() {
  if (bridge != nullptr && core_module != nullptr) {
    return core_init && core_init_ext && core_create && core_evaluate && core_release &&
           dlss_init && dlss_create && dlss_evaluate && dlss_release;
  }
  core_module = LoadLibraryW(L"_nvngx_real.dll");
  if (core_module == nullptr) {
    Log("LoadLibrary(_nvngx_real.dll) failed win32=%lu", GetLastError());
    return false;
  }
  bridge = LoadLibraryW(L"bridge-nvngx.dll");
  if (bridge == nullptr) {
    Log("LoadLibrary(bridge-nvngx.dll) failed win32=%lu", GetLastError());
    return false;
  }
  core_init = Resolve<CoreInit>(core_module, "NVSDK_NGX_D3D12_Init");
  core_init_ext = Resolve<CoreInitExt>(core_module, "NVSDK_NGX_D3D12_Init_Ext");
  core_get_feature_requirements = Resolve<GetFeatureRequirements>(
      core_module, "NVSDK_NGX_D3D12_GetFeatureRequirements");
  core_create = Resolve<Create>(core_module, "NVSDK_NGX_D3D12_CreateFeature");
  core_evaluate = Resolve<Evaluate>(core_module, "NVSDK_NGX_D3D12_EvaluateFeature");
  core_release = Resolve<Release>(core_module, "NVSDK_NGX_D3D12_ReleaseFeature");
  dlss_init = Resolve<Init>(bridge, "Bridge_DLSS_Init");
  dlss_create = Resolve<Create>(bridge, "Bridge_DLSS_Create");
  dlss_evaluate = Resolve<Evaluate>(bridge, "Bridge_DLSS_Evaluate");
  dlss_release = Resolve<Release>(bridge, "Bridge_DLSS_Release");
  nr_init = Resolve<Init>(bridge, "Bridge_Init");
  nr_create = Resolve<Create>(bridge, "Bridge_Create");
  nr_evaluate = Resolve<Evaluate>(bridge, "Bridge_Evaluate");
  nr_release = Resolve<Release>(bridge, "Bridge_Release");
  nr_shutdown = Resolve<Shutdown>(bridge, "Bridge_Shutdown");
  const bool complete = core_init && core_init_ext && core_get_feature_requirements &&
                        core_create && core_evaluate &&
                        core_release && dlss_init && dlss_create && dlss_evaluate &&
                        dlss_release && nr_init && nr_create && nr_evaluate && nr_release &&
                        nr_shutdown;
  Log("runtime resolved complete=%d", complete ? 1 : 0);
  return complete;
}

void InitializeSnippets(unsigned long long application_id, const wchar_t* data_path,
                        ID3D12Device* input_device, NVSDK_NGX_Version api_version,
                        const NVSDK_NGX_Parameter* feature_info) {
  if (snippets_initialized) return;
  device = input_device;
  const NVSDK_NGX_Result standard_result =
      dlss_init(application_id, data_path, input_device, api_version, feature_info);
  standard_ready = NVSDK_NGX_SUCCEED(standard_result);
  Log("direct DLSS Init_Ext result=0x%08x ready=%d", standard_result,
      standard_ready ? 1 : 0);
  const NVSDK_NGX_Result neural_result =
      nr_init(application_id, data_path, input_device, api_version, feature_info);
  neural_ready = NVSDK_NGX_SUCCEED(neural_result);
  Log("DLSSNR Init_Ext result=0x%08x ready=%d", neural_result,
      neural_ready ? 1 : 0);
  snippets_initialized = true;
}

void SetFloatParameter(NVSDK_NGX_Parameter* parameters, const char* name, float value) {
  using Function = void (*)(NVSDK_NGX_Parameter*, const char*, float);
  auto** table = *reinterpret_cast<void***>(parameters);
  reinterpret_cast<Function>(table[6])(parameters, name, value);
}

void SetIntParameter(NVSDK_NGX_Parameter* parameters, const char* name, int value) {
  using Function = void (*)(NVSDK_NGX_Parameter*, const char*, int);
  auto** table = *reinterpret_cast<void***>(parameters);
  reinterpret_cast<Function>(table[3])(parameters, name, value);
}

NVSDK_NGX_Result GetFloatParameter(const NVSDK_NGX_Parameter* parameters,
                                   const char* name, float* value) {
  using Function = NVSDK_NGX_Result (*)(const NVSDK_NGX_Parameter*, const char*, float*);
  auto** table = *reinterpret_cast<void***>(const_cast<NVSDK_NGX_Parameter*>(parameters));
  return reinterpret_cast<Function>(table[14])(parameters, name, value);
}

NVSDK_NGX_Result GetIntParameter(const NVSDK_NGX_Parameter* parameters,
                                 const char* name, int* value) {
  using Function = NVSDK_NGX_Result (*)(const NVSDK_NGX_Parameter*, const char*, int*);
  auto** table = *reinterpret_cast<void***>(const_cast<NVSDK_NGX_Parameter*>(parameters));
  return reinterpret_cast<Function>(table[11])(parameters, name, value);
}

NVSDK_NGX_Result GetResourceParameter(const NVSDK_NGX_Parameter* parameters,
                                      const char* name, ID3D12Resource** value) {
  using Function = NVSDK_NGX_Result (*)(const NVSDK_NGX_Parameter*, const char*,
                                        ID3D12Resource**);
  auto** table = *reinterpret_cast<void***>(const_cast<NVSDK_NGX_Parameter*>(parameters));
  return reinterpret_cast<Function>(table[8])(parameters, name, value);
}

NVSDK_NGX_Result ScalingRatioCallback(NVSDK_NGX_Parameter* parameters) {
  if (parameters == nullptr) return NVSDK_NGX_Result_FAIL_InvalidParameter;
  SetFloatParameter(parameters, "DLSSNR.ScalingRatio", 1.0F);
  return NVSDK_NGX_Result_Success;
}

void SetResource(NVSDK_NGX_Parameter* parameters, const char* name,
                 ID3D12Resource* resource) {
  using Function = void (*)(NVSDK_NGX_Parameter*, const char*, ID3D12Resource*);
  auto** table = *reinterpret_cast<void***>(parameters);
  reinterpret_cast<Function>(table[0])(parameters, name, resource);
}

void Transition(ID3D12GraphicsCommandList* commands, ID3D12Resource* resource,
                D3D12_RESOURCE_STATES before, D3D12_RESOURCE_STATES after) {
  D3D12_RESOURCE_BARRIER barrier{};
  barrier.Type = D3D12_RESOURCE_BARRIER_TYPE_TRANSITION;
  barrier.Transition.pResource = resource;
  barrier.Transition.Subresource = D3D12_RESOURCE_BARRIER_ALL_SUBRESOURCES;
  barrier.Transition.StateBefore = before;
  barrier.Transition.StateAfter = after;
  commands->ResourceBarrier(1, &barrier);
}

bool EnsurePrivateOutput(FeatureState& state, ID3D12Resource* game_output) {
  if (state.private_output && state.observed_output == game_output) return true;
  if (!device || game_output == nullptr) return false;
  D3D12_RESOURCE_DESC description = game_output->GetDesc();
  if (description.Dimension != D3D12_RESOURCE_DIMENSION_TEXTURE2D) return false;
  description.Flags |= D3D12_RESOURCE_FLAG_ALLOW_UNORDERED_ACCESS;
  description.Flags &= ~D3D12_RESOURCE_FLAG_DENY_SHADER_RESOURCE;
  D3D12_HEAP_PROPERTIES heap{};
  heap.Type = D3D12_HEAP_TYPE_DEFAULT;
  heap.CreationNodeMask = 1;
  heap.VisibleNodeMask = 1;
  ComPtr<ID3D12Resource> output;
  const HRESULT hr = device->CreateCommittedResource(
      &heap, D3D12_HEAP_FLAG_NONE, &description,
      D3D12_RESOURCE_STATE_UNORDERED_ACCESS, nullptr, IID_PPV_ARGS(&output));
  if (FAILED(hr)) {
    Log("private output creation failed hr=0x%08x format=%u flags=0x%x", hr,
        static_cast<unsigned int>(description.Format),
        static_cast<unsigned int>(description.Flags));
    return false;
  }
  state.private_output = output;
  state.observed_output = game_output;
  Log("private output created %ux%u format=%u flags=0x%x", state.output_width,
      state.output_height, static_cast<unsigned int>(description.Format),
      static_cast<unsigned int>(description.Flags));
  return true;
}

}  // namespace

extern "C" NVSDK_NGX_Result ProxyCore_D3D12_GetFeatureRequirements(
    IDXGIAdapter* adapter, const NVSDK_NGX_FeatureDiscoveryInfo* discovery,
    NVSDK_NGX_FeatureRequirement* requirement) {
  std::lock_guard<std::mutex> lock(state_mutex);
  if (!EnsureRuntime()) return NVSDK_NGX_Result_FAIL_PlatformError;
  const NVSDK_NGX_Result result =
      core_get_feature_requirements(adapter, discovery, requirement);
  const int feature = discovery == nullptr ? -1 : static_cast<int>(discovery->FeatureID);
  const unsigned int support = requirement == nullptr
                                   ? 0xffffffffU
                                   : static_cast<unsigned int>(requirement->FeatureSupported);
  const unsigned int minimum_architecture =
      requirement == nullptr ? 0xffffffffU : requirement->MinHWArchitecture;
  Log("real core GetFeatureRequirements result=0x%08x feature=%d support=0x%x min_arch=0x%x adapter=%p",
      result, feature, support, minimum_architecture, adapter);
  return result;
}

extern "C" NVSDK_NGX_Result ProxyCore_D3D12_Init(
    unsigned long long application_id, const wchar_t* data_path, ID3D12Device* input_device,
    NVSDK_NGX_Version api_version) {
  std::lock_guard<std::mutex> lock(state_mutex);
  if (!EnsureRuntime()) return NVSDK_NGX_Result_FAIL_PlatformError;
  const NVSDK_NGX_Result result =
      core_init(application_id, data_path, input_device, api_version);
  Log("real core Init result=0x%08x app=%llu api=0x%x", result, application_id,
      static_cast<unsigned int>(api_version));
  if (NVSDK_NGX_SUCCEED(result)) {
    InitializeSnippets(application_id, data_path, input_device, api_version, nullptr);
  }
  return result;
}

extern "C" NVSDK_NGX_Result ProxyCore_D3D12_Init_Ext(
    unsigned long long application_id, const wchar_t* data_path, ID3D12Device* input_device,
    NVSDK_NGX_Version api_version, const NVSDK_NGX_Parameter* feature_info) {
  std::lock_guard<std::mutex> lock(state_mutex);
  if (!EnsureRuntime()) return NVSDK_NGX_Result_FAIL_PlatformError;
  const NVSDK_NGX_Result result =
      core_init_ext(application_id, data_path, input_device, api_version, feature_info);
  Log("real core Init_Ext result=0x%08x app=%llu api=0x%x", result, application_id,
      static_cast<unsigned int>(api_version));
  if (NVSDK_NGX_SUCCEED(result)) {
    InitializeSnippets(application_id, data_path, input_device, api_version, feature_info);
  }
  return result;
}

extern "C" NVSDK_NGX_Result ProxyCore_D3D12_CreateFeature(
    ID3D12GraphicsCommandList* commands, NVSDK_NGX_Feature feature_id,
    const NVSDK_NGX_Parameter* input_parameters, NVSDK_NGX_Handle** output_handle) {
  if (!EnsureRuntime()) return NVSDK_NGX_Result_FAIL_PlatformError;
  if (feature_id != NVSDK_NGX_Feature_SuperSampling || !standard_ready) {
    return core_create(commands, feature_id, input_parameters, output_handle);
  }
  const NVSDK_NGX_Result standard_result =
      dlss_create(commands, feature_id, input_parameters, output_handle);
  if (NVSDK_NGX_FAILED(standard_result) || output_handle == nullptr ||
      *output_handle == nullptr) {
    return standard_result;
  }

  std::lock_guard<std::mutex> lock(state_mutex);
  auto* parameters = const_cast<NVSDK_NGX_Parameter*>(input_parameters);
  FeatureState state{};
  int original_quality = 0;
  parameters->Get("Width", &state.input_width);
  parameters->Get("Height", &state.input_height);
  parameters->Get("OutWidth", &state.output_width);
  parameters->Get("OutHeight", &state.output_height);
  parameters->Get("PerfQualityValue", &original_quality);
  if (state.output_width == 0 || state.output_height == 0) {
    Log("DLSSNR create skipped: invalid output dimensions %ux%u", state.output_width,
        state.output_height);
    features.emplace(*output_handle, std::move(state));
    return standard_result;
  }
  if (!neural_ready) {
    Log("DLSSNR create skipped: neural runtime unavailable");
    features.emplace(*output_handle, std::move(state));
    return standard_result;
  }
  parameters->Set("CreationNodeMask", 1U);
  parameters->Set("VisibilityNodeMask", 1U);
  for (const char* name : {"Width", "OutWidth", "DLSSNR.Width", "DLSSNR.InputWidth",
                           "DLSSNR.OutputWidth", "DLSSNR.Output.Width"}) {
    parameters->Set(name, state.output_width);
  }
  for (const char* name : {"Height", "OutHeight", "DLSSNR.Height", "DLSSNR.InputHeight",
                           "DLSSNR.OutputHeight", "DLSSNR.Output.Height"}) {
    parameters->Set(name, state.output_height);
  }
  parameters->Set("DLSSNR.Hint.Render.Preset", 1U);
  parameters->Set("PerfQualityValue", 6);
  parameters->Set("DLSSNRComputeScalingRatioCallback",
                  reinterpret_cast<void*>(&ScalingRatioCallback));
  SetFloatParameter(parameters, "DLSSNR.ScalingRatio", 1.0F);
  SetFloatParameter(parameters, "DLSSNR.Scale", 1.0F);
  SetIntParameter(parameters, "DLSSNR.Upscaling", 0);
  const NVSDK_NGX_Result neural_result = nr_create(
      commands, NVSDK_NGX_Feature_Reserved18, parameters, &state.neural_handle);
  // The game owns this parameter map. Restore every standard-DLSS value changed
  // for neural creation before returning to it.
  parameters->Set("Width", state.input_width);
  parameters->Set("Height", state.input_height);
  parameters->Set("OutWidth", state.output_width);
  parameters->Set("OutHeight", state.output_height);
  parameters->Set("PerfQualityValue", original_quality);
  Log("DLSSNR CreateFeature result=0x%08x standard=%p neural=%p input=%ux%u output=%ux%u",
      neural_result, *output_handle, state.neural_handle, state.input_width,
      state.input_height, state.output_width, state.output_height);
  features.emplace(*output_handle, std::move(state));
  return standard_result;
}

extern "C" NVSDK_NGX_Result ProxyCore_D3D12_EvaluateFeature(
    ID3D12GraphicsCommandList* commands, const NVSDK_NGX_Handle* standard_handle,
    const NVSDK_NGX_Parameter* input_parameters,
    PFN_NVSDK_NGX_ProgressCallback callback) {
  if (!EnsureRuntime()) return NVSDK_NGX_Result_FAIL_PlatformError;
  std::lock_guard<std::mutex> lock(state_mutex);
  auto iterator = features.find(standard_handle);
  if (iterator == features.end()) {
    return core_evaluate(commands, standard_handle, input_parameters, callback);
  }
  FeatureState& state = iterator->second;
  auto* parameters = const_cast<NVSDK_NGX_Parameter*>(input_parameters);
  // NGX Core normally translates public parameter names to the compact keys
  // consumed by a signed snippet. We bypass Core for the signed DLSS call, so
  // reproduce only the aliases required by Super Resolution evaluation.
  ID3D12Resource* color = nullptr;
  ID3D12Resource* game_output = nullptr;
  ID3D12Resource* motion = nullptr;
  ID3D12Resource* depth = nullptr;
  float sharpness = 0.0F;
  float motion_scale_x = 1.0F;
  float motion_scale_y = 1.0F;
  int reset = 0;
  const NVSDK_NGX_Result color_get =
      GetResourceParameter(parameters, NVSDK_NGX_Parameter_Color, &color);
  const NVSDK_NGX_Result output_get =
      GetResourceParameter(parameters, NVSDK_NGX_Parameter_Output, &game_output);
  const NVSDK_NGX_Result motion_get =
      GetResourceParameter(parameters, NVSDK_NGX_Parameter_MotionVectors, &motion);
  const NVSDK_NGX_Result depth_get =
      GetResourceParameter(parameters, NVSDK_NGX_Parameter_Depth, &depth);
  GetFloatParameter(parameters, NVSDK_NGX_Parameter_Sharpness, &sharpness);
  GetFloatParameter(parameters, NVSDK_NGX_Parameter_MV_Scale_X, &motion_scale_x);
  GetFloatParameter(parameters, NVSDK_NGX_Parameter_MV_Scale_Y, &motion_scale_y);
  GetIntParameter(parameters, NVSDK_NGX_Parameter_Reset, &reset);
  SetResource(parameters, NVSDK_NGX_EParameter_Color, color);
  SetResource(parameters, NVSDK_NGX_EParameter_Output, game_output);
  SetResource(parameters, NVSDK_NGX_EParameter_MotionVectors, motion);
  SetResource(parameters, NVSDK_NGX_EParameter_Depth, depth);
  SetFloatParameter(parameters, NVSDK_NGX_EParameter_Sharpness, sharpness);
  SetFloatParameter(parameters, NVSDK_NGX_EParameter_MV_Scale_X, motion_scale_x);
  SetFloatParameter(parameters, NVSDK_NGX_EParameter_MV_Scale_Y, motion_scale_y);
  SetIntParameter(parameters, NVSDK_NGX_EParameter_Reset, reset);
  if (state.evaluations == 0) {
    ID3D12Resource* encrypted_color = nullptr;
    const NVSDK_NGX_Result encrypted_color_get =
        GetResourceParameter(parameters, NVSDK_NGX_EParameter_Color, &encrypted_color);
    Log("resource aliases public=[0x%08x %p,0x%08x %p,0x%08x %p,0x%08x %p] encrypted_color=[0x%08x %p]",
        color_get, color, output_get, game_output, motion_get, motion, depth_get, depth,
        encrypted_color_get, encrypted_color);
  }
  const NVSDK_NGX_Result standard_result =
      dlss_evaluate(commands, standard_handle, input_parameters, callback);
  if (NVSDK_NGX_FAILED(standard_result) || !neural_ready ||
      iterator->second.neural_handle == nullptr) {
    return standard_result;
  }
  if (game_output == nullptr || !EnsurePrivateOutput(state, game_output)) {
    Log("DLSSNR evaluate skipped: output unavailable");
    return standard_result;
  }

  SetResource(parameters, "DLSSNR.Color", game_output);
  SetResource(parameters, "DLSSNR.Output", state.private_output.Get());
  if (motion != nullptr) SetResource(parameters, "DLSSNR.MVec", motion);
  if (depth != nullptr) SetResource(parameters, "DLSSNR.Depth", depth);
  for (const char* name : {"DLSSNR.ColorSubrectWidth", "DLSSNR.OutputSubrectWidth"}) {
    parameters->Set(name, state.output_width);
  }
  for (const char* name : {"DLSSNR.ColorSubrectHeight", "DLSSNR.OutputSubrectHeight"}) {
    parameters->Set(name, state.output_height);
  }
  for (const char* name : {"DLSSNR.MVecSubrectWidth", "DLSSNR.DepthSubrectWidth"}) {
    parameters->Set(name, state.input_width);
  }
  for (const char* name : {"DLSSNR.MVecSubrectHeight", "DLSSNR.DepthSubrectHeight"}) {
    parameters->Set(name, state.input_height);
  }
  SetFloatParameter(parameters, "DLSSNR.MVecScaleX", 1.0F);
  SetFloatParameter(parameters, "DLSSNR.MVecScaleY", 1.0F);
  SetIntParameter(parameters, "DLSSNR.DepthInverted", 0);
  SetIntParameter(parameters, "DLSSNR.Reset", reset);
  SetIntParameter(parameters, "DLSSNR.Enabled", 1);
  SetFloatParameter(parameters, "DLSSNR.Intensity", 1.0F);
  SetFloatParameter(parameters, "DLSSNR.LocalToneStrength", 1.0F);
  SetFloatParameter(parameters, "DLSSNR.LocalStructureStrength", 1.0F);
  SetFloatParameter(parameters, "DLSSNR.GlobalToneStrength", 1.0F);
  SetIntParameter(parameters, "DLSSNR.UseAutoMask", 0);
  SetFloatParameter(parameters, "DLSSNR.SkinStructureStrength", 1.0F);
  SetIntParameter(parameters, "DLSSNR.Style", 0);
  SetIntParameter(parameters, "DLSSNR.UICorrection", 0);

  D3D12_RESOURCE_BARRIER uav_barrier{};
  uav_barrier.Type = D3D12_RESOURCE_BARRIER_TYPE_UAV;
  uav_barrier.UAV.pResource = game_output;
  commands->ResourceBarrier(1, &uav_barrier);
  Transition(commands, game_output, D3D12_RESOURCE_STATE_UNORDERED_ACCESS,
             D3D12_RESOURCE_STATE_NON_PIXEL_SHADER_RESOURCE);
  const NVSDK_NGX_Result neural_result =
      nr_evaluate(commands, state.neural_handle, parameters, nullptr);
  if (NVSDK_NGX_SUCCEED(neural_result)) {
    Transition(commands, state.private_output.Get(), D3D12_RESOURCE_STATE_UNORDERED_ACCESS,
               D3D12_RESOURCE_STATE_COPY_SOURCE);
    Transition(commands, game_output, D3D12_RESOURCE_STATE_NON_PIXEL_SHADER_RESOURCE,
               D3D12_RESOURCE_STATE_COPY_DEST);
    commands->CopyResource(game_output, state.private_output.Get());
    Transition(commands, state.private_output.Get(), D3D12_RESOURCE_STATE_COPY_SOURCE,
               D3D12_RESOURCE_STATE_UNORDERED_ACCESS);
    Transition(commands, game_output, D3D12_RESOURCE_STATE_COPY_DEST,
               D3D12_RESOURCE_STATE_UNORDERED_ACCESS);
  } else {
    Transition(commands, game_output, D3D12_RESOURCE_STATE_NON_PIXEL_SHADER_RESOURCE,
               D3D12_RESOURCE_STATE_UNORDERED_ACCESS);
  }
  ++state.evaluations;
  if (state.evaluations == 1 || state.evaluations % 300 == 0 ||
      NVSDK_NGX_FAILED(neural_result)) {
    Log("DLSSNR Evaluate result=0x%08x frame=%llu output=%p motion=%p depth=%p",
        neural_result, state.evaluations, game_output, motion, depth);
  }
  return standard_result;
}

extern "C" NVSDK_NGX_Result ProxyCore_D3D12_ReleaseFeature(NVSDK_NGX_Handle* handle) {
  if (!EnsureRuntime()) return NVSDK_NGX_Result_FAIL_PlatformError;
  {
    std::lock_guard<std::mutex> lock(state_mutex);
    auto iterator = features.find(handle);
    if (iterator != features.end()) {
      if (iterator->second.neural_handle != nullptr) {
        Log("DLSSNR ReleaseFeature result=0x%08x frames=%llu",
            nr_release(iterator->second.neural_handle), iterator->second.evaluations);
      }
      const NVSDK_NGX_Result result = dlss_release(handle);
      features.erase(iterator);
      return result;
    }
  }
  return core_release(handle);
}

extern "C" NVSDK_NGX_Result ProxyCore_D3D12_Shutdown1(ID3D12Device* input_device) {
  if (!EnsureRuntime()) return NVSDK_NGX_Result_FAIL_PlatformError;
  std::lock_guard<std::mutex> lock(state_mutex);
  for (auto& [handle, state] : features) {
    if (state.neural_handle != nullptr) nr_release(state.neural_handle);
    dlss_release(const_cast<NVSDK_NGX_Handle*>(handle));
  }
  features.clear();
  if (neural_ready) {
    Log("DLSSNR Shutdown1 result=0x%08x", nr_shutdown(input_device));
    neural_ready = false;
  }
  standard_ready = false;
  snippets_initialized = false;
  device.Reset();
  // Direct snippet initialization shares process-global NGX state with the
  // core. Calling either the snippet or real-core shutdown after releasing the
  // direct feature crashes the current driver runtime. This happens only at
  // process teardown, where Windows owns the remaining module allocations.
  Log("Shutdown1 completed; real-core shutdown intentionally skipped");
  return NVSDK_NGX_Result_Success;
}

extern "C" NVSDK_NGX_Result ProxyCore_D3D12_Shutdown() {
  if (!EnsureRuntime()) return NVSDK_NGX_Result_FAIL_PlatformError;
  std::lock_guard<std::mutex> lock(state_mutex);
  for (auto& [handle, state] : features) {
    if (state.neural_handle != nullptr) nr_release(state.neural_handle);
    dlss_release(const_cast<NVSDK_NGX_Handle*>(handle));
  }
  features.clear();
  if (neural_ready && device) nr_shutdown(device.Get());
  neural_ready = false;
  standard_ready = false;
  snippets_initialized = false;
  device.Reset();
  Log("Shutdown completed; real-core shutdown intentionally skipped");
  return NVSDK_NGX_Result_Success;
}
