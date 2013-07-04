#!/usr/bin/env python

"""
sprites.py - A module for exporting raw sprite data from Ravenskull.

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

# Offsets into the sprite data for the top-left, top-right, bottom-left and
# bottom-right 8 byte pieces of each sprite. For the blank piece, I just chose
# a blank area in the file data.

r = 0x140
c = 0x10

sprite_table = [
    (3*r, 3*r, 3*r, 3*r, 3*r, 3*r, 3*r, 3*r, 3*r),
    (4*r + 8*c, 4*r + 9*c + 8, 4*r + 11*c,
     4*r + 8*c + 8, 4*r + 10*c, 4*r + 11*c + 8,
     4*r + 9*c, 4*r + 10*c + 8, 4*r + 12*c),
    (4*r + 12*c + 8, 4*r + 14*c, 4*r + 15*c + 8,
     4*r + 13*c, 4*r + 14*c + 8, 4*r + 16*c,
     4*r + 13*c + 8, 4*r + 15*c, 4*r + 16*c + 8),
    (4*r + 17*c, 4*r + 18*c + 5, 4*r + 20*c + 8,
     4*r + 17*c + 8, 4*r + 19*c, 4*r + 20*c,
     4*r + 18*c, 4*r + 19*c + 8, 4*r + 21*c),
    (4*r + 21*c + 8, 4*r + 23*c, 4*r + 24*c + 8,
     4*r + 22*c, 4*r + 23*c + 8, 4*r + 25*c,
     4*r + 22*c + 5, 4*r + 24*c, 4*r + 25*c + 8),
    ]

class Reader:

    def __init__(self, data):
    
        self.data = data
    
    def read_sprite(self, offset):
    
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
    
    def read_sprites(self):
    
        sprites = {}
        
        for number in range(len(sprite_table)):
        
            sprite = []
            for row in range(3):
            
                columns = []
                for column in range(3):
                
                    offset = sprite_table[number][row * 3 + column]
                    columns.append(self.read_sprite(offset))
                
                for line in zip(*columns):
                    sprite.append("".join(line))
            
            sprite = "".join(sprite)
            sprites[number] = sprite
        
        return sprites
