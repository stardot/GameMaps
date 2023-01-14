"""
levels.py - Level reading and writing classes for Clogger.

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

class Levels:

    width = 32
    height = 32
    
    sets = ["SLIPPER", "BRUSHES", "ARTIST", "PAINT"]
    
    def __init__(self, data):
    
        self.data = data
    
    def read(self, number):
    
        level_start = 0xf7d + (number * 32 * 32)
        level_finish = level_start + (32 * 32)
        level = self.data[level_start:level_finish]
        
        data = []
        
        for row in range(32):
        
            data.append([])
            
            for column in range(32):
    
                value = ord(level[(row * 32) + column])
                data[-1].append(value)
        
        return data
    
    def palette(self, number):
    
        return [(0,0,0), (255,0,0), (0,255,0), (0,0,255)]
    
    def read_tile(self, number, column, row):
    
        level_start = 0xf7d + (number * 32 * 32)
        
        return ord(self.data[level_start + (row * 32) + column])
    
    def write_tile(self, number, column, row, value):
    
        level_start = 0xf7d + (number * 32 * 32)
        
        self.data[level_start + (row * 32) + column] = chr(value)
    
    def get_password(self, number):
    
        # Decode the password from the level data.
        decoded = ""
        for i in range(number * 7, (number + 1) * 7):
            decoded += chr(ord(self.data[i]) ^ i)
        
        return decoded
    
    def set_password(self, number, text):
    
        if len(text) < 7:
            text += (7 - len(text)) * " "
        else:
            text = text[:7]
        
        # Encode the password and store it in the level data.
        for i in range(min(len(text), 7)):
            offset = (number * 7) + i
            self.data[offset] = chr(ord(text[i]) ^ offset)
    
    def get_target_position(self, number, piece):
    
        offset = 35 + (number * 42) + (piece * 2)
        low, high = map(ord, self.data[offset:offset + 2])
        return low & 0x1f, ((high & 0x03) << 3) | (low >> 5)
    
    def set_target_position(self, number, piece, x, y):
    
        offset = 35 + (number * 42) + (piece * 2)
        low, high = x | ((y & 0x07) << 5), (y >> 3) | 0x04
        self.data[offset] = chr(low)
        self.data[offset + 1] = chr(high)
