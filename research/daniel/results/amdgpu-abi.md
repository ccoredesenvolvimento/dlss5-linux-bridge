# Sanitized AMDGPU kernel ABI

> Derived by static MessagePack decoding of embedded AMDGPU notes. No code bytes or weights are included.

- Installer SHA-256: `b4b31e19e1d9028b3d63b7ac5074d7f71ede736d6185c11d25863f6415c6ece9`
- AMDGPU code objects: `4`

## Code object 0

- File offset: `0xb0e00`
- Intrinsic size: `1179328`
- SHA-256: `e363aa788e7626b93c6c449583e3c3bf340a6fa69d434cf98285fef12ec6b21a`
- Targets: `amdgcn-amd-amdhsa--gfx1100`
- Metadata versions: `[[1, 2]]`
- Relevant kernels: `20`

### `_Z16k_swin_1h_32_fp810SwinParams`

- Symbol: `_Z16k_swin_1h_32_fp810SwinParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `62592` / `64`
- SGPR/VGPR: `35` / `194`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z21k_pre_block_1h_32_fp89PreParams`

- Symbol: `_Z21k_pre_block_1h_32_fp89PreParams.kd`
- Kernarg bytes/alignment: `336` / `8`
- LDS/private bytes: `64640` / `64`
- SGPR/VGPR: `45` / `194`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` | `None` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z22k_post_block_1h_32_fp810PostParams`

- Symbol: `_Z22k_post_block_1h_32_fp810PostParams.kd`
- Kernarg bytes/alignment: `336` / `8`
- LDS/private bytes: `62592` / `64`
- SGPR/VGPR: `43` / `194`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` | `None` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_conv_res10ConvParams`

- Symbol: `_Z10k_conv_res10ConvParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `8192` / `0`
- SGPR/VGPR: `18` / `87`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_qkv_attn10AttnParams`

- Symbol: `_Z10k_qkv_attn10AttnParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `58368` / `0`
- SGPR/VGPR: `32` / `102`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z11k_conv_res211Conv2Params`

- Symbol: `_Z11k_conv_res211Conv2Params.kd`
- Kernarg bytes/alignment: `320` / `8`
- LDS/private bytes: `0` / `0`
- SGPR/VGPR: `107` / `185`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 64 | `None` | `None` | `by_value` | `None` |
| 64 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 68 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 72 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 76 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 78 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 80 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 82 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 84 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 86 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 128 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z11k_qkv_attn210AttnParams`

- Symbol: `_Z11k_qkv_attn210AttnParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `23808` / `24`
- SGPR/VGPR: `49` / `148`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z8k_expand12ExpandParams`

- Symbol: `_Z8k_expand12ExpandParams.kd`
- Kernarg bytes/alignment: `280` / `8`
- LDS/private bytes: `16384` / `0`
- SGPR/VGPR: `20` / `90`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` | `None` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z13k_conv_splitk12ConvParams1d`

- Symbol: `_Z13k_conv_splitk12ConvParams1d.kd`
- Kernarg bytes/alignment: `304` / `8`
- LDS/private bytes: `4096` / `0`
- SGPR/VGPR: `42` / `51`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z5k_qkv9QkvParams`

- Symbol: `_Z5k_qkv9QkvParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `6144` / `0`
- SGPR/VGPR: `106` / `69`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z9k_expand212ExpandParams`

- Symbol: `_Z9k_expand212ExpandParams.kd`
- Kernarg bytes/alignment: `280` / `8`
- LDS/private bytes: `0` / `0`
- SGPR/VGPR: `25` / `163`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` | `None` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z11k_contract212ConvParams1d`

- Symbol: `_Z11k_contract212ConvParams1d.kd`
- Kernarg bytes/alignment: `304` / `8`
- LDS/private bytes: `16384` / `0`
- SGPR/VGPR: `69` / `168`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z6k_qkv29QkvParams`

- Symbol: `_Z6k_qkv29QkvParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `12800` / `0`
- SGPR/VGPR: `34` / `123`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z16k_conv_res_views12ConvPlParams`

- Symbol: `_Z16k_conv_res_views12ConvPlParams.kd`
- Kernarg bytes/alignment: `328` / `8`
- LDS/private bytes: `24576` / `0`
- SGPR/VGPR: `51` / `137`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 72 | `None` | `None` | `by_value` | `None` |
| 72 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 76 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 80 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 84 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 86 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 88 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 90 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 92 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 94 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 136 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z8k_repack12RepackParams`

