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
        random.randrange(244,248)
        for x in range(width)
        for y in range(height)])

    m.tiles.extend([
        random.randrange(248,252)
        for x in range(width)
        for y in range(height)])

    for z in range(depth-2):
        m.tiles.extend([
            random.randrange(252,256)
            for x in range(width)
            for y in range(height)])

    return m
