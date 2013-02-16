#!/usr/bin/env python

# Copyright (c) 2013 Jonathan Gardner jgardner@jonathangardner.net

# Email me for a license you'd like to use this with. I'm open to whatever
# works for you, whatever that may be.

import random

try:
    import pyglet
    from pyglet.gl import *
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
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)

    def unset_state(self):
        glPopMatrix()
    
terrain_group = TerrainGroup()

map_sprites = [
    pyglet.sprite.Sprite(
        grid[random.choice((255,254,253,252))],
        x=(i%16)*16,
        y=(i//16)*16,
        batch=batch,
        group=terrain_group)
    for i in range(256)
]

@window.event
def on_draw():
    window.clear()
    batch.draw()
    fps_display.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.LEFT:
        terrain_group.x -= 10
    elif symbol == pyglet.window.key.RIGHT:
        terrain_group.x += 10
    elif symbol == pyglet.window.key.DOWN:
        terrain_group.y -= 10
    elif symbol == pyglet.window.key.UP:
        terrain_group.y += 10

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons == pyglet.window.mouse.RIGHT and modifiers == 0:
        terrain_group.x += dx
        terrain_group.y += dy

def main():
    pyglet.app.run()


if __name__ == '__main__':
    main()