- Symbol: `_Z8k_repack12RepackParams.kd`
- Kernarg bytes/alignment: `288` / `8`
- LDS/private bytes: `0` / `0`
- SGPR/VGPR: `20` / `17`
- Wave/workgroup: `32` / `1024`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 32 | `None` | `None` | `by_value` | `None` |
| 32 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 36 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 44 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 46 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 48 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 50 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 52 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 54 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 96 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi32ELb1EEv9VarParams`

- Symbol: `_Z10k_swin_varILi32ELb1EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15616` / `24`
- SGPR/VGPR: `69` / `103`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi32ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi32ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15632` / `24`
- SGPR/VGPR: `65` / `92`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi64ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi64ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15616` / `24`
- SGPR/VGPR: `76` / `125`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi128ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi128ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15616` / `24`
- SGPR/VGPR: `76` / `136`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi256ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi256ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `19200` / `24`
- SGPR/VGPR: `76` / `136`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

## Code object 1

- File offset: `0x1d0e00`
- Intrinsic size: `1179328`
- SHA-256: `109498324c893b11b8feea1025068f69c5aa56d20b5d06d83d167005ab202110`
- Targets: `amdgcn-amd-amdhsa--gfx1101`
- Metadata versions: `[[1, 2]]`
- Relevant kernels: `20`

### `_Z16k_swin_1h_32_fp810SwinParams`

- Symbol: `_Z16k_swin_1h_32_fp810SwinParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `62592` / `64`
- SGPR/VGPR: `35` / `194`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z21k_pre_block_1h_32_fp89PreParams`

- Symbol: `_Z21k_pre_block_1h_32_fp89PreParams.kd`
- Kernarg bytes/alignment: `336` / `8`
- LDS/private bytes: `64640` / `64`
- SGPR/VGPR: `45` / `194`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` | `None` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z22k_post_block_1h_32_fp810PostParams`

- Symbol: `_Z22k_post_block_1h_32_fp810PostParams.kd`
- Kernarg bytes/alignment: `336` / `8`
- LDS/private bytes: `62592` / `64`
- SGPR/VGPR: `43` / `194`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` | `None` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_conv_res10ConvParams`

- Symbol: `_Z10k_conv_res10ConvParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `8192` / `0`
- SGPR/VGPR: `18` / `87`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_qkv_attn10AttnParams`

- Symbol: `_Z10k_qkv_attn10AttnParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `58368` / `0`
- SGPR/VGPR: `32` / `102`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z11k_conv_res211Conv2Params`

- Symbol: `_Z11k_conv_res211Conv2Params.kd`
- Kernarg bytes/alignment: `320` / `8`
- LDS/private bytes: `0` / `0`
- SGPR/VGPR: `107` / `185`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 64 | `None` | `None` | `by_value` | `None` |
| 64 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 68 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 72 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 76 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 78 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 80 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 82 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 84 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 86 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 128 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z11k_qkv_attn210AttnParams`

- Symbol: `_Z11k_qkv_attn210AttnParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `23808` / `24`
- SGPR/VGPR: `49` / `148`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z8k_expand12ExpandParams`

- Symbol: `_Z8k_expand12ExpandParams.kd`
- Kernarg bytes/alignment: `280` / `8`
- LDS/private bytes: `16384` / `0`
- SGPR/VGPR: `20` / `90`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` | `None` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z13k_conv_splitk12ConvParams1d`

- Symbol: `_Z13k_conv_splitk12ConvParams1d.kd`
- Kernarg bytes/alignment: `304` / `8`
- LDS/private bytes: `4096` / `0`
- SGPR/VGPR: `42` / `51`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z5k_qkv9QkvParams`

- Symbol: `_Z5k_qkv9QkvParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `6144` / `0`
- SGPR/VGPR: `106` / `69`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z9k_expand212ExpandParams`

