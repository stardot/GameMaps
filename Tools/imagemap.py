#!/usr/bin/env python

import os, sys
import Image
import UEFfile
import dunjunz

type_map = {
    0x28: "treasure",
    0x29: "food",
    0x2a: "crucifix",
    0x2b: "teleport",
    0x51: "exit",
    0x53: "drainer",
    0x5f: "boots",
    0x60: "armour",
    0x61: "potion",
    0x62: "weapons",
    0x63: "dagger"
    }

def get_image_name(level, level_number, row, column):

    if (row, column) == (11, 11):
        return "ranger_up1", None
    elif (row, column) == (12, 11):
        return "wizard_right1", None
    elif (row, column) == (11, 12):
        return "barbarian_down1", None
    elif (row, column) == (12, 12):
        return "fighter_left1", None
    
    elif (column, row) in level.keys:
        n = level.keys[(column, row)]
        return "key", n
    
    elif (column, row) in level.trapdoors:
        return "trapdoor", None
    
    elif level.is_solid(row, column):
        if (column, row) in level.doors:
            n, o = level.doors[(column, row)]
            if o == 0x1d:
                return "v_door", n
            else:
                return "h_door", n
        else:
            return level_number, None
    
    elif level.is_collectable(row, column) and \
         (column, row) in level.lookup:
    
        name = type_map[level.lookup[(column, row)]]
        if name == "teleport":
            return name, level.teleporters.index((column, row))
        else:
            return name, None
    
    else:
        return "blank", None


raw_numbers = [
    "  11  " " 1  1 " "1    1" "1    1" " 1  1 " "  11  ",
    "  11  " " 111  " "  11  " "  11  " "  11  " "111111",
    " 1111 " "1    1" "    1 " "  11  " " 1    " "111111",
    " 1111 " "1    1" "  111 " "     1" "1    1" " 1111 ",
    "  11  " " 1 1  " "111111" "   1  " "   1  " "   1  ",
    "111111" "1     " "11111 " "     1" "1    1" " 1111 ",
    "  111 " " 1    " "11111 " "1    1" "1    1" " 1111 ",
    "111111" "     1" "    1 " "   1  " "  1   " " 1    ",
    " 1111 " "1    1" " 1111 " "1    1" "1    1" " 1111 ",
    " 1111 " "1    1" " 11111" "     1" "     1" " 1111 "
    ]

if __name__ == "__main__":

    if len(sys.argv) != 4:
    
        sys.stderr.write("Usage: %s <Dunjunz UEF file> <level> <output file name>\n" % sys.argv[0])
        sys.exit(1)
    
    level_number = int(sys.argv[2])
    if not 1 <= level_number <= 25:
    
        sys.stderr.write("Please specify a level from 1 to 25.\n")
        sys.exit(1)
    
    u = UEFfile.UEFfile(sys.argv[1])
    output_file_name = sys.argv[3]
    
    for details in u.contents:
    
        if details["name"] == "Dunjunz":
            sprites = dunjunz.Sprites(details["data"])
        
        elif details["name"] == "Level%i" % level_number:
            break
    else:
        sys.stderr.write("Failed to find a suitable data file.\n")
        sys.exit(1)
    
    numbers = {}
    
    for i, n in enumerate(raw_numbers):
        n = n.replace(" ", "\x00").replace("1", "\x02")
        im = Image.fromstring("P", (6, 6), n)
        im.putpalette((0,0,0, 255,0,0, 0,255,0, 255,255,255))
        numbers[i] = im
    
    level = dunjunz.Level(details["data"])
    
    level_image = Image.new("P", (32 * 32, 48 * 24), 0)
    level_image.putpalette((0,0,0, 255,0,0, 0,255,0, 255,255,255))
    
    for row in range(48):
    
        for column in range(32):
        
            image_name, extra = get_image_name(level, level_number, row, column)
            
            if image_name == level_number:
                im = level.wall_sprite.image(size = (32, 24))
            else:
                im = sprites.sprites[image_name].image(size = (32, 24))
            
            level_image.paste(im, (column * 32, row * 24))
            if extra != None:
                extra += 1
                ox = -6
                oy = -1
                while extra > 0:
                    number_im = numbers[extra % 10]
                    ox -= number_im.size[0]
                    level_image.paste(number_im, (
                        (column * 32) + im.size[0] + ox,
                        (row * 24) + im.size[1] - number_im.size[1] + oy))
                    
                    extra = extra / 10
    
    level_image.save(output_file_name)
    
    sys.exit()
