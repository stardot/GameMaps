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
    None,           # blank
    0x48,           # moat, wall, striped wall, wall
    0x90,           # wall, 22*0x48 - 8 (striped wall)
    13*0x48 - 8,    # spiked gate, 18*0x48 - 8 (spiked column), spiked gate, spiked column
    14*0x48 - 8,    # column, 16*0x48 - 8 (square wall), column, square wall
    17*0x48 - 8,    # sarcophagus
    3*0x48,         # upper-right wall
    6*0x48,         # upper-left wall
    5*0x48,         # lower-left wall
    4*0x48,         # lower-right wall
    24*0x48 - 8,    # door
    10*0x48 - 8,    # brick wall, 23*0x48 - 8 (barrel), brick wall, barrel
    7*0x48,         # acid pool, 21*0x48 - 8 (plant), acid pool, plant
    15*0x48 - 8,    # green wall
    12*0x48 - 8,    # decorative wall, 19*0x48 - 8 (earth), decorative wall, earth
    11*0x48 - 8,    # treasure
    ]

small_sprite_table = [
    0,
    20 + 0x3c,
    20 + 64 + 2*0x3c
    ]

class Reader:

    def __init__(self, data):
    
        self.data = data
    
    def read_sprite(self, offset, bytes = 8):
    
        rows = []
        
        for i in range(bytes):
        
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
        base = 4*r + 3*c + 8
        
        for number in range(len(sprite_table)):
        
            sprite = []
            address = sprite_table[number]
            if address is None:
                sprites[number] = 12*24*"\x00"
                continue
            
            columns = []
            for column in range(3):
            
                offset = base + address + (column * 24)
                columns.append(self.read_sprite(offset, 24))
            
            for line in zip(*columns):
                sprite.append("".join(line))
            
            sprite = "".join(sprite)
            sprites[number] = sprite
        
        small_number = number + 1
        base = r + 4*c
        
        for number in range(len(small_sprite_table)):
        
            sprite = []
            address = small_sprite_table[number]
            
            columns = []
            for column in range(3):
            
                offset = base + address + (column * 20)
                columns.append(self.read_sprite(offset, 20))
            
            for line in zip(*columns):
                sprite.append("".join(line))
            
            sprite = ("\x00" * 24) + "".join(sprite) + ("\x00" * 24)
            sprites[small_number] = sprite
            small_number += 1
        
        return sprites
