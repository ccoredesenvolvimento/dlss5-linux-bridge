# DLSS-NR portable reconstruction

This directory is the vendor-neutral reconstruction track. Its target is **not**
to call NVIDIA NGX, Daniel's `version.dll`, CUDA, HIP, DirectML, or any other
vendor/runtime-specific binary. The private archive supplied by the researcher
is the source for model weights, tensor metadata, launch evidence and numerical
validation only.

## Definition of success

A result is complete only when all of the following hold:

1. The model is represented by a canonical graph and canonical logical tensors.
2. No NVIDIA physical packing, CUBIN, SASS launch, captured activation, or
   runtime DLL is required during inference.
3. A reference implementation processes an independent frame and temporal state
   from real inputs to final output.
4. Every reconstructed family is validated at its boundary against independent
   captures before the full graph is trusted.
5. The same checkpoint can be executed by interchangeable backends:
   - NumPy/PyTorch reference;
   - ONNX Runtime;
   - ONNX Runtime Web with the WebGPU execution provider;
   - optional direct WGSL kernels for performance.
6. The browser/native runtime owns explicit temporal state; no hidden global
   state is borrowed from the original DLL.

Exporting a file, replaying a fixed capture, or producing a picture through
fitted per-frame corrections does not satisfy these gates.

## Current evidence boundary

The independently closed operator family is split-Swin-512 for blocks 23–30 and
40–47. The remaining encoder/front-end blocks, the 1024-channel ViT bottleneck,
decoder transitions, final readout, history/reprojection and texture I/O remain
separate validation gates. The code must preserve this boundary instead of
silently replacing missing stages with identity operations.

## Portable artifact layout

A generated model directory uses this layout:

```text
model/
  model.json          # graph, tensor contracts, state API and coverage
  weights.bin         # aligned canonical logical tensor payload
  hashes.json         # whole-file and per-tensor integrity
  validation.json     # numerical gates and their provenance
```

`model.json` references byte ranges in `weights.bin`. Weight storage is separate
from execution precision: E4M3 and other original formats may be retained as
compact source encodings, but backends must declare whether they execute them
natively or expand them to FP16/FP32.

## Why ONNX and WebGPU are backends, not the model

The canonical graph is the source of truth. ONNX export is generated from that
graph and is rejected when it omits a node, changes a state edge, or fails a
numerical comparison. A browser may execute the ONNX model through
`onnxruntime-web/webgpu`; a later optimized backend may lower the same nodes to
WGSL. Neither backend is allowed to redefine the architecture.

## Initial commands

```bash
python -m dlssnr_portable.import_private \
  /path/to/dlssnr-gpt-pro-private-upload-v1.zip \
  --output build/portable-model

python -m dlssnr_portable.inspect build/portable-model/model.json
pytest -q portable/tests
```

The importer never adds private weights to Git. Generated model directories are
ignored and must remain local.
