#!/usr/bin/env python

import pyglet

# Uncomment this line to run BEFORE importing pyglet.window or pyglet.gl to
# disable error checking, which should significantly improve performance.
# Running it with -O should have the same effect.
# http://www.pyglet.org/doc/programming_guide/error_checking.html
# pyglet.options['debug_gl'] = False

from pyglet.window import key, mouse
from pyglet.gl import *

import random

def vec(*args):
    return (GLfloat * len(args))(*args)

window = pyglet.window.Window(fullscreen=True)

# Game mode: Capture mouse, fullscreen
#window = pyglet.window.Window(fullscreen=True)
#window.set_exclusive_mouse()

camera = [0.0,0.0,10.0]

@window.event
def on_key_press(symbol, modifiers):
    print 'A key was pressed'
    if symbol == key.A: print "A"
    elif symbol == key.RIGHT:
        camera[0] += 1
    elif symbol == key.LEFT:
        camera[0] -= 1
    elif symbol == key.UP:
        camera[1] += 1
    elif symbol == key.DOWN:
        camera[1] -= 1
    elif symbol == key.PAGEUP:
        camera[2] += 1
    elif symbol == key.PAGEDOWN:
        camera[2] -= 1

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    # Modifiers may be: # key.MOD_{SHIFT,CTRL,ALT,CAPSLOCK,NUMLOCK,WINDOW,
    #   COMMAND,OPTION,SCROLLLOCK,ACCEL}
    # buttons may be: mouse.LEFT, mouse.MIDDLE, mouse.RIGHT
    if buttons & mouse.RIGHT:
        # TODO: select where they clicked, and then move it so that that
        # point will move with the mouse for the most natural effect.
        camera[0] -= dx/10.0
        camera[1] -= dy/10.0

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    camera[2] += scroll_y
    camera[2] = max(10, min(100, camera[2]))

@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / float(height), .1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

# NEXT STEPS: Draw a potential map with the ceilings and walls.
# Parameterize from a map.
# Vertex arrays: Each square is a new point, 4 new indexes.
# Texture floors and walls with similar texture.
# Add smoothed walls and such.
width = 10
height = 10
batch = pyglet.graphics.Batch()
batch.add_indexed(width*height, GL_QUADS, None,
    sum([(width*y+x, width*y+x+1, width*(y+1)+x+1, width*(y+1)+x)
        for y in range(height-1)
        for x in range(width-1)], ()),
    ('v3i', sum([(x,y,0)
        for y in range(height)
        for x in range(width)], ())),
    ('n3i', sum([(0,0,random.choice((0,1))) for y in range(height) for x in range(width)], ())),
    ('c3B', sum([
        (i*255/width/height, i*255/width/height, random.randrange(0,255))
        for i in range(width*height)], ())))

sphere = gluNewQuadric()

texture = resource.texture(
    'rough-cobblestones-1/brick-floor-tileable_COLOR.jpg')
texture_disp = resource.texture(
    'rough-cobblestones-1/brick-floor-tileable_DISP.jpg')
texture_spec = resource.texture(
    'rough-cobblestones-1/brick-floor-tileable_SPEC.jpg')
glBindTexture(GL_TEXTURE_2D, texture.id)

glEnable(GL_TEXTURE_CUBE_MAP)
cubemap = GLuint()
glGenTextures(1, byref(cubemap))
cubemap = cubemap.value
glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE);
glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR ) #  GL_NEAREST)
glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR ) #  GL_NEAREST)


@window.event
def on_draw():
    glClearColor(0.0, 0.0, 0.0, 0.0)

    # Enable depth tests
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glClearDepth(1.0)

    glEnable(GL_CULL_FACE)

    # Smooth colors between vertexes
    glShadeModel(GL_SMOOTH)
    glPolygonMode(GL_FRONT, GL_FILL)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glDisable(GL_LIGHT2)
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  vec(1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT,  vec(0.0, 0.0, 0.0, 1.0))

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, vec(10.0, 10.0, 10.0, 1.0))
    glRotatef(-30.0, 1, 0, 0)
    glTranslatef(*[-x for x in camera])

    glMaterialfv(GL_FRONT, GL_SPECULAR, vec(1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, vec(0.5, 1.0, 0.5, 1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, vec(20.0))
    glMaterialfv(GL_FRONT, GL_EMISSION, vec(0.2, 0.0, 0.0, 1.0))

    batch.draw()
    gluSphere(sphere, 1.0, 10, 10)

pyglet.app.run()
