# DLSSNR Daniel-route implementation contract

> Compact, metadata-only output from static analysis. No installer, DLL, code object or model weight is included.

## Proven architecture

- Installer SHA-256 validated: `b4b31e19e1d9028b3d63b7ac5074d7f71ede736d6185c11d25863f6415c6ece9`
- Embedded PE images: `2`
- Embedded AMDGPU code objects: `4`
- Contract-bearing x64 functions: `11`
- Relevant AMDGPU kernel records: `80`
- Primary runtime path: converted weight container + custom HIP kernels + D3D12/HIP interop.
- ONNX/DirectML is not evidenced as the in-game backend and remains a secondary export target.

## Contract functions

### `weight_container` — PE 0 RVA `0x1000`–`0x2427`

- References: `dlssnr_on_amd_weights.bin`

```asm
0x0000000140001917: e8fc8a0000                     call       0x14000a418
0x000000014000191c: 4889c7                         mov        rdi, rax
0x000000014000191f: 4889bd80000100                 mov        qword ptr [rbp + 0x10080], rdi
0x0000000140001926: 4883fb08                       cmp        rbx, 8
0x000000014000192a: 488d85a0000100                 lea        rax, [rbp + 0x100a0]
0x0000000140001931: 4c0f42f8                       cmovb      r15, rax
0x0000000140001935: 4c89a590000100                 mov        qword ptr [rbp + 0x10090], r12
0x000000014000193c: 4c89ad98000100                 mov        qword ptr [rbp + 0x10098], r13
0x0000000140001943: 4c8d0436                       lea        r8, [rsi + rsi]
0x0000000140001947: 4889f9                         mov        rcx, rdi
0x000000014000194a: 4c89fa                         mov        rdx, r15
0x000000014000194d: e8ae2a0200                     call       0x140024400
0x0000000140001952: 48b82e0064006c006c00           movabs     rax, 0x6c006c0064002e
0x000000014000195c: 488944770e                     mov        qword ptr [rdi + rsi*2 + 0xe], rax
0x0000000140001961: f30f6f05fd590200               movdqu     xmm0, xmmword ptr [rip + 0x259fd]    ; XREF -> version.dll
0x0000000140001969: f30f7f0477                     movdqu     xmmword ptr [rdi + rsi*2], xmm0
0x000000014000196e: 66c74477160000                 mov        word ptr [rdi + rsi*2 + 0x16], 0
0x0000000140001975: 488bb5b0000100                 mov        rsi, qword ptr [rbp + 0x100b0]
0x000000014000197c: 48b81d00000000000080           movabs     rax, 0x800000000000001d
0x0000000140001986: 4801f0                         add        rax, rsi
0x0000000140001989: 4883f81b                       cmp        rax, 0x1b
0x000000014000198d: 0f86700a0000                   jbe        0x140002403
0x0000000140001993: 4c8bbda0000100                 mov        r15, qword ptr [rbp + 0x100a0]
0x000000014000199a: 488b9db8000100                 mov        rbx, qword ptr [rbp + 0x100b8]
0x00000001400019a1: 660fefc0                       pxor       xmm0, xmm0
0x00000001400019a5: 660f7f45c0                     movdqa     xmmword ptr [rbp - 0x40], xmm0
0x00000001400019aa: 660f7f45d0                     movdqa     xmmword ptr [rbp - 0x30], xmm0
0x00000001400019af: 4c8d661c                       lea        r12, [rsi + 0x1c]
0x00000001400019b3: 41bd07000000                   mov        r13d, 7
```

```asm
0x00000001400020d9: 488d4dc0                       lea        rcx, [rbp - 0x40]
0x00000001400020dd: e83e250000                     call       0x140004620
0x00000001400020e2: 488d4dc0                       lea        rcx, [rbp - 0x40]
0x00000001400020e6: e8a52e0000                     call       0x140004f90
0x00000001400020eb: 4c8d05be540200                 lea        r8, [rip + 0x254be]
0x00000001400020f2: 488d4dc0                       lea        rcx, [rbp - 0x40]
0x00000001400020f6: 488d95a0000100                 lea        rdx, [rbp + 0x100a0]
0x00000001400020fd: e87e310000                     call       0x140005280
0x0000000140002102: 488d4dc0                       lea        rcx, [rbp - 0x40]
0x0000000140002106: e815250000                     call       0x140004620
0x000000014000210b: 488d4dc0                       lea        rcx, [rbp - 0x40]
0x000000014000210f: e87c2e0000                     call       0x140004f90
0x0000000140002114: 488d0d9f570200                 lea        rcx, [rip + 0x2579f]
0x000000014000211b: e8102e0000                     call       0x140004f30
0x0000000140002120: 4c8d0523540200                 lea        r8, [rip + 0x25423]    ; XREF -> dlssnr_on_amd_weights.bin
0x0000000140002127: 488d7dc0                       lea        rdi, [rbp - 0x40]
0x000000014000212b: 488d95a0000100                 lea        rdx, [rbp + 0x100a0]
0x0000000140002132: 4889f9                         mov        rcx, rdi
0x0000000140002135: e846310000                     call       0x140005280
0x000000014000213a: 48837dd808                     cmp        qword ptr [rbp - 0x28], 8
0x000000014000213f: 7204                           jb         0x140002145
0x0000000140002141: 488b7dc0                       mov        rdi, qword ptr [rbp - 0x40]
0x0000000140002145: 4889f9                         mov        rcx, rdi
0x0000000140002148: ff156a3f0200                   call       qword ptr [rip + 0x23f6a]
0x000000014000214e: 8bb578000100                   mov        esi, dword ptr [rbp + 0x10078]
0x0000000140002154: 89c7                           mov        edi, eax
0x0000000140002156: 488d4dc0                       lea        rcx, [rbp - 0x40]
0x000000014000215a: e8312e0000                     call       0x140004f90
0x000000014000215f: 83ffff                         cmp        edi, -1
0x0000000140002162: 742d                           je         0x140002191
0x0000000140002164: 488d0d17580200                 lea        rcx, [rip + 0x25817]
0x000000014000216b: e8c02d0000                     call       0x140004f30
0x0000000140002170: e9d0010000                     jmp        0x140002345
0x0000000140002175: 488d0d50560200                 lea        rcx, [rip + 0x25650]
0x000000014000217c: e8af2d0000                     call       0x140004f30
0x0000000140002181: 41bc01000000                   mov        r12d, 1
0x0000000140002187: e874cc0000                     call       0x14000ee00
0x000000014000218c: e9c8010000                     jmp        0x140002359
0x0000000140002191: 83fe03                         cmp        esi, 3
0x0000000140002194: 7d55                           jge        0x1400021eb
0x0000000140002196: 4c8d0521580200                 lea        r8, [rip + 0x25821]    ; XREF -> nvngx_dlssnr.dll
0x000000014000219d: 488dbd10000100                 lea        rdi, [rbp + 0x10010]
0x00000001400021a4: 488d95a0000100                 lea        rdx, [rbp + 0x100a0]
0x00000001400021ab: 4889f9                         mov        rcx, rdi
0x00000001400021ae: e8cd300000                     call       0x140005280
0x00000001400021b3: 4883bd2800010008               cmp        qword ptr [rbp + 0x10028], 8
0x00000001400021bb: 7207                           jb         0x1400021c4
0x00000001400021bd: 488bbd10000100                 mov        rdi, qword ptr [rbp + 0x10010]
0x00000001400021c4: 4889f9                         mov        rcx, rdi
0x00000001400021c7: ff15eb3e0200                   call       qword ptr [rip + 0x23eeb]
0x00000001400021cd: 83f8ff                         cmp        eax, -1
0x00000001400021d0: 742f                           je         0x140002201
0x00000001400021d2: 4c8d05e5570200                 lea        r8, [rip + 0x257e5]    ; XREF -> nvngx_dlssnr.dll
0x00000001400021d9: 488d4dc0                       lea        rcx, [rbp - 0x40]
0x00000001400021dd: 488d95a0000100                 lea        rdx, [rbp + 0x100a0]
0x00000001400021e4: e897300000                     call       0x140005280
0x00000001400021e9: eb32                           jmp        0x14000221d
0x00000001400021eb: 488b8550000100                 mov        rax, qword ptr [rbp + 0x10050]
0x00000001400021f2: 488b5010                       mov        rdx, qword ptr [rax + 0x10]
0x00000001400021f6: 488d4dc0                       lea        rcx, [rbp - 0x40]
0x00000001400021fa: e8012e0000                     call       0x140005000
0x00000001400021ff: eb1c                           jmp        0x14000221d
0x0000000140002201: 660fefc0                       pxor       xmm0, xmm0
0x0000000140002205: 660f7f45d0                     movdqa     xmmword ptr [rbp - 0x30], xmm0
0x000000014000220a: 660f7f45c0                     movdqa     xmmword ptr [rbp - 0x40], xmm0
0x000000014000220f: 48c745d807000000               mov        qword ptr [rbp - 0x28], 7
0x0000000140002217: 66c745c00000                   mov        word ptr [rbp - 0x40], 0
```

### `weight_container` — PE 0 RVA `0x5420`–`0x7bf2`

- References: `all %zu tensors match DLSS NR 310.8.0.0 exactly; using it`
- References: `DLSSNRW1`
- References: `dlssnr_on_amd_weights.bin`
- References: `wrote %zu blobs, %.1f MB -> dlssnr_on_amd_weights.bin`
- References: `cannot write dlssnr_on_amd_weights.bin`

```asm
0x0000000140007472: 721f                           jb         0x140007493
0x0000000140007474: 4c8b41f8                       mov        r8, qword ptr [rcx - 8]
0x0000000140007478: 4883c1f8                       add        rcx, -8
0x000000014000747c: 4c29c1                         sub        rcx, r8
0x000000014000747f: 4883f920                       cmp        rcx, 0x20
0x0000000140007483: 0f8311070000                   jae        0x140007b9a
0x0000000140007489: 4883c028                       add        rax, 0x28
0x000000014000748d: 4889c2                         mov        rdx, rax
0x0000000140007490: 4c89c1                         mov        rcx, r8
0x0000000140007493: e8782f0000                     call       0x14000a410
0x0000000140007498: e946fcffff                     jmp        0x1400070e3
0x000000014000749d: 4d85ed                         test       r13, r13
0x00000001400074a0: 0f8488000000                   je         0x14000752e
0x00000001400074a6: 48c744242099000000             mov        qword ptr [rsp + 0x20], 0x99
0x00000001400074af: 4c8d05f9160200                 lea        r8, [rip + 0x216f9]    ; XREF -> %zu of %zu tensors do not match DLSS NR 310.8.0.0:
0x00000001400074b6: 488d7db0                       lea        rdi, [rbp - 0x50]
0x00000001400074ba: ba70000000                     mov        edx, 0x70
0x00000001400074bf: 4889f9                         mov        rcx, rdi
0x00000001400074c2: 4d89e9                         mov        r9, r13
0x00000001400074c5: e8461c0000                     call       0x140009110
0x00000001400074ca: 488d8d70000100                 lea        rcx, [rbp + 0x10070]
0x00000001400074d1: 4c8d85b0000100                 lea        r8, [rbp + 0x100b0]
0x00000001400074d8: 4889fa                         mov        rdx, rdi
0x00000001400074db: e8301d0000                     call       0x140009210
0x00000001400074e0: 4c8d05fc160200                 lea        r8, [rip + 0x216fc]
0x00000001400074e7: 488d8dd0000100                 lea        rcx, [rbp + 0x100d0]
0x00000001400074ee: 488d9570000100                 lea        rdx, [rbp + 0x10070]
0x00000001400074f5: e8761c0000                     call       0x140009170
0x00000001400074fa: 488d95d0000100                 lea        rdx, [rbp + 0x100d0]
0x0000000140007501: 488b8da8000100                 mov        rcx, qword ptr [rbp + 0x100a8]
0x0000000140007508: e8431e0000                     call       0x140009350
0x000000014000750d: 488bb568000100                 mov        rsi, qword ptr [rbp + 0x10068]
0x0000000140007514: 488d8dd0000100                 lea        rcx, [rbp + 0x100d0]
0x000000014000751b: e8e00f0000                     call       0x140008500
0x0000000140007520: 488d8d70000100                 lea        rcx, [rbp + 0x10070]
0x0000000140007527: e8d40f0000                     call       0x140008500
0x000000014000752c: eb34                           jmp        0x140007562
0x000000014000752e: 4c8d05fd160200                 lea        r8, [rip + 0x216fd]    ; XREF -> all %zu tensors match DLSS NR 310.8.0.0 exactly; using it
0x0000000140007535: 488d7db0                       lea        rdi, [rbp - 0x50]
0x0000000140007539: ba70000000                     mov        edx, 0x70
0x000000014000753e: 41b999000000                   mov        r9d, 0x99
0x0000000140007544: 4889f9                         mov        rcx, rdi
0x0000000140007547: e8c41b0000                     call       0x140009110
0x000000014000754c: 488b8da8000100                 mov        rcx, qword ptr [rbp + 0x100a8]
0x0000000140007553: 4889fa                         mov        rdx, rdi
0x0000000140007556: e865190000                     call       0x140008ec0
0x000000014000755b: 488bb568000100                 mov        rsi, qword ptr [rbp + 0x10068]
0x0000000140007562: 488b85c8000100                 mov        rax, qword ptr [rbp + 0x100c8]
0x0000000140007569: 4883f810                       cmp        rax, 0x10
0x000000014000756d: 7238                           jb         0x1400075a7
0x000000014000756f: 488b8db0000100                 mov        rcx, qword ptr [rbp + 0x100b0]
0x0000000140007576: 488d5001                       lea        rdx, [rax + 1]
```

