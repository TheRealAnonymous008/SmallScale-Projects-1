import pygame
import sys
import random
import copy
import math

# Define the dimensions of the screen
SWIDTH = 800
SHEIGHT = 800

# Define the dimensions of the board
BWIDTH = 80
BHEIGHT = 80

# Define the offset (the size of the border of each cell)
OFFSETX = 0
OFFSETY = 0

# Define the time constant here
TIMECONSTANT = 0.05

#The following constants define the granularity of heat
MINHEAT, MAXHEAT= -100, 100

#The following defines how many particles to display on screen
PARTICLES = 100

# THe following constant controls the rate in which particles move
PARTICLE_CONSTANT = 1

# Define colors here
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0 )
GREEN = (0, 255, 0)
BLUE = (0, 0 , 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

UWIDTH = SWIDTH / BWIDTH
UHEIGHT = SHEIGHT / BHEIGHT

pygame.init
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))

PARTICLE_RADIUS = math.floor(max(SWIDTH / BWIDTH, SHEIGHT / BHEIGHT) / 2)

class Particle:
    def __init__(self):
        self.x, self.y = random.randrange(0, SWIDTH), random.randrange(0, SHEIGHT)
    
    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), PARTICLE_RADIUS)

    def move(self, newx, newy, wt):
        self.x = self.x + wt * (newx - self.x)
        self.y = self.y + wt * (newy - self.y)

class Cell:
    # The following class defines each cell on the grid
    def __init__(self):
        # Attributes
        self.heat = random.randint(MINHEAT, MAXHEAT)

    def modify(self, attr, val):
        # The following function allows modification of attributes
        if(attr == "HEAT"):
            self.heat = val
        elif(attr == "FROST"):
            self.heat = -1 * val

    def draw(self, i, j):
        # The following function draws the (i, j) cell
        r = 0
        b = 0
        g = 0

        # Rounding down is optional

        if self.heat > 0:
            r += self.heat * (255 / MAXHEAT)
        else:
            b += self.heat * (255 / MINHEAT)

        r = max(0, min(r, 255))
        g = max(0, min(g, 255))
        b = max(0, min(b, 255))

        color = (r, g, b)

        pygame.draw.rect(screen, color, (UWIDTH * i + OFFSETX, UHEIGHT * j + OFFSETY, UWIDTH - 2 * OFFSETX, UHEIGHT - 2 * OFFSETY))

    def updateHeat(self, neighbors):
        sum = 0
        for x in neighbors:
            sum = sum + x.heat
        self.heat = self.heat + TIMECONSTANT * (sum / len(neighbors) - self.heat)


    def update(self, neighbors):
        # The neighbors is a list of cells pertaining to cells adjacent to this cell

        # First update the temperature
        self.updateHeat(neighbors)



    def generateCopy(self):
        # The following function generates a copy of this cell
        return copy.deepcopy(self)
        

class Board:
    # The following class defines the board object, containing a list of all the cells in the grid
    def __init__(self):
        self.cells = [[Cell() for i in range(0, BHEIGHT)] for i in range(0, BWIDTH)]
        self.particles = [Particle() for i in range(0, PARTICLES)]
        self.copycells = []

    def generateCopy(self):
        self.copycells = [[i for i in range(0, BHEIGHT)] for j in range(0, BWIDTH)]

        for i in range(0, BWIDTH):
            for j in range(0, BHEIGHT):
                self.copycells[i][j] = self.cells[i][j].generateCopy()

    def updateCells(self):
        # Generate a copy
        self.generateCopy()

        # The following function updates each cell in frame
        for i in range(0, BWIDTH):
            for j in range(0, BHEIGHT):
                # Perform all cell updates here
                
                # To update temperature, change by the differnce between the current temp and the average
                arr = self.getNeighbors(i, j)
                neighbors = []
                for x in arr:
                    a, b = x
                    neighbors.append(self.copycells[a][b])

                self.cells[i][j].update(neighbors)

    def drawGrid(self):
        # The following function draws the grid
        for i in range(0, BWIDTH):
            for j in range(0, BHEIGHT):
                self.cells[i][j].draw(i, j )

    def getNeighbors(self, i, j):
        # THe following function returns a list of neighbors for cell (i, j)
        neighbors = []

        A = 1
        B = 1
        
        for x in range(i - A, i + A + 1):
            for y in range(j - B, j + B + 1): 
                if x >= 0 and y >= 0 and x < BWIDTH and y < BHEIGHT and (x != i or y != j):
                    neighbors.append((x, y))



        return neighbors

    def updateParticles(self):
        for p in self.particles:
            x, y, wt= self.getHottest(p)
            p.move(x * (SWIDTH / BWIDTH), y * (SHEIGHT / BHEIGHT), wt)
            p.draw()

    def getHottest(self, particle):
        posx = particle.x / SWIDTH  * BWIDTH
        posy = particle.y / SHEIGHT  * BHEIGHT
        
        # Apply floor 
        posx = math.floor(posx)
        posy = math.floor(posy)

        if(posx < 0):
            posx = 0
        if posy < 0:
            posy = 0

        if posx >= BWIDTH:
            posx = BWIDTH - 1
        if posy >= BHEIGHT:
            posy = BHEIGHT - 1

        oposx, oposy = posx, posy

        neighbors = self.getNeighbors(posx, posy)
        wt = 0
        
        for n in neighbors:
            i, j = n
            # Move to coldest
            if(self.cells[posx][posy].heat > self.cells[i][j].heat):
                posx, posy = i, j

                
        # Store weight
        tmp1 = (self.cells[posx][posy].heat - MINHEAT ) / (MAXHEAT - MINHEAT)
        tmp2 = (self.cells[oposx][oposy].heat - MINHEAT ) / (MAXHEAT - MINHEAT)
        wt = (tmp2 - tmp1) * PARTICLE_CONSTANT

        return posx, posy, wt




def drawScreen(board):
    # The following function draws the screen per frame
    screen.fill(BLACK)

    # Draw the grid
    board.drawGrid()

    # Update each cell
    board.updateCells()

    # Update all particles
    board.updateParticles()

    # Update screen
    pygame.display.flip()


def main():
    board = Board()
    playing = False
    drawScreen(board)
    # Main Loop
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    playing = not playing
        
        if playing:
            drawScreen(board)

main()