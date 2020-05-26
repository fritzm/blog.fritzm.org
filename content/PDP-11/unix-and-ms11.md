Title: PDP-11/45: V6 Unix attempts & MS11-L repairs
Date: 2019-01-21
Tags: Retro-Computing, PDP-11

Following up on Noel's suggestion, I decided to give V6 Unix a try to see how it fared in comparison to the
problems seen with RSTS/E V06C.  I recently scored an additional RK05 pack from eBay, and decided to try and
use that so I could keep my current RSTS/E pack intact.

Inspected the pack, and it looked in good shape, clean, with no apparent crashes on the media.  Mounted it up
and was able to do only a partial recovery.  What I got looks like pretty generic RT-11/BASIC-11 stuff, so I'm
not too concerned about attempting a complete recovery.  Went ahead and reformatted the pack, after which I
could read/write the entire pack with no bad sectors.  So now I had two clean packs to work with.

Built a V6 Unix pack image from the Ken Wellsch tape under SIMH (using directions [here](
http://gunkies.org/wiki/Installing_Unix_v6_%28PDP-11%29_on_SIMH)).  Transferred it over using PDP11GUI, and it
did boot in single-user mode.  However, it immediately dumped core on the first `ls` command...  Tried a
multi-user Unix boot (what's to lose?) and this actually fared a bit better; able to `ls`, but still dumped
core when trying to run the C compiler or do anything else memory-intensive.

So, all of this taken together made me (and others collaborating on the troubleshooting on cctalk) think that
I might have a memory issue in the machine.  My machine has a 256KB MS11-L; I had previously spot-checked this
from the front panel by manipulating the KT11-C mapping registers and trying some writes/and reads within each
bank.  This was enough to identify and repair a few major problems (see [this]({filename}ms11-debug.md) older
blog post) and to get me this far.  But I had never thoroughly and substantially beat this card up after
things seemed to be working with RT-11.  There was still also nagging concern that none of the heavier-weight
KT11, MS11, KB11 "exerciser" MAINDEC diagnostics had yet been run to completion on the restored machine
either...

The recommended DEC diagnostic for the MS11-L is ZQMC, but it is complicated, takes a long time to download,
and the available sources don't exactly match the binary.  So, probably better to work up my own standalone
diagnostic to catch and fix obvious things...  Thus followed about a week of part-time work working up and
successively refining the following test code, and repairing identified problems (failed DRAMs) on the MS11-L
along the way.  This code maps and tests every memory location on the MS11-L, using KT11 memory management.
It relocates itself so it can test the lowest physical bank as well.  Tests include all-ones, all-zeros,
write address to location, and a "random" data test which just uses program code test sequence:

```text
        KIPDR0=172300
        KIPDR1=172302
        KIPDR2=172304
        KIPDR3=172306
        KIPDR4=172310
        KIPDR5=172312
        KIPDR6=172314
        KIPDR7=172316

        KIPAR0=172340
        KIPAR1=172342
        KIPAR2=172344
        KIPAR3=172346
        KIPAR4=172350
        KIPAR5=172352
        KIPAR6=172354
        KIPAR7=172356

        SR0=177572

        XCSR=177564
        XBUF=177566

        .ASECT
        .=1000
START:
        MOV     #700,SP         ;INIT STACK POINTER

        ;----- INSTALL TRAP CATCHERS

TRPS:   CLR     R0              ;CURRENT VECTOR
        MOV     #2,R1           ;VECTOR TARGET
        CLR     R2              ;HALT INSTR
        MOV     #100,R3         ;END VECTOR
1$:     MOV     R1,(R0)+        ;STORE TARGET AND ADVANCE
        MOV     R2,(R0)+        ;STORE HALT AND ADVANCE
        ADD     #4,R1           ;UPDATE TARGET
        SOB     R3,1$           ;LOOP OVER VECTORS

        ;----- INIT AND ENABLE MEMORY MAPPING

INITM:  MOV     #IPDRS,R0       ;SRC PDR INIT TABLE
        MOV     #KIPDR0,R1      ;DST KIPDR0
        MOV     #10,R2          ;DO EIGHT PDRS
        MOV     (R0)+,(R1)+     ;COPY AND ADVANCE
        SOB     R2,.-2          ;LOOP OVER PDRS
        MOV     #IPARS,R0       ;SRC PAR INIT TABLE
        MOV     #KIPAR0,R1      ;DST KIPAR0
        MOV     #10,R2          ;DO EIGHT PARS
        MOV     (R0)+,(R1)+     ;COPY AND ADVANCE
        SOB     R2,.-2          ;LOOP OVER PARS
        MOV     #1,@#SR0        ;ENABLE MEMORY MGMT

        ;----- TEST 32K MS11 BANKS AT PA 100000 THRU 700000,
        ;      RELOCATE, THEN TEST BANK AT PA 000000 

DOPASS: MOV     #1000,R0        ;PAR FOR PA 100000
        JSR     PC,DOBANK       ;TEST IT
        MOV     #2000,R0        ;PAR FOR PA 200000
        JSR     PC,DOBANK       ;TEST IT
        MOV     #3000,R0        ;PAR FOR PA 300000
        JSR     PC,DOBANK       ;TEST IT
        MOV     #4000,R0        ;PAR FOR PA 400000
        JSR     PC,DOBANK       ;TEST IT
        MOV     #5000,R0        ;PAR FOR PA 500000
        JSR     PC,DOBANK       ;TEST IT
        MOV     #6000,R0        ;PAR FOR PA 600000
        JSR     PC,DOBANK       ;TEST IT
        MOV     #7000,R0        ;PAR FOR PA 700000
        JSR     PC,DOBANK       ;TEST IT
        MOV     #1000,R5        ;RELOC TARGET PA:100000
        JSR     PC,RELOC        ;GO DO IT
        MOV     #0000,R0        ;PAR FOR PA 000000
        JSR     PC,DOBANK       ;TEST IT

        ;----- ALL DONE WITH PASS

        MOV     #0000,R5        ;RELOC TARGET PA:000000
        JSR     PC,RELOC        ;GO DO IT
        CLR     @#SR0           ;DISABLE MEMORY MGMT
        MOV     #PCOMPL,R5      ;GET PASS COMPLETE MSG
        JSR     PC,PRSTR        ;PRINT IT
        HALT                    ;ALL DONE

        ;----- MAP A SINGLE 32K BANK AT VA 20000

DOBANK: MOV     #KIPAR1,R1      ;WILL MAP USING KIPAR1 THRU KIPAR4
        MOV     #4,R3           ;FOUR KIPARS TO SET
        CMP     R0,#7000        ;UNLESS WE ARE IN PA 700000 BANK...      
        BNE     1$              ;IF NOT, SKIP AHEAD
        MOV     #3,R3           ;OTHERWISE, SCALE BACK TO 3 KIPARS
1$:     MOV     R0,(R1)+        ;SET A KIPAR AND ADVANCE
        ADD     #200,R0         ;INCREMENT VALUE FOR NEXT KIPAR
        SOB     R3,1$           ;LOOP OVER KIPARS

        ;----- CALCULATE END VA

        MOV     #120000,R1      ;MAPPED BANK END IS VA 120000
        CMP     @#KIPAR1,#7000  ;UNLESS WE ARE IN PA 700000 BANK...
        BNE     ZEROS           ;IF NOT, SKIP AHEAD
        MOV     #100000,R1      ;OTHERWISE, END IS VA 100000

        ;----- ZEROS TEST

ZEROS:  CLR     R2              ;EXPECTED VALUE IS 000000
        MOV     #20000,R0       ;START AT VA 20000
1$:     MOV     R2,(R0)+        ;CLEAR A WORD AND ADVANCE
        CMP     R0,R1           ;AT END?
        BNE     1$              ;IF NOT, LOOP
        MOV     #20000,R0       ;START AT VA 20000
2$:     TST     (R0)+           ;CHECK A WORD AND ADVANCE
        BEQ     3$              ;IF ZERO, SKIP AHEAD
        JSR     PC,PRERR        ;OTHERWISE, REPORT ERROR
3$:     CMP     R0,R1           ;AT END?
        BNE     2$              ;IF NOT, LOOP

        ;----- ONES TEST

ONES:   MOV     #177777,R2      ;EXPECTED VALUE US 177777       
        MOV     #20000,R0       ;START AT VA 20000
1$:     MOV     R2,(R0)+        ;WRITE A WORD AND ADVANCE
        CMP     R0,R1           ;AT END?
        BNE     1$              ;IF NOT, LOOP
        MOV     #20000,R0       ;START AT VA 20000
2$:     CMP     (R0)+,R2        ;CHECK A WORD AND ADVANCE
        BEQ     3$              ;IF EXPECTED VALUE, SKIP AHEAD
        JSR     PC,PRERR        ;OTHERWISE, REPORT ERROR
3$:     CMP     R0,R1           ;AT END?
        BNE     2$              ;IF NOT, LOOP

        ;----- WRITE LOCATION WITH ITS VA TEST

ADDRS:  MOV     #20000,R0       ;START AT VA 20000
1$:     MOV     R0,R2           ;USE VA AS TEST VALUE
        MOV     R2,(R0)+        ;WRITE A WORD AND ADVANCE
        CMP     R0,R1           ;AT END?
        BNE     1$              ;IF NOT, LOOP
        MOV     #20000,R0       ;START AT VA 20000
2$:     MOV     R0,R2           ;USE VA AS TEST VALUE
        CMP     (R0)+,R2        ;CHECK A WORD AND ADVANCE
        BEQ     3$              ;IF EXPECTED VALUE, SKIP AHEAD
        JSR     PC,PRERR        ;REPORT ERROR
3$:     CMP     R0,R1           ;AT END?
        BNE     2$

        ;----- "RANDOM" DATA TEST (PROGRAM AS TEST DATA)

RNDM:   MOV     #START,R2       ;SRC: START OF PROGRAM
        MOV     #20000,R0       ;DST: VA 20000
1$:     MOV     (R2)+,(R0)+     ;WRITE A WORD AND ADVANCE
        CMP     R0,R1           ;AT END?
        BEQ     2$              ;IF SO, SKIP AHEAD
        CMP     R2,#END         ;TIME TO RESET SRC?
        BLO     1$              ;IF NOT, GO DO ANOTHER
        MOV     #START,R2       ;OTHERWISE RESET SRC
        BR      1$              ;AND GO DO ANOTHER
2$:     MOV     #START,R2       ;SRC1: START OF PROGRAM
        MOV     #20000,R0       ;SRC2: VA 20000
3$:     CMP     (R2)+,(R0)+     ;COMPARE ONE WORD AND ADVANCE
        BEQ     4$              ;IF SAME, SKIP AHEAD
        MOV     R2,-(SP)        ;SAVE SRC1
        MOV     -2(R2),R2       ;FETCH EXPECTED VALUE
        JSR     PC,PRERR        ;REPORT ERROR
        MOV     (SP)+,R2        ;RESTORE SRC1
4$:     CMP     R0,R1           ;AT END?
        BEQ     5$              ;IF SO, SKIP AHEAD
        CMP     R2,#END         ;TIME TO RESET SRC1?
        BLO     3$              ;IF NOT, GO DO ANOTHER
        MOV     #START,R2       ;OTHERWISE RESET SRC1
        BR      3$              ;AND GO DO ANOTHER

5$:     RTS     PC              ;TESTS DONE, RETURN TO CALLER

        ;----- RELOCATE

RELOC:  MOV     R5,@#KIPAR1     ;MAP VA:020000 -> PA:(R5<<6) 
        CLR     R0              ;SRC VA:000000 
        MOV     #20000,R1       ;DST VA:020000
        MOV     R1,R2           ;FULL PAGE (4K WORDS)
        MOV     (R0)+,(R1)+     ;COPY A WORD
        SOB     R2,.-2          ;LOOP UNTIL DONE
        MOV     R5,@#KIPAR0     ;MAP VA:000000 -> PA:(R5<<6)
        MOV     #RELSTR,R5      ;GET RELOCATED STRING
        JSR     PC,PRSTR        ;PRINT IT
        MOV     @#KIPAR1,R5     ;GET RELOCATION TARGET
        ASHC    #6,R4           ;SHIFT OVER FOR PA IN R4:R5
        JSR     PC,PRW18        ;PRINT IT
        MOV     #CRLF,R5        ;GET CRLF
        JSR     PC,PRSTR        ;PRINT IT
        RTS     PC              ;RETURN TO CALLER

        ;----- REPORT AN ERROR

PRERR:  MOV     @#KIPAR1,R5     ;GET KIPAR FOR MAPPED BASE      
        ASHC    #6,R4           ;SHIFT OVER FOR PA IN R4:R5
        ADD     R0,R5           ;ADD IN ERROR VA
        ADC     R4              ;CARRY IF NECESSSARY
        SUB     #20002,R5       ;SUB VA OFFSET AND BACK UP ONE
        SBC     R4              ;BORROW IF NECESSARY
        JSR     PC,PRW18        ;PRINT PHYSICAL ADDRESS
        MOV     #DELIM1,R5      ;GET DELIMITER
        JSR     PC,PRSTR        ;PRINT IT
        MOV     R2,R5           ;GET EXPECTED VALUE
        JSR     PC,PRW16        ;PRINT IT
        MOV     #DELIM2,R5      ;GET DELIMETER
        JSR     PC,PRSTR        ;PRINT IT
        MOV     R0,R4           ;GET ADDRESS AFTER ERROR
        MOV     -(R4),R5        ;BACK UP AND GET ERROR VALUE
        JSR     PC,PRW16        ;PRINT IT
        MOV     #CRLF,R5        ;GET CRLF
        JSR     PC,PRSTR        ;PRINT IT
        RTS     PC              ;RETURN TO CALLER

        ;----- PRINT SIX DIGIT OCTAL NUMBER

PRW16:  CLR     R4              ;CLEAR UPPER WORD
PRW18:  MOV     #6,R3           ;SIX DIGITS TO PRINT
        ASHC    #1,R4           ;SHIFT IN MSB OF LOW WORD
1$:     ADD     #60,R4          ;MAKE INTO ASCII DIGIT
        MOV     R4,@#XBUF       ;PRINT IT
        TSTB    @#XCSR          ;CHECK IF XMIT DONE
        BPL     .-4             ;LOOP UNTIL SO
        CLR     R4              ;RESET OUTPUT CHAR
        ASHC    #3,R4           ;SHIFT IN NEXT THREE BITS
        SOB     R3,1$           ;LOOP DIGITS
        RTS     PC              ;RETURN TO CALLER

        ;----- PRINT NULL-TERMINATED STRING

PRSTR:  MOVB    (R5)+,@#XBUF    ;PRINT ONE CHAR AND ADVANCE
        TSTB    @#XCSR          ;CHECK IF XMIT DONE
        BPL     .-4             ;LOOP UNTIL SO
        TSTB    @R5             ;CHECK IF END OF STRING
        BNE     PRSTR           ;LOOP IF NOT
        RTS     PC              ;ELSE RETURN TO CALLER

IPDRS:  .WORD   077406,077406,077406,077406
        .WORD   077406,000000,000000,077406

IPARS:  .WORD   000000,000200,000400,000600
        .WORD   001000,000000,000000,007600

DELIM1: .ASCIZ  /: /            ;POST-ADDRESS DELIMETER
DELIM2: .ASCIZ  / /             ;POST-CRC DELIMETER
CRLF:   .ASCIZ  <15><12>        ;LINE DELIMETER
RELSTR: .ASCIZ  /RELOCATED TO PA:/
PCOMPL: .ASCIZ  /PASS COMPLETED/<15><12><15><12>

END:    .END    START
```

The code above is the end result of quite a bit of successive refinement.  Things learned along the way:

* At first the tests consisted only of writing and checking all-ones and all-zeros to each location.  This did
uncover one more bank with a stuck bit at only some addresses, that my previous spot-checking had missed.
Lesson: you really gotta check every byte.  Removed, socketed, and replaced the implicated DRAM, and my tests
passed.

* Maybe I fixed it, so after this I invested the download time to try the the DEC ZQMC diagnostic again.  It
ran better than I had seen before, proceeding through a few subtests, but soon started flagging a lot of
errors that my diagnostic missed. Hmmm.  Inspecting the DEC code, it seemed to be writing and checking random
data at the time, not just all ones an zeros.  Went ahead and implemented "random" data test in my diagnostic,
and it immediately started implicating the same chips.  Lesson: all-ones, all-zeros isn't good enough...

* While I was at it, I implemented an additional "write/check each byte with its virtual address" test.
Interestingly, this found *most*, but not *all* of the same chips as the random data test.  Lesson: all-ones,
all-zeros, and address in each word isn't good enough, either; you really do gotta have that "random" data
test, too. At this point, went ahead and replaced three more implicated DRAMS, and my tests once again passed
clean...

* In the meantime, I did some more code reading on the DEC diagnostic, and found that various features could
be enabled/disabled via the front panel switches.  With some care, the diagnostic might also be restartable
without having to wait for an entire re-download, if stopped carefully and in the right place.  So I spent the
time to re-download, and found with experimentation that the DEC diagnostic would now pass all banks of memory
cleanly, as long as *parity checking was disabled*.  Hmm...

* Moving back to my diagnostic, I noticed that while it ran clean now on all banks, on a fresh power-up it
would usually light the parity-error LED on the MS11-L on its first pass.  Subsequent passes, after every
location had been written at least once, were fine.  Since the MS11-L doesn't have any fancy power-up init
logic, it would make sense to see this if the program read locations without writing them first, but I didn't
think my code did that.  Enabling parity traps let me catch it in the act, and it was happening on a `CLR`
instruction that I was using to init memory!  Lesson: on an 11/45, `CLR` is implemented like other single-
operand, modifying instructions, and actually does a DATIP bus cycle from the destination before writing back
a zero!  So use `MOV` instead of `CLR` to init memory if you are worried about tripping parity errors...
Cleaned this up in my code, and my diagnostic now runs clean on my machine in all circumstances without ever
tripping a parity error.

So, a lot of issues found and repaired on the MS11-L.  Maybe still some issues with parity error handling,
which seems to be halting the machine instead of taking a trap.  Figured it might be worth a shot to try the
operating systems again, so mounted the respective disks and tried both, and... exact same failures in both
cases!  Womp, womp...

Well, might as well continue to look into the parity error handling, since some things still seem fishy there.
The DEC documentation is a bit murky here; various versions of the KB11-A maintenance manual and 11/45
processor handbook say different and somewhat contradictory things; some info in earlier editions is also
removed from later ones.  The available engineering drawings for the relevant parts of the KB11-A CPU look to
have some significant differences from the actual boards I have on hand, and there are more than a few ECO's
for these boards listed as relating specifically to parity handling, but for which no other information is
available.  And Noel has uncovered evidence that even the Unibus signaling related to parity may have been
changed by DEC around the times of the early 11/45. Could be interesting...
