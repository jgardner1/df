#!/usr/bin/env python
"""Functions and classes to generate a map"""

import random

from map import Map

class Vec2(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, Vec2):
        return Vec2(self.x+Vec2.x, self.y+Vec2.y)

    def __iadd__(self, Vec2):
        self.x += Vec2.x
        self.y += Vec2.y
        return self

tiles = {
    # Empty
    0:(0,),
    # Water
    1:(208, 209, 210, 211, 224, 225, 226, 227, 240, 241, 242, 243),
    # Grass
    2:(212, 213, 214, 215, 228, 229, 230, 231, 244, 245, 246, 247),
    # Dirt
    3: (216, 217, 218, 219, 232, 233, 234, 235, 248, 249, 250, 251),
    # Stone
    4:(220, 221, 222, 223, 236, 237, 238, 239, 252, 253, 254, 255),
}

def map_gen(width=100, height=100):
    depth = 5
    m = Map(width, height, depth)

    # Zero everything out. Bottom layer is stone.
    m.terrain_array.extend([0]*width*height*(depth-1))
    m.terrain_array.extend([4]*width*height)

    def coord(x,y,z):
        return x + width*(y + height*z)

    def get(x,y,z):
        return m.terrain_array[coord(x,y,z)]

    def set(x,y,z, val):
        m.terrain_array[coord(x,y,z)] = val

    for j in xrange(100):
        pos = Vec2(random.randrange(width), random.randrange(height))
        for i in xrange(100):
            if 0 <= pos.x < width and 0 <= pos.y < height:
                set(pos.x, pos.y, depth-2, 3)
            pos += random.choice((
                Vec2(1,0),
                Vec2(-1,0),
                Vec2(0,1),
                Vec2(0,-1)))

        



    # Turn the terrain into tiles
    for terrain in m.terrain_array:
        m.tile_array.append(
            random.choice(tiles[terrain]))

    return m