```asm
0x00000001400075cd: e83e2e0000                     call       0x14000a410
0x00000001400075d2: 4d85ed                         test       r13, r13
0x00000001400075d5: 7407                           je         0x1400075de
0x00000001400075d7: 31ff                           xor        edi, edi
0x00000001400075d9: e90d050000                     jmp        0x140007aeb
0x00000001400075de: 660f57c0                       xorpd      xmm0, xmm0
0x00000001400075e2: 660f2985d0000100               movapd     xmmword ptr [rbp + 0x100d0], xmm0
0x00000001400075ea: 48c785e000010000000000         mov        qword ptr [rbp + 0x100e0], 0
0x00000001400075f5: 8b8548000100                   mov        eax, dword ptr [rbp + 0x10048]
0x00000001400075fb: 2b8540000100                   sub        eax, dword ptr [rbp + 0x10040]
0x0000000140007601: 89b570000100                   mov        dword ptr [rbp + 0x10070], esi
0x0000000140007607: 83c010                         add        eax, 0x10
0x000000014000760a: 898510000100                   mov        dword ptr [rbp + 0x10010], eax
0x0000000140007610: 488b95d8000100                 mov        rdx, qword ptr [rbp + 0x100d8]
0x0000000140007617: 4c8d054f160200                 lea        r8, [rip + 0x2164f]    ; XREF -> DLSSNRW1
0x000000014000761e: 488d8dd0000100                 lea        rcx, [rbp + 0x100d0]
0x0000000140007625: 41b908000000                   mov        r9d, 8
0x000000014000762b: e8a00f0000                     call       0x1400085d0
0x0000000140007630: 488b95d8000100                 mov        rdx, qword ptr [rbp + 0x100d8]
0x0000000140007637: 488d8dd0000100                 lea        rcx, [rbp + 0x100d0]
0x000000014000763e: 4c8d8570000100                 lea        r8, [rbp + 0x10070]
0x0000000140007645: 41b904000000                   mov        r9d, 4
0x000000014000764b: e8800f0000                     call       0x1400085d0
0x0000000140007650: 488b95d8000100                 mov        rdx, qword ptr [rbp + 0x100d8]
0x0000000140007657: 488d8dd0000100                 lea        rcx, [rbp + 0x100d0]
0x000000014000765e: 4c8d8510000100                 lea        r8, [rbp + 0x10010]
0x0000000140007665: 41b904000000                   mov        r9d, 4
0x000000014000766b: e8600f0000                     call       0x1400085d0
0x0000000140007670: 4c8b8540000100                 mov        r8, qword ptr [rbp + 0x10040]
```

```asm
0x00000001400078bb: eb0c                           jmp        0x1400078c9
0x00000001400078bd: 4883c102                       add        rcx, 2
0x00000001400078c1: e8522b0000                     call       0x14000a418
0x00000001400078c6: 4989c7                         mov        r15, rax
0x00000001400078c9: 488b8560000100                 mov        rax, qword ptr [rbp + 0x10060]
0x00000001400078d0: 4c897db0                       mov        qword ptr [rbp - 0x50], r15
0x00000001400078d4: 4983fd08                       cmp        r13, 8
0x00000001400078d8: 488d95b0000100                 lea        rdx, [rbp + 0x100b0]
0x00000001400078df: 480f43d0                       cmovae     rdx, rax
0x00000001400078e3: 48895dc0                       mov        qword ptr [rbp - 0x40], rbx
0x00000001400078e7: 4c8965c8                       mov        qword ptr [rbp - 0x38], r12
0x00000001400078eb: 4c8d0436                       lea        r8, [rsi + rsi]
0x00000001400078ef: 4c89f9                         mov        rcx, r15
0x00000001400078f2: e809cb0100                     call       0x140024400
0x00000001400078f7: 0f10054cfc0100                 movups     xmm0, xmmword ptr [rip + 0x1fc4c]    ; XREF -> dlssnr_on_amd_weights.bin
0x00000001400078fe: 410f110477                     movups     xmmword ptr [r15 + rsi*2], xmm0
0x0000000140007903: 0f100550fc0100                 movups     xmm0, xmmword ptr [rip + 0x1fc50]
0x000000014000790a: 410f11447710                   movups     xmmword ptr [r15 + rsi*2 + 0x10], xmm0
0x0000000140007910: 660f100552fc0100               movupd     xmm0, xmmword ptr [rip + 0x1fc52]
0x0000000140007918: 66410f11447720                 movupd     xmmword ptr [r15 + rsi*2 + 0x20], xmm0
0x000000014000791f: 41c74477306e000000             mov        dword ptr [r15 + rsi*2 + 0x30], 0x6e
0x0000000140007928: 48837dc808                     cmp        qword ptr [rbp - 0x38], 8
0x000000014000792d: 7204                           jb         0x140007933
0x000000014000792f: 4c8b75b0                       mov        r14, qword ptr [rbp - 0x50]
0x0000000140007933: 488d15ba0f0200                 lea        rdx, [rip + 0x20fba]
0x000000014000793a: 4c89f1                         mov        rcx, r14
0x000000014000793d: e84a680000                     call       0x14000e18c
0x0000000140007942: 488bb568000100                 mov        rsi, qword ptr [rbp + 0x10068]
0x0000000140007949: 4885c0                         test       rax, rax
```

```asm
0x00000001400079bf: 4c89c1                         mov        rcx, r8
0x00000001400079c2: e8492a0000                     call       0x14000a410
0x00000001400079c7: 4084ff                         test       dil, dil
0x00000001400079ca: 7469                           je         0x140007a35
0x00000001400079cc: 488b85d8000100                 mov        rax, qword ptr [rbp + 0x100d8]
0x00000001400079d3: 482b85d0000100                 sub        rax, qword ptr [rbp + 0x100d0]
0x00000001400079da: 66480f6ec0                     movq       xmm0, rax
0x00000001400079df: 660f620569ea0100               punpckldq  xmm0, xmmword ptr [rip + 0x1ea69]
0x00000001400079e7: 660f5c0571ea0100               subpd      xmm0, xmmword ptr [rip + 0x1ea71]
0x00000001400079ef: 660f28c8                       movapd     xmm1, xmm0
0x00000001400079f3: 660f15c8                       unpckhpd   xmm1, xmm0
0x00000001400079f7: f20f58c8                       addsd      xmm1, xmm0
0x00000001400079fb: f20f590d6dea0100               mulsd      xmm1, qword ptr [rip + 0x1ea6d]
0x0000000140007a03: f20f114c2420                   movsd      qword ptr [rsp + 0x20], xmm1
0x0000000140007a09: 4c8d058e120200                 lea        r8, [rip + 0x2128e]    ; XREF -> wrote %zu blobs, %.1f MB -> dlssnr_on_amd_weights.bin
0x0000000140007a10: 488d5db0                       lea        rbx, [rbp - 0x50]
0x0000000140007a14: ba80000000                     mov        edx, 0x80
0x0000000140007a19: 4889d9                         mov        rcx, rbx
0x0000000140007a1c: 4989f1                         mov        r9, rsi
0x0000000140007a1f: e8ec160000                     call       0x140009110
0x0000000140007a24: 488b8da8000100                 mov        rcx, qword ptr [rbp + 0x100a8]
0x0000000140007a2b: 4889da                         mov        rdx, rbx
0x0000000140007a2e: e88d140000                     call       0x140008ec0
0x0000000140007a33: eb13                           jmp        0x140007a48
0x0000000140007a35: 488d153a120200                 lea        rdx, [rip + 0x2123a]    ; XREF -> cannot write dlssnr_on_amd_weights.bin
0x0000000140007a3c: 488b8da8000100                 mov        rcx, qword ptr [rbp + 0x100a8]
0x0000000140007a43: e878140000                     call       0x140008ec0
0x0000000140007a48: 488b85c8000100                 mov        rax, qword ptr [rbp + 0x100c8]
0x0000000140007a4f: 4883f808                       cmp        rax, 8
0x0000000140007a53: 723f                           jb         0x140007a94
0x0000000140007a55: 488b8db0000100                 mov        rcx, qword ptr [rbp + 0x100b0]
0x0000000140007a5c: 488d144502000000               lea        rdx, [rax*2 + 2]
0x0000000140007a64: 4881fa00100000                 cmp        rdx, 0x1000
0x0000000140007a6b: 7222                           jb         0x140007a8f
0x0000000140007a6d: 4c8b41f8                       mov        r8, qword ptr [rcx - 8]
0x0000000140007a71: 4883c1f8                       add        rcx, -8
0x0000000140007a75: 4c29c1                         sub        rcx, r8
0x0000000140007a78: 4883f920                       cmp        rcx, 0x20
0x0000000140007a7c: 0f8318010000                   jae        0x140007b9a
```

### `weight_container` — PE 1 RVA `0x4670`–`0x5d28`

- References: `dlssnr_on_amd_weights.bin`

```asm
0x00000001800050b8: 4989c6                         mov        r14, rax
0x00000001800050bb: 4c89b580050000                 mov        qword ptr [rbp + 0x580], r14
0x00000001800050c2: eb0d                           jmp        0x1800050d1
0x00000001800050c4: 4c8db580050000                 lea        r14, [rbp + 0x580]
0x00000001800050cb: 41bd07000000                   mov        r13d, 7
0x00000001800050d1: 4883ff08                       cmp        rdi, 8
0x00000001800050d5: 488d7dc0                       lea        rdi, [rbp - 0x40]
0x00000001800050d9: 480f42df                       cmovb      rbx, rdi
0x00000001800050dd: 4c89a590050000                 mov        qword ptr [rbp + 0x590], r12
0x00000001800050e4: 4c89ad98050000                 mov        qword ptr [rbp + 0x598], r13
0x00000001800050eb: 4f8d043f                       lea        r8, [r15 + r15]
0x00000001800050ef: 4c89f1                         mov        rcx, r14
0x00000001800050f2: 4889da                         mov        rdx, rbx
0x00000001800050f5: e866d60400                     call       0x180052760
0x00000001800050fa: 0f100545f60500                 movups     xmm0, xmmword ptr [rip + 0x5f645]    ; XREF -> dlssnr_on_amd_weights.bin
0x0000000180005101: 430f11047e                     movups     xmmword ptr [r14 + r15*2], xmm0
0x0000000180005106: 0f100549f60500                 movups     xmm0, xmmword ptr [rip + 0x5f649]
0x000000018000510d: 430f11447e10                   movups     xmmword ptr [r14 + r15*2 + 0x10], xmm0
0x0000000180005113: 660f10054bf60500               movupd     xmm0, xmmword ptr [rip + 0x5f64b]
0x000000018000511b: 66430f11447e20                 movupd     xmmword ptr [r14 + r15*2 + 0x20], xmm0
0x0000000180005122: 6643c7447e306e00               mov        word ptr [r14 + r15*2 + 0x30], 0x6e
0x000000018000512a: 6643c704660000                 mov        word ptr [r14 + r12*2], 0
0x0000000180005131: 4883bd9805000008               cmp        qword ptr [rbp + 0x598], 8
0x0000000180005139: 7209                           jb         0x180005144
0x000000018000513b: 488b8d80050000                 mov        rcx, qword ptr [rbp + 0x580]
0x0000000180005142: eb07                           jmp        0x18000514b
0x0000000180005144: 488d8d80050000                 lea        rcx, [rbp + 0x580]
0x000000018000514b: ff1567420600                   call       qword ptr [rip + 0x64267]
0x0000000180005151: 89c3                           mov        ebx, eax
```

