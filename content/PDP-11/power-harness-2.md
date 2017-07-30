Title: PDP-11/45: Power Harness, continued
Date: 2016-4-23
Tags: Retro-Computing, PDP-11

Moved the power modules and partial harness back over to the racks today, got everything remounted, finished and
dressed the backplane terminations, and completed the inter-H742 connections.

I did not do the runs for the backplane memory to the lower H742, as I do not have any backplane memory.  I probably
won't ever have any, either: these memory options are specialized to the 11/45, are quite rare, and only cover part of
the available address space.  Additionally, they would require me to track down the details of a backplane ECO to do
the corresponding parts of the harness correctly.  The core and MOS memory that I do actually have are all system-unit
options anyway.

Here are some pics of the in-rack wiring in progress, and a couple views of the finished harness.  If you add up
the capacity of the DC modules, you'll see that an 11/45 like mine (with floating point) is provisioned with +5V at 100
[sic] amps, and -15V at 20 amps.  That's no joke of a power supply...

[pswipe:pdp11,harness-progress.jpg,Finishing up the replacement power harness in the rack]
[pswipe:pdp11,harness-complete.jpg,Completed power harness from above rear]
[pswipe:pdp11,power-supplies.jpg,Completed power harness from side]
