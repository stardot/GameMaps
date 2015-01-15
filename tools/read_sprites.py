#!/usr/bin/env python

"""
read_sprites.py - A tool for exporting the sprites from Repton.

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
import UEFfile
import Image

class Reader:

    # Offsets into the sprite data for the 8 byte pieces of each sprite.
    # For the blank piece, I just chose a blank area in the file data.
    
    sprite_table = {
        0x00: (0x3c0, 0x3c0, 0x3c0, 0x3c0,
               0x3c0, 0x3c0, 0x3c0, 0x3c0,
               0x3c0, 0x3c0, 0x3c0, 0x3c0,
               0x3c0, 0x3c0, 0x3c0, 0x3c0),
        0x01: (0x000, 0x008, 0x000, 0x008,
               0x000, 0x008, 0x000, 0x008,
               0x000, 0x008, 0x000, 0x008,
               0x000, 0x008, 0x000, 0x008),
        0x02: (0x010, 0x018, 0x010, 0x018,
               0x000, 0x008, 0x000, 0x008,
               0x000, 0x008, 0x000, 0x008,
               0x000, 0x008, 0x000, 0x008),
        0x03: (0x010, 0x018, 0x010, 0x020,
               0x000, 0x008, 0x000, 0x008,
               0x000, 0x008, 0x000, 0x008,
               0x000, 0x008, 0x000, 0x008),
        0x04: (0x028, 0x018, 0x010, 0x018,
               0x000, 0x008, 0x000, 0x008,
               0x000, 0x008, 0x000, 0x008,
               0x000, 0x008, 0x000, 0x008),
        0x05: (0x028, 0x018, 0x010, 0x020,
               0x000, 0x008, 0x000, 0x008,
               0x000, 0x008, 0x000, 0x008,
               0x000, 0x008, 0x000, 0x008),
        0x06: (0x030, 0x030, 0x030, 0x030,
               0x030, 0x030, 0x030, 0x030,
               0x030, 0x030, 0x030, 0x030,
               0x030, 0x030, 0x030, 0x030),
        0x07: (0x250, 0x250, 0x250, 0x250,
               0x250, 0x250, 0x250, 0x250,
               0x250, 0x250, 0x250, 0x250,
               0x250, 0x250, 0x250, 0x250),
        0x08: (0x258, 0x258, 0x258, 0x258,
               0x258, 0x258, 0x258, 0x258,
               0x258, 0x258, 0x258, 0x258,
               0x258, 0x258, 0x258, 0x258),
        0x09: (0x278, 0x278, 0x278, 0x278,
               0x278, 0x278, 0x278, 0x278,
               0x278, 0x278, 0x278, 0x278,
               0x278, 0x278, 0x278, 0x278),
        0x0a: (0x260, 0x260, 0x260, 0x260,
               0x260, 0x260, 0x260, 0x260,
               0x260, 0x260, 0x260, 0x260,
               0x260, 0x260, 0x260, 0x260),
        0x0b: (0x050, 0x050, 0x050, 0x050,
               0x050, 0x050, 0x050, 0x050,
               0x050, 0x050, 0x050, 0x050,
               0x050, 0x050, 0x050, 0x050),
        0x0c: (0x058, 0x058, 0x058, 0x058,
               0x058, 0x058, 0x058, 0x058,
               0x058, 0x058, 0x058, 0x058,
               0x058, 0x058, 0x058, 0x058),
        0x0d: (0x3c0, 0x3c8, 0x3c0, 0x3c0,
               0x0d8, 0x0d0, 0x0c8, 0x0c0,
               0x0f8, 0x0f0, 0x0e8, 0x0e0,
               0x118, 0x110, 0x108, 0x100),
        0x0e: (0x3c0, 0x280, 0x288, 0x290,
               0x298, 0x2a0, 0x2a8, 0x2b0,
               0x2b8, 0x2c0, 0x2c8, 0x2d0,
               0x2d8, 0x2e0, 0x2e8, 0x3c0),
        0x0f: (0x3c0, 0x3c0, 0x3c0, 0x3c0,
               0x3c0, 0x3c0, 0x3c0, 0x3c0,
               0x3c0, 0x3c0, 0x3c0, 0x3c0,
               0x060, 0x060, 0x060, 0x060),
        0x26: (0x3c0, 0x3c0, 0x3c0, 0x068,
               0x078, 0x3c0, 0x3c0, 0x070,
               0x098, 0x090, 0x088, 0x080,
               0x0b8, 0x0b0, 0x0a8, 0x0a0),
        0x27: (0x120, 0x3c0, 0x3c0, 0x130,
               0x120, 0x128, 0x128, 0x130,
               0x120, 0x128, 0x128, 0x130,
               0x120, 0x3c0, 0x3c0, 0x130),
        0x28: (0x138, 0x3c0, 0x3c0, 0x120,
               0x138, 0x128, 0x128, 0x120,
               0x138, 0x128, 0x128, 0x120,
               0x138, 0x3c0, 0x3c0, 0x120),
        0x29: (0x140, 0x160, 0x180, 0x1a0,
               0x148, 0x168, 0x188, 0x1a8,
               0x150, 0x170, 0x190, 0x1b0,
               0x158, 0x178, 0x198, 0x1b8),
        0x2a: (0x3c0, 0x1d0, 0x1f0, 0x3c0,
               0x1c0, 0x1d8, 0x1f8, 0x210,
               0x1c8, 0x1e0, 0x200, 0x218,
               0x3c0, 0x1e8, 0x208, 0x3c0)
        }
    
    def __init__(self, data):
    
        self.data = data
    
    def read_sprite(self, number):
    
        offsets = self.sprite_table[number]
        
        columns = []
        for i in range(4):
            columns.append(sum(map(self.read_block, offsets[i::4]), []))
        
        sprite = []
        for pieces in zip(*columns):
            sprite += "".join(pieces)

        sprite = "".join(sprite)
        return sprite
    
    def read_block(self, offset):
    
        rows = []
        
        for i in range(8):
        
            byte = self.data[offset + i]
            rows.append(self.read_columns(byte))
        
        return rows
    
    def read_columns(self, byte):
    
        columns = []
        byte = ord(byte)
        for i in range(4):
        
            v = (byte & 0x01) | ((byte & 0x10) >> 3)
            byte = byte >> 1
            columns.append(v)
        
        columns.reverse()
        return "".join(map(chr, columns))


def read_puzzle(data):

    sprite = []
    blocks = []
    
    for i in range(21):
    
        block = ["", "", "", ""]
        for j in range(4):
        
            for k in range(4):
            
                value = ord(data[(i * 16) + (j * 4) + k])
                
                if value == 0:
                    block[k] += "  "
                else:
                    block[k] += "%02x" % value
        
        blocks.append(block)
    
    for i in range(0, 3):
    
        for pieces in zip(*blocks[i*7:(i+1)*7]):
        
            print "".join(pieces)


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
    
    reader = Reader(details["data"][0xabd:])
    
    for key in reader.sprite_table.keys():
    
        sprite = reader.read_sprite(key)
            
        im = Image.fromstring("P", (16, 32), sprite)
        im.putpalette((0,0,0, 255,0,0, 0,255,0, 0,0,255))
        im.save(os.path.join(output_dir, "%02i.png" % key))
    
    for puzzle in range(5):
        puzzle_start = 0x3a5 + (puzzle * 21 * 16)
        puzzle_finish = 0x3a5 + ((puzzle + 1) * 21 * 16)
        read_puzzle(details["data"][puzzle_start:puzzle_finish])
        print
    
    sys.exit()
