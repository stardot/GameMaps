#!/usr/bin/env python

import sys

class Maps:

    def __init__(self):
    
        self.levels = []
        self.tables = []
    
    def read_maps(self, f):
    
        while True:
        
            a = f.read(1)
            if not a:
                break
            
            b, c = f.read(1), f.read(1)
            
            table = []
            for i in range(8):
                table.append(ord(f.read(1)))
            
            self.tables.append(table)
            
            d = f.read(8)
            level = []
            line = []
            
            while True:
            
                n = ord(f.read(1))
                if n == 0x80:
                    break
                
                if n & 0x80 != 0:
                
                    # Span
                    count = (n >> 3) & 0x0f
                    value = table[n & 0x07]
                    line += [value] * count
                
                elif n & 0x40 != 0:
                
                    # Two byte span
                    value = n & 0x3f
                    count = ord(f.read(1))
                    line += [value] * count
                
                else:
                    line.append(n)
                
                while len(line) >= 20:
                
                    piece, line = line[:20], line[20:]
                    level.append(piece)
            
            if line:
                if len(line) < 20:
                    line += (20 - len(line)) * 0
                level.append(line)
            
            self.levels.append(level)
    
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
    
        sys.stderr.write("Usage: %s <Firetrack map file> <output file>\n" % sys.argv[0])
        sys.exit(1)
    
    map_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        f = open(map_file)
        maps = Maps()
        maps.read_maps(f)
        f.close()
    
    except IOError:
        sys.stderr.write("Failed to read map file: %s\n" % map_file)
        sys.exit(1)
    
    try:
        f = open(output_file, "w")
        maps.export_text(f)
        f.close()
    
    except IOError:
        sys.stderr.write("Failed to write output file: %s\n" % output_file)
        sys.exit(1)
