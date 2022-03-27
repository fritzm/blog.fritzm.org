Title: BASIC-11 under RT11
Date: 2021-8-15
Tags: Retro-Computing, PDP-11

I figured it might be fun to play around a little bit with BASIC-11 under RT11 on the newly-restored
PDP-11/34.  If I got that working, it could also be included on the RK05 RT11 disk image that I use regularly
for demos on the larger PDP-11/45.

The first thing to do was to find a compatible disk image and get it running under simh.  Bitsavers had
`BASIC-11_V2.1_RX02.DSK.zip`, which would seem to fit the bill, but the contained image would not mount
successfully on simh's RY device.  Looking through a dump of the image, there was an apparent "RT11A"
signature, so that looked promising.  Tried `putr` under dosbox as well, but it would hang mounting the image.
So, off to the cctalk mailing list for some advice...

Glen Slick on the list first noticed a file size discrepancy:

> That BASIC.DSK image file has a size of 486,400 bytes. I don't know where that size would come from.
> 
> A physical RX-02 floppy should have a sector size of 256 bytes, with 26 sectors per track, and 77 tracks,
> which would be a total of 512,512 bytes, or 505,856 bytes if the first physical track is ignored.
> 
> Indeed, the other RX-02 floppy images available here do have a size of 505,856 bytes:
> http://www.bitsavers.org/bits/DEC/pdp11/floppyimages/rx02/
> 
> Hmm, maybe that BASIC.DSK image file was created by something that only copied the initial allocated logical
> sectors and ignored unused logical sectors at the end of the floppy, and maybe PUTR doesn't handle disk
> image files that are not the expected full size?
> 
> Example of padding the 486,400 byte BASIC.DSK image file to a size of 512,512 bytes on a Windows system:
> 
>     FSUTIL FILE CREATENEW BLANK 26112
>     COPY /B BASIC.DSK+BLANK TEST.DSK
> 
>     C:\PUTR>DIR TEST.DSK
>     Volume in drive C has no label.
>     Volume Serial Number is 14CE-1A29
>     Directory of C:\PUTR
>     08/11/2021  12:55p             512,512 TEST.DSK
>     
>     C:\PUTR>PUTR
>     PUTR V2.01  Copyright (C) 1995-2001 by John Wilson <wilson@dbit.com>.
>     All rights reserved.  See www.dbit.com for other DEC-related software.
>     
>     COPY mode is ASCII, SET COPY BINARY to change
>     (C:\PUTR)>MOUNT RX: TEST.DSK /RX02 /RT11 /RONLY
>     (C:\PUTR)>DIR RX:
>     
>     Volume in drive RX is RT11A
>     Directory of RX:\*.*
>     
>     11-Aug-2021
>     BSOT0D.EAE    12  04-Apr-1983
>     BSOT0S.EAE    10  04-Apr-1983
>     BSOT1D.EAE     9  04-Apr-1983
>     BSOT1S.EAE     6  04-Apr-1983
>     BSOT0D.EIS    12  04-Apr-1983
>     ...

...etc.  Nice.  Still no luck mounting under simh, though.  Glen further offers:

> As far as I can tell by default PUTR expects to work with logical sector order RX-02 disk images that are
> 512,512 bytes in size. The BASIC-11 RX-02 disk image available here is in logical sector order, but is less
> than 512,512 bytes in size: http://www.bitsavers.org/bits/DEC/pdp11/floppyimages/rx02/ PUTR appears to be
> unhappy with the disk image unless it is padded to 512,512 bytes in size.
> 
> On the other hand as far as I can tell by default SIMH expects to work with physical sector order RX-02 disk
> images. If I mount the logical sector order RX-02 disk image that works with PUTR in SIMH, then RT-11 gives
> a "?DIR-F-Invalid directory" error. If I translate the logical sector order RX-02 disk image back into a
> physical sector order disk image (dealing with track shifting, sector interleaving, and track to track
> sector skewing) then RT-11 on SIMH is happy with the disk image.

and:

