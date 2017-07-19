Title: PDP-11/45: Power fixes and CPU debug
Date: 2016-5-30
Tags: Retro-Computing, PDP-11

Connected up the aforementioned red wire hack to the new power harness, and verified +5V to slots 10 through 15.
Console is no longer all address and data lights on, but basic console load address / examine / deposit operations are
still not working.  A random assortment of address lines seem stuck, different on each power cycle.  About the only
thing that reliably functions from the console is loading the two highest address bits from the switches, immediately
after a reset.  Pulled the floating point unit, un-jumpered the DD11 expansion backplane, and removed all peripherals
except the M792 diode ROM; same (broken) behavior...

Scoped all the DC voltages, and did not notice any glitches.  Pulled the H742s for some bench work: verified AC LO and
DC LO signaling on both units, replaced a broken Mate-n-Lok connector on one of the units, blew out dust from all the 5V
regulators and replaced their indicator bulbs with modern equivalent (CM7381). Sourced and put on order a modern
equivalent (OL-6003BP) for the indicator bulbs on the -15V regulators.

Next steps will be to verify various Unibus signals on the backplane, then maybe play some swap games with CPU card
spares to see if I can get closer to a working console as a starting point.  All I have time for this weekend, though;
sorry nothing new to see so no new pictures this time!
