Title: PDP-11/45: V6 Unix Troubleshooting
Date: 2020-10-24
Tags: Retro-Computing, PDP-11

_[A catch-up article, documenting discoveries of Jan/Feb 2019]_

In early 2019, I made a V6 Unix pack from the Ken Wellsch tape image, as mentioned in [this blog
entry]({filename}unix-and-ms11.md).  It booted on my machine, but dumped core on the first `ls` in single-user
mode, or as soon as I did any heavy lifting in multi-user mode.

The following is the first part of a chronology of the troubleshooting campaign that took place over the next
month and a half, culminating in a smoking gun hardware fix and successful operation of V6 Unix on the
machine.  This was largely a collaborative effort between Noel Chiappa an myself via direct email
correspondence, though help was received from others via the cctalk mailing list as well.

### January 8-9

Initial experiments.  Described the `ls` crashes to Noel.  He theorizes that `ls` works in one case and
crashes in another is because it lands in a different spot in memory in each case.

Luckily, a subsequent `od` on the core file does not crash, and a core file is successfully extracted:
```
140004 000000 141710 141724 
$DK
@rkunix
mem = 1035
RESTRICTED RIGHTS

Use, duplication or disclosure is subject to
restrictions stated in Contract with Western
Electric Company, Inc.
# LS
MEMORY FAULT -- CORE DUMPED
# OD CORE
0000000 141552 141562 000000 000000 000000 000000 000000 000000
0000020 000000
0000060 000000 000000 000000 000001 000000 000000 063260 140076
0000100 001700 000000 000104 066112 067543 062562 000000 000000
0000120 000000 000000 000000 060221 000567 067543 062562 000000
0000140 000000 000000 000000 000000 066112 000000 000020 000000
0000160 000000 000000 000000 000000 177701 000000 000020 000000
0000200 000000 000000 000000 000000 177701 041402 016006 000000
0000220 000000 000000 000000 000000 066016 041402 016006 000000
0000240 000000 000000 000000 000000 066016 075120 075120 075120
0000260 000000
0000300 000000 000000 000000 000000 000013 010400 001050 002366
0000320 000000 000104 000035 000024 000000 141732 141742 141664
0000340 141674 000000 000000 000000 000000 000000 000000 000000
0000360 000000
0000400 000000 000000 000000 000000 000000 000000 000012 000000
0000420 000000 000000 000000 141772 000000 000000 000000 000000
0000440 000000
0001500 000000 025334 003602 001236 025334 003602 002454 003602
0001520 063260 177716 000000 141542 016070 001176 000000 003602
0001540 063260 177716 000000 141562 016070 001176 066352 030300
0001560 063260 025334 003602 077572 000013 107564 141626 000512
0001600 000000 141604 141616 000300 074616 025334 003602 000217
0001620 000203 107404 020276 000512 000000 141634 141640 003602
0001640 000007 000135 107454 141662 014314 003602 066352 005674
0001660 000000 141712 013640 074616 000000 001000 000000 000000
0001700 001000 074616 063260 066352 000013 141726 023730 066352
0001720 063260 000000 000013 141742 023502 003602 000000 177760
0001740 000013 141756 022050 000013 000000 000000 000000 000034
0001760 000444 000031 177760 000000 030351 177770 010210 170010
0002000 000001 177777 177777 023436 023436 020264 000162 000262
0002020 000262 000202 000262 000256 000210 000262 000250 000262
0002040 000262 000216 000262 000262 000262 000262 000262 000224
0002060 000170 000234 000242 000003 100000 000144 040000 000142
0002100 020000 000143 000055 000001 000400 000162 000055 000001
0002120 000200 000167 000055 000002 004000 000163 000100 000170
0002140 000055 000001 000040 000162 000055 000001 000020 000167
0002160 000055 000002 002000 000163 000010 000170 000055 000001
0002200 000004 000162 000055 000001 000002 000167 000055 000001
0002220 000001 000170 000055 000001 010000 000164 000040 020066
0002240 020106 020116 020126 020142 020152 020162 020176 020206
0002260 020216 020226 000056 062457 061564 070057 071541 073563
0002300 000144 062457 061564 063457 067562 070165 005000 071445
0002320 005072 072000 072157 066141 022440 005144 022400 062065
0002340 000040 031045 020144 022400 033055 033056 000163 026445
0002360 062066 022400 062063 022454 062063 022400 071467 020000
0002400 026445 027067 071467 022440 032055 032056 020163 020000
0002420 026445 031061 030456 071462 000040 032045 020144 022400
0002440 005163 022400 030456 071464 000012 071445 072440 071156
0002460 060545 060544 066142 005145 022400 020163 067556 020164
0002500 067546 067165 005144 000000 003750 000144 004076 000157
0002520 004070 000170 004172 000146 004210 000145 004026 000143
0002540 004044 000163 003764 000154 004226 000162 000000 000000
0002560 177774 177760 177775 177770 104404 022376 000000 104405
0002600 000000 000000 104403 000000 001000 104405 000000 000000
0002620 104421 000000 023436 104423 000000 000000 104422 000000
0002640 000000 000037 000034 000037 000036 000037 000036 000037
0002660 000037 000036 000037 000036 000037 043120 020712 020716
0002700 000001 000005 000515 000072 000457 051505 000124 042105
0002720 000124 060504 020171 067515 020156 030060 030040 035060
0002740 030060 030072 020060 034461 030060 000012 072523 046556
0002760 067157 072524 053545 062145 064124 043165 064562 060523
0003000 000164 060512 043156 061145 060515 040562 071160 060515
0003020 045171 067165 072512 040554 063565 062523 047560 072143
0003040 067516 042166 061545 000000 000000 000000 000000 000000
0003060 000000
0010060 000000 000020 000001 177770 177774 177777 071554 000000
0010100 
#
```
Noel prepares to analyze the core file (block quotes here and further below taken from email correspondence):

