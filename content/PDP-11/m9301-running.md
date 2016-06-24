Title: PDP-11/45: Running the M9301 console emulator
Date: 2016-6-23
Tags: Retro-Computing, PDP-11

Replacement DRAMs showed up.  Pulled and replaced the two faulty ones on the MS11.  Pic below -- you can see the
replacements are socketed, and are the TI parts instead of the original ITT.  Full address space is working now!  Now
that bank 0 is repaired, trap vectors can conceivably work.

Jumpered and configured a DL11-E serial card for use as console, slotted in an M9301-YB bootstrap terminator, connected
up the VT52, powered up, and off it goes straight to the console emulator!  That means the basic instruction set tests
in the boot ROM are passing as well, which is great news.

Next step will be to hook up PDP11GUI and load some more in-depth diagnostics, in order to shake out any
remaining bugs with the CPU and memory system.  Will slot in the FPU at that point for testing and debug as well.

[<img class='image-process-thumb' src='/images/pdp11/ms11-repaired.jpg'/>]({filename}/images/pdp11/ms11-repaired.jpg)
[<img class='image-process-thumb' src='/images/pdp11/m9301-running.jpg'/>]({filename}/images/pdp11/m9301-running.jpg)
