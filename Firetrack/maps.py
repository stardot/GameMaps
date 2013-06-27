"""
maps.py - A module for exporting map data from Firetrack.

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

    def __init__(self, data):
    
        self.data = data
        self.levels = []
        self.tables = []
    
    def read_maps(self):
    
        f = StringIO.StringIO(self.data)
        
        while True:
        
            a = f.read(1)
            if not a:
                break
            
            b, c = f.read(1), f.read(1)
            
            table = []
            for i in range(8):
                table.append(ord(f.read(1)))
            
            self.tables.append(table)
            
            d = f.read(8)
            level = []
            line = []
            
            while True:
            
                n = ord(f.read(1))
                if n == 0x80:
                    break
                
                if n & 0x80 != 0:
                
                    # Span
                    count = (n >> 3) & 0x0f
                    value = table[n & 0x07]
                    line += [value] * count
                
                elif n & 0x40 != 0:
                
                    # Two byte span
                    value = n & 0x3f
                    count = ord(f.read(1))
                    line += [value] * count
                
                else:
                    line.append(n)
                
                while len(line) >= 20:
                
                    piece, line = line[:20], line[20:]
                    level.append(piece)
            
            if line:
                if len(line) < 20:
                    line += (20 - len(line)) * 0
                level.append(line)
            
            self.levels.append(level)
        
        return self.levels
