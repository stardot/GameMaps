#!/usr/bin/env python

"""
Copyright (C) 2010 David Boddie <david@boddie.org.uk>

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
import Image

class Sprites:

    def __init__(self):
    
        self.sets = []
        self.offsets = (0x1d00, 0x2100, 0x0000)
        self.blanks = ((0x00, 0x0a), (0x00,), ())
        self.palettes = [
            {0x00: 0x000000, 0x01: 0xff00ff, 0x04: 0x00ff00, 0x05: 0x00ffff,
             0x10: 0x00ff00, 0x11: 0xff00ff, 0x14: 0xffff00, 0x15: 0xffffff,
             0x40: 0x000000, 0x41: 0x000000, 0x44: 0x000000, 0x45: 0x0000ff,
             0x50: 0x0000ff, 0x51: 0x000000, 0x54: 0x000000, 0x55: 0x000000},
            {0x00: 0x000000, 0x01: 0xff00ff, 0x04: 0xff0000, 0x05: 0xffff00,
             0x10: 0x00ff00, 0x11: 0xff00ff, 0x14: 0x00ffff, 0x15: 0xffffff,
             0x40: 0x000000, 0x41: 0x000000, 0x44: 0x000000, 0x45: 0x000000,
             0x50: 0x000000, 0x51: 0x000000, 0x54: 0x000000, 0x55: 0x000000},
            {0x00: 0x000000, 0x01: 0xff00ff, 0x04: 0x00ffff, 0x05: 0xffffff,
             0x10: 0x00ff00, 0x11: 0xff00ff, 0x14: 0xffff00, 0x15: 0xffffff,
             0x40: 0x000000, 0x41: 0x000000, 0x44: 0x000000, 0x45: 0x000000,
             0x50: 0x000000, 0x51: 0x000000, 0x54: 0x000000, 0x55: 0x000000}
            ]
    
    def read_sprites(self, f):
    
        blank = Image.new("RGB", (16, 16), 0)
        
        bytes_per_column = 8
        for level_index in range(len(self.offsets)):
        
            offset = self.offsets[level_index]
            f.seek(offset)
            
            sprites = []
            palette = self.palettes[level_index]
            
            for i in range(16):
            
                image = Image.new("RGB", (16, 16))
                for row in range(2):
                    for column in range(4):
                        for byte in range(bytes_per_column):
                            data = ord(f.read(1))
                            right = data & 0x55
                            left = (data >> 1) & 0x55
                            image.putpixel(((column * 4), (row * 8) + byte),
                                           palette[left])
                            image.putpixel(((column * 4) + 1, (row * 8) + byte),
                                           palette[left])
                            image.putpixel(((column * 4) + 2, (row * 8) + byte),
                                           palette[right])
                            image.putpixel(((column * 4) + 3, (row * 8) + byte),
                                           palette[right])
                
                sprites.append(image)
            
            for i in self.blanks[level_index]:
                sprites[i] = blank
            
            self.sets.append(sprites)
    
    def export_images(self, output_dir):
    
        level_number = 1
        for sprites in self.sets:
        
            i = 0
            for image in sprites:
                image.save(os.path.join(output_dir, "%i-%i.png" % (level_number, i)))
                i += 1
            
            level_number += 1


class Maps:

    def __init__(self):
    
        self.levels = []
        self.tables = []
    
    def read_maps(self, f):
    
        f.seek(0x2be0)
        
        for i in range(3):
        
            level = []
            left_column = []
            right_column = []
            j = 0
            
            while j < 0x408:
            
                n = ord(f.read(1))
                left_column.append(n & 0xf)
                right_column.append(n >> 4)
                
                if len(left_column) == 12:
                    level.append(left_column)
                    level.append(right_column)
                    left_column = []
                    right_column = []
                
                j += 1
            
            self.levels.append(level)
    
    def export_html(self, f, level_number):
    
        level = self.levels[level_number - 1]
        
        f.write('<table cellpadding="0" cellspacing="0">\n')
        for row in range(12):
        
            f.write("<tr>")
            for column in level:
            
                f.write('<td><img src="%i-%i.png" /></td>' % (level_number, column[row]))
            
            f.write("</tr>\n")
        
        f.write("</table>\n")


if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <Shark CODE file> <output directory>\n" % sys.argv[0])
        sys.exit(1)
    
    code_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    try:
        f = open(code_file)
        sprites = Sprites()
        sprites.read_sprites(f)
        maps = Maps()
        maps.read_maps(f)
        f.close()
    
    except IOError:
        sys.stderr.write("Failed to read code file: %s\n" % code_file)
        sys.exit(1)
    
    if not os.path.exists(output_dir):
        try:
            os.mkdir(output_dir)
        except OSError:
            sys.stderr.write("Failed to create output directory: %s\n" % output_dir)
            sys.exit(1)
    
    # Write the images to files in the output directory.
    sprites.export_images(output_dir)
    
    output_file = os.path.join(output_dir, "index.html")
    
    try:
        f = open(output_file, "w")
        f.write("<html>\n<head>\n<title>Shark Levels</title>\n</head>\n")
        f.write("<body>\n")
        
        for level in range(3):
            f.write("\n\n<h2>Level %i</h2>\n" % (level + 1))
            maps.export_html(f, level + 1)
        
        f.write("</body>\n</html>\n")
        f.close()
    
    except IOError:
        sys.stderr.write("Failed to create HTML file: %s\n" % output_file)
        sys.exit(1)
    
    sys.exit()
