#!/usr/bin/env python

"""
imagemap.py - Save a representation of a Icarus level to a PNG file.

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
import icarus

tile_map = {
 0x01: ("blank", 0),
 0x02: ("vending", 0),
 0x0b: ("beam", 0),
 0x20: ("robot_left", 0),
 0x46: ("lift", 0),
 0x5d: ("wall3", 0),
 0x5e: ("wall4", 1),
 0x5f: ("wall3", 2),
 0x60: ("wall4", 3),
 0x63: ("crate", 0),
 0x64: ("breakable0", 0),
 0x65: ("breakable0", 0),
 0x66: ("breakable0", 0),
 0x67: ("breakable1", 0),
 0x68: ("breakable1", 0),
 0x69: ("breakable1", 0),
 0x6a: ("breakable2", 0),
 0x6b: ("breakable2", 0),
 0x6c: ("breakable2", 0),
 0x6d: ("breakable3", 0),
 0x6e: ("breakable3", 0),
 0x6f: ("breakable3", 0),    # destructable block (almost destroyed)
 0xcf: ("switch", 0),    # switches
 0xd0: ("switch", 0),    # 2
 0xd1: ("switch", 0),    # 3
 0xd2: ("switch", 0),    # 4
 0xd9: ("door1", 0),    # door labels
 0xda: ("door2", 0),
 0xdb: ("door3", 0),
 0xdc: ("door4", 0),
 0xdd: ("door5", 0),
 0xde: ("door6", 0),
 0xdf: ("card1", 0),    # access cards
 0xe0: ("card2", 0),
 0xe1: ("card3", 0),
 0xe2: ("card4", 0),
 0xe3: ("card5", 0),
 0xe4: ("card6", 0),
 0xe6: ("one_way_up", 0),    # one-way doors
 0xe7: ("one_way_left", 1), # right
 0xe8: ("one_way_up", 2), # down
 0xe9: ("one_way_left", 0), # left
 0xea: ("mine_inactive", 0),    # mine
 0xeb: ("v_pipe", 0),    # vertical pipe
 0xec: ("h_pipe", 0),    # horizontal pipe
 0xed: ("tl_pipe", 0),    # top-left pipe
 0xee: ("tl_pipe", 1),   # top-right pipe
 0xef: ("tl_pipe", 3),    # bottom-right pipe
 0xf0: ("tl_pipe", 2),   # bottom-left pipe
 0xf1: ("emitter_up", 0),    # beam nozzle (facing up)
 0xf2: ("emitter_left", 1),    # beam nozzle (facing right)
 0xf3: ("emitter_up", 2),    # beam nozzle (facing down)
 0xf4: ("emitter_left", 0),    # beam nozzle (facing left)
 0xf7: ("h_door", 0),
 0xf8: ("v_door", 0),
 0xf9: ("armour", 0),
 0xfa: ("weapon", 0),
 0xfb: ("recharge", 0),
 0xfe: ("credit", 0),
 0xfd: ("exit_closed", 0)
    }

raw_numbers = [
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
    "        "
    ]

def get_image(level, sprites, row, column, tile_size):

    tile = level.tiles[row][column]
    
    if column == level.player_x:
        if level.player_y <= row <= level.player_y + 1:
            return sprites.sprites["player_left0"].image(size = tile_size)
    
    if tile == 0:
        return level.wall_sprite.image(size = tile_size)
    else:
        image_name, orientation = tile_map[tile]
        im = sprites.sprites[image_name].image(size = tile_size)
        if orientation & 1:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        if orientation & 2:
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
        return im


if __name__ == "__main__":

    if not 4 <= len(sys.argv) <= 5:
    
        sys.stderr.write("Usage: %s <Icarus UEF file> <level> <output file name> [scale]\n" % sys.argv[0])
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
    if not 1 <= level_number <= 20:
    
        sys.stderr.write("Please specify a level from 1 to 20.\n")
        sys.exit(1)
    
    u = UEFfile.UEFfile(sys.argv[1])
    output_file_name = sys.argv[3]
    
    for details in u.contents:
    
        if details["name"] == "Prog2":
            sprites = icarus.Sprites(details["data"])
        
        elif details["name"] == "DECK%s" % chr(64 + level_number):
            break
    else:
        sys.stderr.write("Failed to find a suitable data file.\n")
        sys.exit(1)
    
    numbers = {}
    
    for i, n in enumerate(raw_numbers):
        n = n.replace(" ", "\x00").replace("1", "\x02")
        im = Image.fromstring("P", (8, 10), n)
        im.putpalette((0,0,0, 255,0,0, 255,255,255, 0,255,255))
        numbers[i] = im
    
    level = icarus.Level(details["data"])
    
    level_image = Image.new("P", (32 * tile_size[0], 32 * tile_size[1]), 0)
    level_image.putpalette((0,0,0, 255,0,0, 255,255,255, 0,255,255))
    
    for row in range(32):
    
        for column in range(32):
        
            im = get_image(level, sprites, row, column, tile_size)
            level_image.paste(im, (column * tile_size[0], row * tile_size[1]))
    
    for row in range(32):
    
        for column in range(32):
        
            tile = level.tiles[row][column]
            
            if 0xcf <= tile <= 0xd2:
            
                number_im = numbers[tile - 0xcf]
                level_image.paste(number_im, (
                    (column * tile_size[0]) + im.size[0]/2 - number_im.size[0]/2,
                    (row * tile_size[1]) + im.size[1] - number_im.size[1]/2 - 2))
    
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
