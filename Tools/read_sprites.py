#!/usr/bin/env python

import os, sys
import Image
import UEFfile

version = "0.1"

def unscramble_data(data):

    new_data = ""
    for i in range(len(data)):
    
        new_data += chr(ord(data[i]) ^ (i % 256))
    
    return new_data


def read_columns(byte):

    columns = []
    byte = ord(byte)
    for i in range(4):

        v = (byte & 0x01) | ((byte & 0x10) >> 3)
        byte = byte >> 1
        columns.append(v)

    columns.reverse()
    return "".join(map(chr, columns))


def read_sprite(tile):

    sprite = ""
    
    i = 0
    while i < 24:
        sprite += read_columns(tile[i]) + read_columns(tile[i + 1])
        i += 2
    
    return sprite


def save(file_name, sprite):

    im = Image.fromstring("P", (8, 12), sprite)
    im.putpalette((0,0,0, 255,0,0, 0,255,0, 255,255,255))
    im.save(file_name)


sprite_names = {
    0x0140: ("boots", "armour", "potion", "dagger", "weapons", "crucifix"),
    0x0e40: ("sword_up", "sword_right", "sword_down", "sword_left"),
    0x1100: ("ranger_left1", "skull0", "skull1", "skull2", "skull3", "skull4"),
    0x1910: ("drainer",),
    0x19e0: ("exit",),
    0x1a40: ("wizard_up0", "wizard_up1", "wizard_right0", "wizard_right1",
             "wizard_down0", "wizard_down1", "wizard_left0", "wizard_left1",
             "barbarian_up0", "barbarian_up1", "barbarian_right0", "barbarian_right1",
             "barbarian_down0", "barbarian_down1", "barbarian_left0", "barbarian_left1",
             "fighter_up0", "fighter_up1", "fighter_right0", "fighter_right1",
             "fighter_down0", "fighter_down1", "fighter_left0", "fighter_left1",
             "fireball_up", "fireball_right", "fireball_down", "fireball_left",
             "axe_up", "axe_right", "axe_down", "axe_left",
             "key", "treasure", "food"),
    0x2208: ("v_door",),
    0x2240: ("exp0", "exp1", "exp2", "exp3", "trapdoor"),
    0x2340: ("arrow_up", "arrow_right", "arrow_down", "arrow_left", "h_door"),
    0x2440: ("block", "ranger_up0", "ranger_up1", "ranger_right0", "ranger_right1",
             "ranger_down0", "ranger_down1", "ranger_left0",
             "enemy_up0", "enemy_up1", "enemy_right0", "enemy_right1",
             "enemy_down0", "enemy_down1", "enemy_left0", "enemy_left1"),
    }


if __name__ == "__main__":

    if len(sys.argv) != 3:
    
        sys.stderr.write("Usage: %s <Dunjunz UEF file> <output directory>\n" % sys.argv[0])
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    u = UEFfile.UEFfile(sys.argv[1])
    
    for details in u.contents:
    
        if details["name"] == "Dunjunz":
        
            data = details["data"]
            
            for base, names in sprite_names.items():
            
                for s in range(len(names)):
                
                    offset = base + (s * 48)
                    sprite = read_sprite(data[offset:offset + 0x18])
                    save(os.path.join(output_dir, names[s] + ".png"), sprite)
        
        elif details["name"].startswith("Level"):
        
            level = int(details["name"][5:])
            data = unscramble_data(details["data"])
            
            # Read the wall tile for the level.
            sprite = read_sprite(data[-48:-24])
            save(os.path.join(output_dir, "%02i.png" % level), sprite)
    
    sys.exit()
