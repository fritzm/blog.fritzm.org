Title: PDP-11/45: Initial Power On!
Summary: Hold breath; turn key...
Date: 2016-5-8
Tags: Retro-Computing, PDP-11

Beeped out the new harness to check for shorts or incorrect pins, then plugged in just the H742s and fired it
up.  All the DC regulator modules seem to be working, and I was able to trim them up to nominal voltages at
the CPU end of the harness.  The indicator lamps on all but one of the DC regulators seem to be burned out,
though, so I put some new lamps on order (at last for the +5V regulators; a modern equivalent for the -15V
regulators is tougher to find).

Given that success, I plugged in the CPU side of the harness, took a deep breath, and powered on!  Hmmm.  No
detonations or smoke, but all data/address/mode lights lit (see below), which is not right...  Front panel
lamp test and data address mode switches and indicators are working though at least.

Some investigation on the backplane turned up no +5V to slots 10 though 15, which could be part of the
problem.  Ah, that's what the mysterious clipped red wire soldered to the backplane might have been about
(visible in the top right [here]({static}/images/pdp11/kb11a-backplane.jpg)...)  Sure enough, some inspection
shows the corresponding trace on the backplane looks burnt!  I could hack this red wire into my new harness I
guess, but I'd rather remove it and try to repair the board trace with a shunt.  So the backplane will have to
come out.  I guess that's what I get for not investigating the weird red wire and for not beeping out the
power distribution on the backplane before mounting and populating it...

[pswipe:pdp11,initial-power-on.jpg,Initial power on!  No smoke, but all lights on (not right).  Well, it&#39;s a start!]
