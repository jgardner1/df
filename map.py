#!/usr/bin/env python
"""The map class and related functions."""

from array import array

class Map(object):
    """The model for the map terrain."""

    class ArrayWrapper(object):
        """A convenient proxy to the tiles attribute."""
        def __init__(self, map, array):
            self.array = array
            self.width = map.width
            self.height = map.height
            self.depth = map.depth

        def __getitem__(self, (x,y,z)):
            return self.array[x + self.width*(y + self.height*z)]

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
        self.tile = self.ArrayWrapper(self, self.tiles)

        self.terrain = array('B')
        self.terrain = self.ArrayWrapper(self, self.terrain)
