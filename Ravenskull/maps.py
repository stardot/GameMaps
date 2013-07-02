"""
maps.py - A module for exporting map data from Ravenskull.

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

import StringIO

class Maps:

    offsets = [(0x11f, 0x11f, 0x91f), (0x8ff, 0x8ff, 0x10bf), (0x10df, 0x10df, 0x189f), (0x18df, 0x207f, 0x209f)]
    
    def __init__(self, data):
    
        self.data = data
    
    def read_maps(self):
    
        address = 0x00
        items = {0: {}, 1: {}, 2: {}, 3: {}}
        level = 0
        n = 0
        
        while address < 0x100 and level < 4:
        
            column, row, type, x, y = map(ord, self.data[address:address + 5])
            if column >= 128:
                column = column - 256
            if row >= 128:
                row = row - 256
            
            items[level][(row, column)] = (type, y, x)
            address += 5
            
            print n, (column, row, type, x, y)
            n += 1
            if n == 12:
                level += 1
                print map(hex, map(ord, self.data[address:address + 4]))
                address += 4
                n = 0
        
        levels = []
        
        for level in range(4):
        
            start, address, end = self.offsets[level]
            offset = address - start
            length = end - start
            level = []
            
            for column in range(64):
            
                level.append([])
                
                for row_pair in range(32):
                
                    i = start + (offset + (column * 32) + row_pair) % length
                    byte = ord(self.data[i])
                    upper = byte & 0x0f
                    lower = byte >> 4
                    level[-1] += [upper, lower]
            
            # Stored a transposed version of the level.
            levels.append(zip(*level))
        
        return levels, items
