Title: PDP-11/45: Diagnostics XII - FP11 FPU, cont.
Date: 2016-10-30
Tags: Retro-Computing, PDP-11

Some spare 74194 arrived in the mail; popped one in to the socket I had prepared at E15 on the FRL board,
and the FP add/subtract problem is fixed.  The following FP11 diagnostics now pass:

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
<tr><td>CFPDC0.BIC</td><td>ADDF,ADDD,SUBF,SUBD</td><td>pass</td></tr>
<tr><td>CFPEB0.BIC</td><td>CMPF,CMPD</td><td>pass</td></tr>
<tr><td>CFPFB0.BIC</td><td>MULF,MULD</td><td>pass</td></tr>
<tr><td>CFPGC0.BIC</td><td>DIVF,DIVD</td><td>pass</td></tr>
<tr><td>CFPHB0.BIC</td><td>CLR,TST,ABS,NEG</td><td>pass</td></tr>
<tr><td>CFPIB0.BIC</td><td>LDCDF,LDCFD,STCFD,STCDF</td><td>pass</td></tr>
<tr><td>CFPJB0.BIC</td><td>LDCJX,STCXJ</td><td>pass</td></tr>
<tr><td>CFPKB0.BIC</td><td>LDEXP</td><td>pass</td></tr>
<tr><td>CFPMB0.BIC</td><td>MAINT</td><td>pass</td></tr>
</tbody>
</table>

...which is almost everything.  The last failing diagnostic is CFPLB0, which tests MODF and MODD.  Set up
a similar test program for this instruction:

    #!masm
            000000                          AC0=%0
            000001                          AC1=%1
    000000                                  .ASECT
            001000                          .=1000
    001000  170011                  START:  SETD                ;SET DOUBLE PRECISION MODE
    001002  172467  000020                  LDD     D1,AC0      ;FETCH FIRST OPERAND FROM D1
    001006  172567  000024                  LDD     D2,AC1      ;FETCH SECOND OPERAND FROM D2
    001012  171401                          MODD    AC1,AC0     ;MOD (FRAC IN AC0, INT IN AC1)
    001014  174067  000026                  STD     AC0,D3      ;STORE FRAC TO D3
    001020  174167  000032                  STD     AC1,D4      ;STORE INT TO D4
    001024  000000                          HALT
    001026  040200  000000  000000  D1:     .WORD   040200,000000,000000,000000 ;1.0
    001034  000000
    001036  040300  000000  000000  D2:     .WORD   040300,000000,000000,000000 ;1.5
    001044  000000
    001046  000000  000000  000000  D3:     .WORD   000000,000000,000000,000000
    001054  000000
    001056  000000  000000  000000  D4:     .WORD   000000,000000,000000,000000
    001064  000000
            001000                          .END    START

This does show a problem: after exection, the integer result at D4 seems correct, but the fractional result
in D3 is incorrect (037777 177777 177777 177777).  Verified the correct microflow with the KM11.

Stopped in microstate MOD.22, and examined ALUs on FRL where the fractional result is masked.  ALU function
selects (for A & ~B) and B inputs (all zeros for mask) look correct throughout.  A inputs, however,
are all ones except the least significant bit, which seems incorrect.  All for now -- will dig a little deeper on the microcode flows and follow up on this lead next time...
