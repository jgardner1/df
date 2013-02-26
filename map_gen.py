#!/usr/bin/env python
"""Functions and classes to generate a map"""

import random

from map import Map

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
    depth = 20
    m = Map(width, height, depth)

    # 1/4 of the depth will be empty
    m.terrain_array.extend([0
        for x in range(width)
        for y in range(height)])

    # Grass on level 1
    m.terrain_array.extend([2
        for x in range(width)
        for y in range(height)])


    m.terrain_array.extend([3
        for x in range(width)
        for y in range(height)])


    for z in range(depth-2):
        m.terrain_array.extend([4
            for x in range(width)
            for y in range(height)])

    for terrain in m.terrain_array:
        m.tile_array.append(
            random.choice(tiles[terrain]))

    return m