> One bit of information that I found helpful as a reference when I looked at this quite a while ago was the
> 2.11BSD RX02 floppy disk device driver source code, which can be viewed online here:
> 
> https://minnie.tuhs.org/cgi-bin/utree.pl?file=2.11BSD/sys/pdpuba/rx.c
> 
> In particular, the routine rxfactr(), which as the comment says it calculates the physical sector and
> physical track on the disk for a given logical sector.
> 
> I used that as a starting point to write a simple utility to read an RX-02 disk image file in logical sector
> order and output an RX-02 disk image file in physical sector order.
> 
>     :::C
>     /*
>     *  rxfactr -- calculates the physical sector and physical
>     *  track on the disk for a given logical sector.
>     *  call:
>     *      rxfactr(logical_sector,&p_sector,&p_track);
>     *  the logical sector number (0 - 2001) is converted
>     *  to a physical sector number (1 - 26) and a physical
>     *  track number (0 - 76).
>     *  the logical sectors specify physical sectors that
>     *  are interleaved with a factor of 2. thus the sectors
>     *  are read in the following order for increasing
>     *  logical sector numbers (1,3, ... 23,25,2,4, ... 24,26)
>     *  There is also a 6 sector slew between tracks.
>     *  Logical sectors start at track 1, sector 1; go to
>     *  track 76 and then to track 0.  Thus, for example, unix block number
>     *  498 starts at track 0, sector 25 and runs thru track 0, sector 2
>     *  (or 6 depending on density).
>     */
>     static
>     rxfactr(sectr, psectr, ptrck)
>        register int sectr;
>        int *psectr, *ptrck;
>     {
>        register int p1, p2;
>     
>        p1 = sectr / 26;
>        p2 = sectr % 26;
>        /* 2 to 1 interleave */
>        p2 = (2 * p2 + (p2 >= 13 ?  1 : 0)) % 26;
>        /* 6 sector per track slew */
>        *psectr = 1 + (p2 + 6 * p1) % 26;
>        if (++p1 >= 77)
>            p1 = 0;
>        *ptrck = p1;
>     }

An RX02 image shuffled into physical sector order generated by Glen and suitable for use with simh is
attached [here]({attach}PHYS.zip).

Jerry Weiss further suggested that the original, logically ordered image may work as is under simh if attached
as an MSCP device rather than RX02.  This turns out also to be the case:

>> On Fri, Aug 13, 2021 at 9:46 AM Jerry Weiss wrote:  
>> Could you attach logical sector (block?) image as MSCP disk in SIMH?   Other than some minor image
>> manipulation for removing track 0 if present, is there any reason this would not be readable?
> 
> Hmm, it didn't occur to me to try that. Mounting the logical sector order RX-02 disk image, without any
> modification necessary, as a raw MSCP disk does indeed appear to work!
> 
>     sim> ATTACH RQ1 BASIC.DSK
>     RQ1: 'BASIC.DSK' Contains RT11 partitions
>     1 valid partition, Type: V05, Sectors On Disk: 950
>     
>     sim> SHOW RQ1
>     RQ1     486KB, attached to BASIC.DSK, write locked
>            RD54, UNIT=1, autosize
>            RAW format
>     
>     .DIR DU1:
>     
>     BSOT0D.EAE    12  04-Apr-83      BSOT0S.EAE    10  04-Apr-83
>     BSOT1D.EAE     9  04-Apr-83      BSOT1S.EAE     6  04-Apr-83
>     BSOT0D.EIS    12  04-Apr-83      BSOT0S.EIS     9  04-Apr-83
>     BSOT1D.EIS     9  04-Apr-83      BSOT1S.EIS     6  04-Apr-83
>     BSOT0S.FIS     7  04-Apr-83      BSOT1S.FIS     6  04-Apr-83
>     ...

...etc.  Armed with the above, I was able to get BASIC-11 into an RT11 image in the Unibone card, and running
on the new PDP-11/34.  Here's output from the [DEC BASIC mandelbrot
program](https://rosettacode.org/wiki/Mandelbrot_set#DEC_BASIC-PLUS) at rosetta code:

[pswipe:pdp11,basic-mandel-output.jpeg,BASIC-11 Mandelbrot program on a PDP-11/34, program output]
[pswipe:pdp11,basic-mandel-list.jpeg,BASIC-11 Mandelbrot program on a PDP-11/34, program listing]