```asm
0x000000018000528b: 4883c102                       add        rcx, 2
0x000000018000528f: e8b0540200                     call       0x18002a744
0x0000000180005294: 4989c4                         mov        r12, rax
0x0000000180005297: 4c8b8530090000                 mov        r8, qword ptr [rbp + 0x930]
0x000000018000529e: 4c89a590070000                 mov        qword ptr [rbp + 0x790], r12
0x00000001800052a5: 4983f808                       cmp        r8, 8
0x00000001800052a9: 488d45c0                       lea        rax, [rbp - 0x40]
0x00000001800052ad: 4c0f42f8                       cmovb      r15, rax
0x00000001800052b1: 48899da0070000                 mov        qword ptr [rbp + 0x7a0], rbx
0x00000001800052b8: 4c89b5a8070000                 mov        qword ptr [rbp + 0x7a8], r14
0x00000001800052bf: 4e8d046d00000000               lea        r8, [r13*2]
0x00000001800052c7: 4c89e1                         mov        rcx, r12
0x00000001800052ca: 4c89fa                         mov        rdx, r15
0x00000001800052cd: e88ed40400                     call       0x180052760
0x00000001800052d2: 660f1035a0f40500               movupd     xmm6, xmmword ptr [rip + 0x5f4a0]    ; XREF -> nvngx_dlssnr.dll
0x00000001800052da: 66430f11346c                   movupd     xmmword ptr [r12 + r13*2], xmm6
0x00000001800052e0: 660f103da2f40500               movupd     xmm7, xmmword ptr [rip + 0x5f4a2]
0x00000001800052e8: 66430f117c6c10                 movupd     xmmword ptr [r12 + r13*2 + 0x10], xmm7
0x00000001800052ef: 6643c7446c200000               mov        word ptr [r12 + r13*2 + 0x20], 0
0x00000001800052f7: 4883bda807000008               cmp        qword ptr [rbp + 0x7a8], 8
0x00000001800052ff: 488d8d90070000                 lea        rcx, [rbp + 0x790]
0x0000000180005306: 7207                           jb         0x18000530f
0x0000000180005308: 488b8d90070000                 mov        rcx, qword ptr [rbp + 0x790]
0x000000018000530f: ff15a3400600                   call       qword ptr [rip + 0x640a3]
0x0000000180005315: 4189c6                         mov        r14d, eax
0x0000000180005318: 488b85a8070000                 mov        rax, qword ptr [rbp + 0x7a8]
0x000000018000531f: 4883f808                       cmp        rax, 8
0x0000000180005323: 723f                           jb         0x180005364
0x0000000180005325: 488b8d90070000                 mov        rcx, qword ptr [rbp + 0x790]
```

```asm
0x0000000180005581: 4883f920                       cmp        rcx, 0x20
0x0000000180005585: 0f836b070000                   jae        0x180005cf6
0x000000018000558b: 4801c0                         add        rax, rax
0x000000018000558e: 4883c029                       add        rax, 0x29
0x0000000180005592: 4889c2                         mov        rdx, rax
0x0000000180005595: 4c89c1                         mov        rcx, r8
0x0000000180005598: e8e3510200                     call       0x18002a780
0x000000018000559d: 4883bd9805000010               cmp        qword ptr [rbp + 0x598], 0x10
0x00000001800055a5: 7207                           jb         0x1800055ae
0x00000001800055a7: 4c8bb580050000                 mov        r14, qword ptr [rbp + 0x580]
0x00000001800055ae: 488d0538d80500                 lea        rax, [rip + 0x5d838]
0x00000001800055b5: 488d15e1e00500                 lea        rdx, [rip + 0x5e0e1]
0x00000001800055bc: 84db                           test       bl, bl
0x00000001800055be: 480f45d0                       cmovne     rdx, rax
0x00000001800055c2: 488d0d52c90500                 lea        rcx, [rip + 0x5c952]    ; XREF -> weights build from nvngx_dlssnr.dll: %s
0x00000001800055c9: 4d89f0                         mov        r8, r14
0x00000001800055cc: e8cfdfffff                     call       0x1800035a0
0x00000001800055d1: 84db                           test       bl, bl
0x00000001800055d3: 0f8548010000                   jne        0x180005721
0x00000001800055d9: b920000000                     mov        ecx, 0x20
0x00000001800055de: e861510200                     call       0x18002a744
0x00000001800055e3: 4989c5                         mov        r13, rax
0x00000001800055e6: 488b9d90050000                 mov        rbx, qword ptr [rbp + 0x590]
0x00000001800055ed: 48b8b9feffffffffff7f           movabs     rax, 0x7ffffffffffffeb9
0x00000001800055f7: 4839c3                         cmp        rbx, rax
0x00000001800055fa: 0f8d11070000                   jge        0x180005d11
0x0000000180005600: 488b8d80050000                 mov        rcx, qword ptr [rbp + 0x580]
0x0000000180005607: 4c8bbd98050000                 mov        r15, qword ptr [rbp + 0x598]
0x000000018000560e: 660f57c0                       xorpd      xmm0, xmm0
```

```asm
0x0000000180005832: eb0c                           jmp        0x180005840
0x0000000180005834: 498d4d01                       lea        rcx, [r13 + 1]
0x0000000180005838: e8074f0200                     call       0x18002a744
0x000000018000583d: 4889c7                         mov        rdi, rax
0x0000000180005840: 48897dc0                       mov        qword ptr [rbp - 0x40], rdi
0x0000000180005844: 4c89e8                         mov        rax, r13
0x0000000180005847: 4983ff10                       cmp        r15, 0x10
0x000000018000584b: 488d15aedf0600                 lea        rdx, [rip + 0x6dfae]
0x0000000180005852: 490f43d6                       cmovae     rdx, r14
0x0000000180005856: 4c8965d0                       mov        qword ptr [rbp - 0x30], r12
0x000000018000585a: 488945d8                       mov        qword ptr [rbp - 0x28], rax
0x000000018000585e: 4889f9                         mov        rcx, rdi
0x0000000180005861: 4989d8                         mov        r8, rbx
0x0000000180005864: e8f7ce0400                     call       0x180052760
0x0000000180005869: 0f100507d40500                 movups     xmm0, xmmword ptr [rip + 0x5d407]    ; XREF -> dlssnr_on_amd_weights.bin
0x0000000180005870: 0f11041f                       movups     xmmword ptr [rdi + rbx], xmm0
0x0000000180005874: 660f100504d40500               movupd     xmm0, xmmword ptr [rip + 0x5d404]
0x000000018000587c: 660f11441f09                   movupd     xmmword ptr [rdi + rbx + 9], xmm0
0x0000000180005882: c6441f1900                     mov        byte ptr [rdi + rbx + 0x19], 0
0x0000000180005887: 488d0d4adc0600                 lea        rcx, [rip + 0x6dc4a]
0x000000018000588e: 488d55c0                       lea        rdx, [rbp - 0x40]
0x0000000180005892: e8f9ab0000                     call       0x180010490
0x0000000180005897: 88055bdf0600                   mov        byte ptr [rip + 0x6df5b], al
0x000000018000589d: 4c8b45d8                       mov        r8, qword ptr [rbp - 0x28]
0x00000001800058a1: 4983f810                       cmp        r8, 0x10
0x00000001800058a5: 723c                           jb         0x1800058e3
0x00000001800058a7: 488b4dc0                       mov        rcx, qword ptr [rbp - 0x40]
0x00000001800058ab: 498d5001                       lea        rdx, [r8 + 1]
0x00000001800058af: 4881fa00100000                 cmp        rdx, 0x1000
```

### `weight_container` — PE 1 RVA `0x6dd0`–`0x72a7`

- References: `dlssnr_on_amd_weights.bin`

```asm
0x000000018000709c: e8a3360200                     call       0x18002a744
0x00000001800070a1: 4889c6                         mov        rsi, rax
0x00000001800070a4: 488975b0                       mov        qword ptr [rbp - 0x50], rsi
0x00000001800070a8: eb0a                           jmp        0x1800070b4
0x00000001800070aa: 488d75b0                       lea        rsi, [rbp - 0x50]
0x00000001800070ae: 41bc07000000                   mov        r12d, 7
0x00000001800070b4: 4983ff08                       cmp        r15, 8
0x00000001800070b8: 488d55d0                       lea        rdx, [rbp - 0x30]
0x00000001800070bc: 490f43d6                       cmovae     rdx, r14
0x00000001800070c0: 48895dc0                       mov        qword ptr [rbp - 0x40], rbx
0x00000001800070c4: 4c8965c8                       mov        qword ptr [rbp - 0x38], r12
0x00000001800070c8: 4c8d043f                       lea        r8, [rdi + rdi]
0x00000001800070cc: 4889f1                         mov        rcx, rsi
0x00000001800070cf: e88cb60400                     call       0x180052760
0x00000001800070d4: 0f10056bd60500                 movups     xmm0, xmmword ptr [rip + 0x5d66b]    ; XREF -> dlssnr_on_amd_weights.bin
0x00000001800070db: 0f11047e                       movups     xmmword ptr [rsi + rdi*2], xmm0
0x00000001800070df: 0f100570d60500                 movups     xmm0, xmmword ptr [rip + 0x5d670]
0x00000001800070e6: 0f11447e10                     movups     xmmword ptr [rsi + rdi*2 + 0x10], xmm0
0x00000001800070eb: f30f6f0573d60500               movdqu     xmm0, xmmword ptr [rip + 0x5d673]
0x00000001800070f3: f30f7f447e20                   movdqu     xmmword ptr [rsi + rdi*2 + 0x20], xmm0
0x00000001800070f9: 66c7447e306e00                 mov        word ptr [rsi + rdi*2 + 0x30], 0x6e
0x0000000180007100: 66c7045e0000                   mov        word ptr [rsi + rbx*2], 0
0x0000000180007106: 48837dc808                     cmp        qword ptr [rbp - 0x38], 8
0x000000018000710b: 7206                           jb         0x180007113
0x000000018000710d: 488b4db0                       mov        rcx, qword ptr [rbp - 0x50]
0x0000000180007111: eb04                           jmp        0x180007117
0x0000000180007113: 488d4db0                       lea        rcx, [rbp - 0x50]
0x0000000180007117: ff159b220600                   call       qword ptr [rip + 0x6229b]
0x000000018000711d: 83f8ff                         cmp        eax, -1
```

### `frame_staging` — PE 1 RVA `0x9100`–`0xaf6b`

- References: `staging ready: colour %ux%u dxgi %d (pix %d, tonemap %d); motion %dx%d dxgi %d; depth %dx%d dxgi %d (inverted %d); exposure %s; residual %s`

