# Building the eHarp

This is not a detailed construction guide, more a loose description of the approach I took with the prototype!

## The body
The main body of the eHarp is built from four layers of ply. Two sheets of 600x1220mm ply were obtained from my local DIY store; a sheet of 12mm and a sheet of 20mm. I could get two 
body sections from each sheet (see cutting_plan.svg for the layout). These can be cut out with a jigsaw; I used a *big* bandsaw (you won't be able to do it with a small benchtop bandsaw!). It is also easier to make a template from some light ply for marking this out. The template has a couple of functions; it ensures that all your ply sections are the same shape and size, and it also comes in useful later one when you are aligning all those little laser diodes in the array. More on that later.
The 12mm sections form the inner core of the body. Before gluing them together, cut out the rectangular openings marked in red on the diagram for the controls - note that the larger opening is on one section only! Glue and clamp.
Cut out the outer sections from the 20mm ply in the same way. Put them aside until later.
Once the core is glued, cut out a section for the laser array on the longer arm (keep the bit you cut out - you'll need it later), and a section for the sensor at the end of the shorter arm. Again, these are marked in red on the diagram. Use a router to cut channels for the cables for the laser array and the sensor to the electronics bay (the larger opening) in the core section.

The outer sections of 20mm ply can now be glued on and clamped. It is worth laying some cord into the routed channels before doing this. It makes pulling the cables through a lot easier, and prevents a lot of poking with bits of stiff wire and swearing later! Just be careful not to catch the cord between the layers of ply and gluing it permanently into place!
Once everything is glued and dried, the edges can be routed round, any nasty gaps filled, and the whole thing sanded smooth. Finish it with whatever finish takes your fancy. I did mine with a metallic red paint, and a light dusting of an iridescent spray. The whole thing was then given several coats of a hard-wearing varnish (I know how much things can get knocked about!).

## The laser array
This is where that bit you saved (you *did* save it, didn't you?) comes in. It will need to be cut down a little further to leave you with a curved section about 2cm wide on the inside of the curve. Cut a couple of cm off each end as well to allow space to fit it later. Measure the length of the outside curve of the piece, allow another centimeter or so for space, and divide the remainder by 32. This will give you the spacing of the individual laser diodes. Use a pair of dividers to mark off the locations along the edge. 
Draw lines at *exactly* 90 degrees to the edge toward the inner curve. These are the drill guides that you will be using to make the holes for the diodes. Also draw a line along the exact middle of the inner curve.
Measure the diameter of the diode module (mine were 6mm) and using a *sharp* drill bit 0.5mm wider, drill holes from inside curve to outside curve along the guidelines for all 32 diodes. Use a pillar drill, and it's probably worth making a little jig to help with this. You won't be able to do it accurately with a hand drill!

How you assemble the array is up to you, but in my case I found it easiest to take it one diode at a time, testing, aligning and securing each one before moving on to the next one. The diodes I used were 3.3v ones, and you will need a suitable power supply or battery with crocodile clips so that you can power up each diode before soldering it in to anything.
Remember I said that that plywood template would come in useful? Clamp or use double-sided tape to affix the drilled plywood array section to the long arm of the template, and attach a small target (a small round bit of wood, or a pen cap) to the centre of the end of the short arm. Now, for each laser:
- Connect it to the supply. Make sure that the polarity is correct and watch your eyes!
- Check the focus and brightness. When buying in bulk, some diodes can be pretty dim and often out of focus. The lens end can be twisted to focus the beam.
- Put the diode in place in it's hole. If you drilled accurately it should be fairly close to your target. You can wiggle it a bit to get it properly aimed.
- Once aimed, fix it in place with a small drop of thin superglue. Apply the glue to the back, *not* the front (you get glue on the lens otherwise and obscure the beam - don't ask me how I know this!).

The array can be wired. The leads from the diodes are very thin and flimsy, so it is worth keeping them as short as possible, and don't connect them directly to any flying leads for connecion to the main board. Provide some fixed connection points next to the diodes and use those. I found some small copper tacks that worked admirably. If using tacks like this, drill the wood with a small drill and push them in - don't hammer them! Complete the wiring with ribbon cable, and leave enough to reach the main board easily.

## The sensor
The laser sensor is a bit simpler to put together. It was made from a stack of four units cut from 6mm clear acrylic (there is a template in the drawings). Once cut, the segments were glued together using UV-curing glue, and clamped before curing to remove any air bubbles. Once glued, the stack was sanded down to 8000 grit and then polished with cutting compound to get a glassy finish.
In order to maximise light capture it is worth putting some sort of reflective finish on all faces except the front-facing curved face. I used silver leaf, but a reflective silver paint will work too. Mask off the front face before gilding/painting to prevent anything getting on that face.

Once the acrylic block is finished, drill a 6mm hole from one of the flat sides to the centre of the segment. Shorten the leads of a PT334-6C phototransistor and solder a length of coaxial cable on (braid to emitter, core to collector). Use heat-shrink sleeving to insulate the joints. You could use normal cable. but the levels are very low and you may pick up a lot of noise. Coax will reduce this.
Insert the phototransistor into the hole you drilled and secure in place with UV-curing glue.

## The panels
There are three control panels, a menu/display one, a bend/mod and octave selection one, and a connector panel for the interfaces and power. The construction principles are the same for each.
Each panel is made from two layers of 2mm acrylic, laser-cut to shape. All the cutting guides for these are in the diagrams. I have also provided the labels for these panels here. These can be printed out and sandwiched between the layers of acrylic.
I built the circuitry for the panels on stripboard (as this is a prototype). It would be nicer to user proper PCBs.
Again, flying ribbon cables should be attached with sufficient length to reach the electronics bay.

## The main board
All the circuitry was built on one prototyping board (well, it was a prototype!) that fits into the electorincs bay. Again, it would be nicer to use a proper PCB, but this has been through many iterations and I did not want a huge pile of useless boards cluttering up my workshop!

## Assembly
The sensor was placed in the short arm of the eHarp, and glued in place using 2-part epoxy.

The cables for the laser array were drawn through the channel using the previously placed cord, and then the array located in place so that the lowest note (first laser in the array) is towards the base of the harp, and the highest at the top end of the arm. The array is lightly placed initially, as it may need to be repositioned slightly to aim them at the sensor correctly.
The various panels are put in place and secured with small brass screws. All the leads are brought out to the electronics bay (which is now sprouting a bewildering nest of cables! You *did* mark them before putting everything in place, didn't you?).

Finally, the main board is connected and nestled in the electronics bay. Connect up the USB cable to a supply and let it boot up. Once it has finished booting, use the Slow Scan option in the Diagnostics menu to finish aligning the laser array. It can be pressed into place, and secured with a drop of glue if necessary (it should be a tight push fit, and not need glue).

## Final adjustment
There is one small adjustment that will be needed, and this will require an oscilloscope or a logic analyser. This should be attached to the output of the LM393 comparator (U5 on the schematic). Select Mute Lasers from the Diagnostics menu (this will turn off all the lasers) and set RV1 to give a LOW output.
Now select Slow Scan from the Diagnostics menu and tweak RV1 to give a HIGH output for each laser.

You're all done! All that is needed is a cover over the electronics bay. I used a small piece of 3mm ply, coloured to match the rest of the body, and secured with small brass screws.
Connect it to your favourite DAW or VST host and enjoy!

