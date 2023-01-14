#!/usr/bin/env python

"""
readmaps.py - Read Firetrack maps from a UEF file and write them to a text file.

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

import StringIO, sys
import UEFfile

from Firetrack import maps

class Maps(maps.Maps):

    def export_text(self, f):
    
        levels = self.levels[:]
        levels.reverse()
        
        for level in levels:
        
            lines = level[:]
            lines.reverse()
            
            for line in lines:
            
                f.write(" ".join(map(lambda n: "%02x" % n, line)))
                f.write("\n")
            
            f.write("\n")

if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <Firetrack UEF file> <output file>\n" % sys.argv[0])
        sys.exit(1)
    
    uef_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        u = UEFfile.UEFfile(uef_file)
        for details in u.contents:
            if details["name"] == "5":
                break
        else:
            raise IOError
        
        maps = Maps(details["data"])
        maps.read_maps()
    
    except (IOError, UEFfile_error):
        sys.stderr.write("Failed to read UEF file: %s\n" % uef_file)
        sys.exit(1)
    
    try:
        f = open(output_file, "w")
        maps.export_text(f)
        f.close()
    
    except IOError:
        sys.stderr.write("Failed to write output file: %s\n" % output_file)
        sys.exit(1)
