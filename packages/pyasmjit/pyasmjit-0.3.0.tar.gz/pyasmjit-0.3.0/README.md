# PyAsmJIT

*PyAsmJIT* is a Python package for x86/x86_64/ARMv7 assembly code generation
and execution.

This package was developed as part of the BARF project
(https://github.com/programa-stic/barf-project) in order to test instruction
translation from x/86/x86_64/ARM to REIL. The main idea is to be able to run
fragments of code natively. Then, the same fragment is translated to REIL and
executed in a REIL VM. Finally, both final contexts (the one obtained through
native execution and the one from emulation) are compare for differences.

# Installation

The following command installs the package:

```bash
$ python setup.py install
```

# Dependecies

* [NASM] : the Netwide Assembler, a portable 80x86 assembler

# Quickstart

The following extract shows how to execute on-the-fly a fragment of x86_64
assembly code.

```python
import pyasmjit

code = """\
add rax, rbx
"""

context_in = {
    'rax' : 0x1,
    'rbx' : 0x2,
    'rcx' : 0x1,
    'rdx' : 0x1,
    'rdi' : 0x1,
    'rsi' : 0x1,
}

print code
print context_in

rv, context_out = pyasmjit.x86_execute(code, context_in)

print context_out
```
And for ARMv7:

```python
import pyasmjit

code = """\

movs r8, r2, lsl #31
mov r7, #0x7FFFFFFF
mov r8, #0x7FFFFFFF
adds r7, r7, r8
#subs r10, r10, #0xFFFFFFFF
"""

context_in = {
    'r0' : 0x0,
    'r1' : 0x1,
    'r2' : 0x2,
    'r3' : 0x3,
    'r4' : 0x4,
    'r5' : 0x5,
    'r6' : 0x6,
    'r7' : 0x7,
    'r8' : 0x8,
    'r9' : 0x9,
    'r10' : 0xa,
    'r11' : 0xb,
    'r12' : 0xc,
    'apsr' : 0x0,
}

print code
print context_in

rv, context_out, mem = pyasmjit.arm_execute(code, context_in)

print context_out
```

# Overview

The inner workings of the package is very simple. PyAsmJIT communicates with
*nasm* using the ``subprocess`` package. Once the machine code is generated, it
is place in a memory location previously reserved with the proper permissions
flags. Then, the code is executed as a thread.

# Limitations

Currently:

* It does not handle memory operations
* It only works with x86, x86_64 and ARMv7

# License

The BSD 2-Clause License. For more information, see [LICENSE](./LICENSE).

[NASM]: http://nasm.us/
