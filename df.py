#!/usr/bin/env python

# Copyright (c) 2013 Jonathan Gardner jgardner@jonathangardner.net

# Email me for a license you'd like to use this with. I'm open to whatever
# works for you, whatever that may be.

try:
    import pyglet
except ImportError:
    print "It appears that you have not installed pyglet."
    raise

window = pyglet.window.Window()
image = pyglet.resource.image('simple.png')

@window.event
def on_draw():
    window.clear()
    image.blit(0,0)

def main():
    pyglet.app.run()

if __name__ == '__main__':
    main()
