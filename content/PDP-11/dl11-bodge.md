Title: PDP-11/45: Reversing a vintage DL11 hack
Date: 2020-11-27
Tags: Retro-Computing, PDP-11

I recently had need to assess and repair several DL11 serial interfaces in my stock of spares. One of these
had had some sort of end-user hack applied; in the course of putting the board back to factory condition, I
did some analysis of the hack and its intended purpose, documented here.

[pswipe:pdp11,dl11-user-hack.jpg,DL11 with end-user hack]
[pswipe:pdp11,dl11-hack-front.png,DL11 user hack front]
[pswipe:pdp11,dl11-hack-back.png,DL11 user hack back]

Easy enough to beep this out and reverse to a schematic:

<img style="display:block; margin-left:auto; margin-right:auto" src="/images/pdp11/dl11-hack-schem.png" 
title="Schematic of DL11 hack"/>

So, the hack appears to dynamically alter the CSR address and interrupt vector of the card, choosing between
two hard-wired presets, based on whether P1A/P1B are connected together or not.

The CSR jumpers on a stock DL11 operate with pull-ups upstream of the address decode logic, so these can be
directly driven by the hack so long as the jumpers for the bits-to-be-hacked are left open on the board.  The
vector address bits, however, must be driven by the DL11 onto to the Unibus contingent on an appropriate
global enable. On a stock DL11, drivers for _all_ configurable vector bits are activated by a single global
enable, and jumpers downstream of the drivers control which of these activated bits will be admitted to bus.
So, for the vector address part of the hack to function, hack control must be asserted instead of the global
enable for each of the to-be-driven bits, and the corresponding jumpers for these bits must be left in.  And
indeed, upon inspection of the DL11 there are trace cuts that have been done (marked here with "X") to lift
the global enable and allow individual hack control of each of the affected bits:

<img style="display:block; margin-left:auto; margin-right:auto" src="/images/pdp11/dl11-hack-cuts.png" 
title="Trace cuts for DL11 hack"/>

</br>

Last, we can look at the board jumpering and the wiring of the hack to determine the specific CSR and
vector addresses at play:

<style>
.bitlist { border-collapse: collapse; margin-left: auto; margin-right: auto; margin-bottom: 2ex; }
.bitlist caption { font-weight: bold; }
.bitlist .hacked { font-weight: bold; }
.bitlist tr:nth-child(even) :not(th) { background-color: #f2f2f2; }
.bitlist td:nth-child(3n+2) { border-left-color: #000000; }
.bitlist td:nth-child(3n+1) { border-right-color: #000000; }
.bitlist th, .bitlist td { padding: 5px; }
.bitlist td { border: 1px solid lightgray; font-family: Menlo,Consolas,monospace; }
.bitlist tr:first-child td { border-top-color: #000000; }
.bitlist tr:last-child td { border-bottom-color: #000000; }
</style>

<table class="bitlist">
<thead><tr>
    <th></th>
    <th>A11</th><th>A10</th><th>A9</th>
    <th>A8</th><th>A7</th><th>A6</th>
    <th>A5</th><th>A4</th><th>A3</th>
    <th>A2</th><th>A1</th><th>A0</th>
    <th></th>
</tr></thead>
<tbody><tr>
    <th>P1 Open</th>
    <td>1</td>
    <td>1</td>
    <td class="hacked">0</td>
    <td>1</td>
    <td>0</td>
    <td>1</td>
    <td class="hacked">0</td>
    <td class="hacked">0</td>
    <td class="hacked">1</td>
    <td>0</td>
    <td>0</td>
    <td>0</td>
    <th>776510</th>
</tr><tr>
    <th>P1 Closed</th>
    <td>1</td>
    <td>1</td>
    <td class="hacked">1</td>
    <td>1</td>
    <td>0</td>
    <td>1</td>
    <td class="hacked">1</td>
    <td class="hacked">1</td>
    <td class="hacked">0</td>
    <td>0</td>
    <td>0</td>
    <td>0</td>
    <th>777560</th>
</tr></tbody>
</table>

<table class="bitlist">
<thead><tr>
    <th></th>
    <th>V8</th><th>V7</th><th>V6</th>
    <th>V5</th><th>V4</th><th>V3</th>
    <th>V2</th><th>V1</th><th>V0</th>
    <th></th>
</tr></thead>
<tbody><tr>
    <th>P1 Open</th>
    <td>0</td>
    <td class="hacked">1</td>
    <td class="hacked">1</td>
    <td class="hacked">0</td>
    <td class="hacked">0</td>
    <td class="hacked">1</td>
    <td>0</td>
    <td>0</td>
    <td>0</td>
    <th>310</th>
</tr><tr>
    <th>P1 Closed</th>
    <td>0</td>
    <td class="hacked">0</td>
    <td class="hacked">0</td>
    <td class="hacked">1</td>
    <td class="hacked">1</td>
    <td class="hacked">0</td>
    <td>0</td>
    <td>0</td>
    <td>0</td>
    <th>060</th>
</tr></tbody>
</table>

<br/>

We see from these specific addresses that closing the contacts of P1 would dynamically re-jumper the board
from assignment as the 2nd non-console interface to assignment as the console interface.  So perhaps this was
once used (in conjunction with another similarly hacked interface?) to swap console terminals with the flip of
a single switch.