> I just checked, and the binary for the 'ls' command is what's called 'pure code'; i.e. the instructions are
> in a separate (potentially shared) block of memory from the process' data (un-shared).
----
> On another front, that error message ("Memory error") is produced when a process gets a 'memory management
> trap' (trap to 0250). This could be caused by any number of things (it's a pity we don't know the contents
> of SR0 when the trap happened, that would tell us exactly what the cause was).
----
> [Memory management registers in the core dump] are 'prototypes', later modified for actual use by adding in
> the actual address in main memory. Still trying to understand how that works - the code (in sureg() in
> main.c) is kind of obscure.

### January 10-24

Further communication with Noel and the cctalk list raises some suspicion about the memory in my machine.
Though I had done spot checks and repairs on this in the past, which had been sufficient to pass most MAINDEC
diagnostics and to boot and run RT11, in fact the memory had not yet been exhaustively tested.

Over the course of some days, memory test codes are developed and run, and several additional failed DRAMs in
the MS11 memory system are isolated and repaired.  These efforts have previously been reported in detail in
[this blog entry]({filename}unix-and-ms11.md).

After these repairs, the MAINDEC MS11 memory diagnostics and KT11-C MMU diagnostics, both of which are beastly
and exhaustive, are found to pass robustly with one caveat: memory parity tests.  A deep-dive into the design
and implementation of memory parity on the PDP-11/45 follows.  At the end it is concluded that the machine, a
very early serial no. in its line, is in fact functioning per-design. These efforts are documented in [this
blog entry]({filename}parity-handling.md).

Even though the memory system looks solid after this, the V6 Unix crash behavior remains exactly the same...

### January 27-29

With the KT11 and memory now verified, Noel takes up the core dump again:

> The problem is that Unix does not save enough info in the core dump for me to thoroughly diagnose the MM
> fault; e.g. 'ls' is a 'pure text' program/command, and the code's not included in the core dump (in normal
> operation, there's no need/use for it), so I don't have the code that was running at the time, just the data
> and swappable per-process kernel data - which is not all the per-process data, e.g. it doesn't include the
> location of the process's code and data segments in main memory.

> Also, I'll look at the V6 code that sets up the KT11 registers to make sure I understand what it's doing.
> (The dump contains the 'prototype' for those contents, but the values are modified, by adding the actual
> memory location, before being stored in the KT11.)
----
> I did find out that the PC at the time of the segmentation fault was 010210, which I thought looked awfully
> big (so I was wondering if somehow it went crazy), but in fact the text size is 010400, so it's just inside
> the pure text.

