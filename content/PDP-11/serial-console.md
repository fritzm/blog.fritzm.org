Title: PDP-11/45: Serial console and backplane SPC slots
Date: 2016-6-26
Tags: Retro-Computing, PDP-11

Hit a snag on the way to getting PDP11GUI hooked up: while the M9301 console emulator was working fine with the VT52,
I could not get serial communication to my laptop (MacBook Pro + Keyspan USA-19HS USB serial) to work as expected.  Some
detective work showed that the voltages from the EIA output drivers on the DL11 were way out of whack (+3V for mark,
which should have been a negative voltage).  Somehow the VT52 was able to still make sense out of this signaling,
though the laptop was not.

Some investigation of power to the DL11, which was sitting in one of the backplane SPC slots (26-28), showed that there
was no distribution of +15V to pin CU1 of these slots where the DL11 was expecting it.  So that explained the bad
driver output voltages.  Moved the DL11 over to the DD11 expansion backplane which does have +15V to that pin, and
serial to/from the laptop started working fine.

So this raises a bit of a question about the SPC slots on the 11/45 backplane.  Was EIA console serial from these slots
ever supported?  The configurations listed in the 11/45 engineering prints call out only DL11-A, the 20mA current
loop version, which doesn't have EIA drivers and thus doesn't need the +15V supply, so maybe not.  Was +15V distribution
perhaps added to these slots in subsequent revisions or via an ECO?  I'd like to track down a wire list for this or
later revision 11/45 backplanes, and/or a comprehensive list of KB11-A ECOs, but so far haven't seen traces of either
anywhere out there.

One other curiosity of these SPC slots that came up while investigating this: the power distribution table in
the 11/45 maintenance manual, EK-11045-MM-007, page 510, implies that +15V should be distributed to the SPC slots on
CA1.  This is suspicious to me (maybe a typo?) because all other SPC pinouts that I have seen use this pin and CB1
as NPR in/out.  And in checking my backplane, there is no power distribution to those pins.  But slots 27 and 28
(Unibus B) do have their CA1 pins bridged to one another, and their CB1 pins bridged to one another, with what look like
factory installed wire wraps.  This also seems unusual for NPR/NPG.  So, some mysteries remain about these slots...

In other news, the clock oscillator on the VT52 has given out, so that's down now until I can find a replacement.  They
are out of production and aren't easy to track down, but I do have one lead to follow so far.

Also, I pulled the suspected failed subsidiary ALU control ROM, tested it in isolation, and verified that it had indeed
failed.  This card is just a spare for me, but I'd like to go ahead and repair it since the fault is isolated.  With
some help from the classiccmp mailing list (thanks guys!) I have a recommendation for some vintage PROM programmers to
stalk on eBay, and some compatible parts, that would allow me to blow a replacement and make the repair.
