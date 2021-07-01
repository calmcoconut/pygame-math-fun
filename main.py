import pygame, random, sys, time, os
from pygame.locals import *
from local_settings import *

mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

playerRect = pygame.Rect(300, 100, 40, 40)  # left, top, width, height
playerImage = pygame.image.load(os.path.join(PATH, 'img', 'player_simple.png'))
playerStretchedImage = pygame.transform.scale(playerImage, (40, 40))

moveLeft = moveRight = moveUp = moveDown = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_a:
                moveRight = False
                moveLeft = True
            if event.key == K_d:
                moveLeft = False
                moveRight = True
            if event.key == K_w:
                moveDown = False
                moveUp = True
            if event.key == K_s:
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_a:
                moveLeft = False
            if event.key == K_d:
                moveRight = False
            if event.key == K_w:
                moveUp = False
            if event.key == K_s:
                moveDown = False

        windowSurface.fill(BLUE)

        # move the player
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.top += PLAYERMOVESPEED
        if moveUp and playerRect.top > 0:
            playerRect.top -= PLAYERMOVESPEED
        if moveLeft and playerRect.left > 0:
            playerRect.left -= PLAYERMOVESPEED
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.right += PLAYERMOVESPEED

        windowSurface.blit(playerStretchedImage, playerRect)

        pygame.display.update()
        mainClock.tick(FPS)
