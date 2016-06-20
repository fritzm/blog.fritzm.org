Title: PDP-11/45: CPU debug II
Date: 2016-6-5
Tags: Retro-Computing, PDP-11

Received and installed the replacement lamps for the -15V regulators.  Pic below shows what the power supply looks
like with all the lamps functioning.

Verified backplane DC voltages and ripple currents again, and re-trimmed all the DC regulators.  Verified AC LO and
DC LO de-asserted and free of glitches.  Found some harness wiring mistakes to the DD11 expansion backplane; corrected these.

Tried some CPU board-swaps looking for a quick win, but broken console behavior didn't change significantly with
different boards.

Investigated the timing generator board, and found that the crystal oscillator wasn't oscillating.  Tracked this down
to inductor L1 which looked as if it had been partially sheared away from the board at some point during installation/removal/storage.  Repaired this.  Success!  Able to load addresses from the front console now. Switches are mirrored
in the BR when halted in console.

Address bit 0 seems stuck.  Swapped PDR from spare board back to the original.  Can now examine and modify the
light/switch register, and examine the contents of the MR11 ROM.

Jumpered the DD11 expansion backplane back in, and slotted in the MS11-L memory.  Limited success: can modify and
examine memory for example near address 001000, but cannot modify low memory addresses.  In some ranges, can only
modify every other word.  Also, PC seems stuck at 022000.

At this point, I could really use a KM11 maintenance board set.  These are pretty hard to get a hold of, but a few
folks on the web have built their own reproductions.  I put in a PCB order to ExpressPCB with a KM11 layout by Tom
Uban (described [here](http://www.ubanproductions.com/museum.html)), and also put parts on order to stuff it.

Also, figuring I'll need to be going deeper into the CPU debug, I found and bought an
[HP1662A logic analyzer](http://www.ebay.com/itm/142004889393) on eBay, for about the same money as the KM11 PCB and
parts!

[<img class='image-process-thumb' src='/images/pdp11/power-lights.jpg'/>]({filename}/images/pdp11/power-lights.jpg)