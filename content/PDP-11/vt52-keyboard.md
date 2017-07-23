Title: PDP-11/45: VT52 Keyboard Repair
Date: 2017-7-15
Tags: Retro-Computing, PDP-11

The VT52 had a broken ESC key, and with RT-11 up and running I was motivated to dig in and fix it (you need
that ESC key if you are going to run the K52 editor).  Pulling the keycap and giving things a look over, the
leaf contacts and the plastic plunger that activate the key looked fine.  Need to get at the keyboard module
itself to troubleshoot, and on a VT52 that means opening the thing all the way up and pulling the main
boards. In we go...

Extracted the keyboard module, powered it from my bench supply, and used a breadboard and some jumpers to
drive the key select decoders.  Key closure on the back of the module was intermittent, but some flexure of
the entire keyboard PCB seemed to be affecting it.  Replaced/reflowed the solder on the back of the key
switch and that seems to have fixed it.

Back together, working well now.  Test drove it for a while under RT-11...

[<img src='/images/pdp11/vt52-guts_thumbnail_tall.jpg'/>]({filename}/images/pdp11/vt52-guts.jpg)
[<img src='/images/pdp11/vt52-keys_thumbnail_tall.jpg'/>]({filename}/images/pdp11/vt52-keys.jpg)
[<img src='/images/pdp11/rt11-adventure_thumbnail_tall.jpg'/>]({filename}/images/pdp11/rt11-adventure.jpg)
