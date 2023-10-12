import pygame, sys
import random
from pygame.locals import *

#==================================== Var
FPS = 30
windowWidth = 640
windowHeight = 480
revealspeed = 8
boxsize = 40
gapsize = 10
boardWidth = 10
boardHeight = 7
assert (boardWidth * boardHeight) % 2 == 0, 'Board needs to have even number of boxes for pairs of matches'
xMargin = int((windowWidth - (boardWidth * (boxsize + gapsize))) / 2)
yMargin = int((windowHeight - (boardHeight * (boxsize + gapsize))) / 2)

# set color
gray = (100,100,100)
navyblue = (60,60,100)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
orange = (255,128,0)
purple = (255,0,255)
cyan = (0,255,255)

BgColor = navyblue
lightBgColor = gray
boxColor = white
hightLightColor = blue

donut = 'donut'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'

allColor = (red, green, blue, yellow, orange, purple, cyan)
allShapes = (donut, square, diamond, lines, oval)
assert len(allColor) * len(allShapes) * 2 >= boardWidth * boardHeight, "Board is too big for the number of shapes/colors defined"

#===============================function
def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(boardWidth):
        revealedBoxes.append([val] * boardHeight)
    return revealedBoxes

def getRandomSizeBoard():
    #Get a list of avery possible shapes in every possible color
    icons = []
    for color in allColor:
        for shape in allShapes:
            icons.append((shape, color))

    random.shuffle(icons)
    numIconsUsed = int(boardWidth * boardHeight / 2)
    icons = icons[:numIconsUsed]*2
    random.shuffle(icons)

    board = []
    for x in range(boardWidth):
        column = []
        for y in range(boardHeight):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board

def splitItoGroupOf(groupSize, theList):
    #splits a list into a list of lists, where the inner lists have at most groupSize number of imtems
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (boxsize + gapsize) + xMargin
    top = boxy * (boxsize + gapsize) + yMargin
    return (left, top)

def getBoxAtPixel(x, y):
    for boxx in range(boardWidth):
        for boxy in range(boardHeight):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, boxsize, boxsize)
            
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def drawIcon(shape, color, boxx, boxy):
    quarter = int(boxsize * 0.25)
    half = int(boxsize * 0.5)

    left, top = leftTopCoordsOfBox(boxx, boxy)

    #draw
    if shape == donut:
        pygame.draw.circle(Bg, color, (left + half, top + half), half - 5)
        pygame.draw.circle(Bg, BgColor, (left + half, top + half), quarter - 5)
    elif shape == square:
        pygame.draw.rect(Bg, color, (left + quarter, top + quarter, boxsize - half, boxsize - half))
    elif shape == diamond:
        pygame.draw.polygon(Bg, color, ((left + half, top), (left + boxsize - 1, top + half), (left + half, top + boxsize - 1), (left, top + half)))
    elif shape == lines:
        for i in range(0, boxsize, 4):
            pygame.draw.line(Bg, color, (left, top + i), (left + i, top))
            pygame.draw.line(Bg, color, (left + i, top + boxsize - 1), (left + boxsize - 1, top + 1))
    elif shape == oval:
        pygame.draw.ellipse(Bg, color, (left, top + quarter, boxsize, half))
    
def getShapeAndColor(board, boxx, boxy):
    #shape value for x,y spot in stored in board[x][y][0]
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCover(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(Bg, BgColor, (left, top, boxsize, boxsize))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(Bg, BgColor, (left, top, coverage, boxsize))
        pygame.display.update()
        FPSClock.tick(FPS)

def revealBoxesAnimation(board, boxesToReveal):
    #Do the box reveal animation
    for coverage in range(boxsize, (-revealspeed) - 1, - revealspeed):
        drawBoxCover(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
    #Do the "box cover" animation
    for coverage in range(0, boxsize + revealspeed, revealspeed):
        drawBoxCover(board, boxesToCover, coverage)

def drawBoard(board, revealed):
    #draw all of the boxes in their covered or revealed state
    for boxx in range(boardWidth):
        for boxy in range(boardHeight):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                #draw a covered box
                pygame.draw.rect(Bg, boxColor, (left, top, boxsize, boxsize))
            else:
                #draw the (revealed) icon
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(Bg, hightLightColor, (left - 5, top - 5, boxsize + 10, boxsize + 10), 4)

def startGameAnimation(board):
    #randomly reveal the boxes 8 at a time
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(boardWidth):
        for y in range(boardHeight):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitItoGroupOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

def gameWonAnimation(board):
    #Flash the bg color when the player has won
    coveredBox = generateRevealedBoxesData(True)
    color1 = lightBgColor
    color2 = BgColor

    for i in range(13):
        color1, color2 = color2, color1
        Bg.fill(color1)
        drawBoard(board, coveredBox)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    #Return True if all the boxes have been revealed, otherwirse False
    for i in revealedBoxes:
        if False in i:
            return False
            #return False if any boxes are covered
    return True

def main():
    global FPSClock, Bg
    pygame.init()
    FPSClock = pygame.time.Clock()
    Bg = pygame.display.set_mode((windowWidth, windowHeight))

    mousex = 0
    mousey = 0
    pygame.display.set_caption("Game Taido")

    mainBoard = getRandomSizeBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None

    Bg.fill(BgColor)
    startGameAnimation(mainBoard)

    #main loop
    while True:
        mouseClicked = False

        Bg.fill(BgColor)
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            #The mouse is cunrentty over a box
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            elif not revealedBoxes[boxx, boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx, boxy] = True

                if firstSelection == None:
                    firstSelection = (boxx, boxy)
                else:
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        #reset the board
                        mainBoard = getRandomSizeBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        #Show the fully unrevealed board for a second
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        #Replay the start game animation
                        startGameAnimation(mainBoard)
                    firstSelection = None #reset firstSeletion variable
        pygame.display.update()
        FPSClock.tick(FPS)


if __name__ == '__main__':
    main()