- Symbol: `_Z9k_expand212ExpandParams.kd`
- Kernarg bytes/alignment: `280` / `8`
- LDS/private bytes: `0` / `0`
- SGPR/VGPR: `25` / `163`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` | `None` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z11k_contract212ConvParams1d`

- Symbol: `_Z11k_contract212ConvParams1d.kd`
- Kernarg bytes/alignment: `304` / `8`
- LDS/private bytes: `16384` / `0`
- SGPR/VGPR: `69` / `168`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z6k_qkv29QkvParams`

- Symbol: `_Z6k_qkv29QkvParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `12800` / `0`
- SGPR/VGPR: `34` / `123`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z16k_conv_res_views12ConvPlParams`

- Symbol: `_Z16k_conv_res_views12ConvPlParams.kd`
- Kernarg bytes/alignment: `328` / `8`
- LDS/private bytes: `24576` / `0`
- SGPR/VGPR: `51` / `137`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 72 | `None` | `None` | `by_value` | `None` |
| 72 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 76 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 80 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 84 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 86 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 88 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 90 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 92 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 94 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 136 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z8k_repack12RepackParams`

- Symbol: `_Z8k_repack12RepackParams.kd`
- Kernarg bytes/alignment: `288` / `8`
- LDS/private bytes: `0` / `0`
- SGPR/VGPR: `20` / `17`
- Wave/workgroup: `32` / `1024`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 32 | `None` | `None` | `by_value` | `None` |
| 32 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 36 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 44 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 46 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 48 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 50 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 52 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 54 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 96 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi32ELb1EEv9VarParams`

- Symbol: `_Z10k_swin_varILi32ELb1EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15616` / `24`
- SGPR/VGPR: `69` / `103`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi32ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi32ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15632` / `24`
- SGPR/VGPR: `65` / `92`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi64ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi64ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15616` / `24`
- SGPR/VGPR: `76` / `125`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi128ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi128ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15616` / `24`
- SGPR/VGPR: `76` / `136`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi256ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi256ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `19200` / `24`
- SGPR/VGPR: `76` / `136`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

## Code object 2

- File offset: `0x2f0e00`
- Intrinsic size: `1181048`
- SHA-256: `3708f939e94fa7295afc5f80463a8774a84af446f68f8981dc15ae9b923c3958`
- Targets: `amdgcn-amd-amdhsa--gfx1102`
- Metadata versions: `[[1, 2]]`
- Relevant kernels: `20`

### `_Z16k_swin_1h_32_fp810SwinParams`

- Symbol: `_Z16k_swin_1h_32_fp810SwinParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `62592` / `64`
- SGPR/VGPR: `35` / `194`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z21k_pre_block_1h_32_fp89PreParams`

- Symbol: `_Z21k_pre_block_1h_32_fp89PreParams.kd`
- Kernarg bytes/alignment: `336` / `8`
- LDS/private bytes: `64640` / `64`
- SGPR/VGPR: `45` / `194`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` | `None` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z22k_post_block_1h_32_fp810PostParams`

- Symbol: `_Z22k_post_block_1h_32_fp810PostParams.kd`
- Kernarg bytes/alignment: `336` / `8`
- LDS/private bytes: `62592` / `64`
- SGPR/VGPR: `43` / `194`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` | `None` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_conv_res10ConvParams`

- Symbol: `_Z10k_conv_res10ConvParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `8192` / `0`
- SGPR/VGPR: `18` / `59`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_qkv_attn10AttnParams`

- Symbol: `_Z10k_qkv_attn10AttnParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `58368` / `0`
- SGPR/VGPR: `32` / `102`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z11k_conv_res211Conv2Params`

- Symbol: `_Z11k_conv_res211Conv2Params.kd`
- Kernarg bytes/alignment: `320` / `8`
- LDS/private bytes: `0` / `0`
- SGPR/VGPR: `107` / `179`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 64 | `None` | `None` | `by_value` | `None` |
| 64 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 68 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 72 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 76 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 78 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 80 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 82 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 84 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 86 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 128 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z11k_qkv_attn210AttnParams`

- Symbol: `_Z11k_qkv_attn210AttnParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `23808` / `24`
- SGPR/VGPR: `49` / `148`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z8k_expand12ExpandParams`

- Symbol: `_Z8k_expand12ExpandParams.kd`
- Kernarg bytes/alignment: `280` / `8`
- LDS/private bytes: `16384` / `0`
- SGPR/VGPR: `20` / `64`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` | `None` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z13k_conv_splitk12ConvParams1d`

- Symbol: `_Z13k_conv_splitk12ConvParams1d.kd`
- Kernarg bytes/alignment: `304` / `8`
- LDS/private bytes: `4096` / `0`
- SGPR/VGPR: `42` / `51`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z5k_qkv9QkvParams`

