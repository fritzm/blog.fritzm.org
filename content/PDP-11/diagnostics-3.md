Title: PDP-11/45: Diagnostics III - CKBME0
Date: 2016-7-9
Tags: Retro-Computing, PDP-11

Okay, digging into the CKBME0 traps diagnostic now in more detail.  Here I've transcribed the source of the failing
test from the older available diagnostic listing, then re-assembled it at the address matching the more modern
binary.  This makes it a little easier to follow along while debugging the newer binary:

    #!masm
    013604 000230                          SPL     0               ;SET PRIORITY LEVEL 0
    013606 012706  000500                  MOV     #STKPTR,%6      ;SET STACK PTR
    013612 012737  013650  000064          MOV     #TTY7A,@#TPVEC  ;LOAD TTY INTERRUPT VECTOR
    013620 012737  013644  000014          MOV     #TTY7B,@#BPTVEC ;LOAD 'T' BIT TRAP VECTOR
    013626 005002                          CLR     %2              ;CLEAR INDICATOR
    013630 052737  000100  177564          BIS     #100,@#TTCSR    ;ALLOW INTERRUPT INTERRUPT OCCURS AFTER
                                                                   ;THIS INSTRUCTION & BEFORE NEXT
    013636 000001                  WAIT1:  WAIT                    ;WAIT FOR AN INTERRUPT
    013640 005202                          INC     %2              ;INCREMENT INDICATOR
    013642 000000                          HLT                     ;ERROR! NO 'T' TRAP AFTER INTERRUPT
    013644 000000                  TTY7B:  HLT                     ;ERROR! 'T' BIT TRAPPED OUT OF WAIT
    013646 000424                          BR      TTY7EX          ;EXIT TEST
    013650 012737  000040  177566  TTY7A:  MOV     #40,@#177566    ;TYPE SPACE CHAR
    013656 012737  013674  000064          MOV     #TTY7C,@#TPVEC  ;REPOSITION TTY INT VECTOR
    013664 012766  000020  000002          MOV     #20,2(6)        ;PUT 'T' BIT IN RETURN STATUS
    013672 000006                          RTT                     ;RETURN TO WAIT WITH 'T' BIT SET
                                                                   ;AND WAIT FOR TTY INTERRUPT WHEN NULL
                                                                   ;CHARACTER IS TYPED
    013674 012737  013716  000014  TTY7C:  MOV     #TTY7D,@#BPTVEC ;REPOINT 'T' BIT TRAP VECTOR AFTER
                                                                   ;TTY HAS INTERRUPTED
    013702 005037  177564                  CLR     @#TTCSR         ;DISABLE INTERRUPT ENABLE
    013706 012737  000015  177566          MOV     #15,@#177566
    013714 000006                          RTT                     ;RETURN TO INST FOLLOWING WAIT WITH 'T'
                                                                   ;BIT SET
    013716 000240                  TTY7D:  NOP
    013720 012737  000016  000014  TTY7EX: MOV     #BPTVEC+2,@#BPTVEC;RESTORE VECTORS TO HALT AT
    013726 012737  000066  000064          MOV     #66,@#TPVEC     ;VECTOR +2
    013734 005302                          DEC     %2              ;CHECK INDICATOR
    013736 001401                          BEQ     .+4
    013740 000000                          HLT                     ;ERROR! DID NOT DO INC INST AFTER INTERRUPT

This test seems to be designed to return from an interrupt handler to a WAIT instruction, with the T bit set in
the PSW and a serial xmit interrupt pending.  It verifies that the WAIT still "waits" in this circumstance.  It also
verifies that a trace trap *does* occur after the immediately following INC instruction when the xmit interrupt
subsequently terminates the WAIT.

One potential problem with this test concerns the apparent assumption that enabling the xmit interrupt will cause an
immediate trap before the subsequent WAIT instruction.  This is true if the serial transmitter is empty, but if the
transmitter is ever full/busy when this code is entered this assumption may not hold.  Not sure yet if this will ever
be a problem for this test given the surrounding code.

In any case, as currently written this routine fails about 50% of the time on my 11/45.  The failure mode
is that the processor sits at the WAIT instruction, (address display 013640, PC+2).  Intervention with the
console halt switch (halt then back to enabl) breaks the WAIT microcode loop; console cont then takes us to the halt
at 013740 (address display 013742, PC+2).

The fact that the routine is tailing out through the halt at 013740 without hitting the halts at 013642 or 013644 is
interesting; this implies that the second serial xmit interrupt to TTY7C has executed.  This is verified by examining
the break trap from the console after the test hangs up on the WAIT -- in the failure case, it is already reset to
point to TTY7D.  So the failure mode seems to be that the return from the second xmit interrupt sometimes goes to the
WAIT instead of the subsequent INC.

Here is the microcode flow around the WAIT instruction.  The horizontal line across the top is the A fork:

<img src='/images/pdp11/wait-microcode.png'/>

Using the KM11, in the failure case I can see the T bit set and the microcode looping through states WAT.00, WAT.20, WAT.30, WAT.11, which seems expected.  I have also verified that executing a WAIT *without* the T bit set
loops through states WAT.00 and WAT.10.

Lastly, running on the RC maintenance clock at about half the usual clock frequency makes the failure case happen
almost 100% of the time.

Next I'll be needing to learn more about the BRQ logic, and in particular the mechanism by which the second xmit
interrupt nominally causes INTRF to be asserted.  Understanding that should lead me to some things to check with the
logic probe and analyzer...
