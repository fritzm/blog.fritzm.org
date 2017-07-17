Title: PDP-11/45: M9301 Troubles
Date: 2017-7-4
Tags: Retro-Computing, PDP-11

After a lot of recent progress with the RK11, suffered a setback: after trying once again to image
a fresh RT11 pack, the machine began to behave erratically at boot.  Sometimes the boot monitor would run
fine, sometimes it would run for a while and then take a machine exception or vector off to bad address,
and sometimes the machine would fail to boot at all, immediately taking exceptions of various sorts. Getting
so close, but then lost a lot of ground; I guess that's sort of the way it is going to be with a machine
that is this old...

So, back to the top without a working boot monitor.  Microcode sequencing and seemed to be working fine --
exam/deposit/step working reliably from the front panel.  Checked execution of the first few instructions
of the boot ROM in detail, a branch and some single operand instructions, and they seemed to execute
correctly.

Assuming some sort of new failure in the CPU, I prepared to instrument the Unibus with the HP
logic analyzer; it seemed that way I could trigger on machine exceptions then look back over the captured
address traces for a pattern.  To make sense of those, I'd need a listing of the boot ROM in hand.  Noel
Chiappa has a dump for this and a partial disassembly on his site [here](http://ana-3.lcs.mit.edu/~jnc/tech/pdp11/ROMs/M9301-YB.mac),
but is it the same as mine?  Better check...

Started to run through Noel's listing and compare to the ROM contents on my machine via front panel exam.
Sure enough, there seemed to be some words different in a few places.  Maybe the CPU is fine, and the ROM
card is failing?  Swapped out the M9301 for a simpler M792 diode matrix boot ROM, and sure enough -- was
able to boot straight away off my RKDP pack, and from there reliably beat up the CPU with diagnostics.  So,
great news: just a failing M9301!

Alright, so now I want to capture a dump of the M9301 so I can systematically compare with Noel's listing
to see if there's a pattern in failed/flaky bits to help guide my repair.  For this I need a memory dump
utility that I can toggle in from the front panel.  Came up with this:

    #!masm
    001000  012705  START:  MOV     #177564,R5      ;CONSOLE XCSR
            177564
    001004  012700  L0:     MOV     #177570,R0      ;SWITCH REGISTER
            177570
    001010  000000          HALT
    001012  011004          MOV     @R0,R4          ;READ ADDR FROM SWITCHES
    001014  000000          HALT
    001016  011003          MOV     @R0,R3          ;READ COUNT FROM SWITCHES
    001020  012401  L1:     MOV     (R4)+,R1        ;GET NEXT WORD TO DUMP
    001022  012702          MOV     #6,R2           ;SIX DIGITS TO PRINT
            000006
    001026  005000          CLR     R0              ;R0 GETS MSB R1
    001030  073027          ASHC    #1,R0
            000001
    001034  062700  L2:     ADD     #60,R0          ;MAKE INTO ASCII DIGIT
            000060
    001040  010065          MOV     R0,2(R5)        ;OUTPUT
            000002
    001044  105715          TSTB    (R5)
    001046  100376          BPL     .-2
    001050  005000          CLR     R0              ;R0 GETS 3 MSB R1
    001052  073027          ASHC    #3,R0
            000003
    001056  077212          SOB     R2,L2           ;LOOP DIGITS
    001060  012765          MOV     #15,2(R5)       ;OUTPUT '\R'
            000015
            000002
    001066  105715          TSTB    (R5)
    001070  100376          BPL     .-2
    001072  012765          MOV     #12,2(R5)       ;OUTPUT '\N'
            000012
            000002
    001100  105715          TSTB    (R5)
    001102  100376          BPL     .-2
    001104  077333          SOB     R3,L1           ;LOOP WORDS
    001106  000736          BR      L0              ;START OVER

Executed this a few times and got slightly different results, then things settled into a pattern where the
lowest nybble of every word was consistently zeroed but everything else was fine.  Smoking gun pointing to
a single PROM on the M9301.  Pulled and reseated that chip, and did the same for the other three while I
was at it, and ... everything 100% after that.  Wow, really should have just tried that first...

Well, at least I'm up and running again!  The memory dump program might come in useful again at some other
time, and as a byproduct after I fixed my M9301 I got 100% agreement with Noel's listing.  So I think that
listing can be considered authoritative now; good enough to generate replacement PROMs should anybody
ever need to do so.

[<img src='/images/pdp11/M9301_thumbnail_tall.jpg'/>]({filename}/images/pdp11/M9301.jpg)
[<img src='/images/pdp11/M792-YB_thumbnail_tall.jpg'/>]({filename}/images/pdp11/M792-YB.jpg)
{% youtube E7MAFjZVZ2Y?rel=0 328 200 %}