- Symbol: `_Z5k_qkv9QkvParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `6144` / `0`
- SGPR/VGPR: `106` / `69`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z9k_expand212ExpandParams`

- Symbol: `_Z9k_expand212ExpandParams.kd`
- Kernarg bytes/alignment: `280` / `8`
- LDS/private bytes: `0` / `0`
- SGPR/VGPR: `25` / `168`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` | `None` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z11k_contract212ConvParams1d`

- Symbol: `_Z11k_contract212ConvParams1d.kd`
- Kernarg bytes/alignment: `304` / `8`
- LDS/private bytes: `16384` / `0`
- SGPR/VGPR: `69` / `171`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z6k_qkv29QkvParams`

- Symbol: `_Z6k_qkv29QkvParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `12800` / `0`
- SGPR/VGPR: `34` / `123`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z16k_conv_res_views12ConvPlParams`

- Symbol: `_Z16k_conv_res_views12ConvPlParams.kd`
- Kernarg bytes/alignment: `328` / `8`
- LDS/private bytes: `24576` / `0`
- SGPR/VGPR: `51` / `112`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 72 | `None` | `None` | `by_value` | `None` |
| 72 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 76 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 80 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 84 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 86 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 88 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 90 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 92 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 94 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 136 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z8k_repack12RepackParams`

- Symbol: `_Z8k_repack12RepackParams.kd`
- Kernarg bytes/alignment: `288` / `8`
- LDS/private bytes: `0` / `0`
- SGPR/VGPR: `20` / `17`
- Wave/workgroup: `32` / `1024`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 32 | `None` | `None` | `by_value` | `None` |
| 32 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 36 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 44 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 46 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 48 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 50 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 52 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 54 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 96 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi32ELb1EEv9VarParams`

- Symbol: `_Z10k_swin_varILi32ELb1EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15616` / `24`
- SGPR/VGPR: `69` / `91`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi32ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi32ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15632` / `24`
- SGPR/VGPR: `65` / `95`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi64ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi64ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15616` / `24`
- SGPR/VGPR: `76` / `125`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi128ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi128ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15616` / `24`
- SGPR/VGPR: `76` / `125`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi256ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi256ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `19200` / `24`
- SGPR/VGPR: `76` / `125`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

## Code object 3

- File offset: `0x411e00`
- Intrinsic size: `505096`
- SHA-256: `12fdd63876ad0cf9b70c947d369bd8b0ed00aa2345021076d72a008dc8e1f4cd`
- Targets: `amdgcn-amd-amdhsa--gfx1201`
- Metadata versions: `[[1, 2]]`
- Relevant kernels: `20`

### `_Z16k_swin_1h_32_fp810SwinParams`

- Symbol: `_Z16k_swin_1h_32_fp810SwinParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `62592` / `0`
- SGPR/VGPR: `25` / `72`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z21k_pre_block_1h_32_fp89PreParams`

- Symbol: `_Z21k_pre_block_1h_32_fp89PreParams.kd`
- Kernarg bytes/alignment: `336` / `8`
- LDS/private bytes: `64640` / `0`
- SGPR/VGPR: `44` / `72`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` | `None` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z22k_post_block_1h_32_fp810PostParams`

- Symbol: `_Z22k_post_block_1h_32_fp810PostParams.kd`
- Kernarg bytes/alignment: `336` / `8`
- LDS/private bytes: `62592` / `0`
- SGPR/VGPR: `43` / `70`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` | `None` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_conv_res10ConvParams`

- Symbol: `_Z10k_conv_res10ConvParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `8192` / `0`
- SGPR/VGPR: `17` / `60`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_qkv_attn10AttnParams`

