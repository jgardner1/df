#!/usr/bin/env python


import sys
import pygame
import time

class QuitGame(Exception): pass

def main():
    pygame.display.init()
    pygame.display.set_caption("Dwarf Frontier")

    size = (width, height) = (1280, 720)
    speed = [2, 2]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size,
        pygame.RESIZABLE | pygame.DOUBLEBUF)

    ball = pygame.image.load("ball.gif")
    ballrect = ball.get_rect()

    frames = 0
    last_fps = time.time()
    clock = pygame.time.Clock()
    while True:
        frames += 1
        clock.tick(60)

        handle_events()

        screen.fill(black, ballrect)

        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]

        screen.blit(ball, ballrect)

        pygame.display.flip()

        if time.time() - last_fps > 1:
            print "%0.2f" % (frames *1.0 / (time.time() - last_fps),)
            last_fps = time.time()
            frames = 0




def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise QuitGame()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                raise QuitGame()

if __name__ == '__main__':
    try:
        main()
    except QuitGame:
        pass
