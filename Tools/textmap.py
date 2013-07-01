#!/usr/bin/env python

"""
textmap.py - A tool for exporting the levels from Ravenskull as text.

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
from Ravenskull import IncorrectSize, NotFound, Ravenskull

chars = {
    0x0: " ",
    0x1: "~",
    0x2: "#",
    0x3: "X",   # spiked gate
    0x4: "O",
    0x5: "+",   # sarcophagus
    0x6: "\\",  # upper-right wall
    0x7: "/",   # upper-left wall
    0x8: "\\",  # lower-left wall
    0x9: "/",   # lower-right wall
    0xa: "|",   # door
    0xb: "%",   # brick wall
    0xc: "x",   # acid pool
    0xd: "@",   # green wall
    0xe: "*",   # decorative wall
    0xf: "$",   # treasure
    }

type_map = {
    0x0: "gold key",
    0x1: "scroll",
    0x2: "pickaxe",
    0x3: "detonator",
    0x4: "dynamite",
    0x5: "spade",
    0x6: "rusty key",
    0x7: "silver key",
    0x8: "upper-left crucifix",
    0x9: "lower-left crucifix",
    0xa: "lower-right crucifix",
    0xb: "upper-right crucifix",
    0xc: "potion",
    0xd: "scythe",
    0xe: "fish",
    0xf: "wine",
    0x10: "fine bone",
    0x11: "empty glass",
    0x12: "compass",
    0x13: "hand-axe",
    0x14: "cake",
    0x15: "bell",
    0x16: "bow & arrow"
    }

if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <Ravenskull UEF file> <level number>\n" % sys.argv[0])
        sys.exit(1)
    
    uef_file = sys.argv[1]
    
    try:
        level_number = int(sys.argv[2])
        if not 1 <= level_number <= 4:
            raise ValueError
    
    except ValueError:
        sys.stderr.write("The level number must be an integer from 1 to 4.\n")
        sys.exit(1)
    
    try:
        r = Ravenskull(uef_file)
    except NotFound:
        sys.stderr.write("Failed to find the required file in the specified file: %s\n" % uef_file)
        sys.exit(1)
    except IncorrectSize:
        sys.stderr.write("The required file was not the expected size.\n")
        sys.exit(1)
    
    levels, all_items = r.read_levels()
    level = levels[level_number - 1]
    items = all_items[level_number - 1]
    special = {}
    
    for row, column in items.keys():
    
        type, y, x = items[(row, column)]
        special[(row, column)] = type
        special[(y, x)] = type
    
    for row in range(64):
    
        row_items = []
        
        for column in range(64):
        
            drow = 61 - row
            dcolumn = column - 3
            if (drow, dcolumn) in special:
                type = special[(drow, dcolumn)]
                sys.stdout.write("i")
                row_items.append("%02x" % type)
                continue
            
            value = level[row][column]
            
            try:
                char = chars[value]
                sys.stdout.write(char)
            except KeyError:
                sys.stdout.write("%01x" % value)
        
        if row_items:
            print " items:", ",".join(row_items)
        else:
            print
    
    inventory = []
    for r, c in items.keys():
        type, y, x = items[(r, c)]
        inventory.append((type, c, r, x, y))
    
    inventory.sort()
    for type, c, r, x, y in inventory:
        print type_map.get(type, "unknown"), "(%i)" % type, "at (%i, %i)" % (c, r),
        if type == 0:
            print "with door at (%i, %i)" % (x, y)
        elif type == 1:
            if y == 255:
                print "of type", y, x
            else:
                print "with target at (%i, %i)" % (x, y)
        elif type == 2:
            if y & 0x80:
                print "(already used)"
            else:
                print "(unused)"
        else:
            print "with", y, x
    
    sys.exit()
