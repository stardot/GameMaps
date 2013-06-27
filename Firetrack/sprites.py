"""
sprites.py - A module for exporting raw sprite data from Firetrack.

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

class Reader:

    def __init__(self, data):
    
        self.data = data
    
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
    
        sprites = []
        start = 3072 - (64 * 32)
        
        for sprite in range(64):
        
            spr = []
            for r in range(0, 32, 8):
                spr.append([])
                for row in range(r, r+8):
                    spr[-1].append(self.read_columns(self.data[start + sprite + (row * 64)]))
            
            top = "".join(map(lambda row: "".join(row), zip(spr[0], spr[1])))
            bottom = "".join(map(lambda row: "".join(row), zip(spr[2], spr[3])))
            sprites.append(top + bottom)
        
        return sprites
