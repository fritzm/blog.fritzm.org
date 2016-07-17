Title: PDP-11/45: Diagnostics IV - CKBME0
Date: 2016-7-17
Tags: Retro-Computing, PDP-11

Some progress with the CKBME0 diagnostic mentioned previously.  It seems the concern with how the test behaves wrt.
preconditions of the serial interface was well founded.

In order to debug more easily, I extracted the failing test and built a small loop around it, with a pass counter
and display register update, etc.  In the original test suite, a RESET instruction is executed immediately prior to
the failing test, and it takes some time to come around the failing test on each pass, so I included a RESET and
a delay loop in my test code as well.  I then got failure modes and rates consistent with the original test suite.

The experiments previously described had indicated timing sensitivity (e.g. running on the RC maintenance clock at 50%
clock speed changed the pass failure rate from ~50% to 100%) so I began to think more seriously about timing
between the processor and the serial card, and how the time taken to circulate the entire suite of tests could affect
the precondition of the serial interface when entering the test in subsequent passes.  A re-read of the DL11
documentation showed that the transmit data is also double-buffered; if the transmit shift register is empty, a
character written to the output buffer will be latched to the transmit shift register causing the output buffer to
go ready again almost immediately.

I inserted the following code before the BIS/WAIT sequence in the original diagnostic (listed previously), which
establishes consistent preconditions (shift register full, buffer empty) before the BIS.  Success rate went to 100%:

    #!masm
            MOV     #40,@#177566    ;ENSURE XMIT SHIFT REGISTER HAS SOMETHING TO CHEW ON
    L0:     TSTB    @#TTCSR         ;CHECK XMIT BUFFER
            BPL     L0              ;LOOP UNTIL READY, ENSURES INT IMMEDIATELY AFTER BIS

I then further verified that the original diagnostic suite passes 100% if I turn the M7800 down to 1200 Baud.  Worth
noting when trying to run these older diagnostics!
