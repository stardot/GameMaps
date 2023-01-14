#!/usr/bin/env python

"""
textmap.py - A tool for exporting the levels from BoneCruncher as text.

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

import sys
from BoneCruncher import IncorrectSize, NotFound, BoneCruncher

chars = {
    0: " ",
    1: "-",
    2: "|",
    3: "+",
    4: "c",
    5: "d",
    6: "k",
    7: ".",
    8: "x",     # Trapdoor
    9: "~",
 0x0a: "O",
 0x0b: "$",
 0x0c: "m",     # Monster
 0x0d: "S",
 0x0e: "?",
 0x0f: "F",     # Fozzy
 0x1f: ">",
 0x2f: "<",
 0x3f: "^",
 0x4f: "v",
 0x5f: "B",     # Bono
 0x6f: "A",     # Volcano
    }


if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <BoneCruncher UEF file> <level number>\n" % sys.argv[0])
        sys.exit(1)
    
    uef_file = sys.argv[1]
    
    try:
        level = int(sys.argv[2])
        if not 1 <= level <= 30:
            raise ValueError
    
    except ValueError:
        sys.stderr.write("The level number must be an integer from 1 to 30.\n")
        sys.exit(1)
    
    try:
        r = BoneCruncher(uef_file)
    except NotFound:
        sys.stderr.write("Failed to find the required file in the specified file: %s\n" % uef_file)
        sys.exit(1)
    except IncorrectSize:
        sys.stderr.write("The required file was not the expected size.\n")
        sys.exit(1)
    
    level = r.read_levels()[level - 1]
    
    for row in range(25):
    
        for column in range(40):

            value = level[row][column]
            
            try:
                char = chars[value]
                sys.stdout.write(char)
            except KeyError:
                sys.stdout.write("%01x" % (value >> 4))
        
        print
    
    sys.exit()
