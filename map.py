#!/usr/bin/env python
"""The map class and related functions."""

import random

class Map(object):
    """The model for the map terrain."""

    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        self.tiles = [
            [
                [random.randrange(244, 256)
                    for y in range(height)]
                for x in range(width)]
            for z in range(depth)]

    def __getitem__(self, i):
        return self.tiles[i]

