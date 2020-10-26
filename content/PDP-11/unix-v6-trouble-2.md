Title: PDP-11/45: V6 Unix Troubleshooting, Part II
Date: 2020-10-25
Tags: Retro-Computing, PDP-11

_[A catch-up article, documenting discoveries of Feb 2019]_

In early 2019, I made a V6 Unix pack from the Ken Wellsch tape image, as mentioned in [this blog
entry]({filename}unix-and-ms11.md).  It booted on my machine, but dumped core on the first `ls` in single-user
mode, or as soon as I did any heavy lifting in multi-user mode.

The following is the conclusion of a chronology of the troubleshooting campaign that took place over the next
month and a half, culminating in a smoking gun hardware fix and successful operation of V6 Unix on the machine
(part I is [here]({filename}unix-v6-trouble-1.md).)  This was largely a collaborative effort between Noel
Chiappa an myself via direct email correspondence, though some help was received from others via the cctalk
mailing list as well.

By this point, the nature of the `ls` problem had been fairly well characterized: part of the `ls` process
address space ended up holding an incorrect portion of its program text; subsequently, when execution jumped
to some of these unexpected bits, an out-of-bounds memory access would occur triggering a memory management
trap.  Efforts now focus on understanding how and why the bad bits got there...

### February 7

[Here and below, block-quoted content is excerpted from email correspondence.]

Fritz:

> Noel, is it possible for you deduce where Unix _should_ be placing these  "bad" bits (from file offset octal
> 4220)? Maybe a comparison of addresses where the bits should be, with addresses where the "bad" copy ends
> up, could point us at some particular failure modes to check in the KT11, CPU, or RK11...

Noel:

