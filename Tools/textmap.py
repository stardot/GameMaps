#!/usr/bin/env python

import sys
import UEFfile

version = "0.1"

def unscramble_data(data):

    new_data = ""
    for i in range(len(data)):
    
        new_data += chr(ord(data[i]) ^ (i % 256))
    
    return new_data


def read_bits(byte):

    bits = []
    i = 128
    while i > 0:
    
        if byte & i != 0:
            bits.append(1)
        else:
            bits.append(0)
        
        i = i >> 1
    
    return bits


type_map = {
    0x28: "T", # Treasure
    0x29: "F", # Food
    0x2a: "+", # Crucifix
    0x2b: "X", # Teleporter - transports to the square above the next in the list
    0x51: "E", # Exit
    0x53: "*", # Energy drainer
    0x5f: "B", # Boots of speed
    0x60: "A", # Armour
    0x61: "P", # Potion
    0x62: "W", # Weapons pile
    0x63: "D"  # Dagger (+1 damage)
    }

if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <Dunjunz UEF file> <level>\n" % sys.argv[0])
        sys.exit(1)
    
    level = int(sys.argv[2])
    if not 1 <= level <= 25:
    
        sys.stderr.write("Please specify a level from 1 to 25.\n")
        sys.exit(1)
    
    u = UEFfile.UEFfile(sys.argv[1])
    
    for details in u.contents:
    
        if details["name"] == "Level%i" % level:
            break
    else:
        sys.stderr.write("Failed to find a suitable data file.\n")
        sys.exit(1)
    
    data = unscramble_data(details["data"])
    
    solid = []
    collectables = []
    lookup = {}
    
    for i in range(1, 0x20):
    
        x = ord(data[i])
        y = ord(data[0x20 + i])
        t = ord(data[0x40 + i])
        if t != 0xff:
            lookup[(x, y)] = t
    
    doors = {}
    
    for i in range(1, 21):
    
        x = ord(data[0x60 + i])
        y = ord(data[0x75 + i])
        o = ord(data[0x8a + i])
        if x != 0xff and y != 0xff and o != 0xff:
            doors[(x, y)] = (i, o)
    
    keys = {}
    
    for i in range(1, 21):
    
        x = ord(data[0xa0 + i])
        y = ord(data[0xb5 + i])
        if x != 0xff and y != 0xff:
            keys[(x, y)] = i
    
    trapdoors = set()
    
    for i in range(8):
    
        x = ord(data[0xd0 + i])
        y = ord(data[0xd8 + i])
        trapdoors.add((x, y))
    
    offset = 0
    for row in range(48):
    
        r = ((row/8) * 0x20) + (row % 8)
        solid_row = []
        collectables_row = []
        lookup_row = []
        
        for column in range(0, 32, 8):
        
            solid_row += read_bits(ord(data[0xe0 + r + column]))
            collectables_row += read_bits(ord(data[0x1b0 + r + column]))
        
        solid.append(solid_row)
        collectables.append(collectables_row)
    
    for row in range(48):
    
        for column in range(32):
        
            if 11 <= row <= 12 and 11 <= column <= 12:
                sys.stdout.write("S")
            
            elif (column, row) in keys:
                n = keys[(column, row)]
                sys.stdout.write("k")
            
            elif (column, row) in trapdoors:
                sys.stdout.write("O")
            
            elif solid[row][column]:
                if (column, row) in doors:
                    n, o = doors[(column, row)]
                    if o == 0x1d:
                        sys.stdout.write("-")
                    else:
                        sys.stdout.write("|")
                else:
                    sys.stdout.write("#")
            
            elif not collectables[row][column] and (column, row) in lookup:
                t = lookup[(column, row)]
                sys.stdout.write(type_map[t])
            
            else:
                sys.stdout.write(" ")
        
        sys.stdout.write("\n")
    
    sys.exit()
