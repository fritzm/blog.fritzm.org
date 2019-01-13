Title: PDP-11/45 Behaving Badly
Date: 2018-12-9
Tags: Retro-Computing, PDP-11

Wow, a year to the day since the previous post here!  Not a lot of PDP-11 work this past year, with lots of
other stuff like home improvements going on, but a few things worth catching up on here.

Mainly, I got brave this past year and decided to actually rent a van and take the 11/45 out of the basement
to the VCF West show at the Computer History Museum in Mountain View.  This was a *lot* more physical work
than I had anticipated.  Working on this thing a piece at a time, sitting in one place in the basement, you
get kind of used to it and forget how much iron it actually is...  But breaking it down, loading it into a
van, unloading into the show, reassembling, then reversing the whole process at the end of the show is a stark
reminder, both of the size of the machine and of my advancing age, ha!  A _huge_ thank-you to my workmate
Brian, who selflessly gave up a weekend, a vacation day, and some mileage on his back to give me
a hand.  He has already informed me that "the answer for next year is 'no'." :-)

[pswipe:pdp11,VCFW3.jpg,Reassembly on the VCF West show floor]
[pswipe:pdp11,VCFW1.jpg,Running diagnostics and consulting the RK11-C prints...]
[pswipe:pdp11,VCFW2.jpg,Pavl stops by with an RX02 and controller to help out with debug.  Replacement KM11 debug board visible in the upper diagnostic port of the RK11-C.]
[pswipe:pdp11,VCFW4.jpg,With Pete Richert, an old friend from Digidesign days!]

I suppose I should have expected it, but in the course of transportation to the show something shook loose resulting in a machine that wouldn't boot RT-11 when reassembled on the show floor (stupid bumpy rental
van!)  So my show became a two day live-troubleshooting exhibit.  This was fine, and I think a lot of
folks had fun jumping in and helping with troubleshooting (thanks, all!)  There was a lot of interest and
reminiscence about the machine and I met a lot of nice people.  Still, a little disappointing, because I
really had wanted people to be able to sit down and use the machine, and also because my head ended up in the
machine the whole time I really didn't get to see the rest of the show or talk to other people about their
exhibits!  Ah well.  In the end I did cajole a successful boot out of it, 15 mins. before the show closed, so
at least a couple people got to sit down and play Adventure.  Placed 3rd in the restoration category :-)

So, what went wrong?  At the show I managed to isolate the problem to something intermittent related to
interrupts from the RK11-C controller.  I was still able to boot the RKDP diagnostic pack, since its
bootstrap and monitor make very conservative use of processor and device interface features.  Running through
the diagnostics, managed to narrow down the problem to RK11-C completion polling after overlapped seeks.  I
guess RT-11 makes use of this feature.

I got the machine home and reassembled, and verified that the problem was still manifesting.  Then many months
passed, until I found some time to dig deeper into the problem just last night.  The relevant failing
diagnostic is ZRKK test 37, and the output is:

```text
DRIVE 0

RK11 DIDN'T INTRUPT AFTER SK COMPLETED
  PC     RKCS    RKER    RKDS
014476  000310  000000  004713


SCP DIDN'T SET AFTER SEEK WAS DONE
  PC   RKCS
014526  000310


RK11 DIDN'T INTRUPT AFTER SK COMPLETED
  PC     RKCS    RKER    RKDS
014476  000310  000000  004712


SCP DIDN'T SET AFTER SEEK WAS DONE
  PC   RKCS
014526  000310


TIMOUT,PC=004536
```

