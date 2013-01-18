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

class Dart(pygame.sprite.Sprite):

    def __init__(self, tileset, facing, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.tileset = tileset
        self.facing = facing
        self.frame = 0
        self.rect = pygame.Rect(x, y,
            self.tileset.tile_width, self.tileset.tile_height)
        self._update_image()
        self.speed = speed
        self.count = speed

        self.big_count = random.randrange(200)

    def update(self):
        self.big_count -= 1
        if self.big_count <= 0:
            self.facing = random.choice((0,1,2,3))
            self.big_count = random.randrange(200)

        self.count -= 1
        if self.count <= 0:
            self.frame = (self.frame+1)%4
            self.count = self.speed
            if self.facing == 0:
                self.rect.top += 4
            elif self.facing == 1:
                self.rect.left -= 4;
            elif self.facing == 2:
                self.rect.right += 4
            elif self.facing == 3:
                self.rect.top -= 4

            if self.rect.bottom < 0:
                self.rect.bottom = 0
                self.facing = 0
            if self.rect.bottom > 200:
                self.rect.bottom = 200
                self.facing = 3
            if self.rect.left < 0:
                self.rect.left = 0
                self.facing = 2
            if self.rect.right > 200:
                self.rect.right = 200
                self.facing = 1
            self._update_image()


    def _update_image(self):
        self.image = self.tileset[self.frame][self.facing]

class SpriteGroup(pygame.sprite.Group):

    def draw(self, surface, viewport):
        sprites = self.sprites()
        sprites.sort(key=lambda sprite: sprite.rect.bottom)
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image,
                spr.rect.move(viewport.left, viewport.top))
        self.lostsprites = []
    


def main():
    pygame.display.init()
    pygame.font.init()

    font = pygame.font.Font(None, 32)


    size = (width, height) = (640, 480)

    screen = pygame.display.set_mode(size,
        pygame.RESIZABLE | pygame.DOUBLEBUF)

    # The main map and tileset
    tiles = Tileset("RPG_Maker_VX_RTP_Tileset_by_telles0808.png", 16, 16)
    map = Map(tiles)

    # Dart
    dart_tiles = Tileset("dart.png", 32, 48)

    darts = SpriteGroup()
    for i in range(20):
        darts.add(Dart(dart_tiles, random.randrange(4),
            random.randrange(200),
            random.randrange(200),
            random.randrange(2,20)))

            
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

            elif event.type == pygame.KEYDOWN:

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

            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_UP:
                    viewport_velocity[1] -= -10
                if event.key == pygame.K_DOWN:
                    viewport_velocity[1] -= 10
                if event.key == pygame.K_LEFT:
                    viewport_velocity[0] -= -10
                if event.key == pygame.K_RIGHT:
                    viewport_velocity[0] -= 10

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # left button
                    pass
                elif event.button == 2:
                    # middle button
                    pass
                elif event.button == 3:
                    # right button
                    pass
                elif event.button == 4:
                    # scroll up
                    pass
                elif event.button == 5:
                    # scroll down
                    pass

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # left button
                    pass
                elif event.button == 2:
                    # middle button
                    pass
                elif event.button == 3:
                    # right button
                    pass
                elif event.button == 4:
                    # scroll up
                    pass
                elif event.button == 5:
                    # scroll down
                    pass

            elif event.type == pygame.MOUSEMOTION:
                # event.pos: The absolute position of the mouse
                # event.rel: The relative motion since the last firing
                # event.buttons: The buttons pressed (left, middle, right)
                if event.buttons[2]: # RMB
                    viewport.move_ip(event.rel)

            elif event.type == SHOW_FPS:
                
                fps_text = font.render("FPS: %0.1f" % (clock.get_fps()),
                        True,
                        pygame.Color(255,0,0),
                        pygame.Color(0,0,0))


        viewport.move_ip(*viewport_velocity)
        darts.update()

        # Blank the screen
        screen.fill((0,0,0))

        map.draw(screen, viewport)
        darts.draw(screen, viewport)

        screen.blit(fps_text, (300,0))

        pygame.display.flip()


if __name__ == '__main__':
    try:
        main()
    except QuitGame:
        pass
