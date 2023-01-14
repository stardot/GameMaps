#!/usr/bin/env python

"""
read_sprites.py - Save sprites contained in the Icarus game to files.

Copyright (C) 2016 David Boddie <david@boddie.org.uk>

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
import icarus

if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <Icarus UEF file> <output directory>\n" % sys.argv[0])
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    u = UEFfile.UEFfile(sys.argv[1])
    
    for details in u.contents:
    
        if details["name"] == "Prog2":
        
            sprites = icarus.Sprites(details["data"])
            
            for name, sprite in sprites.sprites.items():
                sprite.image().save(os.path.join(output_dir, name + ".png"))
        
        elif details["name"].startswith("DECK"):
        
            level = icarus.Level(details["data"])
            n = ord(details["name"][4:]) - 65
            
            # Read the wall tile for the level.
            level.wall_sprite.image().save(os.path.join(output_dir, "%i.png" % n))
    
    sys.exit()
