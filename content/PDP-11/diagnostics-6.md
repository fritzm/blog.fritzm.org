Title: PDP-11/45: Diagnostics VI - GRA ALU PROM repair
Date: 2016-8-7
Tags: Retro-Computing, PDP-11

Data I/O Series 22 PROM programmer from eBay showed up, as well as some unprogrammed Signetics 82S123.  Punched in the
subsidiary ALU control ROM contents from the listing on GRAK in the 11/45 engineering drawings and burnt a new PROM.
Put a socket and the new PROM in place of the failed part on my original GRA, slotted it into the CPU, and success!
Diagnostic CKBOA0 now passes.  I will probably return to the other faulty GRA at a later point, as it is partially
diagnosed and I like to have spares working and ready to go.

Next time I'll be moving on to the CKT series of tests for the KT11 memory management cards...

[<img src='/images/pdp11/prom-programmer_thumbnail_tall.jpg'/>]({filename}/images/pdp11/prom-programmer.jpg)
[<img src='/images/pdp11/alu-prom-replaced_thumbnail_tall.jpg'/>]({filename}/images/pdp11/alu-prom-replaced.jpg)