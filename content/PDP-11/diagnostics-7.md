Title: PDP-11/45: Diagnostics VII - KT11 MMU
Date: 2016-8-13
Tags: Retro-Computing, PDP-11

Moving on to the KT11 MMU: running the first diagnostic in the CKT suite, got error reports at 010340, 010560, and
011000.  Consulted the diagnostic listings, and these particular tests have to do with D-space translations from
kernel, supervisor, and user modes.  The D-space logic is largely on module SSR, so I swapped this out for a spare.
After that, I was able to pass the full suite of basic MMU tests:

<style>
.diaglist { display: inline; border-collapse: collapse; margin-right: 1em; }
.diaglist caption { font-weight: bold; }
.diaglist tr:nth-child(even) { background-color: #f2f2f2; }
.diaglist th, .diaglist td { padding: 5px; }
.diaglist td { border: 1px solid lightgray; font-family: Menlo,Consolas,monospace; }
</style>

<table class="diaglist">
<thead>
<tr><th>Diagnostic</th><th>BEL</th><th>Description</th><th>Status</th></tr>
</thead>
<tbody>
<tr><td>CKTAB0.BIC</td><td>017412</td><td>KT11-C basic logic part 1</td><td>pass</td></tr>
<tr><td>CKTBC0.BIC</td><td>015674</td><td>KT11-C basic logic part 2</td><td>pass</td></tr>
<tr><td>CKTCA0.BIC</td><td>023304</td><td>KT11-C access keys</td><td>pass</td></tr>
<tr><td>CKTDA0.BIC</td><td>016360</td><td>KT11-C MTPD and MTPI</td><td>pass</td></tr>
<tr><td>CKTEB0.BIC</td><td>015310</td><td>KT11-C MFPD and MFPI</td><td>pass</td></tr>
<tr><td>CKTFD0.BIC</td><td>016422</td><td>KT11-C aborts</td><td>pass</td></tr>
</tbody>
</table>

Put the failing SSE module in the repair queue along with the other failed spares I've identified along the way, and
will return to troubleshoot/repair it later.  For now, things are looking pretty good with the CPU!  I still need to
run and pass the more heavyweight diagnostics: the 11/45 instruction exerciser, KT11 exerciser, and MS11-L exerciser.
All three of these still seem to have halts, but they are quite complicated diagnostics in comparison to the rest,
making use of additional peripherals, etc.  I'll need to study these a bit before I can be sure I am using them
correctly.  I have also skipped the power fail diagnostics for now as I will need to restore some core memory in order
for these to work correctly.

Next up will be to work on the FPU...
