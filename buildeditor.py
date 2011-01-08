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
import UEFfile

version = "0.1"

def system(command):

    if os.system(command):
        sys.exit(1)

def read_basic(path):

    t = open(path).read()
    t = t.replace("\n", "\r")
    lines = t.rstrip().split("\r")
    t = "\r".join(lines) + "\r"
    return t


if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <Shark UEF file> <new UEF file>\n" % sys.argv[0])
        sys.exit(1)
    
    in_uef_file = sys.argv[1]
    out_uef_file = sys.argv[2]
    
    # Read the UEF file
    try:
        uef = UEFfile.UEFfile(in_uef_file)
    except UEFfile_error:
        sys.stderr.write("Couldn't open %s\n" % in_uef_file)
        sys.exit(1)
    
    files = []
    
    system("ophis BASIC/editcode.oph BASIC/EDITCODE")
    files.append(("EDITCODE", 0x1900, 0x1900, open("BASIC/EDITCODE").read()))
    
    t = read_basic("BASIC/EDITOR")
    files.append(("EDITOR", 0xffff0e00, 0xffff802b, open("BASIC/EDITOR").read()))
    
    u = UEFfile.UEFfile(creator = 'SharkMap buildeditor.py '+version)
    u.minor = 6
    u.chunks = uef.chunks[:]
    u.import_files(len(uef.contents), files)
    
    # Write the new UEF file.
    try:
        u.write(out_uef_file, write_emulator_info = False)
    except UEFfile.UEFfile_error:
        sys.stderr.write("Couldn't write the new executable to %s.\n" % out_uef_file)
        sys.exit(1)

    # Exit
    sys.exit()