And the relevant bit of the diagnostic listing:
```masm
014362  2$:     MOV     RKVEC,R1
014366          MOV     #3$,(R1)+               ;SET UP VECTOR ADRES FOR RK11 INTERUPT
014372          MOV     #340,(R1)               ;SET UP PSW ON INTERRUPT
014376          BIS     #40,@RKDA               ;ADRES CYLINDER #1
014404          MOV     #111,@R0                ;SEEK, GO WITH IDE SET
014410          WAT.INT ,300                    ;WAIT FOR THE DRIVE TO
                                                ;INTERRUPT AFTER ADRES WAS RECVD
                                                ;WAITING TIME= 1.4 MS FOR 11/20
                                                ;280 US FOR 11/45
                                                ;ERROR, IF INTERUPT DID NOT OCCUR
                                                ;BY NOW
014414          MOV     #BADINT,@RKVEC          ;RESTORE UNEXPECTED RK11 INTERRUPT
014422          MOV     @R0,$REG0               ;GET RKCS
014426          ERROR   75                      ;INTERRUPT DID NOT OCCUR AFTER
                                                ;SEEK WAS INITIATED WITH IDE SET
014430          BR      3$+4
014432  3$:     CMP     (SP)+,(SP)+             ;OK, IF RK11 INTERRUPTED TO THIS
                                                ;RESTORE STACK POINTER (FROM RK11 INTERRUPT)
014434          CMP     (SP)+,(SP)+             ;RESTORE STACK POINTER (FROM
                                                ;WAT.INT)
014436          MOV     #5$,@RKVEC              ;SET UP NEW VECTOR ADRES FOR RK11
014444          BIT     #20000,@R0              ;IS SCP CLEAR
014450          BEQ     4$                      ;YES, BRANCH
014452          MOV     @R0,$REG0               ;GET RKCS
014456          ERROR   76                      ;SCP SET BEFORE SEEK TO LAST
                                                ;CYLINDER WAS DONE
014460  4$:     WAT.INT ,56700                  ;WAIT FOR DRIVE TO INTERRUPT
                                                ;AFTER SEEK WAS COMPLETED
                                                ;WAITING TIME=180 MS FOR 11/20
                                                ;36 MS FOR 11/45
014464          MOV     #BADINT,@RKVEC          :IT'S AN ERROR IF BY THIS TIME
                                                ;INTERRUPT HAS NOT OCCURERED
014472          JSR     PC,GT3RG                ;GO GET RKCS, ER, DS
014476          ERROR   77                      ;RK11 DID NOT INTERRUPT AFTER SEEK (TO
                                                ;LAST CYLINDER) WAS DONE WITH IDE SET
014500          BR      5$+2
014502  5$:     CMP     (SP)+,(SP)+             ;OK, IF RK11 INTERUPTED TO THIS AFTER
                                                ;SEEK WAS COMPLETED. RESTORE
                                                ;STACK POINTER (FROM RK11 INTERRUPT)
014504          CMP     (SP)+,(SP)+             ;RESTORE STACK POINTER (FROM
                                                ;WAT.INT)
014506          MOV     #BADINT,@RKVEC          ;RESTORE RK11 INTERRUPT VECTOR ADRES
                                                ;FOR UNEXPECTED INTERUTS
014514          BIT     #20000,@R0              ;DID SCP BIT SET?
014520          BNE     6$                      ;YES, BRANCH
014522          MOV     @R0,$REG0               ;GET RKCS
014526          ERROR   53                      ;SCP DID NOT SET AFTER RK11 INTERRUPTED
                                                ;INDICATING SEEK WAS
```
So, based on the fact that we don't hit error 75 from 14426 (and the fact that the previous test, #36, in
this diagnostic is passing) unlike some previous issues the RK11 here *is* able to generate interrupts and the
11/45 CPU is fielding them.  The issue seems related to the seek completion polling circuitry on the RK11.

This circuitry is described in section 3.3.2 of the RK11-C manual, and is detailed in engineering drawings
D-BS-RK11-C-12, sheets 1 and 2.  When a seek or reset is in progress for any drive and the IDE bit in the
controller is set, the controller will poll all drives for completion when it is otherwise idle.  When
polling is active, a pulse train which drives a count through the polled drives should be visible at B27F2:

<img style="display:block; margin-left:auto; margin-right:auto" src="/images/pdp11/poll-counter.png" title="RK11-C polling clock"/>

A quick look with the 'scope shows no joy here.  This clock is initiated by signal POLL; which doesn't seem to
be being asserted.  Checking the origin of that signal takes us to B26 and A26:

<img style="display:block; margin-left:auto; margin-right:auto" src="/images/pdp11/poll-enable.png" title="RK11-C polling clock enable"/>

Hmmm, one of these gates (the inverter at A26) is one that had failed and that I had repaired sometime last
year...  Reseated the socketed replacement on A26, reloaded the diagnostic, but still no go.  Well at least
it wasn't my repair job!  Went ahead and pulled A26 and B26 and bench tested the gates.  The 8-input nand
that outputs to B26J2 does look fishy.  Pulled and socketed the piece, and put a replacement and some spares
on order at Jameco where I can pick them up on my way in to work tomorrow.  All for now!
