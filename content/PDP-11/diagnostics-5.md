Title: PDP-11/45: Diagnostics V - D0AA0-D0MA0, CKBOA0
Date: 2016-7-31
Tags: Retro-Computing, PDP-11

The day gig has been keeping me pretty busy for the last couple of weeks, but had some time to work on the PDP-11
again this weekend, so here's an update.

Looking a little deeper at the diagnostics database over on retrocmp.com, I realized that I had skipped the entire
set of generic 11-family "D0" tests.  Downloaded and ran these via PDP11GUI and they all passed.  BEL character
patch locations, as described previously, are summarized here for future reference:

<style>
.diaglist { display: inline; border-collapse: collapse; margin-right: 1em; }
.diaglist caption { font-weight: bold; }
.diaglist tr:nth-child(even) { background-color: #f2f2f2; }
.diaglist th, .diaglist td { padding: 5px; }
.diaglist td { border: 1px solid lightgray; font-family: Menlo,Consolas,monospace; }
</style>

<table class="diaglist">
<thead>
<tr><th>Diagnostic</th><th>BEL</th><th>Description</th><th>Status</th></tr>
</thead>
<tbody>
<tr><td>D0AA0.BIN</td><td>014212</td><td>Branch</td><td>pass</td></tr>
<tr><td>D0BA0.BIN</td><td>004336</td><td>Con branch</td><td>pass</td></tr>
<tr><td>D0CA0.BIN</td><td>005526</td><td>Unary</td><td>pass</td></tr>
<tr><td>D0DA0.BIN</td><td>016370</td><td>Binary</td><td>pass</td></tr>
<tr><td>D0EA0.BIN</td><td>010562</td><td>Rotate/shift</td><td>pass</td></tr>
<tr><td>D0FA0.BIN</td><td>017224</td><td>CMP equality</td><td>pass</td></tr>
<tr><td>D0GA0.BIN</td><td>013650</td><td>CMP non-equality</td><td>pass</td></tr>
<tr><td>D0HA0.BIN</td><td>013434</td><td>Move</td><td>pass</td></tr>
<tr><td>D0IA0.BIN</td><td>014126</td><td>Bit set clear test</td><td>pass</td></tr>
<tr><td>D0JA0.BIN</td><td>007472</td><td>Add</td><td>pass</td></tr>
<tr><td>D0KA0.BIN</td><td>007124</td><td>Subtract</td><td>pass</td></tr>
<tr><td>D0LA0.BIN</td><td>015722</td><td>Jump</td><td>pass</td></tr>
<tr><td>D0MA0.BIN</td><td>003250</td><td>JSR RTS RTI</td><td>pass</td></tr>
</tbody>
</table>

Of the "CKB" series of tests, CKBOA0 (11/45 states) is the only one I that is not yet passing.  Looking into
this a little further, the first failing sub-test is T65:

    #!masm
    010540 010701                  T65:    SCOPE                    ;
    010542 012737  030000  177776          MOV     #PUM,@#PSW       ;KERNEL MODE, PREV USER MODE
    010550 012706  000500                  MOV     #KPTR,KSP        ;SET KERNEL STACK POINTER
    010554 012716  000700                  MOV     #UPTR,(KSP)
    010560 106606                          MTPD    USP              ;SET USER STATCK POINTER
    010562 005067  170110                  CLR     UPTR-2
    010566 052737  140000  177776          BIS     #UM,@#PSW        ;USER MODE, PREV USER MODE
    010574 106506                          MFPD    USP              ;PUSH USER STACK POINTER ONTO USER STACK
    010576 042737  140000  177776          BIC     #UM,@#PSW        ;KERNEL MODE, PREV USER MODE
    010604 106506                          MFPD    USP              ;PUSH USER STACK POINTER ONTO KERNEL STACK
    010606 022716  000676                  CMP     #UPTR-2,(KSP)    ;CHECK THAT USER STACK POINTER WAS
    010612 001401                          BEQ     .+4              ;PUSHED PROPERLY (ONCE)
    010614 000000                          HLT                      ;ERROR!
    010616 022767  000700  170052          CMP     #UPTR,UPTR-2     ;CHECK THAT USER STACK POINTER IS ON THE
    010624 001401                          BEQ     .+4              ;USERS STACK
    010626 000000                          HLT                      ;ERROR!

This runs amok on the MFPD instruction at 010574, which should push the user stack pointer onto the user stack.
Instead, the user stack pointer is pushed to memory at an incorrect address; 010676 instead of 000676.  This actually
overwrites subsequent test code. Since the value pushed is 000700, a hard-coded loop is created that prevents the
test from completing the pass even if resumed from halt.

The relevant states in the microcode flow here are MFP.80, MFP.90, and MFP.10:

<img src='/images/pdp11/mfpd-microcode.png'/>

Stopping at T2 of MFP.10 using the KM11, I can see that the correct value 000700 was fetched to DR (as displayed by
the console address lights), but the incorrect value of 010676 is appearing at the output of the ALU/shifter (as
displayed by the console data lights when set to data paths).  Throwing the DAP card out on extenders and taking
a look around with a logic probe revealed that the errant bit 12 is sourcing from the ALU.  At each slice of the ALU,
function selectors S3-S0 are correct, CIN is correct, and overall B-mux constant value "2" is correct.  The errant bit
is arriving to the ALU from the A-mux...

Chasing this upstream, A-mux selectors S1,S0 are correct, but the bad bit arrives to the mux input on GRAH SR12.  Hmmm,
maybe this is one of the things the "BAD" sticker on the GRA is referring to...  Next step is to throw the GRA on
the extender, and chase the signal back towards SR and the register files.  However, here I hit a snag: the M9301
monitor does not run correctly when the GRA is on the extender!  That's pretty weird.  Some investigation with the
KM11 and some hand-toggled instructions revealed that at least the Z status bit is not set correctly/reliably when
the card is on the extender.  Some of the Z bit logic lives on the GRA also, so I can take a look at that, but I am
now out of time for this weekend.  Next time!

A few other miscellaneous notes in wrap-up:

* I have been running with the spare GRA marked "BAD" because the first GRA I was using turned out to have a failed ALU
subsidiary PROM.  In the meantime I tracked down a PROM programmer and some compatible parts on eBay -- these should
arrive sometime this week at which point I should be able to repair the original board and give it another try.

* The uPB feature of my home-brew KM11 really doesn't work quite right.  It often stops the machine at the requested
micro-state but on the wrong instruction (skipping the first occurrence of the target state seemingly).  This caused
me a great deal of confusion today, as I was stepping through flows at a different program location than I had assumed,
until I finally noticed the address lights on the console.

* ESC key on the VT52 is non-functional, making it impractical to use for RT-11.  The key mechanism looks okay from the
top (thanks for more helpful advice from the vcfed forum!).  I think I'll need to pull the keyboard PCB and re-flow the
solder on the affected mechanism as a next step.

* Looking forward to checking out Vintage Computer Fest West sometime next weekend!
