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

    offsets = [(0x11f, 3, 0x17f, 0x8df), (0xff, 3, 0x93f, 0x8df), (0x11f, 3, 0x113f, 0x8df), (0x11f, 3, 0x191f, 0x8df)]
    
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
            
            n += 1
            if n == 12:
                level += 1
                address += 4
                n = 0
        
        levels = []
        
        for level in range(4):
        
            start, number, middle, end = self.offsets[level]
            offset = start
            right_margin = 64 - (5 - number)
            level = []
            
            for column in range(64):
            
                level.append([])
                
                for row_pair in range(32):
                
                    if 0 <= column < number:
                        i = start + (column * 32) + row_pair
                    elif 3 <= column < right_margin:
                        i = middle + ((column - number) * 32) + row_pair
                    else:
                        i = end + ((column - right_margin) * 32) + row_pair
                    
                    byte = ord(self.data[i])
                    upper = byte & 0x0f
                    lower = byte >> 4
                    level[-1] += [upper, lower]
            
            # Stored a transposed version of the level.
            levels.append(zip(*level))
        
        return levels, items
