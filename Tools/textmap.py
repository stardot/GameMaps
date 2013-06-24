#!/usr/bin/env python

import sys
import UEFfile

version = "0.1"

def unscramble_data(data):

    new_data = ""
    for i in range(len(data)):
    
        new_data += chr(ord(data[i]) ^ ((i + 1) % 256))
    
    return new_data

tile_map = {
 0x00: "XX",    # wall
 0x01: "  ",    # space
 0x02: "[$",    # vending machine
 0x0b: "##",    # beam
 0x20: "M ",    # monster
 0x46: "L ",    # lift (for monsters)
 0x63: "[]",    # crate
 0x64: "{}",    # destructable block
 0x65: "{}",
 0x66: "{}",
 0x67: "{}",
 0x68: "{}",
 0x69: "{}",
 0x6a: "{}",
 0x6b: "{}",
 0x6c: "{}",
 0x6d: "{}",
 0x6e: "{}",
 0x6f: "{}",    # destructable block (almost destroyed)
 0xcf: "s1",    # switches
 0xd0: "s2",
 0xd1: "s3",
 0xd2: "s4",
 0xd9: "d1",    # door labels
 0xda: "d2",
 0xdb: "d3",
 0xdc: "d4",
 0xdd: "d5",
 0xde: "d6",
 0xdf: "c1",    # access cards
 0xe0: "c2",
 0xe1: "c3",
 0xe2: "c4",
 0xe3: "c5",
 0xe4: "c6",
 0xe6: "^^",    # one-way doors
 0xe7: ">>",
 0xe8: "vv",
 0xe9: "<<",
 0xea: "m ",    # mine
 0xeb: " |",    # vertical pipe
 0xec: "__",    # horizontal pipe
 0xed: " /",    # top-left pipe
 0xee: "_\\",   # top-right pipe
 0xef: "_/",    # bottom-right pipe
 0xf0: " \\",   # bottom-left pipe
 0xf1: "V ",    # beam nozzle (facing up)
 0xf2: "-<",    # beam nozzle (facing right)
 0xf3: "A ",    # beam nozzle (facing down)
 0xf4: ">-",    # beam nozzle (facing left)
 0xf7: "| ",    # door (vertical, below door label)
 0xf8: "--",    # door (horizontal, left of door label)
 0xf9: "Ar",    # armour
 0xfa: "Pw",    # power (gun)
 0xfb: "Sp",    # reload speed
 0xfe: ". ",    # credit
 0xfd: "Ex",    # exit
    }

if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <Icarus UEF file> <deck>\n" % sys.argv[0])
        sys.exit(1)
    
    deck = sys.argv[2]
    if len(deck) != 1 or not ord("A") <= ord(deck) <= ord("T"):
    
        sys.stderr.write("Please specify a deck from A to T.\n")
        sys.exit(1)
    
    u = UEFfile.UEFfile(sys.argv[1])
    
    if deck == "A":
        name = "Prog2"
        unscramble = False
    else:
        name = "DECK" + deck
        unscramble = True
    
    for details in u.contents:
    
        if details["name"] == name:
            break
    else:
        sys.stderr.write("Failed to find a suitable data file.\n")
        sys.exit(1)
    
    data = details["data"]
    if unscramble:
        data = unscramble_data(data)
    
    offset = 0
    for row in range(32):
        for column in range(32):
            sys.stdout.write(tile_map.get(ord(data[offset]), "%02X" % ord(data[offset])))
            #sys.stdout.write("%02X" % ord(data[offset]))
            offset += 1
        sys.stdout.write("\n")
    
    sys.exit()
