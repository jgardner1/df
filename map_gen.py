#!/usr/bin/env python
"""Functions and classes to generate a map"""

import random

from map import Map

def map_gen(width=100, height=100):
    depth = 20
    m = Map(width, height, depth)

    # 1/4 of the depth will be empty
    
    m.tiles.extend([
        0
        for x in range(width)
        for y in range(height)])

    m.tiles.extend([
        random.choice((0, 0, 244, 245, 246, 247))
        for x in range(width)
        for y in range(height)])

    m.tiles.extend([
        random.choice((0, 0, 248, 249, 250, 251))
        for x in range(width)
        for y in range(height)])

    for z in range(depth-2):
        m.tiles.extend([
            random.choice((0, 0, 252, 253, 254, 255))
            for x in range(width)
            for y in range(height)])

    return m
