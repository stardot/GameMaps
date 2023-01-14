#!/usr/bin/env python

"""
read_sprites.py - A tool for exporting the sprites from Clogger.

Copyright (C) 2015 David Boddie <david@boddie.org.uk>

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
import UEFfile
import Image

from Clogger.sprites import Sprites, Puzzle

if __name__ == "__main__":

    if len(sys.argv) != 4:
    
        sys.stderr.write("Usage: %s <Clogger UEF file> <level file> <output directory>\n" % sys.argv[0])
        sys.exit(1)
    
    uef_file = sys.argv[1]
    level_file = sys.argv[2]
    output_dir = sys.argv[3]
    
    uef = UEFfile.UEFfile(uef_file)
    for details in uef.contents:
        if details["name"] == level_file:
            break
    else:
        sys.stderr.write("Failed to find the '%s' file in the UEF file.\n" % level_file)
        sys.exit(1)
    
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    sprites = Sprites(details["data"][0xabd:])
    
    for key in sprites.sprite_table.keys():
    
        sprite = sprites.read_sprite(key)
        
        im = Image.fromstring("P", (16, 32), sprite)
        im.putpalette((0,0,0, 255,0,0, 0,255,0, 0,0,255))
        im.save(os.path.join(output_dir, "%02i.png" % key))
    
    puzzle = Puzzle(details["data"])
    
    for p in range(5):
    
        whole_image = Image.new("P", (7 * 16, 3 * 32))
        whole_image.putpalette((0,0,0, 255,0,0, 0,255,0, 0,0,255))
        
        for i in range(21):
        
            sprite = puzzle.read_sprite(p, i)
            
            im = Image.fromstring("P", (16, 32), sprite)
            im.putpalette((0,0,0, 255,0,0, 0,255,0, 0,0,255))
            im.save(os.path.join(output_dir, "%i-%02i.png" % (p, i)))
            
            x = (i % 7) * 16
            y = (i / 7) * 32
            whole_image.paste(im, (x, y, x + 16, y + 32))
        
        whole_image.save(os.path.join(output_dir, "puzzle-%i.png" % p))
    
    sys.exit()
