import pygame, random, sys, time, os, copy
from pygame.locals import *
from local_settings import *

pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption(TITLE)
pygame.font.init()
font = pygame.font.SysFont(None, 36)

# BG 4/10 OF THE SCREEN, FOREGROUND SHOULD BE 4/10 AS WELL
BG_HEIGHT = int(WINDOWHEIGHT - UIHEIGHT)
BG_RECT_BACK = pygame.Rect(0, 0, WINDOWWIDTH, int(BG_HEIGHT // 1.5))
BG_RECT_FORE = pygame.Rect(0, BG_RECT_BACK.centery, WINDOWWIDTH, int(BG_HEIGHT // 1.5))
# start UI
UI_START = WINDOWHEIGHT - UIHEIGHT
UI_SIZE = (2 / 3 * WINDOWWIDTH, WINDOWHEIGHT - UI_START)
UI_LEFT = (WINDOWWIDTH - UI_SIZE[0]) / 2
UI_QUESTION_RECT = pygame.Rect(UI_LEFT + 5, UI_START + 5, UI_SIZE[0] - 10, UI_SIZE[1] * 1 / 3)
UI_ANSWER_RECT = pygame.Rect(UI_LEFT + 5, UI_START + UI_START * 1 / 6, UI_SIZE[0] - 10, UI_SIZE[1] * 1 / 3)

IMAGES_DICT = {
    'bg_mountains': pygame.transform.scale(pygame.image.load(os.path.join(PATH, 'img', 'country-platform-back.png')),
                                           (WINDOWWIDTH, BG_RECT_BACK.height)),
    'bg_forests': pygame.transform.scale(pygame.image.load(os.path.join(PATH, 'img', 'country-platform-forest.png')),
                                         (WINDOWWIDTH, BG_RECT_FORE.height)),
    'rabbit': pygame.transform.scale(pygame.image.load(os.path.join(PATH, 'img', 'player_simple.png')), (40, 40))
}

PLAYER_IMAGES = {
    'rabbit': IMAGES_DICT['rabbit']
}


playerRect = pygame.Rect(10, 400, 40, 40)  # left, top, width, height
playerImage = pygame.image.load(os.path.join(PATH, 'img', 'player_simple.png'))
playerStretchedImage = pygame.transform.scale(playerImage, (40, 40))

userInput = ""
input_active = False
answer_result = False
USER_ENTERED_ANSW = pygame.USEREVENT + 1


def drawText(text, fontObj, surface, centerCoordsTuple, textColor=None, textBgColor=None):
    if textColor is None:
        textColor = TEXTCOLOR
    textObj = fontObj.render(text, True, textColor, textBgColor)
    textRect = textObj.get_rect()
    textRect.center = centerCoordsTuple
    surface.blit(textObj, textRect)


def drawSimpleUI(surface):
    pygame.draw.rect(surface, STEELBLUE, ((UI_LEFT, UI_START), UI_SIZE))
    pygame.draw.rect(surface, BLUE, UI_QUESTION_RECT)
    pygame.draw.rect(surface, BLACK, UI_ANSWER_RECT)


def drawQuestion(surface, question):
    drawText(question, font, surface, UI_QUESTION_RECT.center)


def checkInputAnswer(surface, correctAnswer):
    global userInput
    try:
        if int(userInput) == correctAnswer:
            userInput = "CORRECT: " + userInput
            return True
        else:
            userInput = "TRY AGAIN: " + userInput
            return False
    except Exception:
        userInput = "TRY AGAIN: " + userInput
        return False


def quitPygame():
    pygame.quit()
    sys.exit()


def refreshScreen():
    pygame.display.update()
    mainClock.tick(40)


while True:
    for event in pygame.event.get():
        if event.type == QUIT and not input_active:
            quitPygame()
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                input_active = not input_active
                oldInput = userInput[:]
                answer_result = checkInputAnswer(windowSurface, 6)
                pygame.time.set_timer(USER_ENTERED_ANSW, 600, True)  # event, time, once?
        if input_active and event.type == KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                userInput = userInput[:-1]
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                pass
            else:
                userInput += event.unicode
        if event.type == KEYUP:
            if event.key == K_ESCAPE and not input_active:
                quitPygame()
            if event.key == K_ESCAPE and input_active:
                input_active = not input_active
        if event.type == pygame.MOUSEBUTTONUP:
            if not input_active and UI_ANSWER_RECT.collidepoint(event.pos):
                input_active = not input_active
        if event.type == USER_ENTERED_ANSW:
            if answer_result:
                userInput = ""
                pygame.event.clear()
                answer_result = False
            else:
                userInput = oldInput

        windowSurface.fill(BACKGROUND)

        windowSurface.blit(IMAGES_DICT['bg_mountains'], BG_RECT_BACK)
        windowSurface.blit(IMAGES_DICT['bg_forests'], BG_RECT_FORE)
        windowSurface.blit(PLAYER_IMAGES['rabbit'], PLAYER_IMAGES['rabbit'].get_rect())
        drawSimpleUI(windowSurface)
        drawQuestion(windowSurface, "2*3=?")
        drawText(userInput, font, windowSurface, UI_ANSWER_RECT.center)
        refreshScreen()
