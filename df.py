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
    SHOW_FPS = pygame.USEREVENT + 1
    pygame.time.set_timer(SHOW_FPS, 1000) 
    while True:
        frames += 1
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise QuitGame()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    raise QuitGame()

            if event.type == SHOW_FPS:
                print clock.get_fps()

        screen.fill(black, ballrect)

        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]

        screen.blit(ball, ballrect)

        pygame.display.flip()


if __name__ == '__main__':
    try:
        main()
    except QuitGame:
        pass
