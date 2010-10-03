				  MoonMap

		     [ A Moon Raider level convertor ]

Created:	Mon 22nd January 2001
Last updated:	Thu 06th September 2001
WWW site:	http://www.david.boddie.net/Software/Python/MoonMap/



Introduction

The Micro Power game "Moon Raider" is a sideways-scrolling arcade game similar to
the arcade classic "Scramble" and was released for both the BBC Micro and Acorn
Electron computers. It has six consecutive levels, but the player can skip up to
the first four. There is a refuelling stage between each level.

Despite having the standard challenges for "Scramble" type games, the description
of the levels is surprisingly flexible. Longer levels than the original can be
designed, and game features are not confined to levels they appeared in during
the original game. For instance, fireballs may be introduced outside level three.

This program allows you to convert between the levels built in to a copy of Moon
Raider and a textual description which can be edited more easily. In order to run
it, you need to obtain a Python interpreter for your computer platform. Look at

http://www.python.org/

for information regarding installation and usage of Python.


Creating a map

You design your levels using a text editor. Each feature of the level is
described on a line which typically looks like the following:

###!

Here, the "#" symbol describes how high the floor is and the "!" symbol tells the
program that the surface is rocky. At the start of level one, the floor should be
three units high. For an empty floor, you just leave a space:

###

You can set the floor up to 27 levels high just by writing more "#" characters

###!
#########
#########

but this jump in height will produce a steep cliff or wall. If you want to create
a hill then use the ">" and "<" symbols:

###>
####>
#####<
####<
###!

Note that you must change the floor height by one when you use these symbols. For
steeper hills, use "\" and "/":

###\
#####\
#######/
#####/
###!

Here, you change the floor height by two characters instead of one.

Missiles, fuel, gun turrets and radar stations are described by the "m", "f", "t"
and "r" symbols. Each of these will sit on a patch of coloured floor which, on
it's own, is described by the "|" symbol. For example, a missile and fuel tank are
separated from a turret and a radar station by a vacant place:

###m
###f
###|
###t
###r

To choose one of these at random, use the "?" symbol. For a fuel tank without a
coloured base, use the "F" symbol. This is useful for placing fuel in tunnels.

Note that Moon Raider appears to prohibit missiles from firing on levels two and
three, traditionally the alien and fireball stages. Be careful when deploying
them on other levels as missiles will still fire whether there is a ceiling
present or not. Despite these restrictions, missiles at the end of levels will
occassionally fire anyway, presumably because the player has already entered the
refuelling stage.

In the original game, the refuelling stage featured a refuelling ship at the
centre of a minefield. Mines are introduced by the use of the "x" symbol, and are
placed randomly above the ground and may overwrite any ceiling present.
The refuelling ship is described by the "1" and "2" symbols, which should be used
in sequence. We can obtain a similar effect to the original game by writing:

###x
###x
###
###
###1
###2
###
###
###x
###x

When the level is finished, you need to inform the program by using the "E"
symbol. You can specify the floor level at the end of the level in the same way as
you would during the level. This is useful as you may wish to revert to a standard
floor height before the refuelling stage:

###E

The description of the next level begins immediately after the end of the previous
one with no blank lines separating the two.

The second level of the original game featured a cave in which the player faced
some bouncing aliens. The ceiling of the cave is described in the same way as the
floor, but is separated by the description of the floor by any object which is
present:

###!
###!                    ###
###                     ###

Since the maximum height of the screen is 27 units, it is useful to separate the
floor and ceiling with an appropriate amount of whitespace, but the amount of
space present is arbitrary. This cave could have equally been described by

###!
###!###
### ###

although the single space is necessary on the third line, as otherwise the program
will interpret it as a wall rather than a separate floor and ceiling.

Aliens are placed in the cave by using the "@" symbol. This is written after the
ceiling description:

###!                    ### @
###>                    ###
####!                   ###@
####<                   ###
###!                    ###	@

Care must be taken to avoid placing aliens which interfere with the floor and
ceiling.

Fireballs may be placed in a similar way, although they may appear near the top
of the screen so caution should be used when using low ceilings. They are
described using the "*" symbol:

###!
###f	*
###?*
###!
###t *

Once you have written five levels, you should ideally write a final level in which
the mission target, the "H" symbol, appears. This level is unlike the other in
that once the player arrives, they will repeatedly fly through it until they
destroy the target, or crash. Other levels are always followed by the refuelling
stage.

The "seventh" level to be defined is the refuelling stage, although it doesn't
have to serve that purpose. This is visited by the player between each stage.

You should save your levels as a plain text file with a "map" extension such as
"mylevels.map" and run the "moonmap.py" program to create a patch file.


Creating a patch file

Once your levels are written, you need to create a file which can be loaded in an
emulator, or possibly on a real Electron or BBC, to replace the default levels.
This is achieved by running the "moonmap.py" program with your filename of your
levels file as the first parameter, the filename of the Moon Raider UEF file as
the second and the filename of the UEF file to be created as the third.
For example,

	moonmap.py mylevels.map MoonRaider_E.uef myraider.uef

will produce a file called "myraider.uef" which contains your levels instead of
the Moon Raider default levels. This can be used in the same way as the original
Moon Raider UEF file.

You may encounter error messages which specify a line in your levels file. These
include:

Message					Meaning

Level too long (or too detailed)	You have included too many lines for that
					level, or have changed the floor or
					ceiling level too much.

Floor is too high			The floor is so high that the player would
					not be able to avoid crashing into a wall.

Step is too high			The floor or ceiling level went up or down
					too sharply.

Ceiling is too low			The ceiling is so low that the player
					would not be able to avoid crashing into a
					wall.


Problems with levels

You may encounter a problem with your level where the floor is not at the level
you expect it to be after the level has been rapidly changed several times. This
appears to be a limitation in the game which can be resolved by delaying steps or
by spreading them out.


History

0.10 (Sun 21st January 2001)

Initial version.

0.11 (Tue 23rd January 2001)

Modified version of 0.10 which allows empty lines to denote no floor or ceiling.

0.12 (Mon 13th August 2001)

Tidied up multi-platform support.

0.13 (Thu 06th September 2001)

Now patches the UEF file directly using UEFfile objects.


Contact address

You can contact me (David Boddie) at david@boddie.net
