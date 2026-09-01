# DLSS Neural Rendering bridge for Linux/Proton

Minimal NGX/D3D12 bridge used to run a Neural Rendering stage after a game's
existing DLSS pass under Linux/Proton.

```text
Game -> NGX/D3D12 proxy -> original DLSS -> Neural Rendering -> game output
```

The proxy intercepts the relevant D3D12 NGX calls, preserves the original DLSS
path, evaluates `NVSDK_NGX_Feature_Reserved18` with the frame resources supplied
by the game, and copies the neural result back to the expected output.

## Included

- `src/core_proxy.cpp`: NGX forwarding proxy and DLSS/NR chaining logic.
- `src/core_proxy.def`: forwarded NGX exports.
- `src/bridge.cpp`: runtime loader for the user-supplied DLSS and NR DLLs.
- `build.sh`: Linux cross-build script using LLVM-MinGW.

No NVIDIA DLL, SDK header, CUBIN, model weight, executable, game file, capture or
log is included.

## Build

Requirements:

- a legally obtained NVIDIA DLSS/NGX SDK for its headers;
- LLVM-MinGW targeting Windows x86-64; and
- Linux with a working Proton/VKD3D D3D12 setup.

```bash
export NGX_SDK_DIR=/path/to/nvidia-dlss-sdk
export LLVM_MINGW_ROOT=/path/to/llvm-mingw
./build.sh
```

Output:

```text
build/_nvngx.dll
build/bridge-nvngx.dll
```

The user must provide compatible, legally obtained copies of:

```text
_nvngx_real.dll
nvngx_dlss_real.dll
nvngx_dlssnr.dll
```

This is an experimental interoperability proof of concept, not a universal
installer. The reserved feature and its parameter contract are not a stable
public API. Incorrect resource formats or states can cause black frames, crashes
or device loss.

A vendor-neutral Vulkan/HIP/ZLUDA `.so` that recreates the neural pipeline is a
possible follow-up, but is not implemented in this repository.

## Notice

This repository contains independently written bridge code only and is not
affiliated with or endorsed by NVIDIA. NVIDIA, GeForce, RTX, NGX and DLSS are
trademarks of NVIDIA Corporation. Users are responsible for complying with the
licenses of their SDK, runtimes, applications and drivers.
