#!/usr/bin/env python


import sys
import pygame
import time
import random

class QuitGame(Exception): pass

def transpose(matrix):
    return map(list, zip(*matrix))

class Map(object):
        
    class Cell(object):
        pass

    def __init__(self, tileset):
        self.tileset = tileset
        self.width = 200
        self.height = 200
        self.depth = 1

        self.tiles = transpose([[(random.choice([2,3]),random.choice((4,5)))
        for i in range(self.width)] for j in range(self.height)]) 

        self._draw_surface()

    def update(self):
        pass

    def _draw_surface(self):
        tileset = self.tileset
        self.surface = pygame.Surface(
            (self.width*tileset.tile_width,
                self.height*tileset.tile_height))
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                self.surface.blit(
                    tileset[tile[0]][tile[1]],
                    (i*tileset.tile_width, j*tileset.tile_height))

    def draw(self, screen, viewport):
        screen.blit(self.surface, viewport)


class Tileset(list):

    def __init__(self, filename, tile_width, tile_height=None):
        self.tile_width = tile_width
        self.tile_height = tile_height or tile_width

        image = pygame.image.load(filename)
        r = image.get_rect()
        for x in range(0, r.width/tile_width):
            self.append([])
            for y in range(0, r.height/tile_height):
                self[-1].append(image.subsurface(x*tile_width, y*tile_height,
                    tile_width, tile_height))


def main():
    pygame.display.init()
    pygame.font.init()

    font = pygame.font.Font(None, 32)


    size = (width, height) = (640, 480)

    screen = pygame.display.set_mode(size,
        pygame.RESIZABLE | pygame.DOUBLEBUF)

    tiles = Tileset("RPG_Maker_VX_RTP_Tileset_by_telles0808.png", 16, 16)
    map = Map(tiles)

            
    # The game clock. This will record how many ticks have passed as well as
    # limit us to 60 fps
    clock = pygame.time.Clock()

    # This event will show the FPS
    SHOW_FPS = pygame.USEREVENT + 1
    pygame.time.set_timer(SHOW_FPS, 1000) 
    fps_text = font.render("FPS:", True, pygame.Color(255,0,0), pygame.Color(0,0,0))

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
                    viewport_velocity[1] += -10
                if event.key == pygame.K_DOWN:
                    viewport_velocity[1] += 10
                if event.key == pygame.K_LEFT:
                    viewport_velocity[0] += -10
                if event.key == pygame.K_RIGHT:
                    viewport_velocity[0] += 10

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_UP:
                    viewport_velocity[1] -= -10
                if event.key == pygame.K_DOWN:
                    viewport_velocity[1] -= 10
                if event.key == pygame.K_LEFT:
                    viewport_velocity[0] -= -10
                if event.key == pygame.K_RIGHT:
                    viewport_velocity[0] -= 10

            if event.type == SHOW_FPS:
                
                fps_text = font.render("FPS: %0.1f" % (clock.get_fps()),
                        True,
                        pygame.Color(255,0,0),
                        pygame.Color(0,0,0))

        viewport.move_ip(*viewport_velocity)

        screen.fill((0,0,0))
        map.draw(screen, viewport)
        screen.blit(fps_text, (300,0))

        pygame.display.flip()


if __name__ == '__main__':
    try:
        main()
    except QuitGame:
        pass