```asm
0x000000018000a3a1: 448b3dc0970600                 mov        r15d, dword ptr [rip + 0x697c0]
0x000000018000a3a8: 448b4d18                       mov        r9d, dword ptr [rbp + 0x18]
0x000000018000a3ac: 4889442470                     mov        qword ptr [rsp + 0x70], rax
0x000000018000a3b1: 4889542468                     mov        qword ptr [rsp + 0x68], rdx
0x000000018000a3b6: 4489542460                     mov        dword ptr [rsp + 0x60], r10d
0x000000018000a3bb: 4489442458                     mov        dword ptr [rsp + 0x58], r8d
0x000000018000a3c0: 44895c2450                     mov        dword ptr [rsp + 0x50], r11d
0x000000018000a3c5: 897c2448                       mov        dword ptr [rsp + 0x48], edi
0x000000018000a3c9: 894c2440                       mov        dword ptr [rsp + 0x40], ecx
0x000000018000a3cd: 895c2438                       mov        dword ptr [rsp + 0x38], ebx
0x000000018000a3d1: 4489742430                     mov        dword ptr [rsp + 0x30], r14d
0x000000018000a3d6: 44897c2428                     mov        dword ptr [rsp + 0x28], r15d
0x000000018000a3db: 8b8558010000                   mov        eax, dword ptr [rbp + 0x158]
0x000000018000a3e1: 89442420                       mov        dword ptr [rsp + 0x20], eax
0x000000018000a3e5: 488d0d34790500                 lea        rcx, [rip + 0x57934]    ; XREF -> staging ready: colour %ux%u dxgi %d (pix %d, tonemap %d); motion %dx%d dxgi %d; depth %dx%d dxgi %d (inverted %d); exposure %s; residual %s
0x000000018000a3ec: 4c8b4538                       mov        r8, qword ptr [rbp + 0x38]
0x000000018000a3f0: 488b5530                       mov        rdx, qword ptr [rbp + 0x30]
0x000000018000a3f4: e8a791ffff                     call       0x1800035a0
0x000000018000a3f9: 488d05eb9a0500                 lea        rax, [rip + 0x59aeb]
0x000000018000a400: 4c8d0d5a9b0500                 lea        r9, [rip + 0x59b5a]
0x000000018000a407: 803dd397060000                 cmp        byte ptr [rip + 0x697d3], 0
0x000000018000a40e: 4c0f45c8                       cmovne     r9, rax
0x000000018000a412: 488d0558980500                 lea        rax, [rip + 0x59858]
0x000000018000a419: 803d0998060000                 cmp        byte ptr [rip + 0x69809], 0
0x000000018000a420: 4c8d059f8f0500                 lea        r8, [rip + 0x58f9f]
0x000000018000a427: 4c0f45c0                       cmovne     r8, rax
0x000000018000a42b: 488d15c4890500                 lea        rdx, [rip + 0x589c4]
0x000000018000a432: 803d3794060000                 cmp        byte ptr [rip + 0x69437], 0
0x000000018000a439: 480f45d0                       cmovne     rdx, rax
```

### `runtime_debug_controls` — PE 1 RVA `0xc540`–`0xdad1`

- References: `DLSSNR_STAGES`

```asm
0x000000018000ca66: 751c                           jne        0x18000ca84
0x000000018000ca68: f30f101560730600               movss      xmm2, dword ptr [rip + 0x67360]
0x000000018000ca70: 0f57c9                         xorps      xmm1, xmm1
0x000000018000ca73: f30fc2ca02                     cmpless    xmm1, xmm2
0x000000018000ca78: 0f54d1                         andps      xmm2, xmm1
0x000000018000ca7b: 0f55c8                         andnps     xmm1, xmm0
0x000000018000ca7e: 0f56ca                         orps       xmm1, xmm2
0x000000018000ca81: 0f28d0                         movaps     xmm2, xmm0
0x000000018000ca84: f30f110d746a0600               movss      dword ptr [rip + 0x66a74], xmm1
0x000000018000ca8c: f30f1115706a0600               movss      dword ptr [rip + 0x66a70], xmm2
0x000000018000ca94: f30f100538730600               movss      xmm0, dword ptr [rip + 0x67338]
0x000000018000ca9c: f30f1105646a0600               movss      dword ptr [rip + 0x66a64], xmm0
0x000000018000caa4: 4585ff                         test       r15d, r15d
0x000000018000caa7: 742e                           je         0x18000cad7
0x000000018000caa9: 488d0d806b0500                 lea        rcx, [rip + 0x56b80]    ; XREF -> DLSSNR_STAGES
0x000000018000cab0: e8dfa60200                     call       0x180037194
0x000000018000cab5: 4885c0                         test       rax, rax
0x000000018000cab8: 741d                           je         0x18000cad7
0x000000018000caba: 4889c1                         mov        rcx, rax
0x000000018000cabd: 4889c6                         mov        rsi, rax
0x000000018000cac0: e86b670400                     call       0x180053230
0x000000018000cac5: 488d0d4c6a0600                 lea        rcx, [rip + 0x66a4c]
0x000000018000cacc: 4889f2                         mov        rdx, rsi
0x000000018000cacf: 4989c0                         mov        r8, rax
0x000000018000cad2: e8397f0100                     call       0x180024a10
0x000000018000cad7: 488d0dea690600                 lea        rcx, [rip + 0x669ea]
0x000000018000cade: 488d04f9                       lea        rax, [rcx + rdi*8]
0x000000018000cae2: 4805f0030000                   add        rax, 0x3f0
0x000000018000cae8: 803d816d060000                 cmp        byte ptr [rip + 0x66d81], 0
```

### `hip_dispatch` — PE 1 RVA `0xec30`–`0xf363`

- References: `_Z10k_qkv_attn10AttnParams`
- References: `_Z11k_conv_res211Conv2Params`
- References: `_Z5k_qkv9QkvParams`
- References: `_Z9k_expand212ExpandParams`
- References: `_Z11k_contract212ConvParams1d`
- References: `_Z8k_repack12RepackParams`
- References: `_Z10k_swin_varILi32ELb1EEv9VarParams`
- References: `_Z10k_swin_varILi32ELb0EEv9VarParams`
- References: `_Z10k_swin_varILi64ELb0EEv9VarParams`
- References: `_Z10k_swin_varILi128ELb0EEv9VarParams`
- References: `_Z10k_swin_varILi256ELb0EEv9VarParams`

```asm
0x000000018000ed2f: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000ed34: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000ed39: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000ed42: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000ed4a: 488d153f540400                 lea        rdx, [rip + 0x4543f]
0x000000018000ed51: 4c8d05ea680400                 lea        r8, [rip + 0x468ea]
0x000000018000ed58: 4889f1                         mov        rcx, rsi
0x000000018000ed5b: 4d89c1                         mov        r9, r8
0x000000018000ed5e: e8bd4f0400                     call       0x180053d20
0x000000018000ed63: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000ed68: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000ed6d: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000ed76: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000ed7e: 488d1513540400                 lea        rdx, [rip + 0x45413]
0x000000018000ed85: 4c8d05d1680400                 lea        r8, [rip + 0x468d1]    ; XREF -> _Z10k_qkv_attn10AttnParams
0x000000018000ed8c: 4889f1                         mov        rcx, rsi
0x000000018000ed8f: 4d89c1                         mov        r9, r8
0x000000018000ed92: e8894f0400                     call       0x180053d20
0x000000018000ed97: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000ed9c: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000eda1: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000edaa: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000edb2: 488d15e7530400                 lea        rdx, [rip + 0x453e7]
0x000000018000edb9: 4c8d05b8680400                 lea        r8, [rip + 0x468b8]
0x000000018000edc0: 4889f1                         mov        rcx, rsi
0x000000018000edc3: 4d89c1                         mov        r9, r8
0x000000018000edc6: e8554f0400                     call       0x180053d20
0x000000018000edcb: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000edd0: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000edd5: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000edde: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000ede6: 488d15bb530400                 lea        rdx, [rip + 0x453bb]
0x000000018000eded: 4c8d059c680400                 lea        r8, [rip + 0x4689c]    ; XREF -> _Z11k_conv_res211Conv2Params
0x000000018000edf4: 4889f1                         mov        rcx, rsi
0x000000018000edf7: 4d89c1                         mov        r9, r8
0x000000018000edfa: e8214f0400                     call       0x180053d20
0x000000018000edff: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000ee04: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000ee09: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000ee12: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000ee1a: 488d158f530400                 lea        rdx, [rip + 0x4538f]
0x000000018000ee21: 4c8d0585680400                 lea        r8, [rip + 0x46885]
0x000000018000ee28: 4889f1                         mov        rcx, rsi
0x000000018000ee2b: 4d89c1                         mov        r9, r8
0x000000018000ee2e: e8ed4e0400                     call       0x180053d20
0x000000018000ee33: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000ee38: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
```

```asm
0x000000018000ee67: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000ee6c: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000ee71: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000ee7a: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000ee82: 488d1537530400                 lea        rdx, [rip + 0x45337]
0x000000018000ee89: 4c8d0553680400                 lea        r8, [rip + 0x46853]
0x000000018000ee90: 4889f1                         mov        rcx, rsi
0x000000018000ee93: 4d89c1                         mov        r9, r8
0x000000018000ee96: e8854e0400                     call       0x180053d20
0x000000018000ee9b: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000eea0: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000eea5: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000eeae: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000eeb6: 488d150b530400                 lea        rdx, [rip + 0x4530b]
0x000000018000eebd: 4c8d053f680400                 lea        r8, [rip + 0x4683f]    ; XREF -> _Z5k_qkv9QkvParams
0x000000018000eec4: 4889f1                         mov        rcx, rsi
0x000000018000eec7: 4d89c1                         mov        r9, r8
0x000000018000eeca: e8514e0400                     call       0x180053d20
0x000000018000eecf: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000eed4: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000eed9: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000eee2: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000eeea: 488d15df520400                 lea        rdx, [rip + 0x452df]
0x000000018000eef1: 4c8d051e680400                 lea        r8, [rip + 0x4681e]
0x000000018000eef8: 4889f1                         mov        rcx, rsi
0x000000018000eefb: 4d89c1                         mov        r9, r8
0x000000018000eefe: e81d4e0400                     call       0x180053d20
0x000000018000ef03: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000ef08: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000ef0d: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000ef16: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000ef1e: 488d15b3520400                 lea        rdx, [rip + 0x452b3]
0x000000018000ef25: 4c8d0508680400                 lea        r8, [rip + 0x46808]    ; XREF -> _Z9k_expand212ExpandParams
0x000000018000ef2c: 4889f1                         mov        rcx, rsi
0x000000018000ef2f: 4d89c1                         mov        r9, r8
0x000000018000ef32: e8e94d0400                     call       0x180053d20
0x000000018000ef37: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000ef3c: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000ef41: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000ef4a: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000ef52: 488d1587520400                 lea        rdx, [rip + 0x45287]
0x000000018000ef59: 4c8d05ef670400                 lea        r8, [rip + 0x467ef]    ; XREF -> _Z11k_contract212ConvParams1d
0x000000018000ef60: 4889f1                         mov        rcx, rsi
0x000000018000ef63: 4d89c1                         mov        r9, r8
0x000000018000ef66: e8b54d0400                     call       0x180053d20
0x000000018000ef6b: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000ef70: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000ef75: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000ef7e: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000ef86: 488d155b520400                 lea        rdx, [rip + 0x4525b]
0x000000018000ef8d: 4c8d05d9670400                 lea        r8, [rip + 0x467d9]
0x000000018000ef94: 4889f1                         mov        rcx, rsi
0x000000018000ef97: 4d89c1                         mov        r9, r8
0x000000018000ef9a: e8814d0400                     call       0x180053d20
0x000000018000ef9f: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000efa4: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
```

```asm
0x000000018000f03b: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000f040: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000f045: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000f04e: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000f056: 488d15ab510400                 lea        rdx, [rip + 0x451ab]
0x000000018000f05d: 4c8d0580670400                 lea        r8, [rip + 0x46780]
0x000000018000f064: 4889f1                         mov        rcx, rsi
0x000000018000f067: 4d89c1                         mov        r9, r8
0x000000018000f06a: e8b14c0400                     call       0x180053d20
0x000000018000f06f: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000f074: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000f079: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000f082: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000f08a: 488d157f510400                 lea        rdx, [rip + 0x4517f]
0x000000018000f091: 4c8d0569670400                 lea        r8, [rip + 0x46769]    ; XREF -> _Z8k_repack12RepackParams
0x000000018000f098: 4889f1                         mov        rcx, rsi
0x000000018000f09b: 4d89c1                         mov        r9, r8
0x000000018000f09e: e87d4c0400                     call       0x180053d20
0x000000018000f0a3: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000f0a8: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000f0ad: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000f0b6: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000f0be: 488d1553510400                 lea        rdx, [rip + 0x45153]
0x000000018000f0c5: 4c8d054f670400                 lea        r8, [rip + 0x4674f]
0x000000018000f0cc: 4889f1                         mov        rcx, rsi
0x000000018000f0cf: 4d89c1                         mov        r9, r8
0x000000018000f0d2: e8494c0400                     call       0x180053d20
0x000000018000f0d7: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000f0dc: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
```

