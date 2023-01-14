#!/usr/bin/env python

import sys
import UEFfile

version = "0.1"

def unlock_block(u, data):

    i = 1
    while data[i] != "\x00":
        i += 1
    
    i += 1
    name = data[1:i]
    load = data[i:i+4]
    exec_ = data[i+4:i+8]
    number = data[i+8:i+10]
    length = data[i+10:i+12]
    flag = chr(ord(data[i+12]) & 0xfe)
    next = data[i+13:i+15]
    unknown = data[i+15:i+17]
    print name[:-1], map(hex, map(ord, next))
    
    new_header = name + load + exec_ + number + length + flag + next + unknown
    crc = u.number(2, u.crc(new_header))
    
    return "*" + new_header + crc + data[i+19:]

if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <Icarus UEF file> <new UEF file>\n" % sys.argv[0])
        sys.exit(1)
    
    u = UEFfile.UEFfile(sys.argv[1])
    
    v = UEFfile.UEFfile(creator = 'unlock.py '+version)
    v.minor = 6
    v.target_machine = "Electron"
    
    for type, data in u.chunks:
    
        if type == 256 and data[0] == "*":
            data = unlock_block(v, data)
        
        v.chunks.append((type, data))
    
    v.write(sys.argv[2], write_emulator_info = False)
    sys.exit()
