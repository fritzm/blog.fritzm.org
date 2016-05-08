Title: PDP-11/45: Power Harness, continued
Date: 2016-4-23
Tags: Retro-Computing, PDP-11

Moved the power modules and partial harness back over to the racks today, got everything remounted, finished and
dressed the backplane end and completed the inter-H742 connections.

I did not do the runs for the backplane memory to the lower H742, as I do not have any of this.  I probably won't ever
have any, either: these options are specialized to the 11/45, are quite rare, and only cover part of the available
address space.  Additionally, I'd need to track down the details of a backplane ECO to do this part of the harness
correctly.  The core and MOS memory that I do have are all system-unit options.

Here are some pics of the in-rack wiring in progress, and a couple of the finished view of the harness.  If you add up
the capacity of the modules, you'll see that an 11/45 like mine, with floating point, is provisioned with +5V at 100
[sic] amps, and -15V at 20 amps.  That's no joke of a power supply...

[<img class='image-process-thumb' src='/images/pdp11/harness-progress.jpg'/>]({filename}/images/pdp11/harness-progress.jpg)
[<img class='image-process-thumb' src='/images/pdp11/harness-complete.jpg'/>]({filename}/images/pdp11/harness-complete.jpg)
[<img class='image-process-thumb' src='/images/pdp11/power-supplies.jpg'/>]({filename}/images/pdp11/power-supplies.jpg)