```asm
0x000000018000f1db: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000f1e0: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000f1e5: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000f1ee: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000f1f6: 488d156b500400                 lea        rdx, [rip + 0x4506b]
0x000000018000f1fd: 4c8d05b3660400                 lea        r8, [rip + 0x466b3]
0x000000018000f204: 4889f1                         mov        rcx, rsi
0x000000018000f207: 4d89c1                         mov        r9, r8
0x000000018000f20a: e8114b0400                     call       0x180053d20
0x000000018000f20f: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000f214: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000f219: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000f222: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000f22a: 488d15d7770400                 lea        rdx, [rip + 0x477d7]
0x000000018000f231: 4c8d0591660400                 lea        r8, [rip + 0x46691]    ; XREF -> _Z10k_swin_varILi32ELb1EEv9VarParams
0x000000018000f238: 4889f1                         mov        rcx, rsi
0x000000018000f23b: 4d89c1                         mov        r9, r8
0x000000018000f23e: e8dd4a0400                     call       0x180053d20
0x000000018000f243: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000f248: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000f24d: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000f256: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000f25e: 488d15ab770400                 lea        rdx, [rip + 0x477ab]
0x000000018000f265: 4c8d0582660400                 lea        r8, [rip + 0x46682]    ; XREF -> _Z10k_swin_varILi32ELb0EEv9VarParams
0x000000018000f26c: 4889f1                         mov        rcx, rsi
0x000000018000f26f: 4d89c1                         mov        r9, r8
0x000000018000f272: e8a94a0400                     call       0x180053d20
0x000000018000f277: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000f27c: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000f281: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000f28a: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000f292: 488d157f770400                 lea        rdx, [rip + 0x4777f]
0x000000018000f299: 4c8d0573660400                 lea        r8, [rip + 0x46673]    ; XREF -> _Z10k_swin_varILi64ELb0EEv9VarParams
0x000000018000f2a0: 4889f1                         mov        rcx, rsi
0x000000018000f2a3: 4d89c1                         mov        r9, r8
0x000000018000f2a6: e8754a0400                     call       0x180053d20
0x000000018000f2ab: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000f2b0: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000f2b5: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000f2be: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000f2c6: 488d1553770400                 lea        rdx, [rip + 0x47753]
0x000000018000f2cd: 4c8d0564660400                 lea        r8, [rip + 0x46664]    ; XREF -> _Z10k_swin_varILi128ELb0EEv9VarParams
0x000000018000f2d4: 4889f1                         mov        rcx, rsi
0x000000018000f2d7: 4d89c1                         mov        r9, r8
0x000000018000f2da: e8414a0400                     call       0x180053d20
0x000000018000f2df: 0f11742438                     movups     xmmword ptr [rsp + 0x38], xmm6
0x000000018000f2e4: 0f11742428                     movups     xmmword ptr [rsp + 0x28], xmm6
0x000000018000f2e9: 48c744244800000000             mov        qword ptr [rsp + 0x48], 0
0x000000018000f2f2: c7442420ffffffff               mov        dword ptr [rsp + 0x20], 0xffffffff
0x000000018000f2fa: 488d1527770400                 lea        rdx, [rip + 0x47727]
0x000000018000f301: 4c8d0556660400                 lea        r8, [rip + 0x46656]    ; XREF -> _Z10k_swin_varILi256ELb0EEv9VarParams
0x000000018000f308: 4889f1                         mov        rcx, rsi
0x000000018000f30b: 4d89c1                         mov        r9, r8
0x000000018000f30e: e80d4a0400                     call       0x180053d20
0x000000018000f313: c744243800000000               mov        dword ptr [rsp + 0x38], 0
0x000000018000f31b: c744243001000000               mov        dword ptr [rsp + 0x30], 1
0x000000018000f323: 48c744242800020000             mov        qword ptr [rsp + 0x28], 0x200
0x000000018000f32c: c744242000000000               mov        dword ptr [rsp + 0x20], 0
0x000000018000f334: 488d15b53d0600                 lea        rdx, [rip + 0x63db5]
0x000000018000f33b: 4c8d0542660400                 lea        r8, [rip + 0x46642]
0x000000018000f342: 4889f1                         mov        rcx, rsi
0x000000018000f345: 4d89c1                         mov        r9, r8
0x000000018000f348: e8e3490400                     call       0x180053d30
0x000000018000f34d: 488d0d1c000000                 lea        rcx, [rip + 0x1c]
0x000000018000f354: 0f28742450                     movaps     xmm6, xmmword ptr [rsp + 0x50]
```

### `runtime_debug_controls` — PE 1 RVA `0x10490`–`0x10e36`

- References: `DLSSNR_NO_REPACK`

```asm
0x00000001800108eb: 31db                           xor        ebx, ebx
0x00000001800108ed: 4d85ff                         test       r15, r15
0x00000001800108f0: 0f855b040000                   jne        0x180010d51
0x00000001800108f6: e98d040000                     jmp        0x180010d88
0x00000001800108fb: 31db                           xor        ebx, ebx
0x00000001800108fd: 4531f6                         xor        r14d, r14d
0x0000000180010900: eb23                           jmp        0x180010925
0x0000000180010902: 4c89f1                         mov        rcx, r14
0x0000000180010905: e83a9e0100                     call       0x18002a744
0x000000018001090a: 4889c3                         mov        rbx, rax
0x000000018001090d: 48899d00020000                 mov        qword ptr [rbp + 0x200], rbx
0x0000000180010914: 48899d08020000                 mov        qword ptr [rbp + 0x208], rbx
0x000000018001091b: 4901de                         add        r14, rbx
0x000000018001091e: 4c89b510020000                 mov        qword ptr [rbp + 0x210], r14
0x0000000180010925: 488d0d212d0500                 lea        rcx, [rip + 0x52d21]    ; XREF -> DLSSNR_NO_REPACK
0x000000018001092c: e863680200                     call       0x180037194
0x0000000180010931: 4885c0                         test       rax, rax
0x0000000180010934: 0f84ce000000                   je         0x180010a08
0x000000018001093a: 4c8ba5e0010000                 mov        r12, qword ptr [rbp + 0x1e0]
0x0000000180010941: 488b85e8010000                 mov        rax, qword ptr [rbp + 0x1e8]
0x0000000180010948: 4989c7                         mov        r15, rax
0x000000018001094b: 4d29e7                         sub        r15, r12
0x000000018001094e: 4929de                         sub        r14, rbx
0x0000000180010951: 4d39f7                         cmp        r15, r14
0x0000000180010954: 0f86ea020000                   jbe        0x180010c44
0x000000018001095a: 4d85ff                         test       r15, r15
0x000000018001095d: 0f88c8040000                   js         0x180010e2b
0x0000000180010963: 4d89f5                         mov        r13, r14
0x0000000180010966: 49d1ed                         shr        r13, 1
```

### `weight_container` — PE 1 RVA `0x13e70`–`0x1655a`

- References: `all %zu tensors match DLSS NR 310.8.0.0 exactly; using it`
- References: `DLSSNRW1`
- References: `dlssnr_on_amd_weights.bin`
- References: `wrote %zu blobs, %.1f MB -> dlssnr_on_amd_weights.bin`
- References: `cannot write dlssnr_on_amd_weights.bin`

```asm
0x0000000180015e42: 4883c1f8                       add        rcx, -8
0x0000000180015e46: 4c29c1                         sub        rcx, r8
0x0000000180015e49: 4883f920                       cmp        rcx, 0x20
0x0000000180015e4d: 0f83d2060000                   jae        0x180016525
0x0000000180015e53: 4883c028                       add        rax, 0x28
0x0000000180015e57: 4889c2                         mov        rdx, rax
0x0000000180015e5a: 4c89c1                         mov        rcx, r8
0x0000000180015e5d: e81e490100                     call       0x18002a780
0x0000000180015e62: 41bd01000000                   mov        r13d, 1
0x0000000180015e68: 48ffc7                         inc        rdi
0x0000000180015e6b: e963fcffff                     jmp        0x180015ad3
0x0000000180015e70: 4d85ed                         test       r13, r13
0x0000000180015e73: 0f8481000000                   je         0x180015efa
0x0000000180015e79: 48c744242099000000             mov        qword ptr [rsp + 0x20], 0x99
0x0000000180015e82: 4c8d05bde20400                 lea        r8, [rip + 0x4e2bd]    ; XREF -> %zu of %zu tensors do not match DLSS NR 310.8.0.0:
0x0000000180015e89: 488d7db0                       lea        rdi, [rbp - 0x50]
0x0000000180015e8d: ba70000000                     mov        edx, 0x70
0x0000000180015e92: 4889f9                         mov        rcx, rdi
0x0000000180015e95: 4d89e9                         mov        r9, r13
0x0000000180015e98: e833bdffff                     call       0x180011bd0
0x0000000180015e9d: 488d8d60000100                 lea        rcx, [rbp + 0x10060]
0x0000000180015ea4: 4c8d85c0000100                 lea        r8, [rbp + 0x100c0]
0x0000000180015eab: 4889fa                         mov        rdx, rdi
0x0000000180015eae: e82d100000                     call       0x180016ee0
0x0000000180015eb3: 4c8d0533e50400                 lea        r8, [rip + 0x4e533]
0x0000000180015eba: 488d8da0000100                 lea        rcx, [rbp + 0x100a0]
0x0000000180015ec1: 488d9560000100                 lea        rdx, [rbp + 0x10060]
0x0000000180015ec8: e82397ffff                     call       0x18000f5f0
0x0000000180015ecd: 488d95a0000100                 lea        rdx, [rbp + 0x100a0]
0x0000000180015ed4: 488b8d98000100                 mov        rcx, qword ptr [rbp + 0x10098]
0x0000000180015edb: e800130000                     call       0x1800171e0
0x0000000180015ee0: 488d8da0000100                 lea        rcx, [rbp + 0x100a0]
0x0000000180015ee7: e82496ffff                     call       0x18000f510
0x0000000180015eec: 488d8d60000100                 lea        rcx, [rbp + 0x10060]
0x0000000180015ef3: e81896ffff                     call       0x18000f510
0x0000000180015ef8: eb2d                           jmp        0x180015f27
0x0000000180015efa: 4c8d05b1e40400                 lea        r8, [rip + 0x4e4b1]    ; XREF -> all %zu tensors match DLSS NR 310.8.0.0 exactly; using it
0x0000000180015f01: 488d7db0                       lea        rdi, [rbp - 0x50]
0x0000000180015f05: ba70000000                     mov        edx, 0x70
0x0000000180015f0a: 41b999000000                   mov        r9d, 0x99
0x0000000180015f10: 4889f9                         mov        rcx, rdi
0x0000000180015f13: e8b8bcffff                     call       0x180011bd0
0x0000000180015f18: 488b8d98000100                 mov        rcx, qword ptr [rbp + 0x10098]
0x0000000180015f1f: 4889fa                         mov        rdx, rdi
0x0000000180015f22: e84996ffff                     call       0x18000f570
0x0000000180015f27: 488b85d8000100                 mov        rax, qword ptr [rbp + 0x100d8]
0x0000000180015f2e: 4883f810                       cmp        rax, 0x10
0x0000000180015f32: 7238                           jb         0x180015f6c
0x0000000180015f34: 488b8dc0000100                 mov        rcx, qword ptr [rbp + 0x100c0]
0x0000000180015f3b: 488d5001                       lea        rdx, [rax + 1]
0x0000000180015f3f: 4881fa00100000                 cmp        rdx, 0x1000
```

```asm
0x0000000180015f92: e8e9470100                     call       0x18002a780
0x0000000180015f97: 4d85ed                         test       r13, r13
0x0000000180015f9a: 4c8b8d08000100                 mov        r9, qword ptr [rbp + 0x10008]
0x0000000180015fa1: 7407                           je         0x180015faa
0x0000000180015fa3: 31ff                           xor        edi, edi
0x0000000180015fa5: e9fa040000                     jmp        0x1800164a4
0x0000000180015faa: 660f57c0                       xorpd      xmm0, xmm0
0x0000000180015fae: 660f2985a0000100               movapd     xmmword ptr [rbp + 0x100a0], xmm0
0x0000000180015fb6: 48c785b000010000000000         mov        qword ptr [rbp + 0x100b0], 0
0x0000000180015fc1: 44898d60000100                 mov        dword ptr [rbp + 0x10060], r9d
0x0000000180015fc8: 8b8548000100                   mov        eax, dword ptr [rbp + 0x10048]
0x0000000180015fce: 2b8540000100                   sub        eax, dword ptr [rbp + 0x10040]
0x0000000180015fd4: 83c010                         add        eax, 0x10
0x0000000180015fd7: 898510000100                   mov        dword ptr [rbp + 0x10010], eax
0x0000000180015fdd: 4c8d05b7d70400                 lea        r8, [rip + 0x4d7b7]    ; XREF -> DLSSNRW1
0x0000000180015fe4: 488d8da0000100                 lea        rcx, [rbp + 0x100a0]
0x0000000180015feb: 41b908000000                   mov        r9d, 8
0x0000000180015ff1: 31d2                           xor        edx, edx
0x0000000180015ff3: e878140000                     call       0x180017470
0x0000000180015ff8: 488b9db0ff0000                 mov        rbx, qword ptr [rbp + 0xffb0]
0x0000000180015fff: 488b95a8000100                 mov        rdx, qword ptr [rbp + 0x100a8]
0x0000000180016006: 488d8da0000100                 lea        rcx, [rbp + 0x100a0]
0x000000018001600d: 4c8d8560000100                 lea        r8, [rbp + 0x10060]
0x0000000180016014: 41b904000000                   mov        r9d, 4
0x000000018001601a: e851140000                     call       0x180017470
0x000000018001601f: 488b95a8000100                 mov        rdx, qword ptr [rbp + 0x100a8]
0x0000000180016026: 488d8da0000100                 lea        rcx, [rbp + 0x100a0]
0x000000018001602d: 4c8d8510000100                 lea        r8, [rbp + 0x10010]
0x0000000180016034: 41b904000000                   mov        r9d, 4
```

