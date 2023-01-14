"""
__init__.py - The main Firetrack Python package file.

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

__all__ = ["maps", "sprites"]

import UEFfile

from maps import Maps
from sprites import Reader

class NotFound(Exception):
    pass

class IncorrectSize(Exception):
    pass

class Firetrack:

    tile_width = 8
    tile_height = 16
    
    def __init__(self, uef_file):
    
        self.uef = UEFfile.UEFfile(uef_file)
        
        self.files = {}
        self.offsets = {}
        file_number = 0
        
        for details in self.uef.contents:
        
            name = details["name"]
            self.files[name] = details["data"]
            self.offsets[name] = file_number
            
            file_number += 1
        
        if "4" not in self.files or "5" not in self.files:
            raise NotFound
        elif len(self.files["4"]) != 0xc00:
            raise IncorrectSize
        elif len(self.files["5"]) != 0x1e73:
            raise IncorrectSize
    
    def read_levels(self):
    
        maps = Maps(self.files["5"])
        levels = maps.read_maps()
        
        new_levels = []
        
        for level in levels:
            lines = level[:]
            lines.reverse()
            new_levels.append(lines)
        
        return new_levels
    
    def write_levels(self, levels):
    
        pass
    
    def read_sprites(self):
    
        reader = Reader(self.files["4"])
        return reader.read_sprites()
    
    def palette(self, level):
    
        return [(0,0,0), (255,0,0), (0,255,0), (0,0,255)]
