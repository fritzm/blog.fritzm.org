Title: PDP-11/45: VT52 repair
Date: 2016-7-16
Tags: Retro-Computing, PDP-11

Replacement oscillator arrived for the VT52, so spent some time getting it back going again.  Things got *much* better
with a stable timing chain, but some glitchiness remained -- tracked this down to the socketed microcode ROMS which
just required a reseat.

Here you can see the new oscillator fitted (silver rectangular can with tie-wrap).  The microcode ROMS are the four
socketed chips towards the right in the picture.  Interestingly, the schematic I have calls for 8 ROMS of half the size
of the ones that are in here, and indeed you can see the unpopulated spaces for these on the board.

[<img src='/images/pdp11/vt52-repair_thumbnail_tall.jpg'/>]({filename}/images/pdp11/vt52-repair.jpg)
