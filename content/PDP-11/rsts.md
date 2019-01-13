Title: PDP-11/45: RSTS/E V06C attempts
Date: 2019-01-7
Tags: Retro-Computing, PDP-11

Okay, back in action after replacing the failed nand at B26 in the RK11-C.  MAINDEC ZRKK now passes reliably.
Wish I'd been able to get to the bottom of this at the show, but it was really hard to effectively debug on
the floor there while the show was in progress -- you naturally want to stop and chat with everybody who drops
by to take a look, so its hard to get into a good technical flow.

Since one of the RK11-C diagnostics I needed to use writes a pack destructively, I had to sacrifice my working
RT-11 pack along the way.  Rather than go back to the same old RT-11 image, I figured maybe time to try
something different?  RSTS/E would probably be more fun with multiple terminals and the DZ11 that I have
anyway, and I've never actually played around with RSTS.  So decided to give that a go...

Did some poking around looking at various available versions, and V06C seemed like a pretty good starting
point: it's new enough to explicitly support all of my hardware (including the DZ11 and excepting the VT100),
but old enough to still have relatively modest storage requirements so I can hope to run it with the single
RK05 that I currently have working.  There is also complete distribution tape available at rsts.org, and a
fairly complete set of documentation at bitsavers.

Spent a bit of time reading the sysgen manual, and managed to sysgen under simh and generate a bootable
RK05 image for my hardware.  I then transferred this image to my single working pack using PDP11GUI; this is
frustratingly slow (~3 hours to write a 2.5mb pack)!!  I had forgotten how bad this is.  I'm not quite sure
why it is as slow as it is; it shouldn't take much more than 45 minutes to push that much data through a DL11
at 9600 baud, even without compression, and the PDP-11 disk subsystem can easily keep up with that.  I'm not
sure if PDP11GUI is spending a lot of time turning around the serial line, or has a bunch of per-character
overhead, or...?  In any case, I'm motivated to do something about it; more on this some other time soon.

So, unfortunately, the RSTS image which works under simh fails to completely boot on the real hardware. It
runs through the initial "Option:" menu without trouble, and upon start the RSTS light chaser runs in the
data lights on the front panel.  Characters are echoed on the console terminal, but it never reaches code to
print the banner or prompt for the initial control file.  The system appears to be in a loop reading the same
section of disk repetitively, and the display register shows a continuously increasing count.

Got a lot of help from folks over on the cctalk mailing list on this one, since I'm a newbie to RSTS.  Paul K.
provided some useful tips:

* RSTS displays an error count in the display register, so that's why I see an increasing count there.

* The "fancy" idle pattern that includes both the address and data lights apparently shows up in a later
release of RSTS and requires a particular sysgen option, so its not surprising that I only see the pattern
in the data lights on my machine.

* The ODT debugger may be loaded with RSTS for startup debugging by configuring it using an undocumented
option in the change memory layout section of the "DEFAULT" command at the boot prompt.  Enter "ODT" there,
and provide a space for it in the memory map.  After that, at ^P at the console will take you to the ODT
prompt. 
```
   Memory allocation table:

     0K: 00000000 - 00123777 (  21K) : EXEC
    21K: 00124000 - 00213777 (  14K) : RTS (BASIC)
    35K: 00214000 - 00227777 (   3K) : ODT
    38K: 00230000 - 00757777 (  86K) : USER
   124K: 00760000 - End              : NXM
```

* A handy way to query the RSTS symbol table is to use the "PATCH" command at the boot prompt (one can also
look through the .MAP files generated during sysgen):
```text
   Option: PA
   File to patch? 
   Module name? 
   Base address? ERL
   Offset address? 
    Base   Offset  Old     New?
   041314  000000  005267  ? ^Z
   Offset address? ^Z
   Base address? 
```

