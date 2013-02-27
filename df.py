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
    pyglet.options['audio'] = ('openal', 'directsound', 'alsa', 'silent')
    import pyglet.media
except ImportError:
    print "It appears that you have not installed pyglet."
    raise

from map_gen import map_gen

class Window(pyglet.window.Window):
    fog_color = (GLfloat*4)(47.0/256, 102.0/256, 117.0/256, 1.0)
    fog_mode = GL_EXP
    fog_density = 0.35

    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)

        glClearColor(*self.fog_color)
        glEnable(GL_FOG)
        glFogi(GL_FOG_MODE, self.fog_mode)
        glFogfv(GL_FOG_COLOR, self.fog_color)
        glFogf(GL_FOG_DENSITY, self.fog_density)
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        glFogi(GL_FOG_START, 1)
        glFogi(GL_FOG_END, 10)


    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(gl.GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -100, 1)
        glMatrixMode(gl.GL_MODELVIEW)

    def on_draw(self):
        # Putting this here drives the clock to be 2x fps_limit
        #pyglet.clock.tick()
        self.clear()
        batch.draw()
        fps_display.draw()

    def on_key_press(self, symbol, modifiers):
        key_state.add(symbol)
        if symbol == key.LEFT:
            start_motion(-1, 0)
        elif symbol == key.RIGHT:
            start_motion( 1, 0)
        elif symbol == key.DOWN:
            start_motion(0, -1)
        elif symbol == key.UP:
            start_motion(0,  1)
        elif symbol == key.COMMA and modifiers == key.MOD_SHIFT:
            map_view.z = max(0, map_view.z-1)
            map_view.gen_sprites()
        elif symbol == key.PERIOD and modifiers == key.MOD_SHIFT:
            map_view.z = min(map.depth-1, map_view.z+1)
            map_view.gen_sprites()

    def on_key_release(self, symbol, modifiers):
        key_state.remove(symbol)
        if symbol == key.LEFT:
            stop_motion(-1, 0)
        elif symbol == key.RIGHT:
            stop_motion( 1, 0)
        elif symbol == key.DOWN:
            stop_motion(0, -1)
        elif symbol == key.UP:
            stop_motion(0,  1)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == mouse.RIGHT and modifiers == 0:
            terrain_group.x += dx
            terrain_group.y += dy

window = Window(caption="df by Jonathan Gardner", resizable=True)

bg_music_player = pyglet.media.Player()

bg_music_player.queue(pyglet.media.load('dungeon02.mp3', streaming=False))

# This is deprecated --- and broken!
#bg_music_player.eos_action = 'loop'
bg_music_player._groups[-1].loop = True

bg_music_player.play()

#@bg_music_player.event
#def on_eos():
#    """Called each time we restart the music."""
#    #print "on_eos()"
#    pass
#
#@bg_music_player.event
#def on_player_eos():
#    """Called when the player runs out of music."""
#    #print "on_player_eos()"
#    pass
#
#@bg_music_player.event
#def on_source_group_eos():
#    """Called when a group runs out of music."""
#    #print "on_source_group_eos()"
#    pass

image = pyglet.resource.image('simple.png')
image_texture = image.get_texture()
grid = pyglet.image.ImageGrid(image, 16, 16)

batch = pyglet.graphics.Batch()

fps_display = pyglet.clock.ClockDisplay(color=(1.0, 1.0, 1.0, 1.0))
# This seems to do nothing as of 1.2
#pyglet.clock.set_fps_limit(60)

class TerrainGroup(pyglet.graphics.Group):
    
    def __init__(self, parent=None):
        pyglet.graphics.Group.__init__(self, parent)
        self.x = 0
        self.y = 0
        self.z = 0

        self.fog_mode = GL_EXP
        self.fog_density = 0.35

    def set_state(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)

        glEnable(image_texture.target)
        glBindTexture(image_texture.target, image_texture.id)

        # Enable the alpha channel
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def unset_state(self):
        glDisable(image_texture.target)
        glPopMatrix()
    
class MapView(object):
    """Shows the map."""

    def __init__(self, model, batch):
        self.batch = batch
        self.terrain_group = TerrainGroup()
        self.sprites = []
        self.model = model

        # The current z level we are looking at.
        self.z = 0

        self.vertex_list = None
        self.gen_sprites()

    def gen_sprites(self):
        b = self.batch
        g = self.terrain_group
        m = self.model.tile
        v = self.model.vis
        z = self.z

        if self.vertex_list:
            self.vertex_list.delete()

        vertices = []
        textures = []

        bit = 1.0/256
        for x in range(m.width):
            for y in range(m.height):
                dz = 0
                while dz < 10 and z+dz < m.depth:
                    if not v[x,y,z+dz]:
                        # If they can't see the square, it is invisible.
                        t = 1
                        break

                    t = m[x,y,z+dz]
                    if t != 0:
                        break
                    else:
                        dz += 1

                vertices.extend([
                    x*16,       y*16+16,    dz,
                    x*16,       y*16,       dz,
                    x*16+16,    y*16,       dz,
                    x*16+16,    y*16+16,    dz,
                ])
                tx = t%16
                ty = t//16
                textures.extend([
                    (tx*16   )*bit, (ty*16+16)*bit,
                    (tx*16   )*bit, (ty*16   )*bit,
                    (tx*16+16)*bit, (ty*16   )*bit,
                    (tx*16+16)*bit, (ty*16+16)*bit,
                ])

        self.vertex_list = self.batch.add(
            m.width*m.height*4, # number of vertices
            GL_QUADS, # mode
            g, # group
            ('v3i', tuple(vertices)),
            ('t2f', tuple(textures)))

map = map_gen(100,100)
map_view = MapView(map, batch)
terrain_group = map_view.terrain_group

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
 

@pyglet.clock.schedule
def tick_motion(dt):
    # Putting pyglet.clock.tick() here causes an infinite recursion.
    if cur_motion != [0,0]:
        dtime = time.time() - motion_started
        if dtime:
            if cur_motion[0]:
                terrain_group.x += calc_motion(dtime, cur_motion[0])
            if cur_motion[1]:
                terrain_group.y += calc_motion(dtime, cur_motion[1])

def main():
    pyglet.app.run()


if __name__ == '__main__':
    main()
