#!/usr/bin/env python

"""
textmap.py - A tool for exporting the levels from Clogger as text.

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

import sys
import UEFfile

chars = {
    0x00: "  ", # blank
    0x01: "ww", # wall
    0x02: "--", # wall with flat top
    0x03: "-\\",# wall with flat top and curved right
    0x04: "/-", # wall with flat top and curved left
    0x05: "/\\",# wall with flat top and curved left and right
    0x06: ",,", # blue earth
    0x07: ",,", # blue earth
    0x08: "..", # yellow earth
    0x09: "..", # RGB earth
    0x0a: "..", # green earth
    0x0b: ">>", # spring (can be entered from the right)
    0x0c: "<<", # spring (can be entered from the left)
    0x0d: "pp", # pie
    0x0e: "aa", # apple
    0x0f: "gg", # grass
    0x25: "m>", # mower (right facing, never used)
    0x26: "<m", # mower (left facing)
    0x27: "d>", # drill (right facing)
    0x28: "<d", # drill (left facing)
    0x29: "GG", # gyroscope
    0x2a: "bb", # buffer
    }


if __name__ == "__main__":

    if len(sys.argv) != 4:
    
        sys.stderr.write("Usage: %s <Clogger UEF file> <file name> <level number>\n" % sys.argv[0])
        sys.exit(1)
    
    uef_file = sys.argv[1]
    level_file = sys.argv[2]
    
    try:
        level = int(sys.argv[3])
        if not 1 <= level <= 5:
            raise ValueError
    
    except ValueError:
        sys.stderr.write("The level number must be an integer from 1 to 4.\n")
        sys.exit(1)
    
    uef = UEFfile.UEFfile(uef_file)
    for details in uef.contents:
        if details["name"] == level_file:
            break
    else:
        sys.stderr.write("Failed to find the '%s' file in the UEF file.\n" % level_file)
        sys.exit(1)
    
    level_start = 0xf7d + ((level - 1) * 32 * 32)
    level_finish = 0xf7d + (level * 32 * 32)
    level = details["data"][level_start:level_finish]
    
    for row in range(32):
    
        for column in range(32):

            value = ord(level[(row * 32) + column])
            
            try:
                char = chars[value]
                sys.stdout.write(char)
            except KeyError:
                sys.stdout.write("%02x" % value)
        
        print
    
    sys.exit()
