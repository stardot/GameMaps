#!/usr/bin/env python

"""
textmap.py - Print a textual representation of a Dunjunz level.

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

import sys
import UEFfile
import dunjunz

type_map = {
    0x28: "T", # Treasure
    0x29: "F", # Food
    0x2a: "+", # Crucifix
    0x2b: "X", # Teleporter - transports to the square above the next in the list
    0x51: "E", # Exit
    0x53: "*", # Energy drainer
    0x5f: "B", # Boots of speed
    0x60: "A", # Armour
    0x61: "P", # Potion
    0x62: "W", # Weapons pile
    0x63: "D"  # Dagger (+1 damage)
    }

if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <Dunjunz UEF file> <level>\n" % sys.argv[0])
        sys.exit(1)
    
    level = int(sys.argv[2])
    if not 1 <= level <= 25:
    
        sys.stderr.write("Please specify a level from 1 to 25.\n")
        sys.exit(1)
    
    u = UEFfile.UEFfile(sys.argv[1])
    
    for details in u.contents:
    
        if details["name"] == "Level%i" % level:
            break
    else:
        sys.stderr.write("Failed to find a suitable data file.\n")
        sys.exit(1)
    
    level = dunjunz.Level(details["data"])
    
    for row in range(48):
    
        for column in range(32):
        
            if 11 <= row <= 12 and 11 <= column <= 12:
                sys.stdout.write("S")
            
            elif (column, row) in level.keys:
                n = level.keys[(column, row)]
                sys.stdout.write("k")
            
            elif (column, row) in level.trapdoors:
                sys.stdout.write("O")
            
            elif level.is_solid(row, column):
                if (column, row) in level.doors:
                    doors = level.doors[(column, row)]
                    # Just use the appropriate sprite for the first door found.
                    n, o = doors[0]
                    if o == 0x1d:
                        sys.stdout.write("-")
                    else:
                        sys.stdout.write("|")
                else:
                    sys.stdout.write("#")
            
            elif level.is_collectable(row, column):
                if (column, row) in level.lookup:
                    t = level.lookup[(column, row)]
                    sys.stdout.write(type_map[t])
                else:
                    sys.stdout.write("!")
            else:
                sys.stdout.write(" ")
        
        sys.stdout.write("\n")
    
    sys.exit()
