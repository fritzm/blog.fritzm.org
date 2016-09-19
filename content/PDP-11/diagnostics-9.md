Title: PDP-11/45: Diagnostics IX - FP11 FPU, cont.
Date: 2016-9-10
Tags: Retro-Computing, PDP-11

Did a lot of reading on the FP11 design.  A few interesting notes that are buried in the maintenance manual:

* When debugging FP11 microcode with a KM11 in single-microstep mode, the 11/45 front panel microcode display shows
the address of the *next* microinstruction, NOT the current microinstruction.  This is because the stop-point for
single microinstruction is at a point between T2 and T3, just *after* the next microinstruction addr has been
calculated.  This is different behavior than the 11/45 CPU front panel microaddress display.

* There's a note in the maintenance manual that explicitly cautions that when using extender boards for debug, the
RC maintenance clock should be used, and set with period >50ns.  I had not been doing similar while debugging the
KB11-A CPU, and maybe this explains the occasional different behavior I'd see when throwing boards out on extenders...
In particular, I had seen this when debugging a spare CPU GRA; next time I return to that board I will try the CPU
RC clock.

Okay, so here's my first simple test program for STST:

    #!masm
    000000                          AC0=%0
    000000                          .ASECT
    001000                          .=1000
    001000  170127  044000  START:  LDFPS   #044000         ;FID+FIUV
    001004  172467  000004          LDF     NEGZ,AC0        ;LOAD A MINUS-ZERO
    001010  170300                  STST    R0              ;STORE FEC TO R0
    001012  000000                  HALT
    001014  100000  000000  NEGZ:   .WORD   100000,000000   ;MINUS-ZERO
    001000                          .END    START

This would be expected to produce the 000014 "Floating Undefined Variable" (minus-zero) exception code in R0, but I see
an incorrect value of 177417.  Using the KM11 on the FPU shows the -0 trap and STST microstate flow is per expectation.

Put the FRL out on the extender and started stepping the microcode, examining the state of the pins at the AC register
file along the way.  In the -0 trap flow, the FEC code 000014 presented (inverted) at TRP.50 via the EALU, and
subsequently retrieved at TRP.60 looks correct. However, the value presented at TRP.70 via QR, BR, and the FALU does
not.  Out of time this weekend; Will have to chase signals back through those paths next time!

<img src='/images/pdp11/minus-zero-microcode.png'/>

