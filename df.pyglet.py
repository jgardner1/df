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

window = pyglet.window.Window()

camera = [0,0,10]

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
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / float(height), .1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

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
    ('c3B', [random.randrange(0,255) for i in range(width*height*3)]))

@window.event
def on_draw():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(*[-x for x in camera])

    batch.draw()

pyglet.app.run()