* Paul also provided this procedure for triggering a crash dump from an ODT breakpoint under RSTS:
```text
1. Make sure crash dump is enabled (in the "default" option).  Start the system.  Let it run for at least one minute.  (I'm not entirely sure about older versions, but I think that a crash within one minute of startup is handled differently and doesn't do all the usual dump and restart machinery.)

2. Set the data switches all UP.  (In SIMH, enter "D SR 177777".)

3. Set a breakpoint.

4. When you hit the breakpoint, change the PC to 52, like this:

    0B:055244 
    _$7/055244 52 
    _P 

  (you enter only "$7/" and "52<return>" and "P", the rest is output from ODT.)

  The system will write the crashdump and then automatically restart.

5. You should now have the crash dump in [0,1]CRASH.SYS
```

Further experiments coordinated by Paul then led to the conclusion that an error like this could reasonably be
expected to be triggered by a corrupted INIT.BAC or BASIC.RTS file.  This led me to wish to verify that the
disk pack contents really matched the image file I was running successfully under simh.  Some standalone code
to dump a CRC of every sector on the pack seemed like it would be useful in this regard, so I coded up the
following:
```masm
        RKDS=177400
        RKER=177402
        RKCS=177404
        RKWC=177406
        RKBA=177410
        RKDA=177412

        XCSR=177564
        XBUF=177566

        .ASECT
        .=1000
START:  
        MOV     #700,SP         ;INIT STACK POINTER

        ;----- INIT CRC LOOKUP TABLE

        MOV     #10041,R0       ;CRC POLYNOMIAL 
        MOV     #CRCTBL,R1      ;LOOKUP TABLE TO FILL
        ADD     #1000,R1        ;START FILLING FROM END (+512 WORDS)
        MOV     #377,R2         ;COUNT DOWN FROM INDEX 511      
L0:     MOV     R2,R4           ;GET COPY OF INDEX
        SWAB    R4              ;MOVE TO UPPER BYTE
        MOV     #10,R3          ;LOOP OVER EIGHT BITS OF INDEX  
L1:     ASL     R4              ;SHIFT, MSB TO CARRY FLAG
        BCC     L2              ;IF MSB NOT SET SKIP AHEAD
        XOR     R0,R4           ;ELSE XOR IN POLYNOMIAL
L2:     SOB     R3,L1           ;LOOP OVER BITS
        MOV     R4,-(R1)        ;SAVE RESULT IN LOOKUP TABLE
        DEC     R2              ;COUNT DOWN
        BPL     L0              ;LOOP OVER TABLE ENTRIES

        CLR     R5              ;INIT SECTOR COUNTER

        ;----- PRINT START OF LINE

L3:     MOV     R5,R0           ;GET SECTOR COUNTER
        JSR     PC,PRNW         ;PRINT IT
        MOV     #DELIM1,R0      ;GET POST-SECTOR DELIMETER
        JSR     PC,PRNSTR       ;PRINT IT

        ;----- READ 8 SECTORS FROM DISK

L4:     MOV     R5,@#RKDA       ;SET START SECTOR
        MOV     #DBUF,@#RKBA    ;SET TARGET ADDRESS
        MOV     #-4000,@#RKWC   ;READ 8 SECTORS (2K WORDS)
        MOV     #5,@#RKCS       ;READ + GO
        TSTB    @#RKCS          ;CHECK RKCS RDY BIT
        BPL     .-4             ;LOOP IF BUSY

        ;----- HANDLE ERROR IF ANY

        BIT     #100000,@#RKCS  ;CHECK FOR ERROR
        BEQ     L5              ;SKIP AHEAD IF NOT
        MOV     #ERRSTR,R0      ;POINT TO ERROR INDICATOR
        JSR     PC,PRNSTR       ;PRINT IT
        MOV     @#RKER,R0       ;GET ERROR REG
        JSR     PC,PRNW         ;PRINT IT
        BR      L8              ;MOVE ON TO NEXT 8 SECTORS

L5:     MOV     #DBUF,R4        ;POINT TO START OF DATA JUST READ

        ;----- RUN CRC FOR ONE SECTOR.  FOR EACH INPUT BYTE CH:
        ;       CRC = CRCTBL[((CRC >> 8) ^ CH) & 255] ^ (CRC << 8)

L6:     CLR     R0              ;RESET CRC
        MOV     #1000,R1        ;LOOP OVER ONE SECTOR (256 WORDS)
L7:     MOV     R0,R2           ;GET COPY OF CRC
        SWAB    R2              ;MOVE HIGH BYTE DOWN
        MOVB    (R4)+,R3        ;GET NEXT INPUT BYTE TO PROCESS
        XOR     R3,R2           ;XOR ONTO MUNGED CRC
        BIC     #177400,R2      ;MASK OFF HIGH BYTE
        ASL     R2              ;TIMES TWO INDEX INTO LOOKUP TABLE
        MOV     CRCTBL(R2),R3   ;LOOKUP VALUE
        SWAB    R0              ;MOVE LOW BYTE OF CRC UP
        CLRB    R0              ;MASK OFF THE BOTTOM
        XOR     R3,R0           ;XOR IN THE LOOKED UP VALUE
        SOB     R1,L7           ;LOOP OVER BYTES

        ;----- PRINT CRC, DELIMIT AND LOOP

        JSR     PC,PRNW         ;PRINT CRC, ALREADY IN R0
        CMP     R4,#DBUF+10000  ;END OF DISK BUFFER?
        BEQ     L8              ;IF SO, EXIT LOOP
        MOV     #DELIM2,R0      ;ELSE POINT TO POST-CRC DELIMETER
        JSR     PC,PRNSTR       ;PRINT IT
        BR      L6              ;GO DO ANOTHER SECTOR

        ;----- DELIMIT END OF LINE, LOOP 

L8:     MOV     #CRLF,R0        ;POINT TO LINE DELIMETER
        JSR     PC,PRNSTR       ;PRINT IT
        ADD     #10,R5          ;MOVE AHEAD 8 SECTORS
        CMP     R5,#11410       ;AT END OF PACK?
        BLT     L3              ;IF NOT, GO DO THE NEXT 8

        HALT                    ;ALL DONE!
        
        ;----- PRINT A WORD IN OCTAL

PRNW:   MOV     #6,R2           ;SIX DIGITS TO PRINT
        MOV     R0,R1           ;MOVE OUTPUT WORD OVER TO R1
        CLR     R0              ;RESET OUTPUT CHAR
        ASHC    #1,R0           ;AND SHIFT IN MSB TO START
L9:     ADD     #60,R0          ;MAKE INTO ASCII DIGIT
        MOV     R0,@#XBUF       ;PRINT IT
        TSTB    @#XCSR          ;CHECK IF XMIT DONE
        BPL     .-4             ;LOOP UNTIL SO
        CLR     R0              ;RESET OUTPUT CHAR
        ASHC    #3,R0           ;SHIFT IN NEXT THREE BITS
        SOB     R2,L9           ;LOOP DIGITS
        RTS     PC              ;RETURN TO CALLER

        ;----- PRINT A NULL-TERMINATED STRING

PRNSTR: MOVB    (R0)+,@#XBUF    ;PRINT ONE CHAR AND ADVANCE
        TSTB    @#XCSR          ;CHECK IF XMIT DONE
        BPL     .-4             ;LOOP UNTIL SO
        TSTB    @R0             ;CHECK IF END OF STRING
        BNE     PRNSTR          ;LOOP IF NOT
        RTS     PC              ;ELSE RETURN TO CALLER

DELIM1: .ASCIZ  /: /            ;POST-SECTOR DELIMETER
DELIM2: .ASCIZ  / /             ;POST-CRC DELIMETER
CRLF:   .ASCIZ  <15><12>        ;LINE DELIMETER
ERRSTR: .ASCIZ  /ERROR: /       ;ERROR INDICATOR

CRCTBL: .BLKW   400             ;CRC LOOKUP TABLE
DBUF:   .BLKW   4000            ;DISK DATA BUFFER

        .END    START
```

Running this indicated the RSTS pack was in good shape, and not corrupt.  So, maybe I have had a lurking
hardware bug in my memory system (a 256KB MS11-L), which never tripped up RT-11 and so has to date
gone undiagnosed?

At this point, Noel suggested on cctalk that I give Release 6 Unix a try as well, and see if it suffers
similarly.  Worth a shot!  Out of time for now, and back to the day gig tomorrow after holiday break.
Happy new year, all!
