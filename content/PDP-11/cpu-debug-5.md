Title: PDP-11/45: CPU debug V -- chasing lights!
Date: 2016-6-19
Tags: Retro-Computing, PDP-11

Tracked down the source of the inverted result after register-to-register move problem on GRA: outputs of the
subsidiary ALU control ROM E74 on pins 6 and 7 are floating.  Will need some closer inspection to determine if this
is a board fault or a chip fault.  In the meantime, I have a spare GRA which I had been reluctant to try because it
has a "bad" sticker on it...  Decided to give it a try anyway, and it seems to be working much better than the one I
have been debugging.

Now have enough of the CPU debugged to toggle in and run a simple light chaser program:

    #!masm
    000000  013700  177570  L0:     MOV     @#177570, R0    ;LOAD COUNT FROM SWITCH REGISTER
    000004  005300          L1:     DEC     R0              ;COUNT DOWN
    000006  001376                  BNE     L1              ;LOOP UNTIL ZERO
    000010  006301                  ASL     R1              ;SHIFT DISPLAY VALUE
    000012  001002                  BNE     L2              ;SKIP AHEAD IF NOT SHIFTED OUT
    000014  012701  000001          MOV     #1,R1           ;ELSE RELOAD
    000020  010137  177570  L2:     MOV     R1,@#177570     ;STORE TO DISPLAY REGISTER
    000024  000765                  BR      L0              ;REPEAT FROM THE TOP

{% youtube ZhuzC9v3q-k %}