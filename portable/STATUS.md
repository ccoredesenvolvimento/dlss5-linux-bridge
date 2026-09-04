# Portable reconstruction status

## Current classification

`PARTIAL_PORTABLE_RUNTIME`

The branch is deliberately independent from Daniel's runtime, NVIDIA NGX, CUDA,
HIP and vendor DLLs. It is not yet a complete renderer.

## Implemented foundation

- canonical JSON graph IR with typed tensors, explicit inputs/outputs/state edges,
  storage hashes and topological validation;
- aligned canonical `weights.bin` with per-tensor and whole-file SHA-256;
- reference E4M3FN conversion path and FP16/FP32 logical storage;
- declarative record slicing, reinterpretation, reshaping and transposition;
- generic gated window-transformer reference operator;
- importer for the user-supplied private ZIP, using direct block/layer records or
  an explicit record map;
- partial graph builder/executor for blocks 23–30 and 40–47;
- standard-op PyTorch lowering and ONNX export/CPU parity gate for that family;
- browser runner using `onnxruntime-web/webgpu`, explicit temporal state and a
  default refusal to execute manifests marked incomplete;
- automated Python and TypeScript build/test workflows.

## Evidence carried forward

The prior reconstruction closed and independently validated the four-record
logical boundary for 16 split-Swin-512 blocks. Those blocks are the only model
family currently eligible to be marked implemented. No fixed captured activation
is copied into the portable inference interface.

## Remaining model gates

| Gate | Blocks/components | State |
|---|---|---|
| Front end and early encoder | 0–22 | Not reconstructed in portable IR |
| 512-channel window families | 23–30 | Operator and canonicalization implemented |
| 1024-channel bottleneck | 31–39 | Not reconstructed in portable IR |
| 512-channel window families | 40–47 | Operator and canonicalization implemented |
| Decoder transitions and tail | 48–70 | Not reconstructed in portable IR |
| Frame resource unpack/repack | colour, depth, motion, exposure, guides | Not complete |
| Reprojection/history/blending | explicit previous/next state | Not complete |
| Full independent-frame reference | real inputs to final image | Not complete |
| Full ONNX CPU parity | all nodes and state edges | Not complete |
| Browser WebGPU parity | full ONNX model | Not complete |
| Direct WGSL optimization | measured bottlenecks only | Not started |

## Non-negotiable completion criteria

The classification may change to `FULL_PORTABLE_RUNTIME` only when:

1. all 71 blocks are represented without identity placeholders;
2. texture preprocessing, guides, final readout and post-processing are explicit;
3. temporal state inputs and outputs are declared and tested across a sequence;
4. inference uses only real frame inputs, model weights and declared state;
5. two or more independent frames not used to infer the operator pass reference
   boundary checks;
6. the complete PyTorch/reference implementation passes PNG/frame-to-frame output;
7. ONNX Runtime CPU and ONNX Runtime Web/WebGPU match declared tolerances;
8. no vendor DLL, CUBIN, HIP code object or captured activation is needed.

## Immediate technical order

1. Run the private importer locally against the 448 MB archive and persist only
   sanitized shape/hash/coverage reports.
2. Convert the already validated 16 blocks into the canonical weight archive and
   compare the new reference executor to the existing stage-3 metrics.
3. Reconstruct blocks 31–39 next, because the 1024-channel bottleneck is the
   largest unresolved compute/portability boundary.
4. Close encoder/decoder transitions and skip edges before integrating image I/O.
5. Model history/reprojection as explicit state, then validate a frame sequence.
6. Export the complete graph to ONNX and only then treat WebGPU as an end-to-end
   backend.
