#!/usr/bin/env python

# Copyright (c) 2013 Jonathan Gardner jgardner@jonathangardner.net

# Email me for a license you'd like to use this with. I'm open to whatever
# works for you, whatever that may be.


import sys
import pygame
import time
import random

# Used to signal the game should stop running. This is how you break out of
# the game loop.
class QuitGame(Exception): pass

# TODO: Use numpy
def transpose(matrix):
    """Transposes an array of arrays into an array of arrays. IE,
    [[1,2,3],[4,5,6]] goes to [[1,4],[2,5],[3,6]]"""
    return map(list, zip(*matrix))

class MapModel(object):
    """Holds the data of the map. This is the tiles that make up the map along
    with all features that are fixed (everything but items and people.)"""

    def __init__(self):
        self.width = 20
        self.height = 20
        self.depth = 1

        self.tiles = transpose([
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,2,2,2,2,2,3,3,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,2,2,2,2,2,3,3,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
        ])

    def terrain(self,x,y):
        if 0 < x < self.width and 0 < y < self.height:
            return self.tiles[x][y]
        else:
            return 0


class MapView(object):
    """The game map view object.

    This contains its own reference to a particular tileset and a Surface that
    contains a rendering of the current Z level.
    """
        
    def __init__(self, model, tileset):
        self.model = model
        self.tileset = tileset
        self.z = 1

        self._draw_surface()

    def update(self):
        pass

    def _draw_surface(self):
        tileset = self.tileset
        self.surface = pygame.Surface(
            (self.model.width*tileset.tile_width,
                self.model.height*tileset.tile_height))

        terrain_map = {
            1:(0,4),
            2:(2,4),
            3:(6,4),
            4:(8,4),
            5:(10,4),
            6:(12,4),
        }

        for x in range(self.model.width):
            for y in range(self.model.height):
                terrain = self.model.tiles[x][y]
                if terrain == 0:
                    terrain_up = self.model.tiles[x][y-1]
                    if terrain_up == 0:
                        terrain_up2 = self.model.tiles[x][y-2]
                        if terrain_up2 == 0:
                            continue
                        else:
                            tile_home = terrain_map[terrain_up2]
                            tile = (tile_home[0]+x%2, tile_home[1]+3)
                    else:
                        tile_home = terrain_map[terrain_up]
                        tile = (tile_home[0]+x%2, tile_home[1]+2)
                else:
                    tile_home = terrain_map[terrain]
                    tile = (tile_home[0]+x%2, tile_home[1]+y%2)

                self.surface.blit(
                    tileset[tile[0]][tile[1]],
                    (x*tileset.tile_width, y*tileset.tile_height))

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
    # Init pygame
    pygame.display.init()
    pygame.font.init()

    font = pygame.font.Font(None, 32)

    # TODO: Base this on the actual window size, using the VIDEORESIZE event.
    size = (width, height) = (640, 480)

    # This is the screen to draw on.
    # TODO: I'd like an overlay of the game title and controls they can click
    # on.
    screen = pygame.display.set_mode(size,
        pygame.RESIZABLE | pygame.DOUBLEBUF)

    # Initialize game objects. Ideally, the models would already be in place.
    # The main map and tileset

    # The map
    tiles = Tileset("RPG_Maker_VX_RTP_Tileset_by_telles0808.png", 16, 16)
    map_model = MapModel()
    map_view = MapView(map_model, tiles)

    # Dart
    dart_tiles = Tileset("dart.png", 32, 48)

    darts = SpriteGroup()
    for i in range(20):
        darts.add(Dart(dart_tiles, random.randrange(4),
            random.randrange(200),
            random.randrange(200),
            random.randrange(2,20)))

            
    # The game clock. This will record how many ticks have passed as well as
    # limit us to 60 fps.
    clock = pygame.time.Clock()

    # This event will show the FPS
    SHOW_FPS = pygame.USEREVENT + 1

    # Set the SHOW_FPS event to update every 10 seconds.
    pygame.time.set_timer(SHOW_FPS, 1000) 

    # Prepare the text to display in every frame. The FPS is updated by
    # modifying this.
    fps_text = font.render("FPS:", True, pygame.Color(255,0,0), pygame.Color(0,0,0))

    # The offset the user has selected either using arrow keys or the mouse.
    # This is passed into the draw functions as a sort of translation matrix.
    # (TODO: Use an actual matrix transform! OpenGL FTW!!!)
    viewport = pygame.Rect(0,0,100,100)

    # The way the arrow keys work is that we get only events when a key is
    # pressed or released. I adjust the velocity of the viewport according to
    # what the key events were. Then I apply it.
    # TODO: Implement some sort of delay so that a tap on the key will not
    # result in several moves.
    viewport_velocity = [0,0]

    # The main game loop.
    while True:

        # Limit the game loop to once per 1/60 of a second.
        clock.tick(60)

        #
        # Event handler.
        # 

        # Ideally, this would dispatch appropriately. I'd have
        # an event dispatch function that would eventually go to the right
        # controller method.
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
                # Our custom event to update the FPS display. Note that all we
                # do is replace the text. The text is drawn every frame.
                fps_text = font.render("FPS: %0.1f" % (clock.get_fps()),
                        True,
                        pygame.Color(255,0,0),
                        pygame.Color(0,0,0))


        # Apply the velocity from the key state for motion.
        viewport.move_ip(*viewport_velocity)

        #
        # Update
        #

        # TODO: The map will come alive, along with all the MOBs. We first
        # call an update to update all their states.

        # Next, we call an update to the sprites. They may need to adjust
        # based on how the map and MOBs have changed.
        # TODO: There is a tricky dependency here. Animating means that the
        # actual representations of the objects move in discrete intervals.
        # We need some way to reconcile the model's idea of where the object
        # is at with the animated representation of it. I do not want to
        # introduce a dependency of the model on the view. An idea is that the
        # sprite knows where it is at on the screen, and the model tells it
        # where it should be. It rounds off to the closest animation cell and
        # actual screen position, keeping track of whether it should be
        # stepping with the right or left leg.
        darts.update()

        #
        # Assemble the Display
        #

        # Blank the screen
        # TODO: Either make sure subsequent blits completely cover the screen,
        # or use dirtying to minimize the amount of updates we actually do.
        screen.fill((0,0,0))

        # TODO: May need to use a clip rect to contain the map and images if
        # we use a square display?
        # Draw the map to the viewport. Note the map rarely changes.
        map_view.draw(screen, viewport)

        # Draw the sprites on top.
        darts.draw(screen, viewport)

        # TODO: Draw a simple toolbar and status message on top of the above.

        # Draw the FPS message.
        screen.blit(fps_text, (300,0))

        # Flip the display!
        pygame.display.flip()

if __name__ == '__main__':
    # This is outside the main loop because I think it may be faster than
    # setting it up during event processing.
    try:
        main()
    except QuitGame:
        pass
