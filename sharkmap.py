#!/usr/bin/env python

"""
sharkmap.py - A Shark level convertor

Copyright (c) 2011, David Boddie <david@boddie.org.uk>

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

import os, sys, UEFfile

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

version = '0.10'
date = '2011-01-07'


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
    
    def export_text(self, f, level_number):
    
        tiles = (" ", "=", "#", "^", "-", "X", "x", "*",
                 "[", "]", ".", "V", "v", "+", ":", "|")
        
        level = self.levels[level_number - 1]
        
        for row in range(12):
        
            for column in level:
                f.write(tiles[column[row]])
            
            f.write("\n")
        
        f.write("\n")


# Read a map file and produce a binary description which can be understood
# by Shark.

tiles = {
    " ": 0, "=": 1, "#": 2, "^": 3, "-": 4, "X": 5, "x": 6, "*": 7,
    "[": 8, "]": 9, ".": 10, "V": 11, "v": 12, "+": 13, ":": 14, "|": 15
    }

def read_map(map_file):

    line_number = 0
    data = ""
    
    for level in (0, 1, 2):
    
        while True:
            line = map_file.readline().rstrip()
            line_number += 1
            
            if line:
                break
        
        rows = []
        for row in range(12):
        
            if len(line) < 172:
                if row < 11:
                    line += " " * (172 - len(line))
                else:
                    line += "^" * (172 - len(line))
            
            elif len(line) > 172:
                sys.stderr.write("Line %i too long.\n" % line_number)
                sys.exit(1)
            
            rows.append(line)
            
            line = map_file.readline().rstrip()
            line_number += 1
        
        column = 0
        while column < 172:
        
            for row in rows:
                pair = row[column:column+2]
                byte = tiles[pair[0]] | (tiles[pair[1]] << 4)
                data += chr(byte)
            
            column += 2
    
    # Return the binary map information.
    return data


def add_map_data(map_file, uef, out_uef_file, position, data):

    try:
        input_file = open(map_file, 'r')
    except IOError:
        sys.stderr.write("Couldn't open "+map_file+' for input.\n')
        sys.exit(1)
        
    # Convert the textual description to a binary format.
    map_data = read_map(input_file)
    if len(map_data) != 0xc18:
        sys.stderr.write("Not enough level data in %s." % map_file)
        sys.exit(1)

    # Close the input file.
    input_file.close()

    # Replace the old map.
    new_data = data[:0x2be0] + map_data + data[0x37f8:]

    # Create a new UEF file.
    n = UEFfile.UEFfile(creator = 'SharkMap '+version)
    # of version 0.6
    n.minor = 6

    # Copy the chunks before the executable into the new file.
    n.chunks += uef.chunks[:uef.contents[position]["position"]]

    # Add the new executable.
    n.import_files(position, (name, load, exe, new_data))

    # Copy the chunks after the executable into the new file.
    n.chunks += uef.chunks[uef.contents[position]["last position"]+1:]

    # Write the new UEF file.
    try:
        n.write(out_uef_file, write_emulator_info = False)
    except UEFfile_error:
        sys.stderr.write("Couldn't write the new executable to %s.\n" % out_uef_file)
        sys.exit(1)

    print 'Replaced the map data in %s.' % out_uef_file


def extract_map_data(uef, map_file, data):

    maps = Maps()
    f = StringIO(data)
    maps.read_maps(f)
    
    try:
        map_f = open(map_file, "w")
        
        for level_number in (1, 2, 3):
            maps.export_text(map_f, level_number)
        
        map_f.close()
    
    except IOError:
        sys.stderr.write("Failed to write map data to %s.\n" % map_file)
        sys.exit(1)


# Main program

if __name__ == '__main__':

    if not 3 <= len(sys.argv) <= 4:

        sys.stderr.write('Usage: %s <map file> <original UEF file> <new UEF file>\n' % sys.argv[0])
        sys.stderr.write('Usage: %s <original UEF file> <new map file>\n\n' % sys.argv[0])
        sys.stderr.write('SharkMap - a Shark level convertor\n\n')
        sys.stderr.write('Version %s\n\n' % version)
        sys.stderr.write('<map file> is a .map file containing a textual description of Shark levels.\n')
        sys.stderr.write('This is converted to a binary description and is added to the relevant file\n')
        sys.stderr.write('contained within the Shark UEF file specified by <original UEF file>.\n')
        sys.stderr.write('A new version is written to the file specified by <new UEF file>.\n\n')
        sys.exit(1)
    
    if len(sys.argv) == 4:
    
        map_file = sys.argv[1]
        in_uef_file = sys.argv[2]
        out_uef_file = sys.argv[3]
        mode = "adding"
    
    else:
        in_uef_file = sys.argv[1]
        map_file = sys.argv[2]
        mode = "extracting"
    
    # Read the UEF file.
    try:
        uef = UEFfile.UEFfile(in_uef_file)
    except UEFfile_error:
        sys.stderr.write("Couldn't open %s\n" % in_uef_file)
        sys.exit(1)

    # Find the executable containing the map.
    f = 0
    while f < len(uef.contents):

        if uef.contents[f]["name"] == "CODE":
            break
        else:
            f = f + 1

    if f == len(uef.contents):

        sys.stderr.write("Couldn't find the correct executable. Please ensure"
                         "that this is the correct UEF file.\n")
        sys.exit(1)

    # Export the file from the UEF file.
    name, load, exe, data = uef.export_files(f)

    if len(data) != 0x3c00:

        sys.stderr.write('The executable in %s is incorrect in length.\n' % execfile)
        sys.exit(1)
    
    if mode == "adding":
        add_map_data(map_file, uef, out_uef_file, f, data)
    else:
        extract_map_data(uef, map_file, data)
    
    # Exit
    sys.exit()
