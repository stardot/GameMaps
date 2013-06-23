"""
__init__.py - The main BoneCruncher Python package file.

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

__all__ = ["sprites"]

import UEFfile

from sprites import Reader, sprite_table

class NotFound(Exception):
    pass

class IncorrectSize(Exception):
    pass

class BoneCruncher:

    tile_width = 16
    tile_height = 32
    
    order = ["BONE_2", "SCREEN 1", "SCREEN 2", "SCREEN 3", "SCREEN 4"]
    lengths = {"BONE_2": 0x5b88,
               "SCREEN 1": 0xc00,
               "SCREEN 2": 0xc00,
               "SCREEN 3": 0xc00,
               "SCREEN 4": 0xc00}
    
    data_offsets = {"BONE_2": 0x2500,
                    "SCREEN 1": 0,
                    "SCREEN 2": 0,
                    "SCREEN 3": 0,
                    "SCREEN 4": 0}
    
    def __init__(self, uef_file):
    
        self.uef = UEFfile.UEFfile(uef_file)
        file_number = 0
        self.files = {}
        self.data = {}
        
        for details in self.uef.contents:
        
            name = details["name"]
            
            if name in self.lengths:
            
                if self.lengths[name] != len(details["data"]):
                    raise IncorrectSize
                
                self.files[name] = file_number
                self.data[name] = details["data"]
            
            file_number += 1
        
        if len(self.files) != 5:
            raise NotFound
    
    def read_levels(self):
    
        levels = []
        
        for group in self.order:
        
            for number in range(6):
            
                address = self.data_offsets[group] + (number * 0x200)
                level = []
                current = 0
                offset = 0
        
                for row in range(25):
        
                    level.append([])
                    
                    column = 0
                    read_more = False
                    
                    while column < 40:
        
                        if offset < 4 or read_more:
                            ch = self.data[group][address]
                            current = current | (ord(ch) << offset)
                            address += 1
                            offset += 8
        
                        while offset >= 4 and column < 40:
                        
                            value = current & 0x0f
                            if value == 0x0f and offset == 4:
                                # Read more data first.
                                read_more = True
                                break
                            
                            if value == 0x0f:
                                current = current >> 4
                                offset -= 4
                                value = value | ((current & 0x0f) << 4)
                                read_more = False
                            
                            current = current >> 4
                            offset -= 4
                            level[-1].append(value)
                            column += 1
                
                levels.append(level)
        
        return levels
    
    def write_levels(self, levels):
    
        group_number = 0
        
        for group in self.order:
        
            file_number = self.files[group]
            start = self.data_offsets[group]
            data = self.uef.contents[file_number]["data"][:start]
            rest = self.uef.contents[file_number]["data"][start + 0xc00:]
            
            for number in range(6):
            
                level = levels[group_number + number]
                
                current = 0
                offset = 0
                length = 0
                
                for row in range(25):
                
                    for column in range(40):
                    
                        value = level[row][column]
                        current = current | ((value & 0x0f) << offset)
                        offset += 4
                        
                        if value & 0x0f == 0x0f:
                            current = current | ((value >> 4) << offset)
                            offset += 4
                        
                        while offset >= 8:
                            data += chr(current & 0xff)
                            current = current >> 8
                            offset -= 8
                            length += 1
                
                if length > 0x200:
                    raise IncorrectSize, "Map too large."
                
                data += "\x00" * (0x200 - length)
            
            self.uef.contents[file_number]["data"] = data + rest
            group_number += 6
    
    def read_sprites(self):
    
        reader = Reader(self.data["BONE_2"][0x0:0x1400])
        
        sprites = {}
        
        for number, offset in sprite_table.items():
        
            if offset is None:
                if number != 0x6f:
                    sprites[number] = "\x00" * self.tile_width * self.tile_height
                else:
                    sprites[number] = sprites[7].replace("\x03", "\x01")
                continue
            
            sprite = []
            for row in range(4):
            
                columns = []
                for i in range(0, 0x20, 8):
                    columns.append(reader.read_sprite(offset + (row * 0x20) + i))
                
                for line in zip(*columns):
                    sprite.append("".join(line))
            
            sprite = "".join(sprite)
            sprites[number] = sprite
        
        return sprites
    
    def palette(self, level):
    
        return [(0,0,0), (255,0,0), (0,255,0), (255,255,255)]
