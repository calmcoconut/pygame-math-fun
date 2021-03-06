import pygame, random, sys, time, os, copy, math_maker
from pygame.locals import *
from local_settings import *
from utils import *
from entities import *

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
    'bg_mountains': pygame.transform.scale(pygame.image.load(getImagePath('country-platform-back.png')),
                                           (WINDOWWIDTH, BG_RECT_BACK.height)),
    'bg_forests': pygame.transform.scale(pygame.image.load(getImagePath('country-platform-forest.png')),
                                         (WINDOWWIDTH, BG_RECT_FORE.height)),
    'rabbit': pygame.transform.scale(pygame.image.load(getImagePath('player_simple.png')), (40, 40))
}

PLAYER_IMAGES = {
    'rabbit': IMAGES_DICT['rabbit']
}

playerRect = pygame.Rect(10, 400, 40, 40)  # left, top, width, height
playerImage = pygame.image.load(os.path.join(PATH, 'img', 'player_simple.png'))
playerStretchedImage = pygame.transform.scale(playerImage, (40, 40))

currentQuestion = math_maker.addition()
userInput = ""
oldInput = ""
input_active = False
answerResult = False
USER_ENTERED_ANSWER = pygame.USEREVENT + 1


def drawText(text, fontObj, surface, centerCoordsTuple, textColor=None, textBgColor=None):
    if textColor is None:
        textColor = TEXTCOLOR
    textObj = fontObj.render(text, True, textColor, textBgColor)
    textRect = textObj.get_rect()
    textRect.center = centerCoordsTuple
    surface.blit(textObj, textRect)


def drawButton(text, fontObj, surface, centerCoordsTuple, textColor=None, textBgColor=None):
    if textColor is None:
        textColor = TEXTCOLOR
    textObj = fontObj.render(text, True, textColor, textBgColor)
    textRect = textObj.get_rect()
    textRect.center = centerCoordsTuple
    surface.blit(textObj, textRect)
    return textRect


def drawSimpleUI(surface):
    pygame.draw.rect(surface, STEELBLUE, ((UI_LEFT, UI_START), UI_SIZE))
    pygame.draw.rect(surface, BLUE, UI_QUESTION_RECT)
    pygame.draw.rect(surface, BLACK, UI_ANSWER_RECT)


def drawQuestion(surface, question):
    drawText(question, font, surface, UI_QUESTION_RECT.center)


def checkInputAnswer(correctAnswer):
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
    mainClock.tick(FPS)


def drawBackground():
    windowSurface.fill(BACKGROUND)
    windowSurface.blit(IMAGES_DICT['bg_mountains'], BG_RECT_BACK)
    windowSurface.blit(IMAGES_DICT['bg_forests'], BG_RECT_FORE)


def recordTextInput():
    global userInput
    if event.key == pygame.K_BACKSPACE:
        userInput = userInput[:-1]
    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
        pass
    else:
        userInput += event.unicode


def handleAnswer():
    global input_active, oldInput, answerResult, currentQuestion
    input_active = not input_active
    oldInput = userInput[:]
    answerResult = checkInputAnswer(currentQuestion[0])
    pygame.time.set_timer(USER_ENTERED_ANSWER, 600, True)  # event, time, once?


def handleTextInput(event):
    global userInput
    if event.key == pygame.K_BACKSPACE:
        userInput = userInput[:-1]
    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
        pass
    else:
        userInput += event.unicode


def checkTermination(event):
    if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE and not input_active)):
        quitPygame()


def handleAnswerEntered():
    global answerResult, userInput
    if answerResult:
        userInput = ""
        pygame.event.clear()
        answerResult = False
        return True
    else:
        userInput = oldInput
        return False


def generateNewQuestion():
    global currentQuestion
    currentQuestion = math_maker.addition()


def draw_health_bar(surf, pos, number):
    heart = pygame.image.load(getImagePath("health_heart.png"))
    heart = pygame.transform.scale(heart, (20,20))
    offset = 20
    for i in range(number):
        surf.blit(heart, pos)
        pos = (pos[0]+offset, pos[1])


sprites = pygame.sprite.Group(Player((100, 100)))


def runGame():
    global input_active
    while True:
        isCorrect = False
        for event in pygame.event.get():
            checkTermination(event)
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    handleAnswer()
            if input_active and event.type == KEYDOWN:
                handleTextInput(event)
            if event.type == KEYUP:
                if event.key == K_ESCAPE and input_active:
                    input_active = not input_active
            if event.type == pygame.MOUSEBUTTONUP:
                if not input_active and UI_ANSWER_RECT.collidepoint(event.pos):
                    input_active = not input_active
            if event.type == USER_ENTERED_ANSWER:
                isCorrect = handleAnswerEntered()
            if isCorrect:
                generateNewQuestion()

        drawBackground()
        windowSurface.blit(PLAYER_IMAGES['rabbit'], playerRect)
        drawSimpleUI(windowSurface)

        sprites.draw(windowSurface)
        sprites.update()
        drawQuestion(windowSurface, currentQuestion[1])
        drawText(userInput, font, windowSurface, UI_ANSWER_RECT.center)
        draw_health_bar(windowSurface,(10, UI_START + 50), 4)
        refreshScreen()


add_but_color = sub_but_color = mult_but_color = div_but_color = BLUE
while True:
    windowSurface.fill(BACKGROUND)
    mainRect = windowSurface.get_rect()
    menuRect = pygame.Rect(mainRect.left + 100, mainRect.top + 100, int(mainRect.width * 2 / 3),
                           int(mainRect.height * 2 / 3))
    pygame.draw.rect(windowSurface, BLACK, menuRect)
    drawText("Welcome", font, windowSurface, (mainRect.midtop[0], int(WINDOWHEIGHT * 1 / 5)))

    optionsStart_x = menuRect.midtop[0]
    optionsStart_y = menuRect.midtop[1] + 100
    add_rect = drawButton("Addition", font, windowSurface, (optionsStart_x, optionsStart_y), textBgColor=add_but_color)
    sub_rect = drawButton("Subtraction", font, windowSurface, (optionsStart_x, optionsStart_y + 50),
                          textBgColor=sub_but_color)
    mult_rect = drawButton("Multiplication", font, windowSurface, (optionsStart_x, optionsStart_y + 100),
                           textBgColor=mult_but_color)
    div_rect = drawButton("Division", font, windowSurface, (optionsStart_x, optionsStart_y + 150),
                          textBgColor=div_but_color)

    for event in pygame.event.get():
        checkTermination(event)
        if event.type == pygame.MOUSEMOTION:
            if add_rect.collidepoint(event.pos):
                add_but_color = STEELBLUE
            else:
                add_but_color = BLUE
            if sub_rect.collidepoint(event.pos):
                sub_but_color = STEELBLUE
            else:
                sub_but_color = BLUE
            if mult_rect.collidepoint(event.pos):
                mult_but_color = STEELBLUE
            else:
                mult_but_color = BLUE
            if div_rect.collidepoint(event.pos):
                div_but_color = STEELBLUE
            else:
                div_but_color = BLUE

        if event.type == pygame.MOUSEBUTTONUP:
            if add_rect.collidepoint(event.pos):
                setting = "add"
                runGame()
            elif sub_rect.collidepoint(event.pos):
                setting = "sub"
                runGame()
            elif mult_rect.collidepoint(event.pos):
                setting = "sub"
                runGame()
            elif div_rect.collidepoint(event.pos):
                setting = "sub"
                runGame()

    refreshScreen()
