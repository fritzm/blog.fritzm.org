Title: PDP-11/45: Diagnostics with PDP11GUI
Date: 2016-7-3
Tags: Retro-Computing, PDP-11

Okay, now that serial is straightened out, on to running diagnostic tests via PDP11GUI.  PDP11GUI itself, as well as
a thorough and useful database of DEC diagnostic programs, are available at [http://www.retrocmp.com/tools](http://www.retrocmp.com/tools).

Since my home computer is a MacBook, I had intended to run PDP11GUI under Wine.  I ran into a problem with this where
PDP11GUI under Wine could not generate its pre-processed machine description temp file, seemingly because of some
incompatible behavior wrt. multiple backslashes in pathnames.  Rather than fight with this too long, I just sprang for
a Windows 10 license and installed a Windows 10 VM; it will come in handy for other Windows-only tools that have
been tweaky to use under Wine as well.

With PDP11GUI up and running under Windows, results of the initial set of 11/45 CPU diagnostics were very encouraging!
In summary:

<style>
.diaglist { display: inline; border-collapse: collapse; margin-right: 1em; }
.diaglist caption { font-weight: bold; }
.diaglist tr:nth-child(even) { background-color: #f2f2f2; }
.diaglist th, .diaglist td { padding: 5px; }
.diaglist td { border: 1px solid lightgray; font-family: "Courier", monospace; }
</style>

<table class="diaglist">
<thead>
<tr><th>Diagnostic</th><th>BEL</th><th>Description</th><th>Status</th></tr>
</thead>
<tbody>
<tr><td>CKBAB0.BIC</td><td>002562</td><td>SXT instruction</td><td>pass</td></tr>
<tr><td>CKBBB0.BIC</td><td>003604</td><td>SOB instruction</td><td>pass</td></tr>
<tr><td>CKBCB0.BIC</td><td>007410</td><td>XOR instruction</td><td>pass</td></tr>
<tr><td>CKBDC0.BIC</td><td>007262</td><td>MARK instruction</td><td>pass</td></tr>
<tr><td>CKBEC0.BIC</td><td>002212</td><td>RTI/RTT instructions</td><td>pass</td></tr>
<tr><td>CKBFD0.BIC</td><td>002272</td><td>stack limit</td><td>pass</td></tr>
<tr><td>CKBGB0.BIC</td><td>001446</td><td>SPL instruction</td><td>halt 001404</td></tr>
<tr><td>CKBHB0.BIC</td><td>003762</td><td>11/45 registers</td><td>pass</td></tr>
<tr><td>CKBIB0.BIC</td><td>013746</td><td>ASH instruction</td><td>pass</td></tr>
<tr><td>CKBJA0.BIC</td><td>014722</td><td>ASHC instruction</td><td>pass</td></tr>
<tr><td>CKBKA0.BIC</td><td>014430</td><td>MUL instruction</td><td>pass</td></tr>
<tr><td>CKBLA0.BIC</td><td>011574</td><td>DIV instruction</td><td>pass</td></tr>
<tr><td>CKBME0.BIC</td><td>016000</td><td>11/45 traps</td><td>halt 005320</td></tr>
<tr><td>CKBNC0.BIC</td><td>004702</td><td>PIRQ instruction</td><td>pass</td></tr>
<tr><td>CKBOA0.BIC</td><td>013640</td><td>11/45 states</td><td>halt 000610</td></tr>
</tbody>
</table>

Note that these tests are written to output an ASCII BEL to the console on each successful pass.  The terminal
built in to PDP11GUI doesn't sound when given a BEL, however, so it is convenient to patch the BEL literal in the
programs to a visible character (e.g. 000052, ASCII '*') before running them.  This may be done in the memory loader
window in PDP11GUI after "Load" but before "Deposit all".  The patch address I identified for each diagnostic is
listed in the table above as well for convenience.

So, out of this initial set of tests, only three halts to investigate.  I'll be posting more information here as I look
further into these.

Regarding the backplane SPC issue discussed in the previous post: Marty from the vcfed.org forum did some investigation
of his 11/45, and reports that he does have +15V (actually +12V on his system) distributed to pin CU1 on slots
26-28.  It seems to be wired over from slot 15 on his system, but it is not clear whether this was a factory wire,
an ECO, or a user mod.

Marty's 11/45 also has no power distributed to CA1 on this slots, so it's really looking to me like the reference
to that on page 510 of the 11/45 maintenance manual is a misprint.  Thanks to Marty for checking all this out!  I'd be
curious to hear from any other 11/45 owners out there regarding wiring of CU1 and CA1 on slots 26-28 in their systems.

[<img src='/images/pdp11/pdp11gui_thumbnail_tall.jpg'/>]({filename}/images/pdp11/pdp11gui.jpg)
