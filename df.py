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
    
terrain_group = TerrainGroup()
item_group = pyglet.graphics.Group(parent=terrain_group)

map_sprites = [
    pyglet.sprite.Sprite(
        grid[random.choice(range(244, 256))],
        x=(i%256)*16,
        y=(i//256)*16,
        batch=batch,
        group=terrain_group)
    for i in range(256*256)
]

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
    terrain_group.x += dx*10
    terrain_group.y += dy*10
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
        cur_motion[0]*4+cur_motion[0]*dtime**2+0.5)))

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
