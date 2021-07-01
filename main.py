import pygame, random, sys, time, os
from pygame.locals import *
from local_settings import *

mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption(TITLE)
pygame.font.init()
font = pygame.font.SysFont(None, 36)

backgroundImageMountainsRect = pygame.Rect(0, 0, WINDOWWIDTH, WINDOWHEIGHT // 1.5)
backgroundImageMountains = pygame.image.load(os.path.join(PATH, 'img', 'country-platform-back.png'))
mountainsStretchedImage = pygame.transform.scale(backgroundImageMountains, (WINDOWWIDTH, int(WINDOWHEIGHT // 1.5)))
backgroundImageForests = pygame.image.load(os.path.join(PATH, 'img', 'country-platform-forest.png'))
backgroundImageForestsRect = pygame.Rect(0, WINDOWHEIGHT - (WINDOWHEIGHT // 1.5), WINDOWWIDTH,
                                         backgroundImageForests.get_height())
forestsStretchedImage = pygame.transform.scale(backgroundImageForests, backgroundImageForestsRect.size)

playerRect = pygame.Rect(10, 400, 40, 40)  # left, top, width, height
playerImage = pygame.image.load(os.path.join(PATH, 'img', 'player_simple.png'))
playerStretchedImage = pygame.transform.scale(playerImage, (40, 40))

moveLeft = moveRight = moveUp = moveDown = False
text = ""
input_active = True


def drawText(text, font, surface, x, y):
    textObj = font.render(text, 1, TEXTCOLOR)
    textrect = textObj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textObj, textrect)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if input_active and event.type == KEYDOWN:
            if event.key == K_RETURN:
                input_active = not input_active
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode
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

        if event.type == pygame.MOUSEBUTTONDOWN:
            input_active = not input_active
        windowSurface.fill(BACKGROUND)

        # move the player
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.top += PLAYERMOVESPEED
        if moveUp and playerRect.top > 0:
            playerRect.top -= PLAYERMOVESPEED
        if moveLeft and playerRect.left > 0:
            playerRect.left -= PLAYERMOVESPEED
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.right += PLAYERMOVESPEED

        windowSurface.blit(mountainsStretchedImage, backgroundImageMountainsRect)
        windowSurface.blit(forestsStretchedImage, backgroundImageForestsRect)
        windowSurface.blit(playerStretchedImage, playerRect)
        drawText("2 + 2 = ?", font, windowSurface, (WINDOWWIDTH/3), (WINDOWHEIGHT/1.3))
        drawText(text, font, windowSurface, (WINDOWWIDTH/3), (WINDOWHEIGHT/1.1))

        pygame.display.update()
        mainClock.tick(40)
