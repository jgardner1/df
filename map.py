#!/usr/bin/env python
"""The map class and related functions."""

import random
from array import array

class Map(object):
    """The model for the map terrain."""

    def __init__(self, width, height, depth):
        width = int(width)
        height = int(height)
        depth = int(depth)

        assert width > 0
        assert height > 0
        assert depth > 2

        self.width = width
        self.height = height
        self.depth = depth

        self.tiles = array('B')

        self.tiles.extend([
            0
            for x in range(width)
            for y in range(height)])

        self.tiles.extend([
            random.randrange(244,248)
            for x in range(width)
            for y in range(height)])

        self.tiles.extend([
            random.randrange(248,252)
            for x in range(width)
            for y in range(height)])

        for z in range(depth-2):
            self.tiles.extend([
                random.randrange(252,256)
                for x in range(width)
                for y in range(height)])

        

    def __getitem__(self, (x,y,z)):
        return self.tiles[x+self.width*(y+z*self.height)]

