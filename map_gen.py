#!/usr/bin/env python
"""Functions and classes to generate a map"""

import random

from map import Map

tiles = {
    'water':(208, 209, 210, 211, 224, 225, 226, 227, 240, 241, 242, 243),
    'grass':(212, 213, 214, 215, 228, 229, 230, 231, 244, 245, 246, 247),
    'dirt': (216, 217, 218, 219, 232, 233, 234, 235, 248, 249, 250, 251),
    'stone':(220, 221, 222, 223, 236, 237, 238, 239, 252, 253, 254, 255),
}

def map_gen(width=100, height=100):
    depth = 20
    m = Map(width, height, depth)

    # 1/4 of the depth will be empty
    m.tiles.extend([
        0
        for x in range(width)
        for y in range(height)])

    # Grass on level 1
    m.tiles.extend([
        random.choice(tiles['grass'])
        for x in range(width)
        for y in range(height)])

    m.tiles.extend([
        random.choice(tiles['dirt'])
        for x in range(width)
        for y in range(height)])

    for z in range(depth-2):
        m.tiles.extend([
            random.choice(tiles['stone'])
            for x in range(width)
            for y in range(height)])

    return m