```asm
0x000000018001628b: eb0c                           jmp        0x180016299
0x000000018001628d: 4883c102                       add        rcx, 2
0x0000000180016291: e8ae440100                     call       0x18002a744
0x0000000180016296: 4989c7                         mov        r15, rax
0x0000000180016299: 4c8b8538000100                 mov        r8, qword ptr [rbp + 0x10038]
0x00000001800162a0: 4c897db0                       mov        qword ptr [rbp - 0x50], r15
0x00000001800162a4: 4883fe08                       cmp        rsi, 8
0x00000001800162a8: 488d95c0000100                 lea        rdx, [rbp + 0x100c0]
0x00000001800162af: 490f43d0                       cmovae     rdx, r8
0x00000001800162b3: 48895dc0                       mov        qword ptr [rbp - 0x40], rbx
0x00000001800162b7: 4c896dc8                       mov        qword ptr [rbp - 0x38], r13
0x00000001800162bb: 4f8d0424                       lea        r8, [r12 + r12]
0x00000001800162bf: 4c89f9                         mov        rcx, r15
0x00000001800162c2: e899c40300                     call       0x180052760
0x00000001800162c7: 0f100578e40400                 movups     xmm0, xmmword ptr [rip + 0x4e478]    ; XREF -> dlssnr_on_amd_weights.bin
0x00000001800162ce: 430f110467                     movups     xmmword ptr [r15 + r12*2], xmm0
0x00000001800162d3: 0f10057ce40400                 movups     xmm0, xmmword ptr [rip + 0x4e47c]
0x00000001800162da: 430f11446710                   movups     xmmword ptr [r15 + r12*2 + 0x10], xmm0
0x00000001800162e0: 660f10057ee40400               movupd     xmm0, xmmword ptr [rip + 0x4e47e]
0x00000001800162e8: 66430f11446720                 movupd     xmmword ptr [r15 + r12*2 + 0x20], xmm0
0x00000001800162ef: 43c74467306e000000             mov        dword ptr [r15 + r12*2 + 0x30], 0x6e
0x00000001800162f8: 48837dc808                     cmp        qword ptr [rbp - 0x38], 8
0x00000001800162fd: 7204                           jb         0x180016303
0x00000001800162ff: 4c8b75b0                       mov        r14, qword ptr [rbp - 0x50]
0x0000000180016303: 488d15a6e40400                 lea        rdx, [rip + 0x4e4a6]
0x000000018001630a: 4c89f1                         mov        rcx, r14
0x000000018001630d: e896b30100                     call       0x1800316a8
0x0000000180016312: 488bb508000100                 mov        rsi, qword ptr [rbp + 0x10008]
0x0000000180016319: 4885c0                         test       rax, rax
```

```asm
0x000000018001638f: 4c89c1                         mov        rcx, r8
0x0000000180016392: e8e9430100                     call       0x18002a780
0x0000000180016397: 4084ff                         test       dil, dil
0x000000018001639a: 7469                           je         0x180016405
0x000000018001639c: 488b85a8000100                 mov        rax, qword ptr [rbp + 0x100a8]
0x00000001800163a3: 482b85a0000100                 sub        rax, qword ptr [rbp + 0x100a0]
0x00000001800163aa: 66480f6ec0                     movq       xmm0, rax
0x00000001800163af: 660f620519f60300               punpckldq  xmm0, xmmword ptr [rip + 0x3f619]
0x00000001800163b7: 660f5c0521f60300               subpd      xmm0, xmmword ptr [rip + 0x3f621]
0x00000001800163bf: 660f28c8                       movapd     xmm1, xmm0
0x00000001800163c3: 660f15c8                       unpckhpd   xmm1, xmm0
0x00000001800163c7: f20f58c8                       addsd      xmm1, xmm0
0x00000001800163cb: f20f590d1df60300               mulsd      xmm1, qword ptr [rip + 0x3f61d]
0x00000001800163d3: f20f114c2420                   movsd      qword ptr [rsp + 0x20], xmm1
0x00000001800163d9: 4c8d05a7e00400                 lea        r8, [rip + 0x4e0a7]    ; XREF -> wrote %zu blobs, %.1f MB -> dlssnr_on_amd_weights.bin
0x00000001800163e0: 488d5db0                       lea        rbx, [rbp - 0x50]
0x00000001800163e4: ba80000000                     mov        edx, 0x80
0x00000001800163e9: 4889d9                         mov        rcx, rbx
0x00000001800163ec: 4989f1                         mov        r9, rsi
0x00000001800163ef: e8dcb7ffff                     call       0x180011bd0
0x00000001800163f4: 488b8d98000100                 mov        rcx, qword ptr [rbp + 0x10098]
0x00000001800163fb: 4889da                         mov        rdx, rbx
0x00000001800163fe: e86d91ffff                     call       0x18000f570
0x0000000180016403: eb13                           jmp        0x180016418
0x0000000180016405: 488d1553e00400                 lea        rdx, [rip + 0x4e053]    ; XREF -> cannot write dlssnr_on_amd_weights.bin
0x000000018001640c: 488b8d98000100                 mov        rcx, qword ptr [rbp + 0x10098]
0x0000000180016413: e85891ffff                     call       0x18000f570
0x0000000180016418: 488b85d8000100                 mov        rax, qword ptr [rbp + 0x100d8]
0x000000018001641f: 4883f808                       cmp        rax, 8
0x0000000180016423: 723f                           jb         0x180016464
0x0000000180016425: 488b8dc0000100                 mov        rcx, qword ptr [rbp + 0x100c0]
0x000000018001642c: 488d144502000000               lea        rdx, [rax*2 + 2]
0x0000000180016434: 4881fa00100000                 cmp        rdx, 0x1000
0x000000018001643b: 7222                           jb         0x18001645f
0x000000018001643d: 4c8b41f8                       mov        r8, qword ptr [rcx - 8]
0x0000000180016441: 4883c1f8                       add        rcx, -8
0x0000000180016445: 4c29c1                         sub        rcx, r8
0x0000000180016448: 4883f920                       cmp        rcx, 0x20
0x000000018001644c: 0f83d3000000                   jae        0x180016525
```

### `runtime_debug_controls` — PE 1 RVA `0x1db30`–`0x20622`

- References: `DLSSNR_SLOW_PREPOST`
- References: `DLSSNR_NOBLEND`
- References: `DLSSNR_NOPOSTHIST`

```asm
0x000000018002052a: 5f                             pop        rdi
0x000000018002052b: 5e                             pop        rsi
0x000000018002052c: 415c                           pop        r12
0x000000018002052e: 415d                           pop        r13
0x0000000180020530: 415e                           pop        r14
0x0000000180020532: 415f                           pop        r15
0x0000000180020534: 5d                             pop        rbp
0x0000000180020535: c3                             ret
0x0000000180020536: 0f0b                           ud2
0x0000000180020538: 488d0d753a0500                 lea        rcx, [rip + 0x53a75]
0x000000018002053f: e870a20000                     call       0x18002a7b4
0x0000000180020544: 488b8db0060000                 mov        rcx, qword ptr [rbp + 0x6b0]
0x000000018002054b: 833d623a0500ff                 cmp        dword ptr [rip + 0x53a62], -1
0x0000000180020552: 0f8543d6ffff                   jne        0x18001db9b
0x0000000180020558: 488d0dab300400                 lea        rcx, [rip + 0x430ab]    ; XREF -> DLSSNR_SLOW_PREPOST
0x000000018002055f: e8306c0100                     call       0x180037194
0x0000000180020564: 4885c0                         test       rax, rax
0x0000000180020567: 0f9505423a0500                 setne      byte ptr [rip + 0x53a42]
0x000000018002056e: 488d0d3f3a0500                 lea        rcx, [rip + 0x53a3f]
0x0000000180020575: e8b6a20000                     call       0x18002a830
0x000000018002057a: 488b8db0060000                 mov        rcx, qword ptr [rbp + 0x6b0]
0x0000000180020581: e915d6ffff                     jmp        0x18001db9b
0x0000000180020586: 488d0d2f3a0500                 lea        rcx, [rip + 0x53a2f]
0x000000018002058d: e822a20000                     call       0x18002a7b4
0x0000000180020592: 488b8db0060000                 mov        rcx, qword ptr [rbp + 0x6b0]
0x0000000180020599: 833d1c3a0500ff                 cmp        dword ptr [rip + 0x53a1c], -1
0x00000001800205a0: 0f85edf7ffff                   jne        0x18001fd93
0x00000001800205a6: 488d0dc7300400                 lea        rcx, [rip + 0x430c7]    ; XREF -> DLSSNR_NOBLEND
0x00000001800205ad: e8e26b0100                     call       0x180037194
0x00000001800205b2: 4885c0                         test       rax, rax
0x00000001800205b5: 0f9505fc390500                 setne      byte ptr [rip + 0x539fc]
0x00000001800205bc: 488d0df9390500                 lea        rcx, [rip + 0x539f9]
0x00000001800205c3: e868a20000                     call       0x18002a830
0x00000001800205c8: 488b8db0060000                 mov        rcx, qword ptr [rbp + 0x6b0]
0x00000001800205cf: e9bff7ffff                     jmp        0x18001fd93
0x00000001800205d4: 488d0de9390500                 lea        rcx, [rip + 0x539e9]
0x00000001800205db: e8d4a10000                     call       0x18002a7b4
0x00000001800205e0: 488b8db0060000                 mov        rcx, qword ptr [rbp + 0x6b0]
0x00000001800205e7: 833dd6390500ff                 cmp        dword ptr [rip + 0x539d6], -1
0x00000001800205ee: 0f85c5f7ffff                   jne        0x18001fdb9
0x00000001800205f4: 488d0d23300400                 lea        rcx, [rip + 0x43023]    ; XREF -> DLSSNR_NOPOSTHIST
0x00000001800205fb: e8946b0100                     call       0x180037194
0x0000000180020600: 4885c0                         test       rax, rax
0x0000000180020603: 0f9505b6390500                 setne      byte ptr [rip + 0x539b6]
0x000000018002060a: 488d0db3390500                 lea        rcx, [rip + 0x539b3]
0x0000000180020611: e81aa20000                     call       0x18002a830
0x0000000180020616: 488b8db0060000                 mov        rcx, qword ptr [rbp + 0x6b0]
0x000000018002061d: e997f7ffff                     jmp        0x18001fdb9
```

### `runtime_debug_controls` — PE 1 RVA `0x234c0`–`0x235ab`

- References: `DLSSNR_WBLOG`

