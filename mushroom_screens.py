#!/usr/bin/env python

"""
Copyright (C) 2011 David Boddie <david@boddie.org.uk>

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
import UEFfile

class Sprites:

    palette = {0x00: 0x000000, 0x01: 0x0000ff, 0x04: 0x00ff00, 0x05: 0x00ffff,
               0x10: 0xff0000, 0x11: 0xff00ff, 0x14: 0xffff00, 0x15: 0xffffff,
               0x40: 0x000000, 0x41: 0x000000, 0x44: 0xffffff, 0x45: 0x000000,
               0x50: 0x000000, 0x51: 0x000000, 0x54: 0x000000, 0x55: 0x000000}
    
    def __init__(self):
    
        self.sprites = []
    
    def read_sprites(self, sprite_data):
    
        blank = Image.new("RGB", (16, 8), 0)
        
        bytes_per_column = 8
        
        self.sprites = [blank]
        
        offset = 0
        for i in range(15):
        
            image = Image.new("RGB", (16, 8))
            for column in range(4):
                for byte in range(bytes_per_column):
                    data = ord(sprite_data[offset])
                    right = data & 0x55
                    left = (data >> 1) & 0x55
                    image.putpixel(((column * 4), byte), self.palette[left])
                    image.putpixel(((column * 4) + 1, byte), self.palette[left])
                    image.putpixel(((column * 4) + 2, byte), self.palette[right])
                    image.putpixel(((column * 4) + 3, byte), self.palette[right])
                    
                    offset += 1
            
            self.sprites.append(image)
    
    def export_images(self, output_dir):
    
        i = 0
        for image in self.sprites:
            image.save(os.path.join(output_dir, "%i.png" % i))
            i += 1


class Maps:

    def __init__(self):
    
        self.levels = []
    
    def read_maps(self, map_data):
    
        for i in range(9):
        
            level = []
            row = []
            j = 0
            
            while j < 0xdc:
            
                n = ord(map_data[(i * 0xf0) + j])
                row.append(n >> 4)
                row.append(n & 0xf)
                
                if len(row) == 20:
                    level.append(row)
                    row = []
                
                j += 1
            
            title = ""
            for c in map_data[(i * 0xf0) + j:(i * 0xf0) + j + 20]:
                if 32 <= ord(c) <= 122:
                    title += c
            
            self.levels.append((title, level))
    
    def export_html(self, f, level_number):
    
        title, level = self.levels[level_number - 1]
        
        f.write('<table cellpadding="0" cellspacing="0" style="margin-bottom: 1.0em">\n')
        f.write('<tr><td align="center" colspan="20" style="font-weight: bold; font-size: 1.5em; padding-bottom: 0.25em">%s</td></tr>\n' % title)
        
        for row in level:
        
            f.write("<tr>")
            for column in row:
            
                f.write('<td><img src="%i.png" /></td>' % column)
            
            f.write("</tr>\n")
        
        f.write("</table>\n")


if __name__ == "__main__":

    if len(sys.argv) != 5:
    
        sys.stderr.write("Usage: %s <Magic Mushrooms UEF file> <map UEF file> <map file name> <output directory>\n" % sys.argv[0])
        sys.exit(1)
    
    mm_uef_file = sys.argv[1]
    map_uef_file = sys.argv[2]
    map_file = sys.argv[3]
    output_dir = sys.argv[4]
    
    # Read the Magic Mushrooms UEF file.
    try:
        uef = UEFfile.UEFfile(mm_uef_file)
    except UEFfile.UEFfile_error:
        sys.stderr.write("Couldn't open %s\n" % mm_uef_file)
        sys.exit(1)
    
    # Find the file containing the sprites.
    f = 0
    while f < len(uef.contents):

        if uef.contents[f]['name'] == "\r":
            break
        else:
            f = f + 1
    
    # Export the file from the UEF file.
    name, load, exe, data = uef.export_files(f)
    
    # Read the sprites from the file.
    sprites = Sprites()
    sprites.read_sprites(data[0x2440:0x25a0] + data[0x2400:0x2420] + data[0x25a0:0x2600])
    
    # Read the map UEF file.
    try:
        uef = UEFfile.UEFfile(map_uef_file)
    except UEFfile.UEFfile_error:
        sys.stderr.write("Couldn't open %s\n" % map_uef_file)
        sys.exit(1)
    
    # Find the file containing the map
    f = 0
    while f < len(uef.contents):

        if uef.contents[f]['name'] == map_file:
            break
        else:
            f = f + 1
    
    if f == len(uef.contents):

        # Failed to find map file.
        sys.stderr.write("Couldn't find the map file in the UEF file. Please ensure"
                         "that this is the correct UEF file.\n")
        sys.exit(1)

    # Export the file from the UEF file.
    name, load, exe, data = uef.export_files(f)
    
    maps = Maps()
    maps.read_maps(data)
    
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
        f.write("<html>\n<head>\n<title>Magic Mushrooms Levels</title>\n</head>\n")
        f.write("<body>\n")
        f.write('<table>\n')
        
        for level in range(9):
        
            if level % 3 == 0:
                f.write('<tr>\n')
            
            f.write('<td>\n')
            maps.export_html(f, level + 1)
            f.write("</td>\n")
            
            if level % 3 == 2:
                f.write("</tr>\n")
        
        f.write("</table>\n")
        f.write("</body>\n</html>\n")
        f.close()
    
    except IOError:
        sys.stderr.write("Failed to create HTML file: %s\n" % output_file)
        sys.exit(1)
    
    sys.exit()
