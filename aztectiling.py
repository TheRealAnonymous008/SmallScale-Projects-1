import random
import sys
import pygame


SWIDTH, SHEIGHT = 800, 800
pygame.init()
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

HORIZONTALBIAS = 0.5


def main():
    
    drawScreen()

def drawScreen():
    n = 100
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    screen.fill(BLACK)
                    grid = generateAztecGrid(n)
                    tiling = tileGrid(n)
                    drawTilingOnScreen(tiling)
                    pygame.display.flip()
        

def drawTilingOnScreen(tiling):
    UNIT = SWIDTH / len(tiling)
    for i in range(0, len(tiling)):
        for j in range(0, len(tiling)):
            if tiling[i][j] == "x":
                pygame.draw.rect(screen, WHITE, (UNIT * i, UNIT * j, UNIT, UNIT))
            elif tiling[i][j] == "n":
                pygame.draw.rect(screen, RED, (UNIT * i, UNIT * j, UNIT, UNIT))
            elif tiling[i][j] == "w":
                pygame.draw.rect(screen, BLUE, (UNIT * i, UNIT * j, UNIT, UNIT))
            elif tiling[i][j] == "e":
                pygame.draw.rect(screen, GREEN, (UNIT * i, UNIT * j, UNIT, UNIT))
            elif tiling[i][j] == "s":
                pygame.draw.rect(screen, YELLOW, (UNIT * i, UNIT * j, UNIT, UNIT))

def generateAztecGrid(n):
    grid = [[0 for i in range(0, 2 * n)] for j in range(0, 2 * n)]
    for i in range(0, n):
        for j in range(0, n):
            x = n + i
            y = n + j
            if(i >= j):
                grid[i][y] = "x"
            if(n - j - 1>= i):
                grid[x][y] = "x"
            if(n - j - 1 <= i):
                grid[i][j] = "x"
            if(i <= j):
                grid[x][j] = "x"
    
    return grid

def tileGrid(n):
    tiling = generateAztecGrid(1)
    partition(tiling)

    for order in range(1, n):
        dummyGrid = generateAztecGrid(order + 1)
        transferToDummy(dummyGrid, tiling)

        removeBad(dummyGrid)

        dummyGrid = shuffle(dummyGrid)
        partition(dummyGrid)

        tiling = dummyGrid


        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

        screen.fill(BLACK)
        drawTilingOnScreen(tiling)
        pygame.time.delay(100)
        pygame.display.flip()
    
    return tiling

def transferToDummy(dummy, grid):
    off = int((len(dummy) - len(grid)) / 2)
    for i in range(0, len(grid)):
        for j in range(0, len(grid)):
            if grid[i][j] != 0:
                dummy[i + off][j + off] = grid[i][j]

def removeBad(grid):
    for i in range(0, len(grid)):
        for j in range(0, len(grid)):
            if not isinstance(grid[i][j], int):
                if grid[i][j] == "n" and grid[i][j - 1] == "s":
                    grid[i][j] = "x"
                    grid[i][j - 1] = "x"
                elif grid[i - 1][j] == "e" and grid[i][j] == "w":
                    grid[i - 1][j] = "x"
                    grid[i][j] = "x"


def shuffle(grid):
    empty = generateAztecGrid(int(len(grid) / 2) )
    for i in range(0, len(grid)):
        for j in range(0, len(grid)):
            if not isinstance(empty[i][j], int):              
                if grid[i][j] == "n":
                    empty[i][j - 1] = "n"
                elif grid[i][j] == "e":
                    empty[i + 1][j] ="e"
                elif grid[i][j] == "w":
                    empty[i - 1][j] = "w"
                elif grid[i][j] == "s":
                    empty[i][j + 1] = "s"
                grid[i][j] = "x"

    return empty.copy()


def partition(grid):
    for i in range(0, len(grid) - 1):
        for j in range(0, len(grid) - 1):
            if not isinstance(grid[i][j], int):
                if grid[i][j] == "x" and grid[i][j + 1] == "x" and grid[i + 1][j] == "x" and grid[i + 1][j + 1] == "x":
                    if random.random() < HORIZONTALBIAS:
                        grid[i][j] = "w"
                        grid[i][j + 1] = "w"
                        grid[i + 1][j] = "e"
                        grid[i + 1][j + 1] = "e"
                    else:
                        grid[i][j] = "n"
                        grid[i][j + 1] = "s"
                        grid[i + 1][j] = "n"
                        grid[i + 1][j + 1] = "s"

def printAztecGrid(grid):
    print("=====")
    for i in range(0, len(grid)):
        stream = ""
        for j in range(0, len(grid)):
            stream += str(grid[j][i]) + " "
        print(stream)

    print("=====")
main()