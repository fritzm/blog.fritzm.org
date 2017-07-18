Title: PDP-11/45: CPU debug VI - RK11 NPRs and first disk boot!
Date: 2017-5-14
Tags: Retro-Computing, PDP-11

Took a little of time to sort through BC11 cables to find a good one for drive interfacing, but in the end I
found one that worked okay and got the seek tester code from the previous post working reliably.  At this
point I mounted one of the recently cleaned RK05 packs, but found that the M9301 bootstrap would hang the bus
on the first read operation.

A little scoping around on the RK11-C showed that it was asserting NPR to the processor, but never receiving
NPG.  A quick check of NPG continuity on the backplane showed a missing jumper on one slot of my DD11-D.
Wrapped this on, verified NPG continuity all the way out to the RK11, but still no joy.  Turns out the CPU
is not asserting NPG at all.

Threw the CPU UBC card out on extenders and had a go at chasing though the NPG logic with a logic probe.
Turns out to be a failed 8881 bus driver for NPG at the end of the line (E55 on KB11-A drawing UBCD). Pulled,
socketed, replaced.

After this, the CPU was asserting NPG, but the signaling still looked a little squirrelly.  Turns out that
there are jumpers (W1-W5) on the M9301 bootstrap terminator that need to be installed to provide grant
pull-ups when they are not otherwise provided internally by the processor (and the 11/45 is one such
case).  After installing the jumpers, NPG signaling looked solid.

Tried mounting a booting a few packs.  Packs marked as having RT-11 would run for a short while and then hang.
But an RKDP pack _successfully booted!_  Wow, that feels pretty good after about two years of working
seriously on this restoration.  :-)

Going to stop here on a high note, and pick up trying to get a good RT-11 boot next time.

[<img src='/images/pdp11/rkdp-boot_thumbnail_tall.jpg'/>]({filename}/images/pdp11/rkdp-boot.jpg)
