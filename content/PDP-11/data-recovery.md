Title: PDP-11/45: Data Recovery
Date: 2017-7-9
Tags: Retro-Computing, PDP-11

Okay, the system is working well enough now to start attempting recovery and archive of the dozen or so RK05
packs that I have on-hand.  These were all obtained (along with the RK05 drives, controller and power supply)
in a surplus auction downstream of the Stanford Hansen Experimental Physics Lab, sometime in the early '90s.

The packs date from the mid-70's to early-80's, and the labels indicate contents related to experiments and
research projects taking place at the lab at that time.  One particular pack seems associated with the
Stanford Gravity Wave Project, which built early resonant mass detectors.  Other packs labeled "FEL" would
be related to early free-electron laser research.  Many of the names on the packs are are readily found on
related scientific publications from the time.

The process for dealing with these packs involves opening them up for inspection and cleaning before
mounting them, with hopes of avoiding beating up or destroying the drive heads and/or media with head crashes.
Much has been written about pack cleaning on the classicmp mailing lists and in the vcfed forums, but briefly
the process involves some clean-room nitrile gloves, lint-free wipes, and anhydrous isopropyl alcohol.  The
outside of the pack is first cleaned of dust and grime, then the packs are opened and inspected and the disk
surfaces given a scrub with the wipes and alcohol.  If a pack seems in good enough shape to mount, I'll spin
it up and run it in the drive with head load disabled for about a half-hour.  This gets a good air-flow over
the disk to blow out remaining loose particulates and also lets the disk come up to thermal equilibrium.
After that I let the heads load, standing by with a finger on the unload switch in case there are any bad
noises...

I've already been dealing with two of the packs extensively during the restoration: one is an RKDP
diagnostics pack, and the other was a backup pack of same.  I was able to capture a complete, error-free
image of the RKDP pack using PDP11GUI.  This seems to be an earlier version of this disk that what is
already available on bitsavers; I've sent the bits to Al Kossow, but as I understand it his project has
a big backlog at the moment so it may be a while before he can consider my submission.  In the meantime,
for those interested, the disk image is available [here](http://www.slac.stanford.edu/~fritzm/data/pdp11/rk05/MAINDEC-11-DZZAA-J-HB.dsk).

The RKDP backup disk was used as a test pack during the RK11/RK05 restoration work, and was overwritten
by the RK05 diagnostic read/write tests.  It now contains a bootable RT-11 image, written via PDP11GUI.
Mixed results on the other packs so far: some have had severe head crashes (see pic below) or are otherwise
damaged to the point that I am hesitant to mount them.  Some have been mysteriously unreadable.  It looks
like I can expect about 50% recovery.  Results so far are tabulated here.  I hope to be able to make other
recovered images available soon, but since they contain original research materials I am trying to contact
the authors for permission first.

<style>
.disklist { display: inline; border-collapse: collapse; margin-right: 1em; }
.disklist caption { font-weight: bold; }
.disklist tr:nth-child(even) { background-color: #f2f2f2; }
.disklist th, .disklist td { padding: 5px; }
.disklist td { border: 1px solid lightgray; font-family: Menlo,Consolas,monospace; }
</style>

<table class="disklist">
<thead>
<tr><th>Serial #</th><th>Label</th><th>OS</th><th>Notes</th></tr>
</thead>
<tbody><tr>
    <td>ZO 50511</td>
    <td>MAINDEC-11-DZZAA-J-HB 9/21/74 M<br>XXDP RKDP RK11 DIAGNOSTIC PACKAGE</td>
    <td>DZQUD-A RKDP-RK11 MONITOR</td>
    <td>[1974] MAINDEC diagnostics for PDP-11/40/45 CPU/MMU/FPU, MS11, DL11, DR11, RK11, LC11/LA30, KW11-L/P. Full recovery.</td>
</tr><tr>
    <td>B1-28320</td>
    <td><span style="text-decoration:underline;">Gravitational</span> <span style="text-decoration:underline;">Radiation</span> <span style="text-decoration:underline;">Experiment</span><br>Boughn, Hollenhorst, Paik, Sears, Taber MSA</td>
    <td>DOS/BATCH V09-20</td>
    <td>[1976-77] Fortran and MACRO-11 codes, mostly calculations relating to resonant mass detector design. Full recovery.</td>
</tr><tr>
    <td>AD-21279</td>
    <td>BLAZQUEZ RT-11 AUG 83</td>
    <td>RT-11FB (S) V04.00L</td>
    <td>[1983] Fortran and MACRO-11 codes relating to image processing and display.  Device driver code for Deanza Systems ID-2000 display and Calcomp plotter.  Names: Ken Dinwiddie (De Anza codes), Art Vetter (Calcomp codes). Full recovery.</td>
</tr><tr>
    <td>BAK 9069 A</td>
    <td>W. COLSON</td>
    <td>DOS/BATCH V9-20C</td>
    <td>[1977-78] Full recovery.</td>
</tr><tr>
    <td>AE 61745</td>
    <td>FEL L.ELIAS</td>
    <td>DOS/BATCH V9-20C</td>
    <td>[1974-78] Head crash on read (ouch!) Partial recovery.  Unrecovered data looks to be mostly OS files; may be patchable.</td>
</tr><tr>
    <td>AE 20116</td>
    <td>DEACON FEL</td>
    <td>unknown</td>
    <td>[unknown] Corrosion spots on media; did not mount.</td>
</tr><tr>
    <td>ZO 50399</td>
    <td>TRANSPORT + DATA<br>1/18/80</td>
    <td>DOS/BATCH V9-20C</td>
    <td>[1980-83] Minor corrosion spot. Partial recovery. Data files and compiled Fortran programs.</td>
</tr></tbody>
</table>

[<img src='/images/pdp11/rk05-packs_thumbnail_tall.jpg'/>]({filename}/images/pdp11/rk05-packs.jpg)
[<img src='/images/pdp11/head-crashes_thumbnail_tall.jpg'/>]({filename}/images/pdp11/head-crashes.jpg)
[<img src='/images/pdp11/gravity-pack_thumbnail_tall.jpg'/>]({filename}/images/pdp11/gravity-pack.jpg)
