#!/usr/bin/env python

import os, sys
import UEFfile
import dunjunz

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
        
            sprites = dunjunz.Sprites(details["data"])
            
            for name, sprite in sprites.sprites.items():
                sprite.image().save(os.path.join(output_dir, name + ".png"))
        
        elif details["name"].startswith("Level"):
        
            level = dunjunz.Level(details["data"])
            n = int(details["name"][5:])
            
            # Read the wall tile for the level.
            level.wall_sprite.image().save(os.path.join(output_dir, "%02i.png" % n))
    
    sys.exit()
