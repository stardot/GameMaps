#!/usr/bin/env python

"""
read_sprites.py - Extract Firetrack sprites from a UEF file to a directory.

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
import Image
import UEFfile

def read_columns(byte):

    columns = []
    byte = ord(byte)
    for i in range(4):

        v = (byte & 0x01) | ((byte & 0x10) >> 3)
        byte = byte >> 1
        columns.append(v)

    columns.reverse()
    return "".join(map(chr, columns))

def read_sprites(data):

    sprites = []
    start = 3072 - (64 * 32)
    
    for sprite in range(64):
    
        spr = []
        for r in range(0, 32, 8):
            spr.append([])
            for row in range(r, r+8):
                spr[-1].append(read_columns(data[start + sprite + (row * 64)]))
        
        top = "".join(map(lambda row: "".join(row), zip(spr[0], spr[1])))
        bottom = "".join(map(lambda row: "".join(row), zip(spr[2], spr[3])))
        sprites.append(top + bottom)
    
    return sprites

if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <Firetrack UEF file> <output directory>\n" % sys.argv[0])
        sys.exit(1)
    
    uef_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    try:
        u = UEFfile.UEFfile(uef_file)
        for details in u.contents:
            if details["name"] == "4":
                break
        else:
            raise IOError
        
        sprites = read_sprites(details["data"])
    
    except (IOError, UEFfile.UEFfile_error):
        sys.stderr.write("Failed to read UEF file: %s\n" % uef_file)
        sys.exit(1)
    
    i = 0
    for sprite in sprites:
    
        im = Image.fromstring("P", (8, 16), sprite)
        im.putpalette((0,0,0, 255,0,0, 0,255,0, 0,0,255))
        im.save(os.path.join(output_dir, "%02i.png" % i))
        i += 1
    
    sys.exit()
