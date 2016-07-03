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

{% youtube ZhuzC9v3q-k?rel=0 %}

Some notes on the program and video above since I've received some questions:

- The listing here is shown assembled at location 000000, but the program is relocatable and can be toggled in at any
convenient address (000000, on top of the trap vectors, probably isn't the best choice!)

- Data display should be on "DISPLAY REGISTER" to see the chase.

- The front panel toggles are loaded into a counter to control the speed of the chase.  Without some of the most
significant bits set the chase may go too fast to see, especially on older 11's with incandescent indicators.  All
toggles off is a special case: this will be the slowest chase, since as written the counter wraps around when
decremented before being checked for zero.  The video has toggles 15 and 14 up.

- If you look at the address lights in the video, you can see that I ran this program from address 100000.  This was
because at the time I had a fault in the first 16KW of memory on my MS11-L so I couldn't execute any code at lower
addresses.
