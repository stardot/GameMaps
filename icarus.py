#!/usr/bin/env python

"""
icarus.py - Classes and functions for extracting data from Icarus.

Copyright (C) 2016 David Boddie <david@boddie.org.uk>

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

import sys
import Image
import UEFfile

def unscramble_data(data):

    new_data = ""
    for i in range(len(data)):
    
        new_data += chr(ord(data[i]) ^ ((i + 1) % 256))
    
    return new_data


checksums = [0xf4, 0x6f, 0xfe, 0x74, 0x83, 0x5b, 0x5f, 0x14, 0xd3, 0xdc,
             0x18, 0x89, 0xf1, 0xbd, 0x20, 0x34, 0xfa, 0xbb, 0x06, 0x73]

def add_checksum(level_number, data):

    """Accepts a complete set of level data and calculates the appropriate
    value to replace the last byte with in order to make the calculated
    checksum for the data match the one stored in the game itself. The data
    must be scrambled after this value has been added."""
    
    total = 0
    
    for i in range(len(data) - 1):
        total += ord(data[i])
    
    total = total & 0xff
    
    c = checksums[level_number - 1]
    if c < total:
        v = 0x100 + c - total
    else:
        v = c - total
    
    return data[:-1] + chr(v)


class Level:

    def __init__(self, data, scrambled = True):
    
        if scrambled:
            data = unscramble_data(data)
        
        self.read_data(data)
    
    def read_data(self, data):
    
        offset = 0
        self.tiles = []
        
        for row in range(32):
        
            tile_row = []
            for column in range(32):
            
                tile_row.append(ord(data[offset]))
                offset += 1
            
            self.tiles.append(tile_row)
        
        # Read the wall tile for the level.
        self.wall_sprite = Sprite(data[-48:-24])
        
        # Read the exit position - this doesn't seem to be used.
        self.exit_x = ord(data[0x402])
        self.exit_y = ord(data[0x403])
        
        # Read the players' starting position.
        self.player_x = ord(data[0x40a])
        self.player_y = ord(data[0x40b])


class Sprite:

    def __init__(self, data):
    
        self.data = self.read_sprite(data)
    
    def read_columns(self, byte):
    
        columns = []
        byte = ord(byte)
        for i in range(4):
    
            v = (byte & 0x01) | ((byte & 0x10) >> 3)
            byte = byte >> 1
            columns.append(v)
    
        columns.reverse()
        return "".join(map(chr, columns))
    
    def read_sprite(self, tile):
    
        sprite = ""
        
        i = 0
        while i < 24:
            sprite += self.read_columns(tile[i]) + self.read_columns(tile[i + 1])
            i += 2
        
        return sprite
    
    def image(self, size = None):
    
        im = Image.fromstring("P", (8, 12), self.data)
        im.putpalette((0,0,0, 255,0,0, 255,255,255, 0,255,255))
        if size != None:
            im = im.resize(size, Image.NEAREST)
        return im


class Sprites:

    sprite_names = {
        0x040c: ("wall1",),
        0x0500: ("wall2",),
        0x0530: ("vending", "player_up0", "player_up1", "player_right0",
                 "player_left0", "beam", "robot_up", "robot_left",
                 "v_laser", "h_laser", "fire_up", "fire_left",
                 "explosion0", "explosion1", "lift", "v_dead_top",
                 "v_dead_bottom", "h_dead_top", "h_dead_bottom",
                 "breakable0", "breakable1", "breakable2", "breakable3",
                 "one_way_up", "one_way_left", "mine_inactive", "v_pipe",
                 "h_pipe", "tl_pipe", "tl_pipe", "emitter_up",
                 "emitter_left", "switch", "h_door1", "h_door2",
                 "h_door3", "v_door1", "v_door2", "v_door3",
                 "blank", "h_door_thin1", "h_door_thin2", "h_door_thin3",
                 "v_door_thin1", "v_door_thin2", "v_door_thin3",
                 "exit_open", "exit_closed", "credit", "mine_active",
                 "crate", "card1", "door1", "door2",
                 "door3", "door4", "door5", "door6",
                 "card2", "card3", "card4", "card5",
                 "card6", "wall3", "wall4", "h_door",
                 "v_door", "armour", "weapon", "recharge"),
        }
    
    def __init__(self, data):
    
        self.data = data
        self.sprites = {}
        self.read_all(data)
    
    def read_all(self, data):
    
        for base, names in self.sprite_names.items():
        
            for s in range(len(names)):
            
                offset = base + (s * 24)
                sprite = Sprite(data[offset:offset + 0x18])
                self.sprites[names[s]] = sprite
