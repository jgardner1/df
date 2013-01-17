#!/usr/bin/env python


import sys
import pygame
import time

class QuitGame(Exception): pass


class Map(object):

    def __init__(self):
        self.tiles = [
            [1,1,1,1,],
            [1,1,1,1,],
            [1,1,1,1,],
        ]

class Tileset(list):

    def __init__(self, filename, tile_width, tile_height=None):
        self.tile_width = tile_width
        self.tile_height = tile_height or tile_width

        image = pygame.image.load("tileset.png")
        r = image.get_rect()
        for x in range(0, r.width/16):
            self.append([])
            for y in range(0, r.height/16):
                self[-1].append(image.subsurface(x*16, y*16, 16, 16))


def main():
    pygame.display.init()
    pygame.font.init()

    pygame.display.set_caption("Dwarf Frontier")

    font = pygame.font.Font(None, 32)


    size = (width, height) = (1280, 720)

    screen = pygame.display.set_mode(size,
        pygame.RESIZABLE | pygame.DOUBLEBUF)

    tiles = Tileset("tileset.png", 16, 16)

            
    # The game clock. This will record how many ticks have passed as well as
    # limit us to 60 fps
    clock = pygame.time.Clock()

    # This event will show the FPS
    SHOW_FPS = pygame.USEREVENT + 1
    pygame.time.set_timer(SHOW_FPS, 1000) 

    viewport = pygame.Rect(0,0,100,100)
    viewport_velocity = [0,0]
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise QuitGame()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    raise QuitGame()

                if event.key == pygame.K_UP:
                    viewport_velocity[1] += 10
                if event.key == pygame.K_DOWN:
                    viewport_velocity[1] += -10
                if event.key == pygame.K_LEFT:
                    viewport_velocity[0] += -10
                if event.key == pygame.K_RIGHT:
                    viewport_velocity[0] += 10

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_UP:
                    viewport_velocity[1] -= 10
                if event.key == pygame.K_DOWN:
                    viewport_velocity[1] -= -10
                if event.key == pygame.K_LEFT:
                    viewport_velocity[0] -= -10
                if event.key == pygame.K_RIGHT:
                    viewport_velocity[0] -= 10

            if event.type == SHOW_FPS:
                screen.blit(
                    font.render("%0.1f" % (clock.get_fps()),
                        True,
                        pygame.Color(255,0,0),
                        pygame.Color(0,0,0)),
                    (300,0))

        viewport.move_ip(*viewport_velocity)

        for i in range(4):
            for j in range(4):
                screen.blit(tiles[0][0], (i*20+viewport.left,j*20+viewport.top))

        pygame.display.flip()


if __name__ == '__main__':
    try:
        main()
    except QuitGame:
        pass
