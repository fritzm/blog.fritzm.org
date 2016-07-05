Title: PDP-11/45: Diagnostics II
Date: 2016-7-4
Tags: Retro-Computing, PDP-11

Investigated some of the halted diagnostics a bit today.  CKBGB0 (SPL instruction test) was halting at 001404.
Looking at the sources, the diagnostic was waiting at this point for a transmit interrupt from the DL11 that didn't
seem to be arriving. Some troubleshooting turned up that the vector address on my DL11 was jumpered incorrectly.  Fixed this, and the diagnostic now passes.

CKBME0 (11/45 traps test) is a bit more complicated.  The halt address of 005320 here indicates that the floating
point coprocessor is detected but not trapping per design.  Pulled the floating point cards for now; the diagnostic
now runs through several passes successfully, but regularly hangs up at 013640.  Hitting the halt
switch when it is hung up displays 000342 in the address lights, then with a couple continues it will start up again,
run a bunch more passes, but sooner or later hang up at 013640 again with the same behavior.  This behavior is a
little more difficult to decode because the diagnostic itself is more complicated, and also the binary available from
classicmp is a later revision than the available source code so the addresses don't quite match up.  So I'll need to
spend a little more time reading the diagnostic sources and examining the disassembly in PDP11GUI to make sense of this
one.  And it looks like there will be some downstream work to debug the floating point unit as well; I haven't studied
its design yet at all.