> Yes, it's quite simple: just add the virtual address in the code to the physical address of the bottom of
> the text segment (given in UISA0). The VA is actually 04200, though: the 04220 includes 020 to hold the
> a.out header at the start of the command file.
> 
> So, with UISA0 containing 01614, that gives us PA:161400 + 04200 = PA:165600, I think. And it wound up at
> PA:171600 - off by 04000 (higher) - which is obviously an interesting number.
----
> Here's where it gets 'interesting'.
> 
> Executing a command with pure text on V6 is a very complicated process. The shells fork()s a copy of itself,
> and does an exec() system call to overlay the entire memory in the new process with a copy of the command
> (which sounds fairly simple, at a high level) - but the code path to do the exec() with a pure text is
> incredibly hairy, in detail. In particular, for a variety of reasons, the memory of the process can get
> swapped in and out several times during that. I apparently used to understand how this all worked, see this
> message:
> 
> <https://minnie.tuhs.org/pipermail/tuhs/2018-February/014299.html>
>
> but it's so complicated it's going to take a while to really comprehend it again. (The little grey cells are
> aging too, sigh...)
> 
> The interesting point is that when V6 first copies the text in from the file holding the command (using
> readi(), Lions 6221 for anyone who's masochistic enough to try and actually follow this :-), it reads it in
> starting from the bottom, one disk block at a time (since in V6, files are not stored contiguously).
> 
> So, if it starts from the bottom, and copies the wrong thing from low in the file _up_ to VA:010200, when it
> later gets to VA:010200 in the file contents, that _should_ over-write the stuff that got put there in the
> wrong place _earlier_. Unless there's _another_ problem which causes that later write to _also_ go somewhere
> wrong...
> 
> So, I'm not sure when this trashage is happening, but because of the above, my _guess_ is that it's in one
> of the two swap operations on the text (out, and then back in). (Although it might be interesting to look at
> PA:165600 and see what's actually _there_.) Unix does swapping of pure texts in a single, multi-block
> transfer (although not always as an integral number of blocks, as we found out the hard way with the QSIC
> :-).
> 
> So my suspicions have now switched back to the RK11... One way to proceed would be to stop the system after
> the pure text is first read in (say around Lions 4465), and look to see what the text looks like in main
> memory at _that_ point. (This will require looking at KT11 registers to see where it's holding the text
> segment, first.)
> 
> If that all looks good, we'll have to figure out how to stop the system after the pure text is read back in
> (which does not happen in exec(), it's done by the normal system operation to swap in the text and data of a
> process which is ready to run).
> 
> We could also stop the system after the text is swapped out, and key in a short (~ a dozen words) program to
> read the text back in from the swap device, and examine it - although we'd have to grub around in the system
> a bit to figure out where it got written to. (It might be just easier to stop it at, say, Lions 5196 and
> look at the arguments on the kernel stack.)

Fritz:

>>...it might be interesting to look at PA:165600 and see what's actually _there_
>
> A sea of zeros, as it turns out.
----
>> The most valuable thing ... would be to look at the text segment, after it's read in and before it's
>> swapped out. I can work out where to put a halt, if you want to try that.
>
> Yes, this sounds like a good plan to me!  Is this as simple as dropping a HALT at VA:0 in the text? 

Noel:

> No; actually, probably easier! :-) Probably easiest is to, just before you type 'ls', put a HALT in the OS
> just after 4467 in Lions. Halt the machine momentarily, patch the kernel, and CONT. (Basically the same as
> your patch to the trap vector, just a different address.) That'll be at 021320 (should contain 062706),
> physical or virtual. :-)
>
> When the system halts, you'll need to look at the text in memory. Two ways to find the location: look on the
> kernel stack, the address should be the second thing down:
>
>     mov 16(r3),-(sp)
>     add $20,(sp)
>     mov (r4),-(sp)
>     jsr pc,*$_swap 
> 
> (i.e. the thing that 020 got added to). Probably easier, though, is just to look in UISA0 (which at this
> point is pointing to the block of memory that's been allocated to read the text into, Lions 4459-60).
> 
> That number in UISA0, T, will be the click address of the text. So PA:T00 should be the start of the text
> (170011 010600, etc). So then PA:(T00+010200) should be the trashed chunk of text: 110024 010400 000167
> 000016 010500 etc (right) or 016162 004767 000224 000414 016700 (wrong).

### February 8

Noel:

> In addition to the info I already sent about how to [set the breakpoint], if you could note down the top 3
> words on the kernel stack, and the contents of the RK registers, those would be really useful; the first
> will allow us to work out what _should_ be in the RK registers after the swap I/O operation completes - I
> don't think the RK11 will be asked to do anything after that finishes and before the system hits that halt
> in xalloc().
> 
> To find the kernel stack.... read out KISA6, S. This value will point to the 'user' area of that process,
> plus the kernel stack. The kernel SP should be something like 01417xx; subtract 140000 (the segment number),
> and add what's left to S00.  Alternatively, you can probably use the rotating switch on the front panel to
> just look up VA:1417xx (whatever's in R6) directly.
>
> Oh, if you need some bed-time reading to put you to sleep, check out the bottom section ("exec() and
> pure-text images") in:
> 
> <http://gunkies.org/wiki/Unix_V6_internals>
>
> which will explain what's going on here with the swapping in and out, which is sorta complicated.

### February 9

Noel:

>> just halt the machine after the text is swapped in
> 
> The code we need is at Lions 2034, where the pure text of a process is swapped in (and this should only be
> traversed once; I don't think the system will need to swap in the text of the shell); just put a HALT in (in
> the usual manner, just before trying 'ls') at 015406, which should contain a 062706 (again).
> 
> At that point, since the text size is 010400, and the location of the text in physical memory is 0161400,
> the BAR _should_ contain 0172000. If not, and it's 0232000 (note that the 0200000 bit will be in the CSR,
> the lower XM bit) instead, Bazinga!, it's nailed (unless the system somehow snuck another RK operation in
> there, but I don't see anything that could do that).

I finally get some time back in front of the machine, after a few days in bed with a cold:

>> ...put a HALT in the OS just after 4467 in Lions. Halt the machine momentarily, patch the kernel, and CONT.
>> (Basically the same as your patch to the trap vector, just a different address.) That'll be at 021320
>> (should contain 062706)...
> 
> But alas, it does not.  [PA:021320] = 010246.  Furthermore, [PA:015406] = 016504.
----
> I just tried under SIMH, also, and got consistent results:
> 
>     [PA:015406] = 016504
>     [PA:021320] = 010246
>
> ...so, one would think, my rkunix and yours are different?

Noel:

> That must be it. I thought we were both working from the V6 distribution? Oh, yours prints out that Western
> Electric copyright notice, I don't think mine has that...

### February 10

The first part of the day is spent sorting out and comparing the "Wellsch" V6 distribution that I have been
using, and the "Ritchie" version that Noel has been using.  Noel comes to the conclusion that the only
differences in the kernel sources are in fact the four `printfs` for the copyright notice, but this is enough
to perturb the locations of various symbols of interest between the two kernels.  He also finds the binaries
`ls`, `cc`, `as`, `as2`, `ld` `c0`, `c1`, and `c2` all match; as do liba.a, libc.a and crt0.o.

Getting back on the trail of the bug:

> So the first place I'd like to try HALTing is just after the call to swap, Lions 4467; at that point, the
> text should be in main memory, and also just written to disk. Should be at 021320 (old contents should be
> 062706).
> 
> Fun things to do here: look at the text in main memory (0161400 and up), see if it's correct at this point.
> Also: pull the arguments off the top of the stack, and write a small program to read it back in...

This turns out to be one last typo ("rkunix" vs. "rrkunix" on Noel's part) resulting in incorrect symbol
addresses for my kernel, but I'm hip to Noel's curveballs now so:

> Okay, using today's newly acquired 'db' skillz :-), in my rkunix, that spot is at PA:21420.  Firing up the
> machine again and trying that now...

It works; I end up stopped at the breakpoint and start extracting data:

> Hmmm:
> 
>     PA:161400: 141644 141660 000000 000000 000000 000000 000000 000000
>     PA:161420: 000000 000000 000000 000000 000000 000000 000000 000000

Noel:

> The text is probably at a different location in PA at this point. Read out UISA0 for its base.

Fritz:

>     UISA0: 001654
> 
>     PA:165400: 170011 010600 011046 005720 010066 000002 004767 000010
> 
>     KSP: 141656 -> PA:165256 
> 
>     PA:165256: 007656 001654 000104 000000 101602 066312 000000 141726
>     PA:175600: 110024 010400 000167 000016 010500 010605 101446 010346
>
> So far so good -- both beginning and eventually-bogus sections of text check out at this point!

Noel:

> Woo-Hoo!!!! YEAH!!!!
> 
> So that part of the text _is_ right at this point.
> 
> Needless to say, this is _very_, very important data.
> 
> So chances are very strong, at this point, that it's the RK11.
> 
> What did you want to do next? You could start with the RK11 registers. Also, use PDP11GUI to read the copy
> off the swap device, once I decipher the stack?
----
>     PA:165256: 007656 001654 000104 000000 101602 066312 000000 141726
> 
> OK, so the 01654 is the start address in PA (in clicks) for the area to swap out, and that matches UISA0.
> 0104 is the text length (also in clicks), and that also matches. The 0 is a flag which says it's a write
> (read is 01). And the 07656 is the block number (4014.).

Fritz:

> I should have a valid swap on the disk from before I shut down... Going to fire up PDP11GUI and grab it now
> to have a look. We want blocks 4014-4022, then? (9 x 512-byte blocks = 0110 clicks if I got that right?)

Noel:

> 4014.-4023., I think...
> 
>> (9 x 512-byte blocks = 0110 clicks if I got that right?)
> 
> I think 8-1/2 or so; text is 010400 bytes (a little less, actually, but that's what the system is using),
> 01000 bytes/block, = 010.4 blocks.

Fritz:

Hmm, the beginning looks good, but it seems to cut off to soon:

>     0000000    000000  000000  000000  000000  000000  000000  000000  000000
>     *
>     7656000    170011  010600  011046  005720  010066  000002  004767  000010
>     7656020    010016  004737  006374  104401  004567  010154  162706  000044
>     7656040    012716  000001  004737  004652  010067  022314  010516  062716
>     7656060    177762  004737  006346  016500  177762  062700  177413  010067
>        |
>     7660320    000137  002346  016516  000004  012746  020452  004737  003562
>     7660340    005726  000137  002542  005067  017552  012704  022336  005003
>     7660360    012716  021050  004737  005042  110024  005203  022703  000020
>     7660400    000000  000000  000000  000000  000000  000000  000000  000000
>     *
>     11410000

Noel:

>>     7656000    170011  010600  011046  005720  010066  000002  004767  000010
> 
> Yup, good start; SETD, etc.
> 
>>     7660360    012716  021050  004737  005042  110024  005203  022703  000020
>>     7660400    000000  000000  000000  000000  000000  000000  000000  000000
> 
> Hunh; not good. (Might be worth looking at that location in main memory, see if it's zeros or not.)
>
> That's so odd that it's all zeros - I wonder where they came from? Maybe they were already on the disk, and
> the write stopped way early? (At 01000 bytes per block, it stopped after 2-1/2 blocks; 056000s, 057000s,
> stopped half-way through the 060000's.)
> 
> Would be useful to have the RK register contents after the swap() call returns...

Fritz:

> Okay, the write should be from PA:165400 - PA:175777, to sectors 07656 - 07667.  Block 7667 encodes to an
> RKDA value of 012363.
> 
> After the halt, I find:
> 
>     RKDS: 004707 (OK)
>     RKER: 000000 (OK)
>     RKCS: 000322 (BOGUS! EX.MEM = 01)
>     RKWC: 000000 (OK)
>     RKBA: 176000 (OK)
>     RKDA: 012363 (OK)
> 
> So, EX.MEM are the smoking bits here!  I will review the associated designs and come up with things the
> try/check.
-----
> Okay, taking a look:
> 
> RKBA is implemented in the M795 module in slots AB07, as detailed on sheet RK11-C-15.  The M795 is a generic
> WC/BA Unibus interfacing module.  The BA part only covers 16 bits, but generates an overflow out "D15
> RKBA=ALL 1 L".
> 
> EX MEM 01 and EX MEM 02 are maintained on the M239 module in slot A17, as detailed on sheet RK11-C-03.  The
> M239 is a 3x 4-bit counter/register module, so this also implements counting up these bits, when triggered
> by "D15 RKBA = ALL 1 L".
> 
> Based on where we see the data on disk fall off (offset 2400) and the start PA (165400), I'm guessing we get
> a false trigger on this "ALL 1" at RKBA 167777.  So that looks like a false "1" detect on RKBA bit 12.
> 
> So I think the thing to do is to put the M795 out on an extender, load RKBA with 167777, and have a check at
> E28 pin 5, and E34 pin 8!
> 
> And we leave the cliffhanger there, for now, at least until tomorrow evening.  Because due to the way the
> RK11-C is mounted, in order to do the above I'm going to have to spin the whole machine around (its a dual
> H960), extend the RK05's so there is room to physically climb in the back, rig a work light, and get on in
> there...

### February 11

> SUCCESS!!
> 
> Put the M795 out on an extender, loaded 167777 in RKBAR, and had a look around with a logic probe.  Narrowed
> it down to E34 (a 7430 8-input NAND).  Pulled, socketed, replaced, and off she goes!
> 
> I can now successfully boot and run both V6 Unix and RSTS/E V06C from disk.
> 
> *THAT* was a really fun and rewarding hunt :-)  First message in the thread was back on Dec 30, 2018.  Lots
> of debugging and DRAM repairs, then the final long assault to this single, failed gate...
>
> Thanks to all here for the help and resources, and particular shout-outs for Noel and Paul who gave
> generously of their time and attention working through the densest bits, both on and off the list.
>
> I predict a long happy weekend and a big power bill at the end of the month :-)

<img style="display:block; margin-left:auto; margin-right:auto" src="/images/pdp11/M795.png" 
title="M795 WC/BAModule"/>
<p style="text-align: center;"><em>M795 module and the single failed gate</em></p>