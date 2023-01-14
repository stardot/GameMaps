"""
sprites.py - Sprite reading classes for Clogger.

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

class Sprites:

    # Offsets into the sprite data for the 8 byte pieces of each sprite.
    # For the blank piece, I just chose a blank area in the file data.
    
    sprite_table = {
        0x00: (0x3c0, 0x3c0, 0x3c0, 0x3c0,
               0x3c0, 0x3c0, 0x3c0, 0x3c0,
               0x3c0, 0x3c0, 0x3c0, 0x3c0,
               0x3c0, 0x3c0, 0x3c0, 0x3c0),
        0x01: (0x2f0, 0x2f8, 0x2f0, 0x2f8,
               0x2f0, 0x2f8, 0x2f0, 0x2f8,
               0x2f0, 0x2f8, 0x2f0, 0x2f8,
               0x2f0, 0x2f8, 0x2f0, 0x2f8),
        0x02: (0x300, 0x308, 0x300, 0x308,
               0x2f0, 0x2f8, 0x2f0, 0x2f8,
               0x2f0, 0x2f8, 0x2f0, 0x2f8,
               0x2f0, 0x2f8, 0x2f0, 0x2f8),
        0x03: (0x300, 0x308, 0x300, 0x310,
               0x2f0, 0x2f8, 0x2f0, 0x2f8,
               0x2f0, 0x2f8, 0x2f0, 0x2f8,
               0x2f0, 0x2f8, 0x2f0, 0x2f8),
        0x04: (0x318, 0x308, 0x300, 0x308,
               0x2f0, 0x2f8, 0x2f0, 0x2f8,
               0x2f0, 0x2f8, 0x2f0, 0x2f8,
               0x2f0, 0x2f8, 0x2f0, 0x2f8),
        0x05: (0x318, 0x308, 0x300, 0x310,
               0x2f0, 0x2f8, 0x2f0, 0x2f8,
               0x2f0, 0x2f8, 0x2f0, 0x2f8,
               0x2f0, 0x2f8, 0x2f0, 0x2f8),
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
               0x3c0, 0x1e8, 0x208, 0x3c0),
        0xff: (0x60, 0x40, 0x20, 0x00,
               0x68, 0x48, 0x28, 0x08,
               0x70, 0x50, 0x30, 0x10,
               0x78, 0x58, 0x38, 0x18)
        }
    
    tile_width = 16
    tile_height = 32
    
    def __init__(self, data):
    
        self.data = data
    
    def read_sprite(self, level, number):
    
        offsets = self.sprite_table[number]
        
        if level % 2 == 1 and 1 <= number <= 5:
            offsets = map(lambda x: x + 0x30, offsets)
        
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


class Puzzle(Sprites):

    blocks = {
        0x00: 0xabd + 0x3c0,    # black
        0x08: 0xabd + 0x038,
        0x09: 0xabd + 0x040,
        0x0a: 0xabd + 0x048,    # light blue
        0x45: 0xabd + 0x220,    # red
        0x46: 0xabd + 0x228,    # blue
        0x47: 0xabd + 0x230,
        0x48: 0xabd + 0x238,
        0x49: 0xabd + 0x240,    # dark blue
        0x4a: 0xabd + 0x248,    # yellow
        0x4e: 0xabd + 0x268,
        0x4f: 0xabd + 0x270
        }
    
    columns = 7
    rows = 3
    
    block_width = 4
    block_height = 8
    
    def __init__(self, data):
    
        self.data = data
    
    def read_sprite(self, level, number):
    
        start = 0x3a5 + (level * 21 * 16) + (number * 16)
        
        columns = []
        for j in range(4):
        
            column = []
            for k in range(4):
            
                value = ord(self.data[start + (j * 4) + k])
                
                # Read a list of rows for this block of data.
                try:
                    offset = self.blocks[value]
                except KeyError:
                    print "No definition for value: %02x" % value
                    offset = self.blocks[0x00]
                
                column += self.read_block(offset)
            
            # Append the column of rows to the list of columns.
            columns.append(column)
        
        # Combine corresponding rows from all the columns to create the whole
        # piece.
        piece = []
        for row in zip(*columns):
            piece.append("".join(row))
        
        return "".join(piece)
    
    def read_block_number(self, level, number, c, r):
    
        start = 0x3a5 + (level * 21 * 16) + (number * 16)
        
        return ord(self.data[start + (c * 4) + r])
    
    def write_block_number(self, level, number, c, r, value):
    
        start = 0x3a5 + (level * 21 * 16) + (number * 16)
        offset = start + (c * 4) + r
        
        self.data[offset] = chr(value)
