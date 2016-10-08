Title: PDP-11/45: Diagnostics X - FP11 FPU, cont.
Date: 2016-10-1
Tags: Retro-Computing, PDP-11

Okay, here's the dig in on the FP11 STST diagnostic failure.  As detailed previously, I'd been seeing an
incorrect FEC after executing a small test program to generate a minus-zero condition.  I'd verified that
the microcode sequence was per expectation, and that the correct FEC was being stored and retrieved from
AC7[1:0] in microstates TRP.50 and the start of TRP.60.

The end of TCP.60 and all of state TRP.70 are used to move the FEC and FEA from AC7[1:0] to AC7[3:2] via QR
and BR, and something was going awry here.  Since the nominal FEC is octal 14, I decided just to trace the
four least significant bits.  Consulting the engineering drawings, the nominal flow of these bits through
logic on the FRL during these states would be:

<style>
.logiclist { display: inline; border-collapse: collapse; margin-right: 1em; }
.logiclist caption { font-weight: bold; }
.logiclist tr:nth-child(4n+2), .logiclist tr:nth-child(4n+3) { background-color: #f2f2f2; }
.logiclist .microstate { background-color: #ffffff; }
.logiclist th, .logiclist td { padding: 5px; }
.logiclist td { border: 1px solid lightgray; font-family: Menlo,Consolas,monospace; }
</style>

<table class="logiclist">
<thead>
<tr><th>Function</th><th>Package</th><th>Dir</th><th colspan="4">Pin:Level</th><th>Microstate</th></tr>
</thead>
<tbody>
<tr><td>ACi&lt;03:00&gt;</td><td>E85</td><td>out</td><td>11:H</td><td>9:H</td><td>7:L</td><td>5:L</td><td class="microstate" rowspan="2">TRP.60 (2)</td></tr>
<tr><td>QR&lt;06:03&gt;</td><td>E74</td><td>in</td><td>3:H</td><td>4:H</td><td>5:L</td><td>6:L</td></tr>
<tr><td></td><td></td><td>out</td><td>15:H</td><td>14:H</td><td>13:L</td><td>12:L</td><td class="microstate" rowspan="14">TRP.70 (3)</td></tr>
<tr><td>BR&lt;07:04&gt;</td><td>E75</td><td>in</td><td>13:H</td><td>12:H</td><td>4:L</td><td></td></tr>
<tr><td></td><td></td><td>out</td><td>15:H</td><td>10:H</td><td>2:L</td><td></td></tr>
<tr><td>BR&lt;03:00&gt;</td><td>E87</td><td>in</td><td></td><td></td><td></td><td>5:L</td></tr>
<tr><td></td><td></td><td>out</td><td></td><td></td><td></td><td>7:L</td></tr>
<tr><td>FALU&lt;07:04&gt;</td><td>E77</td><td>in</td><td>20:H</td><td>22:H</td><td>1:L</td><td></td></tr>
<tr><td></td><td></td><td>out</td><td>11:L</td><td>10:L</td><td>9:H</td><td></td></tr>
<tr><td>FALU&lt;03:00&gt;</td><td>E89</td><td>in</td><td></td><td></td><td></td><td>18:L</td></tr>
<tr><td></td><td></td><td>out</td><td></td><td></td><td></td><td>13:H</td></tr>
<tr><td>ACMX&lt;03:02&gt;</td><td>E83</td><td>in</td><td>13:L</td><td>3:L</td><td></td><td></td></tr>
<tr><td></td><td></td><td>out</td><td>9:L</td><td>7:L</td><td></td><td></td></tr>
<tr><td>ACMX&lt;01:00&gt;</td><td>E84</td><td>in</td><td></td><td></td><td>13:H</td><td>3:H</td></tr>
<tr><td></td><td></td><td>out</td><td></td><td></td><td>9:H</td><td>7:H</td></tr>
<tr><td>ACi&lt;03:00&gt;</td><td>E85</td><td>in</td><td>12:L</td><td>10:L</td><td>6:H</td><td>4:H</td></tr>
</tbody>
</table>

Note that the bit values are inverted here by the FALU, since the reigster file used on the FP11 has
inverting outputs.

Threw the FRL out on extenders and starting verifying the chart above with a logic probe.  Surprisingly,
everything probed out correctly (?!)  Reset and ran the test program and verified that the bug had gone away.
Hmmm...  My only guess here is that there was some dust or a whisker shorting some of the pins that I
dislodged with the logic probe, or perhaps an oxidized board conection.  In any case, it seems to work
robustly now.  Of the FP11 diagnostics, the following now pass:

<style>
.diaglist { display: inline; border-collapse: collapse; margin-right: 1em; }
.diaglist caption { font-weight: bold; }
.diaglist tr:nth-child(even) { background-color: #f2f2f2; }
.diaglist th, .diaglist td { padding: 5px; }
.diaglist td { border: 1px solid lightgray; font-family: Menlo,Consolas,monospace; }
</style>

<table class="diaglist">
<thead>
<tr><th>Diagnostic</th><th>Description</th><th>Status</th></tr>
</thead>
<tbody>
<tr><td>CFPAB0.BIC</td><td>LDFPS,STFPS,SETI,SETL,SETF,SETD,CFCC</td><td>pass</td></tr>
<tr><td>CFPBB0.BIC</td><td>STST</td><td>pass</td></tr>
<tr><td>CFPCD0.BIC</td><td>LDF,LDD,STF,STD</td><td>pass</td></tr>
</tbody>
</table>

CFPDB0.BIC, which tests floating point adds/subtracts, is failing.  All for now -- on to debugging
add/subtract next time...
