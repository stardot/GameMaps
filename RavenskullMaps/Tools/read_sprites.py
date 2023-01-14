#!/usr/bin/env python

"""
read_sprites.py - A tool for exporting the sprites from Ravenskull.

Copyright (C) 2013 David Boddie <david@boddie.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os, sys

import Image
from Ravenskull import IncorrectSize, NotFound, Ravenskull

if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <Ravenskull UEF file> <output directory>\n" % sys.argv[0])
        sys.exit(1)
    
    uef_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    try:
        r = Ravenskull(uef_file)
    except NotFound:
        sys.stderr.write("Failed to find the required file in the specified file: %s\n" % uef_file)
        sys.exit(1)
    except IncorrectSize:
        sys.stderr.write("The required file was not the expected size.\n")
        sys.exit(1)
    
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    sprites = r.read_sprites()
    
    for number, sprite in sprites.items():
    
        im = Image.fromstring("P", (12, 24), sprite)
        im.putpalette((0,0,0, 255,0,255, 0,255,0, 0,0,255))
        im.save(os.path.join(output_dir, "%02i.png" % number))
    
    sys.exit()
