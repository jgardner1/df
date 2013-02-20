#!/usr/bin/env python

# Copyright (c) 2013 Jonathan Gardner jgardner@jonathangardner.net

# Email me for a license you'd like to use this with. I'm open to whatever
# works for you, whatever that may be.

import random
import time

try:
    import pyglet
    from pyglet.gl import *
    from pyglet.window import key, mouse
except ImportError:
    print "It appears that you have not installed pyglet."
    raise

window = pyglet.window.Window()

bg_music_player = pyglet.media.Player()
bg_music_player.queue(pyglet.resource.media('dungeon02.mp3'))
bg_music_player.play()

image = pyglet.resource.image('simple.png')
grid = pyglet.image.ImageGrid(image, 16, 16)

batch = pyglet.graphics.Batch()

fps_display = pyglet.clock.ClockDisplay(color=(1.0, 1.0, 1.0, 1.0))
clock = pyglet.clock.get_default()
clock.set_fps_limit(60)

class TerrainGroup(pyglet.graphics.Group):
    
    def __init__(self, parent=None):
        pyglet.graphics.Group.__init__(self, parent)
        self.x = 0
        self.y = 0
        self.z = 0

    def set_state(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)

    def unset_state(self):
        glPopMatrix()
    
class Map(object):
    """The model for the map terrain."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [
            [random.randrange(244, 256) for y in range(height)]
            for x in range(width)]

    def __getitem__(self, i):
        return self.tiles[i]

class MapView(object):
    """Shows the map."""

    def __init__(self, model, batch):
        self.batch = batch
        self.terrain_group = TerrainGroup()
        self.sprites = []
        self.model = model

        self.gen_sprites()

    def gen_sprites(self):
        b = self.batch
        g = self.terrain_group

        self.sprites = [
                [pyglet.sprite.Sprite(
                    grid[self.model[x][y]],
                    x=x*16,
                    y=y*16,
                    batch=b,
                    group=g)
                for y in range(self.model.height)]
            for x in range(self.model.width)
        ]

map = Map(100,100)
map_view = MapView(map, batch)
terrain_group = map_view.terrain_group

@window.event
def on_draw():
    window.clear()
    batch.draw()
    fps_display.draw()

key_state = set()
cur_motion = [0,0]
motion_started = None

def start_motion(dx, dy):
    global motion_started, cur_motion
    cur_motion[0] += dx
    cur_motion[1] += dy
    motion_started = time.time()
    
def stop_motion(dx, dy):
    global motion_started, cur_motion
    cur_motion[0] -= dx
    cur_motion[1] -= dy
    motion_started = time.time()

def calc_motion(dtime, direction):
    return int(max(-100, min(100,
        direction*4+direction*dtime**2+0.5)))
        

@clock.schedule
def tick_motion(dt):
    if cur_motion != [0,0]:
        dtime = time.time() - motion_started
        if dtime:
            if cur_motion[0]:
                terrain_group.x += calc_motion(dtime, cur_motion[0])
            if cur_motion[1]:
                terrain_group.y += calc_motion(dtime, cur_motion[1])


@window.event
def on_key_press(symbol, modifiers):
    key_state.add(symbol)
    if symbol == key.LEFT:
        start_motion(-1, 0)
    elif symbol == key.RIGHT:
        start_motion( 1, 0)
    elif symbol == key.DOWN:
        start_motion(0, -1)
    elif symbol == key.UP:
        start_motion(0,  1)


@window.event
def on_key_release(symbol, modifiers):
    key_state.remove(symbol)
    if symbol == key.LEFT:
        stop_motion(-1, 0)
    elif symbol == key.RIGHT:
        stop_motion( 1, 0)
    elif symbol == key.DOWN:
        stop_motion(0, -1)
    elif symbol == key.UP:
        stop_motion(0,  1)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons == mouse.RIGHT and modifiers == 0:
        terrain_group.x += dx
        terrain_group.y += dy

def main():
    pyglet.app.run()


if __name__ == '__main__':
    main()
