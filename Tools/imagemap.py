#!/usr/bin/env python

"""
imagemap.py - Save a representation of a Dunjunz level to a PNG file.

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
import Image
import UEFfile
import dunjunz

type_map = {
    0x28: "treasure",
    0x29: "food",
    0x2a: "crucifix",
    0x2b: "teleport",
    0x51: "exit",
    0x53: "drainer",
    0x5f: "boots",
    0x60: "armour",
    0x61: "potion",
    0x62: "weapons",
    0x63: "dagger"
    }

def get_image_name(level, level_number, row, column):

    if (row, column) == (11, 11):
        return "ranger_up1", None
    elif (row, column) == (12, 11):
        return "wizard_right1", None
    elif (row, column) == (11, 12):
        return "barbarian_down1", None
    elif (row, column) == (12, 12):
        return "fighter_left1", None
    
    elif (column, row) in level.keys:
        n = level.keys[(column, row)]
        return "key", n
    
    elif (column, row) in level.trapdoors:
        return "trapdoor", None
    
    elif level.is_solid(row, column):
        if (column, row) in level.doors:
            n, o = level.doors[(column, row)]
            if o == 0x1d:
                return "v_door", n
            else:
                return "h_door", n
        else:
            return level_number, None
    
    elif level.is_collectable(row, column) and \
         (column, row) in level.lookup:
    
        name = type_map[level.lookup[(column, row)]]
        if name == "teleport":
            return name, level.teleporters.index((column, row)) + 1
        else:
            return name, None
    
    else:
        return "blank", None


raw_numbers = [
    "        "
    "  1111  "
    " 1    1 "
    "1      1"
    "1      1"
    "1      1"
    "1      1"
    " 1    1 "
    "  1111  "
    "        ",
    
    "        "
    "   11   "
    "  111   "
    "   11   "
    "   11   "
    "   11   "
    "   11   "
    "   11   "
    " 111111 "
    "        ",
    
    "        "
    "  1111  "
    " 1    1 "
    "     1  "
    "    1   "
    "   1    "
    "  1     "
    " 1      "
    " 111111 "
    "        ",
    
    "        "
    "  1111  "
    " 1    1 "
    "      1 "
    "   111  "
    "      1 "
    "      1 "
    " 1    1 "
    "  1111  "
    "        ",
    
    "        "
    "    1   "
    "   11   "
    "  1 1   "
    " 1  1   "
    "1111111 "
    "    1   "
    "    1   "
    "    1   "
    "        ",
    
    "        "
    " 111111 "
    " 1      "
    " 1      "
    " 11111  "
    "      1 "
    "      1 "
    " 1    1 "
    "  1111  "
    "        ",
    
    "        "
    "   111  "
    "  1     "
    " 1      "
    " 11111  "
    " 1    1 "
    " 1    1 "
    " 1    1 "
    "  1111  "
    "        ",
    
    "        "
    " 1111111"
    "       1"
    "      1 "
    "     1  "
    "    1   "
    "   1    "
    "  1     "
    " 1      "
    "        ",
    
    "        "
    "  1111  "
    " 1    1 "
    " 1    1 "
    "  1111  "
    " 1    1 "
    " 1    1 "
    " 1    1 "
    "  1111  "
    "        ",
    
    "        "
    "  1111  "
    " 1    1 "
    " 1    1 "
    "  11111 "
    "      1 "
    "      1 "
    " 1    1 "
    "  1111  "
    "        "
    ]

if __name__ == "__main__":

    if not 4 <= len(sys.argv) <= 5:
    
        sys.stderr.write("Usage: %s <Dunjunz UEF file> <level> <output file name> [scale]\n" % sys.argv[0])
        sys.exit(1)
    
    elif len(sys.argv) == 5:
        try:
            scale = float(sys.argv[4])
            if scale <= 0.0 or scale > 2.0:
                raise ValueError
        
        except ValueError:
            sys.stderr.write("Invalid scale specified. Must be 0.0 < scale <= 2.0.\n")
            sys.exit(1)
    else:
        scale = 1
    
    tile_size = (32, 24)
    
    level_number = int(sys.argv[2])
    if not 1 <= level_number <= 25:
    
        sys.stderr.write("Please specify a level from 1 to 25.\n")
        sys.exit(1)
    
    u = UEFfile.UEFfile(sys.argv[1])
    output_file_name = sys.argv[3]
    
    for details in u.contents:
    
        if details["name"] == "Dunjunz":
            sprites = dunjunz.Sprites(details["data"])
        
        elif details["name"] == "Level%i" % level_number:
            break
    else:
        sys.stderr.write("Failed to find a suitable data file.\n")
        sys.exit(1)
    
    numbers = {}
    
    for i, n in enumerate(raw_numbers):
        n = n.replace(" ", "\x00").replace("1", "\x02")
        im = Image.fromstring("P", (8, 10), n)
        im.putpalette((0,0,0, 255,0,0, 0,255,0, 255,255,255))
        numbers[i] = im
    
    level = dunjunz.Level(details["data"])
    
    level_image = Image.new("P", (32 * tile_size[0], 48 * tile_size[1]), 0)
    level_image.putpalette((0,0,0, 255,0,0, 0,255,0, 255,255,255))
    
    for row in range(48):
    
        for column in range(32):
        
            image_name, extra = get_image_name(level, level_number, row, column)
            
            if image_name == level_number:
                im = level.wall_sprite.image(size = tile_size)
            else:
                im = sprites.sprites[image_name].image(size = tile_size)
            
            level_image.paste(im, (column * tile_size[0], row * tile_size[1]))
            
    for row in range(48):
    
        for column in range(32):
        
            image_name, extra = get_image_name(level, level_number, row, column)
            
            if extra != None:
            
                ox = -8
                while extra > 0:
                    number_im = numbers[extra % 10]
                    ox -= number_im.size[0]
                    level_image.paste(number_im, (
                        (column * tile_size[0]) + im.size[0] + ox,
                        (row * tile_size[1]) + im.size[1] - number_im.size[1]/2))
                    
                    extra = extra / 10
    
    if scale != 1:
        i = int(scale)
        
        if scale != i or scale < 1:
            level_image = level_image.convert("RGB")
        else:
            while i & 1 == 0:
                i = i >> 1
            
            # The lowest bit is 1. Remove it and check for other bits.
            i = i >> 1
            if i & 1 != 0:
                # Not a multiple of 2, so convert the image to RGB format.
                level_image = level_image.convert("RGB")
        
        level_image = level_image.resize((int(level_image.size[0] * scale),
                                          int(level_image.size[1] * scale)),
                                         Image.ANTIALIAS)
    
    level_image.save(output_file_name)
    
    sys.exit()
