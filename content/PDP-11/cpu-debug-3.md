Title: PDP-11/45: KM11 replica and CPU debug III
Date: 2016-6-11
Tags: Retro-Computing, PDP-11

Received the boards and components for the KM11 replica; stuffed and soldered, and it appears to work!  There are
some photos below.  I can easily single-step microcode, clock states, and bus cycles now, which should really help
with the CPU debug.

Swapped DAP for a spare, and this has fixed the stuck PC issue.  Memory issues remain, but by choosing a working
memory range, I can start to toggle in and attempt to execute very simple programs.

The simplest possible program, unconditional branch to self, seems to execute correctly:

    #!masm
    001000 000777         BR      .-2

A register to register data move test does not however:

    #!masm
    001000 010203         MOV     R2,R3
    001002 000776         BR      .-4

Control flow is as expected, but the value that ends up in R3 seems to be negated.  Still, pretty good progress!
Now that I can step machine states, the next step will be to put the DAP out on an extender card and start tracking
down signals with a logic probe.

The HP1662A logic analyzer from eBay has also arrived; should come in handy in investigating the memory issue.

[<img class='image-process-thumb' src='/images/pdp11/km11.jpg'/>]({filename}/images/pdp11/km11.jpg)
[<img class='image-process-thumb' src='/images/pdp11/km11-action.jpg'/>]({filename}/images/pdp11/km11-action.jpg)