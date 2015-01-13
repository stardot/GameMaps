#!/usr/bin/env python

"""
sprites.py - A module for exporting raw sprite data from Repton.

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

class Reader:

    # Offsets into the sprite data for the top-left, top-right, bottom-left and
    # bottom-right 8 byte pieces of each sprite. For the blank piece, I just chose
    # a blank area in the file data.
    
    sprite_table = [
        (0x6a0, 0x6a0, 0x6a0, 0x6a0),   # blank
        (0x110, 0x118, 0x120, 0x128),   # diamond
        (0x130, 0x138, 0x140, 0x148),   # boulder
        (0x150, 0x158, 0x160, 0x168),   # egg
        (0x170, 0x178, 0x180, 0x188),   # key
        (0x108, 0x108, 0x108, 0x108),   # earth
        (0x0f0, 0x0f8, 0x100, 0x0f0),   # earth
        (0x0f8, 0x0f0, 0x0f0, 0x100),   # earth
        (0x0d0, 0x0d8, 0x0e0, 0x0e8),   # safe
        (0x050, 0x050, 0x050, 0x050),   # brick wall
        (0x0b0, 0x0b8, 0x0b0, 0x0b8),   # double (top/bottom) wall
        (0x0a0, 0x0a0, 0x0a8, 0x0a8),   # double (left/right) wall
        (0x000, 0x008, 0x008, 0x000),   # quadruple wall
        (0x0c0, 0x0c8, 0x0c0, 0x0c8),   # fancy wall
        (0x098, 0x098, 0x098, 0x098),   # smooth wall
        (0x098, 0x098, 0x078, 0x078),   # lower edged smooth wall
        (0x060, 0x060, 0x098, 0x098),   # upper edged smooth wall
        (0x098, 0x090, 0x098, 0x090),   # right edged smooth wall
        (0x088, 0x098, 0x088, 0x098),   # left edged smooth wall
        (0x098, 0x090, 0x078, 0x080),   # lower right curved smooth wall
        (0x088, 0x098, 0x070, 0x078),   # lower left curved smooth wall
        (0x060, 0x068, 0x098, 0x090),   # upper right curved smooth wall
        (0x058, 0x060, 0x088, 0x098),   # upper left curved smooth wall
        (0x190, 0x198, 0x1a0, 0x1a8),   # map
        (0x050, 0x050, 0x030, 0x030),   # lower edged brick wall
        (0x018, 0x018, 0x050, 0x050),   # upper edged brick wall
        (0x050, 0x048, 0x050, 0x048),   # right edged brick wall
        (0x040, 0x050, 0x040, 0x050),   # left edged brick wall
        (0x050, 0x048, 0x030, 0x038),   # lower right curved brick wall
        (0x040, 0x050, 0x028, 0x030),   # lower left curved brick wall
        (0x018, 0x020, 0x050, 0x048),   # upper right curved brick wall
        (0x010, 0x018, 0x040, 0x050),   # upper left curved brick wall
        ]
    
    def __init__(self, data):
    
        self.data = data
    
    def read_sprite(self, offsets):
    
        lefts = sum(map(self.read_block, offsets[::2]), [])
        rights = sum(map(self.read_block, offsets[1::2]), [])
        
        sprite = []
        for left, right in zip(lefts, rights):
            sprite += left + right

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


class BBCReader(Reader):

    # Offsets into the sprite data for the 8 byte pieces of each sprite.
    # For the blank piece, I just chose a blank area in the file data.
    
    sprite_table = [
        (0x6a0, 0x6a0, 0x6a0, 0x6a0,
         0x6a0, 0x6a0, 0x6a0, 0x6a0,
         0x6a0, 0x6a0, 0x6a0, 0x6a0,
         0x6a0, 0x6a0, 0x6a0, 0x6a0),   # blank
        (0x6a0, 0x0e0, 0x0e8, 0x6a0,
         0x0e0, 0x100, 0x108, 0x0e8,
         0x0f0, 0x108, 0x100, 0x0f8,
         0x6a0, 0x0f0, 0x0f8, 0x6a0),   # diamond
        (0x000, 0x008, 0x010, 0x018,
         0x140, 0x148, 0x150, 0x158,
         0x280, 0x288, 0x290, 0x298,
         0x3c0, 0x3c8, 0x3d0, 0x3d8),   # boulder
        (0x020, 0x028, 0x030, 0x038,
         0x160, 0x168, 0x170, 0x178,
         0x2a0, 0x2a8, 0x2b0, 0x2b8,
         0x3e0, 0x3e8, 0x3f0, 0x3f8),   # egg
        (0x040, 0x048, 0x050, 0x058,
         0x180, 0x188, 0x190, 0x198,
         0x2c0, 0x2c8, 0x2d0, 0x2d8,
         0x400, 0x408, 0x410, 0x418),   # key
        (0x110, 0x118, 0x120, 0x128,
         0x130, 0x138, 0x128, 0x130,
         0x110, 0x120, 0x138, 0x138,
         0x128, 0x110, 0x120, 0x130),   # earth
        (0x138, 0x110, 0x120, 0x138,
         0x118, 0x128, 0x118, 0x110,
         0x138, 0x120, 0x110, 0x138,
         0x110, 0x118, 0x130, 0x128),   # earth
        (0x110, 0x118, 0x120, 0x128,
         0x130, 0x138, 0x118, 0x130,
         0x110, 0x120, 0x118, 0x138,
         0x128, 0x110, 0x120, 0x130),   # earth
        (0x1b8, 0x1c0, 0x1c0, 0x1c8,
         0x1d0, 0x1d8, 0x1d8, 0x1e0,
         0x1d0, 0x1d8, 0x1d8, 0x1e0,
         0x1e8, 0x1f0, 0x1f0, 0x1f8),   # safe
        (0x200, 0x208, 0x200, 0x208,
         0x200, 0x208, 0x200, 0x208,
         0x200, 0x208, 0x200, 0x208,
         0x200, 0x208, 0x200, 0x208),   # brick wall
        (0x088, 0x080, 0x080, 0x090,
         0x098, 0x070, 0x070, 0x0a0,
         0x088, 0x080, 0x080, 0x090,
         0x098, 0x070, 0x070, 0x0a0),   # double (top/bottom) wall
        (0x0d0, 0x0d8, 0x0d0, 0x0d8,
         0x0b0, 0x0b8, 0x0b0, 0x0b8,
         0x0b0, 0x0b8, 0x0b0, 0x0b8,
         0x0c0, 0x0c8, 0x0c0, 0x0c8),   # double (left/right) wall
        (0x0d0, 0x0d8, 0x0d0, 0x0d8,
         0x0c0, 0x0c8, 0x0c0, 0x0c8,
         0x0d0, 0x0d8, 0x0d0, 0x0d8,
         0x0c0, 0x0c8, 0x0c0, 0x0c8),   # quadruple wall
        (0x1a0, 0x1a8, 0x1a8, 0x1b0,
         0x1a8, 0x1b0, 0x1a0, 0x1a8,
         0x1a0, 0x1a8, 0x1a8, 0x1b0,
         0x1a8, 0x1b0, 0x1a0, 0x1a8),   # fancy wall
        (0x060, 0x060, 0x060, 0x060,
         0x060, 0x060, 0x060, 0x060,
         0x060, 0x060, 0x060, 0x060,
         0x060, 0x060, 0x060, 0x060),   # smooth wall
        (0x060, 0x060, 0x060, 0x060,
         0x060, 0x060, 0x060, 0x060,
         0x060, 0x060, 0x060, 0x060,
         0x070, 0x070, 0x070, 0x070),   # lower edged smooth wall
        (0x080, 0x080, 0x080, 0x080,
         0x060, 0x060, 0x060, 0x060,
         0x060, 0x060, 0x060, 0x060,
         0x060, 0x060, 0x060, 0x060),   # upper edged smooth wall
        (0x060, 0x060, 0x060, 0x078,
         0x060, 0x060, 0x060, 0x078,
         0x060, 0x060, 0x060, 0x078,
         0x060, 0x060, 0x060, 0x078),   # right edged smooth wall
        (0x068, 0x060, 0x060, 0x060,
         0x068, 0x060, 0x060, 0x060,
         0x068, 0x060, 0x060, 0x060,
         0x068, 0x060, 0x060, 0x060),   # left edged smooth wall
        (0x060, 0x060, 0x060, 0x078,
         0x060, 0x060, 0x060, 0x078,
         0x060, 0x060, 0x060, 0x078,
         0x070, 0x070, 0x070, 0x0a0),   # lower right curved smooth wall
        (0x068, 0x060, 0x060, 0x060,
         0x068, 0x060, 0x060, 0x060,
         0x068, 0x060, 0x060, 0x060,
         0x098, 0x070, 0x070, 0x070),   # lower left curved smooth wall
        (0x080, 0x080, 0x080, 0x090,
         0x060, 0x060, 0x060, 0x078,
         0x060, 0x060, 0x060, 0x078,
         0x060, 0x060, 0x060, 0x078),   # upper right curved smooth wall
        (0x088, 0x080, 0x080, 0x080,
         0x068, 0x060, 0x060, 0x060,
         0x068, 0x060, 0x060, 0x060,
         0x068, 0x060, 0x060, 0x060),   # upper left curved smooth wall
        (0x200, 0x208, 0x200, 0x208,
         0x200, 0x208, 0x200, 0x208,
         0x200, 0x208, 0x200, 0x208,
         0x200, 0x208, 0x200, 0x208),   # brick wall
        (0x200, 0x208, 0x200, 0x208,
         0x200, 0x208, 0x200, 0x208,
         0x200, 0x208, 0x200, 0x208,
         0x230, 0x238, 0x230, 0x238),   # lower edged brick wall
        (0x210, 0x218, 0x210, 0x218,
         0x200, 0x208, 0x200, 0x208,
         0x200, 0x208, 0x200, 0x208,
         0x200, 0x208, 0x200, 0x208),   # upper edged brick wall
        (0x200, 0x208, 0x200, 0x228,
         0x200, 0x208, 0x200, 0x228,
         0x200, 0x208, 0x200, 0x228,
         0x200, 0x208, 0x200, 0x228),   # right edged brick wall
        (0x220, 0x208, 0x200, 0x208,
         0x220, 0x208, 0x200, 0x208,
         0x220, 0x208, 0x200, 0x208,
         0x220, 0x208, 0x200, 0x208),   # left edged brick wall
        (0x200, 0x208, 0x200, 0x228,
         0x200, 0x208, 0x200, 0x228,
         0x200, 0x208, 0x200, 0x228,
         0x230, 0x238, 0x270, 0x278),   # lower right curved brick wall
        (0x220, 0x208, 0x200, 0x208,
         0x220, 0x208, 0x200, 0x208,
         0x220, 0x208, 0x200, 0x208,
         0x260, 0x268, 0x230, 0x238),   # lower left curved brick wall
        (0x210, 0x218, 0x250, 0x258,
         0x200, 0x208, 0x200, 0x228,
         0x200, 0x208, 0x200, 0x228,
         0x200, 0x208, 0x200, 0x228),   # upper right curved brick wall
        (0x240, 0x248, 0x210, 0x218,
         0x220, 0x208, 0x200, 0x208,
         0x220, 0x208, 0x200, 0x208,
         0x220, 0x208, 0x200, 0x208)    # upper left curved brick wall
        ]
    
    def read_sprite(self, offsets):
    
        columns = []
        for i in range(4):
            columns.append(sum(map(self.read_block, offsets[i::4]), []))
        
        sprite = []
        for pieces in zip(*columns):
            sprite += "".join(pieces)

        sprite = "".join(sprite)
        return sprite