```asm
0x000000018002354e: 4989f8                         mov        r8, rdi
0x0000000180023551: e85a000000                     call       0x1800235b0
0x0000000180023556: 488b4610                       mov        rax, qword ptr [rsi + 0x10]
0x000000018002355a: 4883c430                       add        rsp, 0x30
0x000000018002355e: 5b                             pop        rbx
0x000000018002355f: 5f                             pop        rdi
0x0000000180023560: 5e                             pop        rsi
0x0000000180023561: c3                             ret
0x0000000180023562: 488d0d6b0a0500                 lea        rcx, [rip + 0x50a6b]
0x0000000180023569: 4889c3                         mov        rbx, rax
0x000000018002356c: e843720000                     call       0x18002a7b4
0x0000000180023571: 4889d8                         mov        rax, rbx
0x0000000180023574: 833d590a0500ff                 cmp        dword ptr [rip + 0x50a59], -1
0x000000018002357b: 0f8577ffffff                   jne        0x1800234f8
0x0000000180023581: 488d0dd6000400                 lea        rcx, [rip + 0x400d6]    ; XREF -> DLSSNR_WBLOG
0x0000000180023588: e8073c0100                     call       0x180037194
0x000000018002358d: 4885c0                         test       rax, rax
0x0000000180023590: 0f9505390a0500                 setne      byte ptr [rip + 0x50a39]
0x0000000180023597: 488d0d360a0500                 lea        rcx, [rip + 0x50a36]
0x000000018002359e: e88d720000                     call       0x18002a830
0x00000001800235a3: 4889d8                         mov        rax, rbx
0x00000001800235a6: e94dffffff                     jmp        0x1800234f8
```

## AMDGPU kernel ABI

### Code object 0 at `0xb0e00`

- Size/hash: `1179328` / `e363aa788e7626b93c6c449583e3c3bf340a6fa69d434cf98285fef12ec6b21a`
- Target metadata: `["amdgcn-amd-amdhsa--gfx1100"]`
- Relevant kernels: `20`

#### `_Z16k_swin_1h_32_fp810SwinParams`

- Kernarg `296` bytes; LDS `62592`; SGPR/VGPR `35/194`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z21k_pre_block_1h_32_fp89PreParams`

- Kernarg `336` bytes; LDS `64640`; SGPR/VGPR `45/194`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z22k_post_block_1h_32_fp810PostParams`

- Kernarg `336` bytes; LDS `62592`; SGPR/VGPR `43/194`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_conv_res10ConvParams`

- Kernarg `296` bytes; LDS `8192`; SGPR/VGPR `18/87`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_qkv_attn10AttnParams`

- Kernarg `296` bytes; LDS `58368`; SGPR/VGPR `32/102`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z11k_conv_res211Conv2Params`

- Kernarg `320` bytes; LDS `0`; SGPR/VGPR `107/185`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 64 | `None` | `None` | `by_value` |
| 64 | 4 | `None` | `None` | `hidden_block_count_x` |
| 68 | 4 | `None` | `None` | `hidden_block_count_y` |
| 72 | 4 | `None` | `None` | `hidden_block_count_z` |
| 76 | 2 | `None` | `None` | `hidden_group_size_x` |
| 78 | 2 | `None` | `None` | `hidden_group_size_y` |
| 80 | 2 | `None` | `None` | `hidden_group_size_z` |
| 82 | 2 | `None` | `None` | `hidden_remainder_x` |
| 84 | 2 | `None` | `None` | `hidden_remainder_y` |
| 86 | 2 | `None` | `None` | `hidden_remainder_z` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 128 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z11k_qkv_attn210AttnParams`

- Kernarg `296` bytes; LDS `23808`; SGPR/VGPR `49/148`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z8k_expand12ExpandParams`

- Kernarg `280` bytes; LDS `16384`; SGPR/VGPR `20/90`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z13k_conv_splitk12ConvParams1d`

- Kernarg `304` bytes; LDS `4096`; SGPR/VGPR `42/51`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z5k_qkv9QkvParams`

- Kernarg `296` bytes; LDS `6144`; SGPR/VGPR `106/69`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z9k_expand212ExpandParams`

- Kernarg `280` bytes; LDS `0`; SGPR/VGPR `25/163`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z11k_contract212ConvParams1d`

- Kernarg `304` bytes; LDS `16384`; SGPR/VGPR `69/168`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z6k_qkv29QkvParams`

- Kernarg `296` bytes; LDS `12800`; SGPR/VGPR `34/123`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z16k_conv_res_views12ConvPlParams`

- Kernarg `328` bytes; LDS `24576`; SGPR/VGPR `51/137`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 72 | `None` | `None` | `by_value` |
| 72 | 4 | `None` | `None` | `hidden_block_count_x` |
| 76 | 4 | `None` | `None` | `hidden_block_count_y` |
| 80 | 4 | `None` | `None` | `hidden_block_count_z` |
| 84 | 2 | `None` | `None` | `hidden_group_size_x` |
| 86 | 2 | `None` | `None` | `hidden_group_size_y` |
| 88 | 2 | `None` | `None` | `hidden_group_size_z` |
| 90 | 2 | `None` | `None` | `hidden_remainder_x` |
| 92 | 2 | `None` | `None` | `hidden_remainder_y` |
| 94 | 2 | `None` | `None` | `hidden_remainder_z` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 136 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z8k_repack12RepackParams`

- Kernarg `288` bytes; LDS `0`; SGPR/VGPR `20/17`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 32 | `None` | `None` | `by_value` |
| 32 | 4 | `None` | `None` | `hidden_block_count_x` |
| 36 | 4 | `None` | `None` | `hidden_block_count_y` |
| 40 | 4 | `None` | `None` | `hidden_block_count_z` |
| 44 | 2 | `None` | `None` | `hidden_group_size_x` |
| 46 | 2 | `None` | `None` | `hidden_group_size_y` |
| 48 | 2 | `None` | `None` | `hidden_group_size_z` |
| 50 | 2 | `None` | `None` | `hidden_remainder_x` |
| 52 | 2 | `None` | `None` | `hidden_remainder_y` |
| 54 | 2 | `None` | `None` | `hidden_remainder_z` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 96 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi32ELb1EEv9VarParams`

- Kernarg `424` bytes; LDS `15616`; SGPR/VGPR `69/103`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi32ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `15632`; SGPR/VGPR `65/92`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi64ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `15616`; SGPR/VGPR `76/125`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi128ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `15616`; SGPR/VGPR `76/136`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi256ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `19200`; SGPR/VGPR `76/136`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

### Code object 1 at `0x1d0e00`

- Size/hash: `1179328` / `109498324c893b11b8feea1025068f69c5aa56d20b5d06d83d167005ab202110`
- Target metadata: `["amdgcn-amd-amdhsa--gfx1101"]`
- Relevant kernels: `20`

#### `_Z16k_swin_1h_32_fp810SwinParams`

- Kernarg `296` bytes; LDS `62592`; SGPR/VGPR `35/194`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z21k_pre_block_1h_32_fp89PreParams`

- Kernarg `336` bytes; LDS `64640`; SGPR/VGPR `45/194`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z22k_post_block_1h_32_fp810PostParams`

- Kernarg `336` bytes; LDS `62592`; SGPR/VGPR `43/194`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_conv_res10ConvParams`

- Kernarg `296` bytes; LDS `8192`; SGPR/VGPR `18/87`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_qkv_attn10AttnParams`

- Kernarg `296` bytes; LDS `58368`; SGPR/VGPR `32/102`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z11k_conv_res211Conv2Params`

- Kernarg `320` bytes; LDS `0`; SGPR/VGPR `107/185`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 64 | `None` | `None` | `by_value` |
| 64 | 4 | `None` | `None` | `hidden_block_count_x` |
| 68 | 4 | `None` | `None` | `hidden_block_count_y` |
| 72 | 4 | `None` | `None` | `hidden_block_count_z` |
| 76 | 2 | `None` | `None` | `hidden_group_size_x` |
| 78 | 2 | `None` | `None` | `hidden_group_size_y` |
| 80 | 2 | `None` | `None` | `hidden_group_size_z` |
| 82 | 2 | `None` | `None` | `hidden_remainder_x` |
| 84 | 2 | `None` | `None` | `hidden_remainder_y` |
| 86 | 2 | `None` | `None` | `hidden_remainder_z` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 128 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z11k_qkv_attn210AttnParams`

- Kernarg `296` bytes; LDS `23808`; SGPR/VGPR `49/148`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z8k_expand12ExpandParams`

- Kernarg `280` bytes; LDS `16384`; SGPR/VGPR `20/90`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z13k_conv_splitk12ConvParams1d`

- Kernarg `304` bytes; LDS `4096`; SGPR/VGPR `42/51`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z5k_qkv9QkvParams`

- Kernarg `296` bytes; LDS `6144`; SGPR/VGPR `106/69`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z9k_expand212ExpandParams`

- Kernarg `280` bytes; LDS `0`; SGPR/VGPR `25/163`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z11k_contract212ConvParams1d`

- Kernarg `304` bytes; LDS `16384`; SGPR/VGPR `69/168`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z6k_qkv29QkvParams`

- Kernarg `296` bytes; LDS `12800`; SGPR/VGPR `34/123`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z16k_conv_res_views12ConvPlParams`

- Kernarg `328` bytes; LDS `24576`; SGPR/VGPR `51/137`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 72 | `None` | `None` | `by_value` |
| 72 | 4 | `None` | `None` | `hidden_block_count_x` |
| 76 | 4 | `None` | `None` | `hidden_block_count_y` |
| 80 | 4 | `None` | `None` | `hidden_block_count_z` |
| 84 | 2 | `None` | `None` | `hidden_group_size_x` |
| 86 | 2 | `None` | `None` | `hidden_group_size_y` |
| 88 | 2 | `None` | `None` | `hidden_group_size_z` |
| 90 | 2 | `None` | `None` | `hidden_remainder_x` |
| 92 | 2 | `None` | `None` | `hidden_remainder_y` |
| 94 | 2 | `None` | `None` | `hidden_remainder_z` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 136 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z8k_repack12RepackParams`

- Kernarg `288` bytes; LDS `0`; SGPR/VGPR `20/17`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 32 | `None` | `None` | `by_value` |
| 32 | 4 | `None` | `None` | `hidden_block_count_x` |
| 36 | 4 | `None` | `None` | `hidden_block_count_y` |
| 40 | 4 | `None` | `None` | `hidden_block_count_z` |
| 44 | 2 | `None` | `None` | `hidden_group_size_x` |
| 46 | 2 | `None` | `None` | `hidden_group_size_y` |
| 48 | 2 | `None` | `None` | `hidden_group_size_z` |
| 50 | 2 | `None` | `None` | `hidden_remainder_x` |
| 52 | 2 | `None` | `None` | `hidden_remainder_y` |
| 54 | 2 | `None` | `None` | `hidden_remainder_z` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 96 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi32ELb1EEv9VarParams`

- Kernarg `424` bytes; LDS `15616`; SGPR/VGPR `69/103`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi32ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `15632`; SGPR/VGPR `65/92`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi64ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `15616`; SGPR/VGPR `76/125`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi128ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `15616`; SGPR/VGPR `76/136`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi256ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `19200`; SGPR/VGPR `76/136`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

### Code object 2 at `0x2f0e00`

- Size/hash: `1181048` / `3708f939e94fa7295afc5f80463a8774a84af446f68f8981dc15ae9b923c3958`
- Target metadata: `["amdgcn-amd-amdhsa--gfx1102"]`
- Relevant kernels: `20`

#### `_Z16k_swin_1h_32_fp810SwinParams`

- Kernarg `296` bytes; LDS `62592`; SGPR/VGPR `35/194`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z21k_pre_block_1h_32_fp89PreParams`

- Kernarg `336` bytes; LDS `64640`; SGPR/VGPR `45/194`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z22k_post_block_1h_32_fp810PostParams`

- Kernarg `336` bytes; LDS `62592`; SGPR/VGPR `43/194`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_conv_res10ConvParams`

- Kernarg `296` bytes; LDS `8192`; SGPR/VGPR `18/59`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_qkv_attn10AttnParams`

- Kernarg `296` bytes; LDS `58368`; SGPR/VGPR `32/102`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z11k_conv_res211Conv2Params`

- Kernarg `320` bytes; LDS `0`; SGPR/VGPR `107/179`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 64 | `None` | `None` | `by_value` |
| 64 | 4 | `None` | `None` | `hidden_block_count_x` |
| 68 | 4 | `None` | `None` | `hidden_block_count_y` |
| 72 | 4 | `None` | `None` | `hidden_block_count_z` |
| 76 | 2 | `None` | `None` | `hidden_group_size_x` |
| 78 | 2 | `None` | `None` | `hidden_group_size_y` |
| 80 | 2 | `None` | `None` | `hidden_group_size_z` |
| 82 | 2 | `None` | `None` | `hidden_remainder_x` |
| 84 | 2 | `None` | `None` | `hidden_remainder_y` |
| 86 | 2 | `None` | `None` | `hidden_remainder_z` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 128 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z11k_qkv_attn210AttnParams`

