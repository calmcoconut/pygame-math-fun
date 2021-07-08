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
backgroundImageForestsRect = pygame.Rect(0, FORESTSTART, WINDOWWIDTH, backgroundImageForests.get_height())
forestsStretchedImage = pygame.transform.scale(backgroundImageForests, backgroundImageForestsRect.size)
# start UI
UISTART = FORESTSTART + backgroundImageForests.get_height()
UISIZE = (2 / 3 * WINDOWWIDTH, WINDOWHEIGHT - UISTART)
UILEFT = (WINDOWWIDTH - UISIZE[0]) / 2
UIQUESTIONRECT = pygame.Rect(UILEFT + 5, UISTART + 5, UISIZE[0] - 10, UISIZE[1] * 1 / 3)
UIANSWERRECT = pygame.Rect(UILEFT + 5, UISTART + UISTART * 1 / 6, UISIZE[0] - 10, UISIZE[1] * 1 / 3)

playerRect = pygame.Rect(10, 400, 40, 40)  # left, top, width, height
playerImage = pygame.image.load(os.path.join(PATH, 'img', 'player_simple.png'))
playerStretchedImage = pygame.transform.scale(playerImage, (40, 40))

userInput = ""
input_active = False


def drawText(text, fontObj, surface, centerCoordsTuple, textColor=None, textBgColor=None):
    if textColor is None:
        textColor = TEXTCOLOR
    textObj = fontObj.render(text, True, textColor, textBgColor)
    textRect = textObj.get_rect()
    textRect.center = centerCoordsTuple
    surface.blit(textObj, textRect)


def drawSimpleUI(surface):
    pygame.draw.rect(surface, STEELBLUE, ((UILEFT, UISTART), UISIZE))
    pygame.draw.rect(surface, BLUE, UIQUESTIONRECT)
    pygame.draw.rect(surface, BLACK, UIANSWERRECT)


def quitPygame():
    pygame.quit()
    sys.exit()


while True:
    for event in pygame.event.get():
        if event.type == QUIT and not input_active:
            quitPygame()
        if input_active and event.type == KEYDOWN:
            if event.key == K_RETURN:
                input_active = not input_active
            elif event.key == pygame.K_BACKSPACE:
                userInput = userInput[:-1]
            else:
                userInput += event.unicode
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                quitPygame()

        if event.type == pygame.MOUSEBUTTONUP:
            if not input_active and UIANSWERRECT.collidepoint(event.pos):
                input_active = not input_active
        if event.type == K_RETURN:
            input_active = not input_active
        windowSurface.fill(BACKGROUND)

        windowSurface.blit(mountainsStretchedImage, backgroundImageMountainsRect)
        windowSurface.blit(forestsStretchedImage, backgroundImageForestsRect)
        windowSurface.blit(playerStretchedImage, playerRect)
        drawSimpleUI(windowSurface)
        drawText("2 + 2 = ?", font, windowSurface, UIQUESTIONRECT.center)
        drawText(userInput, font, windowSurface, UIANSWERRECT.center)

        pygame.display.update()
        mainClock.tick(40)
