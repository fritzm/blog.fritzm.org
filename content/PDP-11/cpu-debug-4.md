Title: PDP-11/45: MS11-L and CPU debug IV
Date: 2016-6-12
Tags: Retro-Computing, PDP-11

Made some progress on the inverted result after register-to-register move problem: with the help of the KM11, extender
card, and a logic probe I was able to track down that signal ALUM L coming onto the DAP is not asserted when it should
be for a MOV instruction.  This means the ALU is performing in arithmetic instead of logic mode and thus the incorrect
result.

I next moved the extender card over to GRA, where this signal originates from a subsidiary ROM, but unfortunately at
that point the MS11-L memory behavior got even worse, putting and end to these experiments.  So I'll have to tackle
that first...

Moved the MR11 ROM over to the expansion backplane where the MS11-L resides, and it works fine there.  So it doesn't
seem to be a bus wiring or jumper problem onto the expansion backplane.  Checked the power input pins on the backplane
behind the MS11-L.  5V was a little low there; trimmed this up.  Probably need to clean or replace the Molex contacts
on the power distribution board in the cabinet, as it seems a few mV are being shed there needlessly compared to the
output of the same regulator on the main backplane, but things seem within stated tolerances for now.

The -15V input to the MS11-L was missing entirely.  Removed the DD11 expansion backplane, and added jumpers between
the battery backup supply inputs and the corresponding main supply inputs, per documentation.  Now have -15 to the
MS11-L, but still no joy.

Will need to go deeper into the MS11-L next time...