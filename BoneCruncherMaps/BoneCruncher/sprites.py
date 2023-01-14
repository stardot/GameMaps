#!/usr/bin/env python

"""
sprites.py - A module for exporting raw sprite data from BoneCruncher.

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

sprite_table = {
    0: None,
    1: 0x000,
    2: 0x080,
    3: 0x100,
    4: 0x200,
    5: 0x480,
    6: 0x500,
    7: 0x600,
    8: 0x580,
    9: 0x180,
 0x0a: 0x780,   # First glook
 0x0b: 0x680,   # First skeleton
 0x0c: 0x900,   # First monster
 0x0d: 0xa80,   # First spider
 0x0e: None,
 0x0f: 0xb80,   # First fozzy
 0x1f: 0x280,
 0x2f: 0x300,
 0x3f: 0x380,
 0x4f: 0x400,
 0x5f: 0x1380,  # Bono
 0x6f: None     # Volcano
    }

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