- Symbol: `_Z10k_qkv_attn10AttnParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `58368` / `0`
- SGPR/VGPR: `30` / `94`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z11k_conv_res211Conv2Params`

- Symbol: `_Z11k_conv_res211Conv2Params.kd`
- Kernarg bytes/alignment: `320` / `8`
- LDS/private bytes: `0` / `0`
- SGPR/VGPR: `107` / `203`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 64 | `None` | `None` | `by_value` | `None` |
| 64 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 68 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 72 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 76 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 78 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 80 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 82 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 84 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 86 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 128 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z11k_qkv_attn210AttnParams`

- Symbol: `_Z11k_qkv_attn210AttnParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `23808` / `24`
- SGPR/VGPR: `33` / `99`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z8k_expand12ExpandParams`

- Symbol: `_Z8k_expand12ExpandParams.kd`
- Kernarg bytes/alignment: `280` / `8`
- LDS/private bytes: `16384` / `0`
- SGPR/VGPR: `19` / `41`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` | `None` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z13k_conv_splitk12ConvParams1d`

- Symbol: `_Z13k_conv_splitk12ConvParams1d.kd`
- Kernarg bytes/alignment: `304` / `8`
- LDS/private bytes: `4096` / `0`
- SGPR/VGPR: `31` / `82`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z5k_qkv9QkvParams`

- Symbol: `_Z5k_qkv9QkvParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `6144` / `0`
- SGPR/VGPR: `40` / `119`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z9k_expand212ExpandParams`

- Symbol: `_Z9k_expand212ExpandParams.kd`
- Kernarg bytes/alignment: `280` / `8`
- LDS/private bytes: `0` / `0`
- SGPR/VGPR: `20` / `162`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` | `None` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z11k_contract212ConvParams1d`

- Symbol: `_Z11k_contract212ConvParams1d.kd`
- Kernarg bytes/alignment: `304` / `8`
- LDS/private bytes: `16384` / `0`
- SGPR/VGPR: `55` / `170`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z6k_qkv29QkvParams`

- Symbol: `_Z6k_qkv29QkvParams.kd`
- Kernarg bytes/alignment: `296` / `8`
- LDS/private bytes: `12800` / `0`
- SGPR/VGPR: `20` / `96`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z16k_conv_res_views12ConvPlParams`

- Symbol: `_Z16k_conv_res_views12ConvPlParams.kd`
- Kernarg bytes/alignment: `328` / `8`
- LDS/private bytes: `24576` / `0`
- SGPR/VGPR: `49` / `90`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 72 | `None` | `None` | `by_value` | `None` |
| 72 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 76 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 80 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 84 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 86 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 88 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 90 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 92 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 94 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 136 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z8k_repack12RepackParams`

- Symbol: `_Z8k_repack12RepackParams.kd`
- Kernarg bytes/alignment: `288` / `8`
- LDS/private bytes: `0` / `0`
- SGPR/VGPR: `21` / `15`
- Wave/workgroup: `32` / `1024`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 32 | `None` | `None` | `by_value` | `None` |
| 32 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 36 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 40 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 44 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 46 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 48 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 50 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 52 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 54 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 96 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi32ELb1EEv9VarParams`

- Symbol: `_Z10k_swin_varILi32ELb1EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15616` / `24`
- SGPR/VGPR: `82` / `81`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi32ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi32ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15632` / `24`
- SGPR/VGPR: `67` / `76`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi64ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi64ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15616` / `24`
- SGPR/VGPR: `61` / `120`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi128ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi128ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `15616` / `24`
- SGPR/VGPR: `60` / `120`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |

### `_Z10k_swin_varILi256ELb0EEv9VarParams`

- Symbol: `_Z10k_swin_varILi256ELb0EEv9VarParams.kd`
- Kernarg bytes/alignment: `424` / `8`
- LDS/private bytes: `19200` / `24`
- SGPR/VGPR: `60` / `120`
- Wave/workgroup: `32` / `256`

| Offset | Size | Name | Type | Kind | Address space |
|---:|---:|---|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` | `None` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` | `None` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` | `None` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` | `None` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` | `None` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` | `None` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` | `None` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` | `None` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` | `None` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` | `None` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` | `None` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` | `None` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` | `None` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` | `None` |
