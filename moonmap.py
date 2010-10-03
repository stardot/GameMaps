#!/usr/bin/env python

"""
moonmap.py - A Moon Raider level convertor

Copyright (c) 2001-2010, David Boddie <david@boddie.org.uk>

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

# History
#
# 0.10 (Sun 21st January 2001)
# 
# Initial version.
# 
# 0.11 (Tue 23rd January 2001)
# 
# Modified version of 0.10 which allows empty lines to denote no floor or ceiling.
# 
# 0.12 (Mon 13th August 2001)
#
# Tidied up multi-platform support.
#
# 0.13 (Thu 06th September 2001)
#
# Now patches the UEF file directly using UEFfile objects.
#


import os, string, sys, UEFfile

version = '0.13 (Thu 06th September 2001)'

# Global variables

start_level = 3
screen_height = 27


def count_left(s):

    i = 0
    l = 0
    while i < len(s):

        if s[i] == '#':
            l = l + 1
            i = i + 1
        else:
            break

    return l, s[i:]


def count_right(s):

    i = len(s)-1
    l = 0
    while i >= 0:

        if s[i] == '#':
            l = l - 1
            i = i - 1
        else:
            break

    return l, s[:i+1]


def check_length(bin, level_offset, line_no):

    if (len(bin) - level_offset) > 0xff:
        sys.stderr.write('Level too long (or too detailed) at line %i.\n' % line_no)
        sys.exit(1)


# Read a map file and produce a binary description which can be understood
# by Moon Raider

def read_map(map):

    building_level = start_level
    ceiling_level = 0
    level_offset = 0x000

    line_no = 1

    bin = ''

    while 1:

        line = map.readline()
        if not line:
            break

        line = string.strip(line)

        # Determine the presence of aliens or fireballs
        code = 0

        if line != '':

            if line[-1] == '@':
                code = code | 0x40
                line = line[:-1]
            elif line[-1] == '*':
                code = code | 0x20
                line = line[:-1]

        # Count the building level
        blevel, line = count_left(line)

        if blevel > (screen_height+ceiling_level-1):
            sys.stderr.write('Floor is too high at line %i.\n' % line_no)
            sys.exit(1)

        if blevel > building_level:
            if (blevel-building_level) < 32:
                bin = bin + chr(0x80 | (blevel-building_level))
                check_length(bin, level_offset, line_no)
            else:
                sys.stderr.write('Step is too high at line %i.\n' % line_no)
                sys.exit(1)

            building_level = blevel

        elif blevel < building_level:
            if (building_level-blevel) < 32:
                bin = bin + chr(0xa0 | (building_level-blevel))
                check_length(bin, level_offset, line_no)
            else:
                sys.stderr.write('Step is too high at line %i.\n' % line_no)
                sys.exit(1)

            building_level = blevel

        else:
            # Do nothing (same level)
            pass

        # Count the ceiling level
        clevel, line = count_right(line)

        if clevel < (-screen_height+building_level+1):
            sys.stderr.write('Ceiling is too low at line %i.\n' % line_no)
            sys.exit(1)

        if clevel < ceiling_level:
            if (ceiling_level-clevel) < 32:
                bin = bin + chr(0xe0 | (ceiling_level-clevel))
                check_length(bin, level_offset, line_no)
            else:
                sys.stderr.write('Step is too high at line %i.\n' % line_no)
                sys.exit(1)

            ceiling_level = clevel

        elif clevel > ceiling_level:
            if (clevel-ceiling_level) < 32:
                bin = bin + chr(0xc0 | (clevel-ceiling_level))
                check_length(bin, level_offset, line_no)
            else:
                sys.stderr.write('Step is too high at line %i.\n' % line_no)
                sys.exit(1)

            ceiling_level = clevel

        else:
            # Do nothing (same level)
            pass

        # The rest of the information must be the object present
        line = string.strip(line)

        if line == 'E':
            bin = bin + chr(0xff)
            chars = level_offset + 0x100 - len(bin)

            if chars > 0:
                bin = bin + (chars * '\000')

            level_offset = level_offset + 0x100
            if level_offset == 0x700:
                break
        else:
            if line == '!':
                code = code | 0x00
            elif line == 'm':
                code = code | 0x01
            elif line == 'f':
                code = code | 0x02
            elif line == '>':
                building_level = building_level + 1
                code = code | 0x03
            elif line == '<':
                building_level = building_level - 1
                code = code | 0x04
            elif line == '\\':
                building_level = building_level + 2
                code = code | 0x05
            elif line == '/':
                building_level = building_level - 2
                code = code | 0x06
            elif line == 'r':
                code = code | 0x07
            elif line == 't':
                code = code | 0x08
            elif line == 'x':
                code = code | 0x09
            elif line == '|':
                code = code | 0x0a
            elif line == '?':
                code = code | 0x0b
            elif line == '':
                code = code | 0x0c
            elif line == 'F':
                code = code | 0x0d
#            elif line == '|':
#                code = code | 0x0e
#            elif line == '|':
#                code = code | 0x0f
            elif line == 'H':
                code = code | 0x10
            elif line == '1':
                code = code | 0x11
            elif line == '2':
                code = code | 0x12

            bin = bin + chr(code)
    
            check_length(bin, level_offset, line_no)

        line_no = line_no + 1

    # Return the binary map information
    return bin


def hex2num(s):
    """Convert a string of hexadecimal digits to an integer."""

    n = 0

    for i in range(0,len(s)):

        a = ord(s[len(s)-i-1])
        if (a >= 48) & (a <= 57):
            n = n | ((a-48) << (i*4))
        elif (a >= 65) & (a <= 70):
            n = n | ((a-65+10) << (i*4))
        elif (a >= 97) & (a <= 102):
            n = n | ((a-97+10) << (i*4))
        else:
            return None

    return n


def get_leafname(path):
    """Get the leafname of the specified file."""

    pos = string.rfind(path, os.sep)
    if pos != -1:
        return path[pos+1:]
    else:
        return path


# Main program

if __name__ == '__main__':

    if os.sep != '.':
        suffix = '.'
    else:
        suffix = '/'
    
    if len(sys.argv) < 4:

        sys.stderr.write('Syntax: moonmap'+suffix+'py <map file> <original UEF file> <new UEF file>\n\n')
        sys.stderr.write('MoonMap - a Moon Raider level convertor\n\n')
        sys.stderr.write('Version %s\n\n' % version)
        sys.stderr.write('<map file> is a .map file containing a textual description of Moon Raider levels.\n')
        sys.stderr.write('This is converted to a binary description and is added to the relevant file\n')
        sys.stderr.write('contained within the Moon Raider UEF file specified by <original UEF file>.\n')
        sys.stderr.write('A new version is written to the file specified by <new UEF file>.\n\n')
        sys.exit(1)
    
    map_file = sys.argv[1]
    in_uef_file = sys.argv[2]
    out_uef_file = sys.argv[3]

    try:
        input = open(map_file, 'r')
    except IOError:
        sys.stderr.write("Couldn't open "+map_file+' for input.\n')
        sys.exit(1)
        
    # Convert the textual description to a binary format
    map_data = read_map(input)

    # Close the input file        
    input.close()

    # Read the UEF file
    try:
        uef = UEFfile.UEFfile(in_uef_file)
    except UEFfile_error:
        sys.stderr.write("Couldn't open %s\n" % in_uef_file)
        sys.exit(1)

    # Find the executable containing the map
    f = 0
    while f < len(uef.contents):

        if uef.contents[f]['load'] == 0x1900:
            break
        else:
            f = f + 1

    if f == len(uef.contents):

        # Failed to find executable
        sys.stderr.write("Couldn't find the correct executable. Please ensure"
                         "that this is the correct UEF file.\n")
        sys.exit(1)

    # Export the file from the UEF file
    name, load, exe, data = uef.export_files(f)

    if len(data) != 0x3f00:

        sys.stderr.write('The executable in %s is incorrect in length.\n' % execfile)
        sys.exit(1)

    # Replace the old map
    new_data = data[:0x5000 - 0x1900] + map_data + data[0x5700 - 0x1900:]

    # Create a new UEF file
    n = UEFfile.UEFfile(creator = 'MoonMap '+version)
    # of version 0.6
    n.minor = 6

    # Copy the files before the executable into the new file
    n.import_files(0, uef.export_files(range(0,f)))
    # Add the new executable
    n.import_files(f, (name, load, exe, new_data))
    # Copy the files after the executable into the new file
    n.import_files(f+1, uef.export_files(range(f+1,len(uef.contents))))

    # Write the new executable
    try:
        n.write(out_uef_file)
    except UEFfile_error:
        sys.stderr.write("Couldn't write the new executable to %s.\n" % out_uef_file)
        sys.exit(1)

    print 'Replaced the map data in %s.' % out_uef_file
    
    # Exit
    sys.exit()
