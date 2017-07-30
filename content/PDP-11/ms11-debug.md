Title: PDP-11/45: MS11-L debug
Date: 2016-6-18
Tags: Retro-Computing, PDP-11

After addressing the -15V problem on the MS11, most of the bad behaviors seem to have cleared up except a stuck (on)
bit 6 in the first 16K words of address space (000000-077776).  Hooked up the new logic analyzer, and it has been very
useful in troubleshooting the board -- can easily capture and inspect the timing of complete memory cycles.  Definitely
worth the investment!

Using the analyzer, I was able to verify the refresh and chip select logic on the board, then track down the stuck bit
to what seems to be a single failed DRAM chip (E96 on the MS11-L engineering drawings).  I'd like to test the entire
card before ordering replacement parts, but need to set up address translation to get beyond the first two banks from
the console.

Here is the address translation register setup that I used for testing.  This was followed by a deposit of 000001 to
KT11 SR0 (777572) to enable translation.  KT11 SR3 was left all zeros to keep D space disabled.  This setup allows
console access to physical addresses in banks 1 through 7 by appropriate settings of virtual address bits 13 through
15.  I wanted to reserve PAR7 to map I/O space, so I left out bank 0 since it was one of the two already tested.

<style>
.memlist { display: inline; border-collapse: collapse; margin-right: 1em; }
.memlist caption { font-weight: bold; }
.memlist tr:nth-child(even) { background-color: #f2f2f2; }
.memlist th, .memlist td { padding: 5px; }
.memlist td { border: 1px solid lightgray; font-family: Menlo,Consolas,monospace; }
</style>

<table class="memlist">
<caption>Kernel I PAR</caption>
<tbody>
<tr><td>772340</td><td>001000</td></tr>
<tr><td>772342</td><td>002000</td></tr>
<tr><td>772344</td><td>003000</td></tr>
<tr><td>772346</td><td>004000</td></tr>
<tr><td>772350</td><td>005000</td></tr>
<tr><td>772352</td><td>006000</td></tr>
<tr><td>772354</td><td>007000</td></tr>
<tr><td>772356</td><td>007600</td></tr>
</tbody>
</table>

<table class="memlist">
<caption>Kernel I PDR</caption>
<tbody>
<tr><td>772300</td><td>077406</td></tr>
<tr><td>772302</td><td>077406</td></tr>
<tr><td>772304</td><td>077406</td></tr>
<tr><td>772306</td><td>077406</td></tr>
<tr><td>772310</td><td>077406</td></tr>
<tr><td>772312</td><td>077406</td></tr>
<tr><td>772314</td><td>077406</td></tr>
<tr><td>772316</td><td>077406</td></tr>
</tbody>
</table>

This worked as expected according to panel PROG PHY and the logic analyzer, so the KT11 option which I had not
previously tested is at least working for kernel I space.  Tested each bank on the MS11 from the front panel using this
setup, and uncovered that bank 4 bit 10 also has a stuck on condition.  Since bank 1 is working now, I can use that
as work space for the time being in order to continue the CPU debug while awaiting some replacement DRAM chips in the
mail.

Pics here of the logic analyzer setup, and captured traces of a write and subsequent read to one of the misbehaving
chips:

[pswipe:pdp11,ms11-debug.jpg,MS11 memory card debug in progress, with board extender, logic analyzer, and KM11]
[<img src='/images/pdp11/bad-dram-write_thumbnail_tall.jpg'/>]({filename}/images/pdp11/bad-dram-write.jpg)
[<img src='/images/pdp11/bad-dram-read_thumbnail_tall.jpg'/>]({filename}/images/pdp11/bad-dram-read.jpg)
