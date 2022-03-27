Title: Unibone
Date: 2021-3-24
Tags: Retro-Computing, PDP-11

I have been keeping an eye on Jörg Hoppe's interesting [Unibone project](http://retrocmp.com/projects/unibone)
for some time -- it is a general-purpose Unibus device emulator and diagnostic tool, built around a
[BeagleBone Black](https://beagleboard.org/black) compute module running embedded real-time Linux. The
PDP-11/34 restoration project finally provided enough impetus for me to pull the trigger on getting one.

Sent Jörg an email to order a kit, which arrived some weeks later complete with bundled BeagleBone. The kit is
pretty well thought-out and was enjoyable to put together.  Had to throw in a few of my own pin headers and
jumpers to complete the assembly.  The only other small confusions were a few of the resistor packs which did
not match the schematic (Jörg informed me these are non-critical values.)

The kit did not include card handles.  I decided to try having some 3D printed by Shapeways, using their
"processed versatile plastic" process, which is a laser sintered nylon, color dyed and smoothed.  I used a
card handle model by Vince Slyngstad found [here](https://so-much-stuff.com/pdp8/cad/3d.php).  The results
were nice, sturdy, and dimensionally correct. The chosen "purple" color is a rather intense magenta in real
life.  Not exactly cheap for just a couple parts, but I had been wanting to try their print service.

[pswipe:pdp11,unibone-kit.jpeg,Unibone: unassembled kit]
[pswipe:pdp11,unibone-handles.jpeg,Unibone: 3d printed handles]
[pswipe:pdp11,unibone-assembled.jpeg,Unibone assembled]

The Unibone has all sorts of capabilities, and proved itself _very_ useful during the '11/34 restoration:

* Ability to bus master to probe the Unibus address space and run diagnostics on memory found there.  This was
  very useful for debugging the memory card that came with the -11/34 and sussing out its undocumented
  configuration switch settings.

* Ability to directly load and execute MAINDEC diagnostics, without needing a functioning console emulator or
  storage subsystem.  This is a convenient and speedier alternative to PDP11GUI.

* Subsequently, the ability to emulate entire storage subsystems, very useful for loading and running full
  operating systems on this -11/34 which otherwise has no storage of its own.

The Unibone goes in a quad SPC slot; I opted for slot 9 on the -11/34, and this entailed removing the NPG
jumper on the backplane there to allow the Unibone to bus master.  The device worked well straight-away after
assembly.

There are, alas, a couple small frustrations with the current design:

* It is desireable to configure the Unibone and backplane to allow the Unibone to bus master and interrupt.
  However, this leaves grant chain(s) open at boot until the Unibone's own embedded software can boot and take
  control of the card (which takes on the order of a minute or so).  During this time the host system is
  non-functional or may hang, and it needs to be subsequently reset (this reset can be scripted from the
  Unibone, but all of this does significantly increase end-to-end boot time of the machine). It would be nice
  if the Unibone had something like some normally-closed relays on the grant chains, to preserve grant
  continuity until control is actively assumed.

* It would be desireable to be able to power the embedded BeagleBone in isolation, in place in a
  system, without having to having to have the entire host system powered at the same time (e.g. for
  maintenance of the Unibone's embedded software stack, maintenance of locally stored storage system media
  images, etc.)  There is a relay on the Unibone which switches in Unibus power when available, but
  unfortunately, the design is such that if the BeagleBone is also externally powered the relay remains
  engaged when the host system is shut down.  This could lead to the BeagleBone trying to power then entire
  Unibus via its 5V supply/connector, which could obviously be problematic...  For now it seems best just to
  pull the card in order to run it in isolation, which is a little less than convenient.

That said, the designs and software are open source, and the card comes with some generous prototyping areas
built right in, so some mods to address these issues could be a fun project.  All in all, Jörg has put
together a fantasically useful bit of kit, and I'm certainly glad to have it in my toolbox!
