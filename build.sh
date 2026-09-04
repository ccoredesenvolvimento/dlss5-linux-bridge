#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${NGX_SDK_DIR:-}" ]]; then
  echo "NGX_SDK_DIR must point to a legally obtained NVIDIA DLSS/NGX SDK." >&2
  exit 2
fi

if [[ -n "${CXX:-}" ]]; then
  compiler="${CXX}"
elif [[ -n "${LLVM_MINGW_ROOT:-}" ]]; then
  compiler="${LLVM_MINGW_ROOT}/bin/x86_64-w64-mingw32-clang++"
else
  compiler="x86_64-w64-mingw32-clang++"
fi

if [[ ! -x "${compiler}" ]] && ! command -v "${compiler}" >/dev/null 2>&1; then
  echo "Windows x86-64 cross-compiler not found: ${compiler}" >&2
  exit 3
fi

if [[ ! -f "${NGX_SDK_DIR}/include/nvsdk_ngx.h" ]]; then
  echo "Missing ${NGX_SDK_DIR}/include/nvsdk_ngx.h" >&2
  exit 4
fi

output_dir="${OUT_DIR:-build}"
mkdir -p "${output_dir}"

common_flags=(
  -std=c++17
  -O2
  -Wall
  -Wextra
  -Wpedantic
  -DNDEBUG
  -DNOMINMAX
  -I"${NGX_SDK_DIR}/include"
  -shared
  -static-libgcc
  -static-libstdc++
)

"${compiler}" "${common_flags[@]}" \
  src/bridge.cpp \
  -o "${output_dir}/bridge-nvngx.dll" \
  -ld3d12 -ldxgi

"${compiler}" "${common_flags[@]}" \
  src/core_proxy.cpp \
  src/dlssnr_weight_api.cpp \
  src/core_proxy.def \
  -o "${output_dir}/_nvngx.dll" \
  -ld3d12 -ldxgi

echo "Built ${output_dir}/bridge-nvngx.dll"
echo "Built ${output_dir}/_nvngx.dll (including DLSSNRW1 weight API)"
