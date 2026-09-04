# Clean-room Daniel-route investigation

This directory investigates the architecture demonstrated by the public
`danielblnc/DLSS-NR-on-AMD` releases without redistributing or executing the
closed installer.

## Confirmed public evidence

- The installer consumes a user-provided `nvngx_dlssnr.dll` and emits a reusable
  `dlssnr_on_amd_weights.bin` alongside `version.dll` and an INI file.
- Release 0.2.9 changed recognition from a whole-DLL hash to matching the embedded
  weights, explicitly supporting repacked DLL builds.
- A working RX 9070 XT installation exposes a `gfx1201` HIP code object with
  network-specific kernels including `k_qkv`, `k_qkv_attn`, `k_expand2`,
  `k_contract2`, `k_swin_var<256>` and `k_conv_res2`.
- The reported runtime uses D3D12/HIP zero-copy interop.  This is consistent with
  the independently demonstrated shared-memory + shared-fence route in
  `skchen17/dlssnr-amd-lab`.

These facts point to a custom HIP reimplementation fed by converted model
weights. They do **not** point to ONNX Runtime being the primary in-game backend.

## Implementation plan

1. **Static installer inspection** — identify container, imports, embedded names,
   weight-file contract and HIP code-object metadata without launching the EXE.
2. **Weight contract** — map the private tensor inventory to a deterministic,
   versioned container independent of NVIDIA CUBIN/SASS launch layout.
3. **Reference graph** — implement the network as explicit stages:
   preprocessing/repack, convolutional encoder, Swin/QKV/attention,
   `expand2 -> activation/FP8 boundary -> contract2`, decoder, history/blend and
   post-processing.
4. **Numerical gates** — validate fixed contracts against private captures.  No
   per-capture fitting and no use of captured intermediate tensors at inference.
5. **Backends** — keep one reference implementation, then lower it separately to
   HIP and ONNX. ONNX success means an actual end-to-end image matches the
   reference within declared tolerances, not merely that export completed.
6. **Game integration** — import shared D3D12 resources into HIP, synchronize with
   an external D3D12 fence, run on a separate HIP stream and return the result to
   the game resource.

## Static-analysis safety

`analyze_installer.py` downloads the public release, checks the release digest,
parses/extracts it as data and reports metadata. It never invokes Wine, Windows,
`CreateProcess`, or the installer itself. Downloaded and extracted binaries are
kept in a temporary directory and excluded from the uploaded report artifact.
