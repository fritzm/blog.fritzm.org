Title: Apple II Plus: power supply and language card
Date: 2022-3-21
Tags: Retro-Computing

Okay, so the Apple II Plus I was using to test the VM4209 monitor worked fine for about a half hour, then
smoked a RIFA cap in its power supply.  These are a very common known failure in various old microcomputer
power supplies, and I really should have already caught this on inspection and shotgunned it.  Boy, do they
generate a lot of smoke and stink when they go...

Electrolytics in here are also all pushing 40 years at this point and Astec opted for only 85C parts for many
of these, so I went ahead and ordered a [whole replacement
kit](https://console5.com/store/apple-2-power-supply-cap-kit-p-n-605-5703-astec-aa11040b-aa11040-b.html) from
Console5.  I replaced the front end filters and anything on the back end that was 85C or looked even slightly
bulgy, which ended up being most of them:

[pswipe:micros,apple-ii-rifa.jpeg,Blown RIFA capacitor from Apple II Plus power supply]
[pswipe:micros,apple-ii-pwr-before.jpeg,Apple II Plus power supply before cap replacements]
[pswipe:micros,apple-ii-pwr-after.jpeg,Apple II Plus power supply after cap replacements]

Put it all back together and back in business, except noticed an additional problem: DOS 3.3 booted but
neither recognized nor loaded the "language card" (soft ROM) present in the machine.  Since my machine has
Applesoft BASIC in system ROM, this meant no Integer BASIC (and no ROM mini-assembler) for me until this was
fixed.

For those who might not be familiar with the Apple II language card, it provides several features.  An Apple
II or II Plus can have at most 48K of RAM on the system board.  The overall memory map looks like this:

<style>
.memmap {
  font-family: monospace;
  width: 30em;
  margin-left: auto;
  margin-right: auto;
  margin-top: 1rem;
  margin-bottom: 2rem;
  border-collapse: true; 
}
.memmap td {
  border: 1px solid black;
  padding: .5em;
  text-align: center;
}
</style>

<table class="memmap">
  <tr><td>$0000-$BFFF</td><td>RAM (48K)</td></tr>
  <tr><td>$C000-$CFFF</td><td>IO space (4K)</td></tr>
  <tr><td>$D000-$FFFF</td><td>ROM (12K)</td></tr>
</table>

The first thing the language card provides is a 2K ROM which by default overlays whatever ROM is in the system
board socket for addresses `$F800` to `$FFFF`. This ROM holds the 6502 reset vector and the boot monitor; the
version provided on the language card has an "autostart" capability that will search for and boot off an
attached Disk II floppy.  I am not sure why Apple provided this ROM on the language card since the same ROM
could be upgraded directly on the fully-socketed system board, and indeed everything after the Apple II Plus
came with this autostart ROM pre-installed. Possibly this was done for maximum backward compatibility with
Apple's previously-offered "Firmware Card", which also contained this ROM?  Third-parties would later offer
clones of the language card that did _not_ contain the additional/redundant F8 ROM, and nobody seems to have
particularly cared or noticed...

The second thing the language card provides is an additional 16K of RAM.  This can be loaded, then
write-protected and mapped over the entire ROM space of the machine from `$D000` to `$FFFF`, providing a "soft
ROM" capability.  Since the available ROM address space is only 12K, the leftover 4K or RAM on the language
card is bank switchable at address range `$D000` to `$DFFF`.

Advanced software which doesn't depend on the system ROMs at all can also map the RAM over the system ROM
address space and leave it in read/write mode, thus gaining access to a full 64K of RAM (with the caveat of
the switched bank at `$D000`.)

The language card programming interface presents as follows:

<br><img style="display:block; margin-left:auto; margin-right:auto" src="/images/micros/apple-ii-lang-controls.png" title="Apple II language card control codes"/><br>

My goal is to be able to run the initial (1980) release of Apple DOS 3.3. This version loads up the language
card at boot in soft ROM mode with Integer BASIC and an older version of the F8 monitor ROM, which contains a
few extra niceties like a built in mini-assembler and primitive step/trace capabilities.  A system so loaded
can then be conveniently switched back and forth between BASIC and monitor versions with the DOS "INT" and
"FP" commands.  But detection of my language card seemed to be failing, so it was never loaded up at boot.
Attempts to manually load and activate it also came to naught.

So, time to dig in and see what's going wrong... DOS 3.3 does initial checks and setup of the language card
via a small machine language program, loaded into RAM at boot by the DOS master disk's `HELLO` BASIC program.
Machine code is used for this part rather than BASIC so the probe/setup code can be placed and run from RAM
outside the mapping range of the language card (the BASIC interpreter itself running from ROM addresses
_within_ this mapping range). Here is the machine language program, after being `POKE`d into RAM by `HELLO`,
listed via the ROM monitor:

<div style="text-align: center"><img style="display:inline-block" src="/images/micros/dos33-hello-1.jpeg"
title="DOS 3.3 language probe, part 1/2"/> <img style="display:inline-block"
src="/images/micros/dos33-hello-2.jpeg" title="DOS 3.3 language probe, part 2/2"/></div>

I interpret the actions of this code as follows:

* The code first retrieves and stashes the contents of location `$E000`, within the mappable address range. A
  read of `$C081` then maps the ROMs on the system board (see programming interface above), and the contents
  of `$E000` are checked again.  If the contents now differ, the code assumes the card, now in mapped ROM
  mode, was previously in mapped RAM mode, and it jumps to address `$0332` to put things back the way it found
  them and bail out.

* If not, the code reads from address `$C083` twice, which puts the card, if present, in writable mapped RAM
  mode.  Two different values are written to and compared back from location `$D000`.  If a language card is
  _not_ present, this location will still be mapped to ROM on the system board, and at least one of these
  compares will fail; if either one does, the code jumps to `$0332` to bail out.

* Otherwise, we've verified that a card is present and wasn't already in active play.  The program now reads
  from address `$C081` twice to move back to mapped ROM mode, but leaving RAM writable to be loaded by the
  remainder of the `HELLO` program after return (in this mode, reads will come from system ROMs, but writes
  will go to the corresponding locations in language card RAM). A success return code is loaded, and the code
  jumps forward to the exit code at `$0334` to return to the caller.

* The bail out routine at `$0332` just sets up a fail return code, then falls through to `$0334`.  Code here
  stores the return code to the return code location and does one last compare between the stashed and current
  values at `$E000` to determine if mapped RAM mode must be restored; if so this is done via a read from
  location `$C080` (RAM is left write-protected).  Control is then returned to BASIC.

In any case, the above is what the code _does_, even if I may have misinterpreted some of its motivations.  On
my system, the ROM on the language card seemed to be working correctly (monitor ran fine, but if ROM on
language card was pulled the machine failed to boot, indicating the monitor was in fact running successfully
out of ROM on the card). However, mapped RAM mode seemed never to engage.  The machine code snippet above
returned "00" without crashing, and the DOS `HELLO` program assumed no card present.  Manually accessing the
appropriate control registers also had no effect.

The language card design does not seem to be documented in detail, but a schematic is available and it is not
too hard to suss out.  The first thing to check would seem to be the register interface.  Here is an excerpt
from the schematic, with a couple of annotations added:

<br><img style="display:block; margin-left:auto; margin-right:auto" src="/images/micros/apple-ii-lang-schem.png" title="Apple II language card schematic excerpt"/><br>

The register interface is principally implemented by a 74LS175 quad flip-flop at D4.  These flip-flops share a
common reset at power-on, and a common clock based on the expansion slot DEV_L signal; DEV_L is a
slot-specific signal strobed by the system on any bus cycles to IO address space allocated to that slot.
Examination of the programming interface along with address line decodes feeding the D inputs here leads to
the conclusion that the top-most flip-flop holds RAM/ROM mapping mode, the next one down is RAM bank select,
the next is RAM write-enable, and the last is a one-bit count to support write-enable after only two
successive reads.

Put a chipclip on at D4, and observed behavior of the flip-flops on the logic analyzer while exercising the
control registers via the monitor.  Problems were apparent right away: while the bank select and count
flip-flops were responding as expected, the mapping mode and wite-enable flip-flops were not.  The shared
reset and clock appeared correct, and all flip-flops themselves were responding logically correctly with
respect to their inputs.  The issue was apparently with the incoming D lines to two of the flip-flops.
Starting with the ROM/RAM enable flip-flop, then, that D line is fed via C3 and C4.  And a visual inspection
in preparation for clipping these up for the analyzer revealed that, surprisingly, these two chips had
actually been reversed on the board!

The language card is fully socketed, so presumeably this reversal had occured during previous troubleshooting
or service by the former owner?  In any case, it was easy to swap the chips back to their correct locations,
and the logic analyzer showed that the entire register interface seemed to be behaving according to design
after that.  DOS 3.3 now recognized the card at boot (yay!), but the system would crash after loading and
mapping the RAM.  So, maybe a bad RAM chip as well?

To troubleshoot the RAM, I followed a technique described in [this
video](https://www.youtube.com/watch?v=wVUWaodwNNI&t=1309s) on the "Adrian's Digital Basement" YouTube
channel.  Basically, a couple short machine language programs, entered and executed via the monitor, to copy
ROM contents into the language card RAM, then copy back out to another location in system RAM.  This allows a
comparison of source data in ROM and round-tripped data in system RAM; a mismatch indicates a RAM problem on
the card.  Here are the two programs I used and, and dumps of the resulting data:

<div style="text-align: center">
  <img style="display:inline-block" src="/images/micros/apple-ii-copy-in.jpeg" title="Copy ROM to language card RAM"/>
  <img style="display:inline-block" src="/images/micros/apple-ii-copy-out.jpeg" title="Copy language card RAM to system RAM"/>
  <img style="display:inline-block" src="/images/micros/apple-ii-data-comp.jpeg" title="ROM data vs round-trip language card data"/>
</div>

And sure enough, it's quite visible here that bit 7 is having problems.  Swapped out the 4116 at A2, and
that seems to have done it for this one.  Now I need to go find a copy of Choplifter...

[pswipe:micros,apple-ii-lang-card.jpeg,Apple II Plus language card repairs: yellow indicates two chips that were found swapped on the card; red indicates a failed 4116 RAM chip that was replaced.]
[pswipe:micros,apple-ii-repaired.jpeg,Apple II Plus: Successful DOS 3.3 boot after language card repairs]
