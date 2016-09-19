Title: PDP-11/45: Diagnostics VIII - FP11 FPU
Date: 2016-9-3
Tags: Retro-Computing, PDP-11

Slotted in FP11 spares that I hadn't tried previously, and this has produced some improved results -- returning to
diagnostic CKBME0 (11/45 traps) this now passes with the floating point installed.  Additionally, diagnostic
CFPAB0 passes.

CFPBB0 and CFPCD0, however, are failing.  Unfortunately, the source code for these is not available in the PDP-11
diagnostics database at retrocmp.  The names of the diagnostics tell which instructions they are testing, though.
CFPBB0 is annotated as testing the STST instruction.  Rather than work through disassembling the rather lengthy
diagnostics, I'll probably just write some simple test programs around the STST instruction for next time.  In the
meantime, I'll do some reading on the FP11 in preparation for microcode-step debug.
