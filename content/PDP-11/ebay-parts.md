Title: PDP-11/45: Some parts from eBay
Date: 2016-4-9 11:25
Tags: Retro-Computing, PDP-11

I've been keeping an eye on eBay and have collected a few more goodies: a DD11-D nine-slot expansion backplane, a fully
populated (128K x 18bit) MS11-L MOS memory board, and a couple of replacement BC08-R cables for connecting the console
to the CPU cards.  The MS11-L is a bit of a luxury; I am figuring it will be easier to deal with during bringup than
the core memory systems I have on hand.  It will also be nice to run with a full address space.

Below is an updated shot of the CPU chassis with the expansion backplane installed, populated with bus jumpers,
terminators, grant continuity cards, the MS11-L memory, a DL11 serial interface, and an MR11-DB boostrap ROM.  I've gone
ahead and slotted in the FPU in the first four slots, since the cleaned and refurbished CPU cabinet is probably the
safest place to store them now.  Console cables are also installed:

[<img class='image-process-thumb' src='/images/pdp11/boards-in-chassis-2.jpg'/>]({filename}/images/pdp11/boards-in-chassis-2.jpg)

The MR11 ROM is an interesting bit, and probably worth a comment.  This is a 32-word diode-matrix ROM card.  The bits
are physically laid out on the card (see pictures below); where there is a diode, there is a logical 1 bit and where
there is the absence of a diode there is a logical 0 bit.  Typically the matrix would be loaded with a bootstrap program,
to save the operator from having to toggle it in from the console on each boot.

The program could be modified by pysically adding or removing diodes in the matrix.  My card has had such a mod; there
is a handwritten note attached from some engineer describing this.  The mod customizes the bootstrap to always load
from an RK disk unit, to avoid having to toggle in the device address at boot.  I will probably revert this mod because
I like having things in fairly stock/usual condition.

[<img class='image-process-thumb' src='/images/pdp11/mr11-with-note.jpg'/>]({filename}/images/pdp11/mr11-with-note.jpg)
[<img class='image-process-thumb' src='/images/pdp11/mr11-bare.jpg'/>]({filename}/images/pdp11/mr11-bare.jpg)

For fun, here's the source listing of the stock bootstrap.  You can match the octal digits of the machine code against
the diodes in the ROM above (low word addresses at the top of the matrix, and least-significant-bits on the left).

    #!masm
                  ; REGISTER ASSIGNMENTS:
           000000 R0=%0
           000001 R1=%1
                  ;
    173100 013701         MOV     @#177570,R1     ;READ SWITCH REG FOR ....
           177570
    173104 000005 BEGIN:  RESET                   ;FORCE CLEAR IF RETRY
    173106 010100         MOV     R1,R0           ;....DEVICE WC ADDRESS
    173110 012710         MOV     #-256.,@R0      ;SET TO READ 256 WORDS
           177400
    173114 020027         CMP     R0,#177344      ;IS IT DECTAPE?
           177344
    173120 001007         BNE     START           ;NO. GO TO START
    173122 012740         MOV     #4002,-(R0)     ;YES. MOVE TAPE TO FRONT
           004002
    173126 005710         TST     @R0             ;WAIT FOR ERROR!
    173130 100376         BPL     .-2
    173132 005740         TST     -(R0)           ;IS IT ENDZONE?
    173134 100363         BPL     BEGIN           ;NO. TRY AGAIN
    173136 022020         CMP     (R0)+,(R0)+     ;ADJUST POINTER
    173140 012740 START:  MOV     #5,-(R0)        ;NOW START ACTUAL READ
           000005
    173144 105710         TSTB    @R0             ;WAIT FOR DONE
    173146 100376         BPL     .-2
    173150 005710         TST     @R0             ;ERROR ENCOUNTERED?
    173152 100754         BMI     BEGIN           ;IF SO START OVER
    173154 105010         CLRB    @R0             ;FOR DECTAPE,STOP TRANSPORT
    173156 000137         JMP     @#0             ;GO TO ROUTINE LOADED
           000000
           000001         .END

    BEGIN      000004R         R0    =%000000      R1    =2000001
    START      000040R         .     = 000062R

Hmmm, the Pygments syntax hightlighting package used by my blog generator doesn't seem to grok MACRO-11; may have to
do something about that...