We agree to use
[_Lions_](https://en.wikipedia.org/wiki/Lions%27_Commentary_on_UNIX_6th_Edition,_with_Source_Code) as a common
reference point for detailed discussion of the loading and running of "ls" and what may be seen in the core
dump.


### January 30

Noel:

> So, a bit more from my examination of the swappable per-process kernel data (the 'user' structure - not sure
> how much of a Unix internals person you are).
>
> It gives the following for the text, data and stack sizes:
> 
>     tsize 000104
>     dsize 000035
>     ssize 000024
>
> which seems reasonable/correct, because looking at the header for 'ls' we see:
>
>     000410 010400 001050 002366 000000 000000 000000 000001 
>
> '0410' says it's pure text, non-split; the 010400 is the text size, which matches (those sizes above are in
> 'clicks', i.e. the 0100 byte quantum used in the PDP-11 memory management).
> 
> The data size also appears to be correct:
> 
>     001050 (initialized)
>     002366 (BSS)
>     ------
>     003436
> 
> which again matches (round up and divide by 0100).
> 
> I have yet to dig around through the system sources and see what the initial stack allocation is, to see if
> that's reasonable (of course, it may have been extended during execution).
> 
> And here are the 'prototype' segmentation register contents:
> 
>     UISA 000000 000020 000000 000000 000000 000000 000000 177701
>     UDSA 000000 000020 000000 000000 000000 000000 000000 177701
>     UISD 041402 016006 000000 000000 000000 000000 000000 066016
>     UDSD 041402 016006 000000 000000 000000 000000 000000 066016
>
> Since it's not split, the D-space ones are clones of the I-space (which is what the code does - I don't
> think it turns user D off and on, depending on what the process has: I'd have made context switching faster
> by not having to set up the D-space registers for non-split processes, but I guess the extra overhead is
> pretty minimal).
>
> I have yet to check all the contents to make sure they look good, but the U?SA registers look OK; the '020'
> is for the data, and that's kept contiguous with the 'user' area, so the '020' is to offset past that.
> 
> The PC at fault time of 010210 seems to point to the following code (assuming what was in main memory was
> actually the same as the binary on the disk):
>
>             mov r4,r0
>             jmp 10226
>     210:    mov r5,r0 
>             mov sp,r5
>
> We don't have SSR2, which points to the failing instruction, and I forget whether the saved PC on an MMU
> fault points to the failing instruction, or the next one; I'm going to assume the latter.
>
> But either way, this is very puzzling, because I don't see an instruction there that could have gotten an
> MMU fault! The jump is to a location within the text segment (albeit at the end), and everything else it
> just register-register moves!
> 
> And how could the fault depend on the location in main memory?!?!
> 
> If you want to poke around in the core dump yourself, to verify that I haven't made a mistake, see this
> page:
> 
> <http://gunkies.org/wiki/Unix_V6_dump_analysis>
> 
> which gives useful offsets. (The ones in the user table I verified by writing a short program which did
> things like 'printf("%o", &0->u_uisa)', and the data at those locations looks like what should be there, so
> I'm pretty sure that table is good. For the other one, core(5) (in the V6 man pages) gives the register
> offsets (albeit in a different form), so you can check that I worked them out correctly.
> 
> Two things you could try to get rid of potential pattern sensitivities: before doing the 'ls', say 'sleep
> 360 &' first; that running in the background _should_ cause the 'ls' to be loaded and run from a different
> address in main memory. The other thing you could try is 'cp /bin/ls xls' and then 'xls', to load the
> command from a different disk location. (Both of these assume that you don't get another fault, of course!)
----
> [Initial stack size] is 20\. clicks, which is what it still is (024 clicks) in the process core dump, so
> the stack has _not_ been extended. So any MM fault you see after starting 'ls' will _probably_ be the one
> that's causing the process to blow out.
----
> I tried to re-create that exact version of the 'ls' binary, because the one in the distro is stripped, and I
> wanted one with symbols to look at. I failed, because a library routine (for dates) has changed on my
> machine, see here:
> 
> <http://www.chiappa.net/~jnc/tech/V6Unix.html#Issues>
>
> However, I did verify that the binary for ls.o is identical to what I can produce (using the -O flag). It's
> just that library routine which is different. I don't think it's worth backing out my library; I did manage
> to hand-produce a stub of the symbol table for where the error is happening in the old 'ls' binary:
>
>     010210T csv
>     010226T cret
>     010244T cerror
>     010262T _ldiv
>     010304T _lrem
>     010324T _dpadd
> 
> The fault does indeed seem to be happening at either the last instruction in the previous routine (ct_year,
> in ctime.c), or the first of csv.
> 
> (I should explain that PDP-11 C uses two small chunks of code, CSV and CRET, to construct and take down
> stack frames on procedure entry and exit. So on exit from _any_ C procedure, the last instruction is always
> an PC-relative jump to CRET.)
> 
> It looks like that's what's blowing up - but it apparently works with the command at a different location in
> main memory! So it pretty much has to be a pattern sensitivity.
> 
> However, I think the KT11 does the bounds checking _before_ it does the relocation - the bounds checking is
> done on virtual, un-relocated addresses. So _that_ part of it _should_ be the same for both locations! So
> here's my analysis:
> 
> Is it actually an indexed jump that's blowing up? I've been looking at the command binary, but that might
> not be what's in main memory. Or the CPU might be looking somewhere else (because of a KT error). (If we
> don't find the problem soon, we might want to put in that breakpoint so we can look in main memory and see
> what inst is actually at the location where SSR2 says the failing inst was; that can rule out a whole bunch
> of potential causes in one go - e.g. RK11 errors.)
> 
> If it is actually that jump that's failing - how? The PC hasn't been updated yet, so it can't be the fetch
> of the next instruction that's failing. Is the fetch of the index word producing the MM fault?

Fritz:

> It occurs to me that we don't even *really* know if the fault occurs from the same address every time, since
> we have a core sample size of 1; I should duplicate the fail and extract another core file to compare.
----
> Another thing I thought I might try tonight: deposit a trap catcher in the memory mgmt trap location from
> the front panel, just before issuing the 'ls' command.  I can then check the PSW, PC, SP, and KT11 regs
> right at the time of fault.

Experiments begin from the front panel, and continue on into the early hours, producing:

Core #2:
```
140004 000000 141710 141724
$DK
@rkunix
mem = 1035
RESTRICTED RIGHTS

Use, duplication or disclosure is subject to
restrictions stated in Contract with Western
Electric Company, Inc.
# RM CORE
# LS
MEMORY FAULT -- CORE DUMPED
# OD CORE
0000000 141552 141562 000000 000000 000000 000000 000000 000000
0000020 000000
0000060 000000 000000 000000 000001 000000 000000 063260 140076
0000100 001700 000000 000104 066112 067543 062562 000000 000000
0000120 000000 000000 000000 060221 000571 067543 062562 000000
0000140 000000 000000 000000 000000 066112 000000 000020 000000
0000160 000000 000000 000000 000000 177701 000000 000020 000000
0000200 000000 000000 000000 000000 177701 041402 016006 000000
0000220 000000 000000 000000 000000 066016 041402 016006 000000
0000240 000000 000000 000000 000000 066016 075120 075120 075120
0000260 000000
0000300 000000 000000 000000 000000 000013 010400 001050 002366
0000320 000000 000104 000035 000024 000000 141732 141742 141664
0000340 141674 000000 000000 000000 000000 000000 000000 000000
0000360 000000
0000400 000000 000000 000000 000000 000000 000000 000011 000000
0000420 000000 000000 000000 141772 000000 000000 000000 000000
0000440 000000
0001500 000000 000000 000000 000000 000000 000000 000000 003602
0001520 063260 177716 000000 141542 016070 001176 000000 003602
0001540 063260 177716 000000 141562 016070 001176 066352 030300
0001560 063260 141576 000005 003602 066352 001612 074376 044516
0001600 003602 025334 003602 000000 000443 107144 141646 000512
0001620 000000 141624 141640 000300 020276 020356 030000 003602
0001640 000007 000135 107454 141662 014314 003602 066352 004404
0001660 000000 141712 013640 074616 000000 001000 000000 000000
0001700 001000 074616 063260 066352 000013 141726 023730 066352
0001720 063260 000000 000013 141742 023502 003602 000000 177760
0001740 000013 141756 022050 000013 000000 000000 000000 000034
0001760 000444 000031 177760 000000 030351 177770 010210 170010
0002000 000001 177777 177777 023436 023436 020264 000162 000262
0002020 000262 000202 000262 000256 000210 000262 000250 000262
0002040 000262 000216 000262 000262 000262 000262 000262 000224
0002060 000170 000234 000242 000003 100000 000144 040000 000142
0002100 020000 000143 000055 000001 000400 000162 000055 000001
0002120 000200 000167 000055 000002 004000 000163 000100 000170
0002140 000055 000001 000040 000162 000055 000001 000020 000167
0002160 000055 000002 002000 000163 000010 000170 000055 000001
0002200 000004 000162 000055 000001 000002 000167 000055 000001
0002220 000001 000170 000055 000001 010000 000164 000040 020066
0002240 020106 020116 020126 020142 020152 020162 020176 020206
0002260 020216 020226 000056 062457 061564 070057 071541 073563
0002300 000144 062457 061564 063457 067562 070165 005000 071445
0002320 005072 072000 072157 066141 022440 005144 022400 062065
0002340 000040 031045 020144 022400 033055 033056 000163 026445
0002360 062066 022400 062063 022454 062063 022400 071467 020000
0002400 026445 027067 071467 022440 032055 032056 020163 020000
0002420 026445 031061 030456 071462 000040 032045 020144 022400
0002440 005163 022400 030456 071464 000012 071445 072440 071156
0002460 060545 060544 066142 005145 022400 020163 067556 020164
0002500 067546 067165 005144 000000 003750 000144 004076 000157
0002520 004070 000170 004172 000146 004210 000145 004026 000143
0002540 004044 000163 003764 000154 004226 000162 000000 000000
0002560 177774 177760 177775 177770 104404 022376 000000 104405
0002600 000000 000000 104403 000000 001000 104405 000000 000000
0002620 104421 000000 023436 104423 000000 000000 104422 000000
0002640 000000 000037 000034 000037 000036 000037 000036 000037
0002660 000037 000036 000037 000036 000037 043120 020712 020716
0002700 000001 000005 000515 000072 000457 051505 000124 042105
0002720 000124 060504 020171 067515 020156 030060 030040 035060
0002740 030060 030072 020060 034461 030060 000012 072523 046556
0002760 067157 072524 053545 062145 064124 043165 064562 060523
0003000 000164 060512 043156 061145 060515 040562 071160 060515
0003020 045171 067165 072512 040554 063565 062523 047560 072143
0003040 067516 042166 061545 000000 000000 000000 000000 000000
0003060 000000
0010060 000000 000020 000001 177770 177774 177777 071554 000000
0010100
#
```
and also:

> 'db' works  
> 'cp' works  
> 'rm' works  
> 
> 'sleep 360 &' followed by 'ls' works, and then when the 'sleep' ends no longer works!  So confirmation about
> memory location dependence.
> 
> 'cp /bin/ls xls' followed by 'xls' does not work (dumps core); works with 'sleep' as with 'ls' above.
----
> Okay, last experiment, booting up, then depositing trap catcher from the front panel into vector 250:
> 
>     000250: 000252
>     000252: 000000
> 
> ...then issuing the 'ls' seems to catch it.  I can then examine registers and memory etc. from the front
> panel.  This is a quick and easy repro.  I went ahead and dumped a few of the KT11 registers (but its late,
> so I can't guarantee I didn't slip up -- should try this again when I'm fresh):
> 
>     SR0: 040143 (ah! page length fault, user I-space, page 1)
>     SR1: 000000 (no auto inc/dec to clean up)
>     SR2: 010210 (virtual PC, agrees with your deduction from core dump)
>     SR3: 000000 (that's odd -- shouldn't split I/D be enabled?)
> 
>     UIPDR: 041402 016006 000000 000000 000000 000000 000000 066116
>     UIPAR: 001614 001760 001614 001614 001614 001614 001614 001614
>     
>     UDPDR: 010501 057517 077717 077717 037611 067616 076300 064317
>     UDPAR: 002417 002564 007777 007766 005635 005656 007777  oops
> 
> ...where "oops" means I thought I was done scribbling all these down, and turned off the machine.  Did I
> mention it's late? :-)

[Note: It _was_ late, and there is an error with UIPAR7 in this transcription.  This will be the source of
some uncertainty until corrected on February 2.]

### January 31

Noel:

>> 'sleep 360 &' followed by 'ls' works, and then when the 'sleep' ends no longer works! So confirmation about
>> memory location dependence.
>
> Yeah, that's a really important data-point. The fact that it is physical location dependent really does tend
> to implicate the KT11; I think the KB11 mostly only knows/has virtual addresses? (So I probably shouldn't
> bang my head trying to think of failure modes in the KB11?) If you have the source for its diag, you might
> try looking through it, looking for things it doesn't try...
> 
> Although I suppose it could be a location-dependent issue with the RK11. I should explain how to find, and
> examine the pure-text for the 'ls' command; if you halt the CPU on the trap again, look at UISA0, and that
> should give you the 'click' where the text starts; at that point I'd probably examine every 256th (block
> size) word and we can compare them to the original to make sure the in-core copy is OK.
----
>>     SR0: 040143 (ah! page length fault, user I-space, page 1)
>>     SR2: 010210 (virtual PC, agrees with your deduction from core dump
>
> If it's really 010210, I wonder how it could be a fault on page 1; each page (segment, really) of virtual
> address space is 020000 long, so that address is well inside page 0?
> 
> Unless it has fetched some other instruction, due to some other error, one which does try and do something
> on page 1... Might want to try looking at a few instructions around 010210 when you try this again, see
> what's actually there. Let's see, code starts at 0161400 in real memory (per UIPAR0 below), so 010210 is at
> 0171610... Maybe dump a few words from 171600 on?
> 
>>     SR3: 000000 (that's odd -- shouldn't split I/D be enabled?)
> 
> No; you're running binary for a /40 system, so no split I/D. So also, all the UDPARs and UDPDRs will contain
> junk.
>
>>     UIPAR: 001614 001760 001614 001614 001614 001614 001614 001614
> 
> ?? UIPAR7 looks wrong; if the data is really at 01760, I think the stack should be above that in real memory
> \- but I might be wrong, I will check.
> 
> If it is wrong, did something cause the wrong value to be stored there (e.g. an error in the execution of
> lines 1750/1751 in Lions); or was the prototype calculated wrong (around line 1704) - but I think the
> prototypes looked correct in the process' core dump, but I will check them; or did the hardware flake out,
> and e.g. copy a later store (the code fills them from the top down) up to UISA7?
> 
> To check out the latter, maybe a bespoke tiny program, toggled in, to try storing the 'correct' data in the
> UISPARs, in the exact way that the Unix code does it, and then look and see what's in there?
> 
> This might also correlate to the strange stuff I saw in the process' user-mode stack, in the dump - I will
> go back and look at that now.
> 
> If you do this again, please add KISA6 and KISD6 to the registers to dump (you can skip UDS*), so we can see
> what it thinks is going on with the per-process swappable data, which should be just below the process'
> user-mode data, in terms of real memory.
____
> Yes, the stack is directly above the user data, which is directly above the swappable per-process data (user
> struct, and kernel stack). But the address math for stack segments in the KT11 is weird (see below).
> 
> I _think_ the prototypes:
> 
>     UISA 000000 000020 000000 000000 000000 000000 000000 177701
>     UISD 041402 016006 000000 000000 000000 000000 000000 066016
> 
> are right, but the negative direction of the stack is making my head hurt (and the UISA7 you recorded from
> the hardware might be right after all - but then the UISA0 might be wrong - it's suspicious, but not
> impossible, that they are the same value).
> 
> If the SPPD is at physical xxx, the user data will be at xxx+20 (in clicks, as above) through xxx+20+34
> (below), and then the stack above that. Per the SPPD:
> 
>     tsize 000104
>     dsize 000035
>     ssize 000024
> 
> the stack should then run from xxx+20+35 to xxx+20+35+23. The way the MM hardware works for stack segment,
> the 'base' is where the first click would be if the segment were a full 0200 clicks. (Per the example in the
> /45 proc handbook; for a 3-click stack running from physical 0331500 to 0331776, the PAR would contain
> 03120, i.e. segment base at 0312000.)
> 
> So let me do the math (please check to see if I'm confused :-); base of user data is at 0176000 (per UISA1
> contents), runs to 0201476 (i.e. plus 03500); the stack would run from 0201500 to 0204076 (i.e. plus 02400).
> So the stack segment 'base' would be 020000 below the next word, or 0164100.
> 
> (My head hurts too much to work out if the 177701 of the prototype is right; basically, the location of the
> SPPD in clicks would be 01740 (I _think_ - 01760 - 020), and that plus 177701 should give us 01641.)
> 
> But, anyway, I'm fairly sure that 01614 is _not_ right for UISA7 (unless it really was 1641 and you inverted
> the digits because it looked so close).
> 
> Having KISA6 would help since it would give us a cross-check on the value of UISA1.....
----
> So, according to the process core dump, these are the register contents at the time of the fault:
> 
>     R0 177770
>     R1 0
>     R2 0
>     R3 0
>     R4 34
>     R5 444
>     SP 177760
>     PC 010210
>     PS 170010
>
> Now, PDP-11 uses R5 for a frame pointer, set up thus:
>
>             jsr     r5,csv		(first instruction in every C routine)
>     
>     csv:
>             mov     r5,r0
>             mov     sp,r5
>             mov     r4,-(sp)
>             mov     r3,-(sp)
>             mov     r2,-(sp)
>             tst     -(sp)
>             jmp     (r0)
>
> on subroutine entry (the 'jsr r5, csv' pushes the old R5 contents, and temporarily saves the return PC - to
> just after the call to CSV, not to the sunroutine which called this one, that's further down - in R5). So,
> except for the first two instructions of CSV, R5 _always_ contains an old SP.
> 
> Now look at the R5 from the crash. That's not an old SP. Something has already gone seriously wrong by this
> point - actually, likely the process has just started to run the newly-loaded command code (see below), and
> hasn't even set up its first stack frame yet.
> 
> Now look at the top of the stack, as recorded in the process' core dump:
> 
>     0010060: 000000 000020 000001 177770 177774 177777 071554 000000
> 
> And that's _it_; the rest if all 0's! (The base address does seem to correspond; with:
> 
>     dsize 000035
>     ssize 000024
>
> and the SPPD being 020 clicks, that puts the top of the stack at 0101 clicks, or 010100, and the last
> location there is 010076.
> 
> The core dump routine, core() writes the user data out in two transfers (Lions 4113-4124), one for the SPPD,
> one for the user's data+stack. So we probably got the SPPD OK, but the rest - who knows?
> 
> It does call estabur(), which sets up the prototype MM register contents, and then writes them into the
> actual registers, so the prototypes in the process' core dump that I was looking at before have already been
> overwritten. :-(But estabur() then called sureg (Lions 1724) so hopefully the MM regs wound up pointing to
> the actual memory being used for the stack - but who knows?
> 
> Anyway, looking at the contents, the top of the stack does look vaguely like what it should be when the
> command _starts_ executing, after the exec() call; the SP is even reasonable; it points to that 0 at offset
> 010060.
> 
> The 020 is the return point for the call to _main (see below; that 'jsr pc,_main' ends at 016); the '1' is
> probably 'nargs' (see Exec(II) in the V6 Manual), the '0177770' is argv, '177774' is argv[0], 177777 is
> argv[1] (end of list marker), and '071554' is 'ls' (the command name, by convention the first argument).
> 
> R0 contains what looks like an old SP, although I suppose that could have been
> left over from the assembler startup:
> 
>     start:
>               setd
>               mov     sp,r0
>               mov     (r0),-(sp)
>               tst     (r0)+
>               mov     r0,2(sp)
>               jsr     pc,_main 
>
> but clearly the attempt to execute the first instruction in CSV blew up. And where did the '444' in R5 come
> from? The call to CSV is at 030?

### February 1

Noel, regarding the second core file:

> I took a quick look, and everything 'important' seems to be identical: the registers, PC, etc at the time of
> the trap (including that mysterious '444' in R5); the prototype MM registers; the user's stack (looking
> again like the command just started.
----
>> I went ahead and dumped a few of the KT11 registers
>>
>>     UIPDR: 041402 016006 000000 000000 000000 000000 000000 066116
> 
> Oh, BTW, I checked, and these match the prototype values in the user struct.

### February 2-3

A tip from Noel:

> Something stirred this in my memory: the best quick overview of the internals of the Bell PDP-11 Unixes is
> K. Thompson, "UNIX Implementation", available here:
>
> <https://users.soe.ucsc.edu/~sbrandt/221/Papers/History/thompson-bstj78.pdf>
>
> if you want to know more about what the insides are like.

Fritz:

> Okay, here's the latest, done with some care:
> 
>     UISD: 041402 016006 000000 000000 000000 000000 000000 066116
>     UISA: 001614 001760 001614 001614 001614 001614 001614 001641
> 
>     KISD: 077406 077406 077406 077506 077506 077406 007506 077506
>     KISA: 000000 000200 000400 000600 001000 001200 001740 007600
> 
>     SRs: 040143 000000 010210 000000
> 
>     171600: 016162 004767 000224 000414 006700 006152 006702 006144

[Note: this fixes the previous late-night transcription error with UISA7...]

Noel:

>>     UISD: 041402 016006 000000 000000 000000 000000 000000 066116
>>     UISA: 001614 001760 001614 001614 001614 001614 001614 001641
> 
> So, 'good news' is these are the same except for UISA7, for which as I suspected, it looks like the digits
> were transposed. But the new value is exactly the one I calculated.
> 
> 'Bad news' is that takes out what I was thinking might be a potential cause, which was UPAR's getting
> trashed by hardware failure. So more hard work ahead (see below).
> 
>>     KISD: 077406 077406 077406 077506 077506 077406 007506 077506
>>     KISA: 000000 000200 000400 000600 001000 001200 001740 007600
> 
> Those all look OK: KISD6 show the segment length as 020 (017 being the last valid click), which is right,
> and KISA6 is 01740, so with the user area and kernel stack being 20 clicks, that makes the start of the user
> data 01760, which is what UISA1 contains.
>
>>     SRs: 040143 000000 010210 000000
> 
> OK, same failing location as before (010210); SSR0 shows:
> 
>     Abort - page length error
>     User mode
>     Page 1
>
> which is the same as last time.
>
>     171600: 016162 004767 000224 000414 006700 006152 006702 006144
>
> Let me just re-check the math here: text base is 0161400, plus a PC of 010210, gives us 0171610, which is
> right in the middle there - thanks!
> 
> That does not, alas, look anything _at all_ like what's _supposed_ to be there, which is:
> 
>     010200: 110024
>             010400  mov r4,r0
>	          000167  jmp 10226 (cret)
>	          000016
>	          010500  mov r5,r0 (start of CSV)
>	          010605  mov sp,r5
>	          010446  mov r4,-(sp)
>             010346  mov r3,-(sp)
>
> So maybe the RK11 went berserk? But maybe not...
> 
> The 4767 is a 'jsr pc, xxx' which is typical C compiler emission, but the rest looks like rubbish - 6700 is
> a SXT R0, for instance.
> 
> What's actually there at 010210 (virtual) still doesn't explain the MM trap we got; 'SXT R0' should have
> executed OK, no matter what? Confoozled...
>
> What's also odd is how it got here; it's almost like the first few instructions:
> 
>     start:
>               setd
>               mov     sp,r0
>               mov     (r0),-(sp)
>               tst     (r0)+
>               mov     r0,2(sp)
>               jsr     pc,_main 
>
>     _main:
>               jsr     r5,csv
>
> executed OK, and then it tried to go off to csv, only there's trash there? And what's with the 0444 in R5?
> That should be 034, the return from that last JSR.
>
> I'm going to go ponder all this. One more thing you could try is do this all again, and write down the first
> couple of instructions at the start of the text segment (UISA0 = 01614, so 0161400 on for a few words), so
> we can see if _that_ looks OK.
> 
> If so, it will look like the command got read in off the disk wrong - since it's not coming from swap (it's
> just starting), it's coming out of the file system wrong. Why will be a good question.
> 
> And I still don't understand the 'segment 1' fault, and the R5 contents - so many things going wrong all at
> once, for reasons that make no sense... I wonder if there's a noise glitch hitting several things all at the
> same time?

Fritz:

> I read a bit through the KT11 maintenance manual you sent yesterday, to refresh myself on it a bit (thanks
> for that!).  I realized I almost always use my console in "PROG PHY" or "CONS PHY" mode; but using "USER I"
> and "KERNEL I" I may be able to verify quickly that the KT11 is thinking VA:010210 -> PA:171610.
> 
> When I set this up to try later, I'll examine that start of the text segment at 161400 as well, per your
> recommend.

### February 4

Noel sends up a flare on cctalk in the the early AM, summarizing the problem and experiments to date.
Suggestions start to flow in.  Some have already been tried or can be ruled out.  Some others:

- Bob Smith: "I keep wondering about the psu...".  This gets some agreement from the list, and a few
  interesting/relevant anecdotes are relayed.  Paul Koning:

    > In RSTS development we once ran into DMC-11s not working reliably.  The field service tech knew exactly
    > what to look for, and started checking all the supply voltages.  The spec says allowed tolerances are
    > +/- 5%.  He knew the reality for correct operation was -0%, +5%, so he tweaked all the supplies to read
    > a hair above nominal.
    
    Warner Losh:

    > I recall our PDP-11 tech tweaking +5V from 5.05V to 4.95V and back again to demonstrate that tiny
    > differences matter a lot on one of the cranky 11/23+''s we had after I made a particularly unhelpful
    > teenage smart ass remark... The 11/23+ wouldn't boot at the slightly lower than full voltage.

    It is worth noting that in both of these cases, a slight undervoltage proved problematic...

- Paul Koning suggests a potential KT11 failure mode:

    > Another possibility occurs to me: bad bits in the MMU (UISAR0 register if I remember correctly).  Bad
    > memory is likely to show up with a few bits wrong; if UISAR0 has a stuck bit so the "plain" case maps
    > incorrectly you'd expect to come up with execution that looks nothing at all like what was intended.

    Noel provides a short diagnostic (apparently, straight from his mind to machine code; props! :-) to check
    read-after-write on UISA* so we can rule this out:

        1000:   12706	    / Put stack at 0700
                700
                12701	    / Load UISA0 address in R1
                177640
                5000	    / Start testing at 0
                10011	    / Store it
                20011	    / Check it
                1401	    / Skip if match
                0		    / Halt here on error
                5200	    / Next value
                20027		/ 07777 or less?
                7777
                101770		/ Go around
                5721		/ Next register
                20127		/ Done them all?
                177660
                101401		/ Skip if not
                0		    / Halt here when done
                137		    / Go back
                1010

    This is toggled in and passes on the machine.

- Mattis Lind:

    > Would it be any difference if you run the machine at full speed or lower speed or even single step past
    > this instruction? ... The TIG module has a separate non crystal controlled oscillator which one could
    > tune for marginal checking.

    Ah, yes, the margining clock!  Always worth a check, and very easy to use with if you have a KM11 handy.
    A variety of clock speeds are tried, but the behavior remains the same.

- Brent Hilpert:

    > For consideration, what about the refresh circuitry of the memory board?
    >
    > Mem diagnostics, unless they explicitly account for it, may not show up problems with memory refresh if
    > the loop times are short enough to effectively substitute as refresh cycles, while they could show up
    > later in real-world use with arbitrary time between accesses.
    >
    > Refresh on some early boards/systems was asynchronously timed by monostables or onboard oscillators
    > which can drift or fail on the margin/slope. (I don't know what DEC's design policy was for DRAM
    > refresh). It might also explain why a number of 4116s were (apparently) failing earlier in the efforts
    > (if I recall the discussion correctly), replacing them might have just replaced them with 'slightly
    > better' chips, i.e. with a slightly longer refresh tolerance.

    This one also gets some follow-up.  The schematics are consulted, and the MS11-L refresh is seen, indeed,
    to be driven by a simple free-running 555.  Further from Brent:

    > 4116 datasheet specs 2mS, my calcs give a refresh period of 1.5mS, the 14.5uS from the manual would give
    > 1.86 mS, 7% shy of 2. The schematic specs 1% resistors, and the parts list does appear to spec a
    > high-tolerance "1%200PPM" cap.
    > 
    > Although there are the internal voltage divider Rs in the 555 which are also critical for the timing and
    > everything is 40+ years old...

    The actual MS11 in use measures out on my 'scope at 15.2us.  From Brent:

    > 15.2uS gives a 1.95mS refresh, so it's awfully close to the 2mS spec, but still within.  The datasheet I
    > was looking at doesn't seem to give any spec for tolerance on the refresh so one would guess there's a
    > safety margin built into the 2mS spec.

Fritz:

>>     R0 177770
>>     R1 0
>>     R2 0
>>     R3 0
>>     R4 34
>>     R5 444
>>     SP 177760
>>     PC 010210
>> 
>>     060: 000000 000020 000001 177770 177774 177777 071554 000000
>
> Okay, I've had a bit of time in front of the machine to repro this and take a look.  What I actually see is:
> 
>     R0 177770
>     R1 0
>     R2 0
>     R3 0
>     R4 0
>     R5 34
>     R6 141774
>     PC 000254
>
> (remember, for the last, this will have been after taking a trap to 250, where I have the usual "BR .+2;
> HALT" catcher installed)
> 
> Also, memory at 060 (PA:164060) is all zeros as far as the eye can see...

Then, a big discovery from Noel:

> Argh. (Very red face!)
> 
> I worked out the trap stack layout by looking at m40.s and trap.c, and totally forgot about the return PC
> (that's the 0444) from the call to trap():
>
>     0001740 000013 141756 022050 000013 000000 000000 000000 000034
>     0001760 000444 000031 177760 000000 030351 177770 010210 170010
> 
> I clearly should have looked at core(V) in the V6 manual!
> 
> The R6 you have recorded is correct for just after the trap; that's the kernel mode SP, which points to the
> top of the kernel stack, in segment 6 (in the swappable per-process kernel area, which runs from
> 140000-1776).
>
> So there is no R5 mystery, I was just confused. Back to the other two!

But meanwhile, back in front of the actual machine:

> Seeing some quite strange stuff now, after the crash, flipping between "CONS PHY" and "PROG PHY"...
> 
> Bits 6-12 are not acting as I would expect, almost as if the KT11 ALU is doing an incorrect operation
> (subtraction rather than add!)  
> 
> I see these are 74S181 bit slice ALUs, and function code should be hardwired to "A+B"... So that brings us
> back around to really checking those supply voltages...

It turns out the +5V supplies were, in fact, slightly low (about 4.9 or so).  Trimmed these up, and the the
observed problems with bits 6-12 receded, though the "ls" crash remained exactly the same.  It would appear,
though, consistent with remarks above, that the machine has very little undervoltage tolerance on +5V --
certainly less than the documented -5%.

How long had the machine been in this condition, and what else might have been affected?  It could not have
been for very long, since the previously run KT11 diagnostics would certainly have failed.  But the situation
was spooky, and instilled some uncertainty about other data that had recently been retrieved via the front
panel...

### February 5

Noel clears away one additional address calculation error:

> So I had to grub a bit to find this, but here's what I said:
> 
>> With KISA7 at 001641, 0164100 should be the first location after the stack, so 0164060 and up would be
>> good. They _should_ be:
>> 
>>     060: 000000 000020 000001 177770 177774 177777 071554 000000
>
> and I have no idea how I screwed the address there up that that badly. The data I'm showing there is the top
> (address-wise; i.e. bottom, push-pop-wise) of the user stack, and I think it's correct. However, it's UISA7
> which contains 01641, and that's the 'bottom' of that segment. I had previously done the math correctly:
>
>> base of user data is at 0176000 (per UISA1 contents), runs to 0201476 (i.e. plus 03500); the stack would
>> run from 0201500 to 0204076 (i.e. plus 02400). So the stack segment 'base' would be 020000 below the next
>> word, or 0164100.
> 
> So physical 0164060 is just in the middle of nowhere; it's somewhere in the middle of the text (which starts
> at physical 0161400).
> 
> If you could try this again, and check the top of the _actual_ user stack (which will be at physical
> 0204060-0204076), I'd really appreciate it. I do expect it to be correct: the process core dump has it
> correct (as shown by the analysis of argc, argv, etc).

And I am able to get some consistent, correct, data after the power-supply tune-up:

> Okay, latest numbers for you!
> 
> Stack, confirmed:
> 
>     PA:204060: 000000 000020 000001 177770 177774 777777 071554 000000
> 
> Text; as I had feared, a few dropped bits there!  Went ahead and grabbed you eight extra words while I was
> there:
> 
>     PA:171600: 016162 004767 000224 000414 016700 016152 016702 016144
>     PA:171620: 004767 000206 000405 012404 012467 016124 000167 177346
> 
> In disassembly from 171602, this yields:
> 
>     171602:	JSR     PC,172032
>     171606:	BR      171640
>     171610:	MOV     7766,R0
>     171614:	MOV     7764,R2
>     171620:	JSR     PC,172032
>     171624:	BR      171640
>     171626:	MOV     (R4)+,R4
>     171630:	MOV     (R4)+,7760
>     171634:	JMP     171206
> 
> ...which looks at least like feasible code, if not the code we are expecting?

Last, a note on procedure for using the front panel to verify KT11 address mappings:

> The way this works is you select the mapping set you want (in our case, USER I) with the top knob on the
> console, then toggle in a _virtual_ address, hit "LOAD ADRS", and then when you hit "EXAM" it maps your
> provided address through the selected set.  Under these circumstances, I'll also see the "KERNEL" light go
> out and the "USER" light light up on the front panel indicating the active mapping set.  You can then flip
> to "PROG PHY" to see the mapped-to physical address.  This is not explained very clearly in the handbooks;
> it took me a little experimentation to figure out how to do it.
>
> Anyway, in our case, I toggle in "10210", and can read out "171610".

### February 6

Noel:

>> In disassembly from 171602, this yields: ...which looks at least like feasible code
> 
> The first 4 words, yes, but not the rest. (Oh, and your disassembly is wrong; you used PA addresses, not
> VA.)
> 
> But excitingly, that _could_ explain the MM trap, since 16700/16152 at VA: 010210 gives us:
>
>     MOV 26364, R0
>
> and that address is in segment 1, which is only 03500 long...

Fritz:

> Also, that exact sequence does occur in the ls binary!
>
> From last night:
> 
>     PA:171600: 016162 004767 000224 000414 016700 016152 016702 016144
>     PA:171620: 004767 000206 000405 012404 012467 016124 000167 177346
> 
> And from an od on bin/ls:
> 
>     0004220 016162 004767 000224 000414 016700 016152 016702 016144
>     0004240 004767 000206 000405 012404 012467 016124 000167 177346

All together, this brings us to a significant juncture in the debug effort: the power supply issue has been
addressed, and various red herring have been cleared away.  Pre-conditions which exactly match the observed
fault are apparent.  We are left with a single, consistent, and reproducible issue: part of the process
address space ends up holding the wrong part of the program text.  But how, and why?