- Kernarg `296` bytes; LDS `23808`; SGPR/VGPR `49/148`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z8k_expand12ExpandParams`

- Kernarg `280` bytes; LDS `16384`; SGPR/VGPR `20/64`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z13k_conv_splitk12ConvParams1d`

- Kernarg `304` bytes; LDS `4096`; SGPR/VGPR `42/51`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z5k_qkv9QkvParams`

- Kernarg `296` bytes; LDS `6144`; SGPR/VGPR `106/69`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z9k_expand212ExpandParams`

- Kernarg `280` bytes; LDS `0`; SGPR/VGPR `25/168`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z11k_contract212ConvParams1d`

- Kernarg `304` bytes; LDS `16384`; SGPR/VGPR `69/171`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z6k_qkv29QkvParams`

- Kernarg `296` bytes; LDS `12800`; SGPR/VGPR `34/123`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z16k_conv_res_views12ConvPlParams`

- Kernarg `328` bytes; LDS `24576`; SGPR/VGPR `51/112`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 72 | `None` | `None` | `by_value` |
| 72 | 4 | `None` | `None` | `hidden_block_count_x` |
| 76 | 4 | `None` | `None` | `hidden_block_count_y` |
| 80 | 4 | `None` | `None` | `hidden_block_count_z` |
| 84 | 2 | `None` | `None` | `hidden_group_size_x` |
| 86 | 2 | `None` | `None` | `hidden_group_size_y` |
| 88 | 2 | `None` | `None` | `hidden_group_size_z` |
| 90 | 2 | `None` | `None` | `hidden_remainder_x` |
| 92 | 2 | `None` | `None` | `hidden_remainder_y` |
| 94 | 2 | `None` | `None` | `hidden_remainder_z` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 136 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z8k_repack12RepackParams`

- Kernarg `288` bytes; LDS `0`; SGPR/VGPR `20/17`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 32 | `None` | `None` | `by_value` |
| 32 | 4 | `None` | `None` | `hidden_block_count_x` |
| 36 | 4 | `None` | `None` | `hidden_block_count_y` |
| 40 | 4 | `None` | `None` | `hidden_block_count_z` |
| 44 | 2 | `None` | `None` | `hidden_group_size_x` |
| 46 | 2 | `None` | `None` | `hidden_group_size_y` |
| 48 | 2 | `None` | `None` | `hidden_group_size_z` |
| 50 | 2 | `None` | `None` | `hidden_remainder_x` |
| 52 | 2 | `None` | `None` | `hidden_remainder_y` |
| 54 | 2 | `None` | `None` | `hidden_remainder_z` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 96 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi32ELb1EEv9VarParams`

- Kernarg `424` bytes; LDS `15616`; SGPR/VGPR `69/91`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi32ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `15632`; SGPR/VGPR `65/95`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi64ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `15616`; SGPR/VGPR `76/125`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi128ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `15616`; SGPR/VGPR `76/125`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi256ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `19200`; SGPR/VGPR `76/125`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

### Code object 3 at `0x411e00`

- Size/hash: `505096` / `12fdd63876ad0cf9b70c947d369bd8b0ed00aa2345021076d72a008dc8e1f4cd`
- Target metadata: `["amdgcn-amd-amdhsa--gfx1201"]`
- Relevant kernels: `20`

#### `_Z16k_swin_1h_32_fp810SwinParams`

- Kernarg `296` bytes; LDS `62592`; SGPR/VGPR `25/72`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z21k_pre_block_1h_32_fp89PreParams`

- Kernarg `336` bytes; LDS `64640`; SGPR/VGPR `44/72`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z22k_post_block_1h_32_fp810PostParams`

- Kernarg `336` bytes; LDS `62592`; SGPR/VGPR `43/70`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 80 | `None` | `None` | `by_value` |
| 80 | 4 | `None` | `None` | `hidden_block_count_x` |
| 84 | 4 | `None` | `None` | `hidden_block_count_y` |
| 88 | 4 | `None` | `None` | `hidden_block_count_z` |
| 92 | 2 | `None` | `None` | `hidden_group_size_x` |
| 94 | 2 | `None` | `None` | `hidden_group_size_y` |
| 96 | 2 | `None` | `None` | `hidden_group_size_z` |
| 98 | 2 | `None` | `None` | `hidden_remainder_x` |
| 100 | 2 | `None` | `None` | `hidden_remainder_y` |
| 102 | 2 | `None` | `None` | `hidden_remainder_z` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 136 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 144 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_conv_res10ConvParams`

- Kernarg `296` bytes; LDS `8192`; SGPR/VGPR `17/60`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_qkv_attn10AttnParams`

- Kernarg `296` bytes; LDS `58368`; SGPR/VGPR `30/94`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z11k_conv_res211Conv2Params`

- Kernarg `320` bytes; LDS `0`; SGPR/VGPR `107/203`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 64 | `None` | `None` | `by_value` |
| 64 | 4 | `None` | `None` | `hidden_block_count_x` |
| 68 | 4 | `None` | `None` | `hidden_block_count_y` |
| 72 | 4 | `None` | `None` | `hidden_block_count_z` |
| 76 | 2 | `None` | `None` | `hidden_group_size_x` |
| 78 | 2 | `None` | `None` | `hidden_group_size_y` |
| 80 | 2 | `None` | `None` | `hidden_group_size_z` |
| 82 | 2 | `None` | `None` | `hidden_remainder_x` |
| 84 | 2 | `None` | `None` | `hidden_remainder_y` |
| 86 | 2 | `None` | `None` | `hidden_remainder_z` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 128 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z11k_qkv_attn210AttnParams`

- Kernarg `296` bytes; LDS `23808`; SGPR/VGPR `33/99`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z8k_expand12ExpandParams`

- Kernarg `280` bytes; LDS `16384`; SGPR/VGPR `19/41`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z13k_conv_splitk12ConvParams1d`

- Kernarg `304` bytes; LDS `4096`; SGPR/VGPR `31/82`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z5k_qkv9QkvParams`

- Kernarg `296` bytes; LDS `6144`; SGPR/VGPR `40/119`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z9k_expand212ExpandParams`

- Kernarg `280` bytes; LDS `0`; SGPR/VGPR `20/162`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 24 | `None` | `None` | `by_value` |
| 24 | 4 | `None` | `None` | `hidden_block_count_x` |
| 28 | 4 | `None` | `None` | `hidden_block_count_y` |
| 32 | 4 | `None` | `None` | `hidden_block_count_z` |
| 36 | 2 | `None` | `None` | `hidden_group_size_x` |
| 38 | 2 | `None` | `None` | `hidden_group_size_y` |
| 40 | 2 | `None` | `None` | `hidden_group_size_z` |
| 42 | 2 | `None` | `None` | `hidden_remainder_x` |
| 44 | 2 | `None` | `None` | `hidden_remainder_y` |
| 46 | 2 | `None` | `None` | `hidden_remainder_z` |
| 64 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 88 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z11k_contract212ConvParams1d`

- Kernarg `304` bytes; LDS `16384`; SGPR/VGPR `55/170`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 48 | `None` | `None` | `by_value` |
| 48 | 4 | `None` | `None` | `hidden_block_count_x` |
| 52 | 4 | `None` | `None` | `hidden_block_count_y` |
| 56 | 4 | `None` | `None` | `hidden_block_count_z` |
| 60 | 2 | `None` | `None` | `hidden_group_size_x` |
| 62 | 2 | `None` | `None` | `hidden_group_size_y` |
| 64 | 2 | `None` | `None` | `hidden_group_size_z` |
| 66 | 2 | `None` | `None` | `hidden_remainder_x` |
| 68 | 2 | `None` | `None` | `hidden_remainder_y` |
| 70 | 2 | `None` | `None` | `hidden_remainder_z` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 104 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 112 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z6k_qkv29QkvParams`

- Kernarg `296` bytes; LDS `12800`; SGPR/VGPR `20/96`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 40 | `None` | `None` | `by_value` |
| 40 | 4 | `None` | `None` | `hidden_block_count_x` |
| 44 | 4 | `None` | `None` | `hidden_block_count_y` |
| 48 | 4 | `None` | `None` | `hidden_block_count_z` |
| 52 | 2 | `None` | `None` | `hidden_group_size_x` |
| 54 | 2 | `None` | `None` | `hidden_group_size_y` |
| 56 | 2 | `None` | `None` | `hidden_group_size_z` |
| 58 | 2 | `None` | `None` | `hidden_remainder_x` |
| 60 | 2 | `None` | `None` | `hidden_remainder_y` |
| 62 | 2 | `None` | `None` | `hidden_remainder_z` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 96 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 104 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z16k_conv_res_views12ConvPlParams`

- Kernarg `328` bytes; LDS `24576`; SGPR/VGPR `49/90`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 72 | `None` | `None` | `by_value` |
| 72 | 4 | `None` | `None` | `hidden_block_count_x` |
| 76 | 4 | `None` | `None` | `hidden_block_count_y` |
| 80 | 4 | `None` | `None` | `hidden_block_count_z` |
| 84 | 2 | `None` | `None` | `hidden_group_size_x` |
| 86 | 2 | `None` | `None` | `hidden_group_size_y` |
| 88 | 2 | `None` | `None` | `hidden_group_size_z` |
| 90 | 2 | `None` | `None` | `hidden_remainder_x` |
| 92 | 2 | `None` | `None` | `hidden_remainder_y` |
| 94 | 2 | `None` | `None` | `hidden_remainder_z` |
| 112 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 120 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 128 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 136 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z8k_repack12RepackParams`

- Kernarg `288` bytes; LDS `0`; SGPR/VGPR `21/15`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 32 | `None` | `None` | `by_value` |
| 32 | 4 | `None` | `None` | `hidden_block_count_x` |
| 36 | 4 | `None` | `None` | `hidden_block_count_y` |
| 40 | 4 | `None` | `None` | `hidden_block_count_z` |
| 44 | 2 | `None` | `None` | `hidden_group_size_x` |
| 46 | 2 | `None` | `None` | `hidden_group_size_y` |
| 48 | 2 | `None` | `None` | `hidden_group_size_z` |
| 50 | 2 | `None` | `None` | `hidden_remainder_x` |
| 52 | 2 | `None` | `None` | `hidden_remainder_y` |
| 54 | 2 | `None` | `None` | `hidden_remainder_z` |
| 72 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 80 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 88 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 96 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi32ELb1EEv9VarParams`

- Kernarg `424` bytes; LDS `15616`; SGPR/VGPR `82/81`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi32ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `15632`; SGPR/VGPR `67/76`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi64ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `15616`; SGPR/VGPR `61/120`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi128ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `15616`; SGPR/VGPR `60/120`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

#### `_Z10k_swin_varILi256ELb0EEv9VarParams`

- Kernarg `424` bytes; LDS `19200`; SGPR/VGPR `60/120`; wave `32`.

| Offset | Size | Name | Type | Kind |
|---:|---:|---|---|---|
| 0 | 168 | `None` | `None` | `by_value` |
| 168 | 4 | `None` | `None` | `hidden_block_count_x` |
| 172 | 4 | `None` | `None` | `hidden_block_count_y` |
| 176 | 4 | `None` | `None` | `hidden_block_count_z` |
| 180 | 2 | `None` | `None` | `hidden_group_size_x` |
| 182 | 2 | `None` | `None` | `hidden_group_size_y` |
| 184 | 2 | `None` | `None` | `hidden_group_size_z` |
| 186 | 2 | `None` | `None` | `hidden_remainder_x` |
| 188 | 2 | `None` | `None` | `hidden_remainder_y` |
| 190 | 2 | `None` | `None` | `hidden_remainder_z` |
| 208 | 8 | `None` | `None` | `hidden_global_offset_x` |
| 216 | 8 | `None` | `None` | `hidden_global_offset_y` |
| 224 | 8 | `None` | `None` | `hidden_global_offset_z` |
| 232 | 2 | `None` | `None` | `hidden_grid_dims` |

## Success gates

1. Decode and round-trip the `DLSSNRW1` header/index without using captured activations.
2. Map independent private tensors into the same logical blob order and verify hashes/shapes locally.
3. Reproduce fixed-contract `expand2 -> activation/FP8 -> contract2` and QKV/Swin blocks numerically.
4. Complete pre/repack, convolutional encoder/decoder, history/blend and post stages.
5. Validate one full frame through the reference graph, then the HIP backend.
6. Export ONNX only from the already validated reference graph and require end-to-end PNG equivalence.
