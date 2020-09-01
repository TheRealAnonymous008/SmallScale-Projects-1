#Program to simulate and visualize the Gale-Shapley algorithm for the Stable Marriage Problem

import pygame
import random
import sys
from time import sleep

# Initialize everything
pygame.init()
(SWIDTH, SHEIGHT) = (800, 600)
SIZE = 100
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))

pygame.font.init() 
myfont = pygame.font.SysFont('Cambria Math', 30)

class Vertex:
    def __init__(self, index, color):
        self.index = index 
        self.color = color 
        self.preferences = [i for i in range(0, SIZE)]

        # Preference list stores ranked list of indices
        self.partner = None
        random.shuffle(self.preferences)

        loc = (0, 0)
        if color == 0:
            loc = (int(index * (SWIDTH / SIZE) + SWIDTH / (2 *SIZE )), int(SHEIGHT / 4))
        else:
            loc = (int(index * (SWIDTH / SIZE) + SWIDTH / (2 *SIZE)), int(3 * SHEIGHT /4))

        self.loc = loc
        self.proposeList = []

    def draw(self):
        col = (255, 0, 0)

        if self.color == 0:
            col = (0, 0, 255)
        else:
            col = (255, 0, 0)

        pygame.draw.circle(screen, col, self.loc, min(5, SWIDTH / 2))


class Bipartite:
    def __init__(self):
        self.first = []
        self.second = []

        for i in range(0, SIZE):
            self.first.append(Vertex(i, 0))
            self.second.append(Vertex(i, 1))

    def draw(self):
        screen.fill((0, 0, 0))
        for v in self.first:
                
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
            
            v.draw()

        for v in self.second:
                
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
            v.draw()

        # Draw edges
    def showData(self, matched):
        text = str(int( (SIZE - matched )/ SIZE * 100))
        surface = myfont.render("Progress: " + text + "%" , False, (255, 255, 255))
        screen.blit(surface, (10, 10))

    def drawConnections(self, animated = False):
        for v in self.first:
            for i in range(0 ,len(v.preferences)):
                
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        sys.exit()
                x = v.preferences[i]
                (a, b) = self.second[x].loc
                (p, q) = v.loc 
                fact = 255 / SIZE
                color = (0, 0, int(255 - i * fact))

                pygame.draw.aaline(screen, color , v.loc, ((a + p)/ 2, SHEIGHT / 2))
                if animated:
                    sleep(0.01)
                    pygame.display.flip()

        # Draw edges
        for v in self.second:
            for i in range(0 ,len(v.preferences)):
                        
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        sys.exit()
                x = v.preferences[i]
                (a, b) = self.first[x].loc
                (p, q) = v.loc 
                fact = 255 / SIZE

                color = (int(255 - i * fact), 0, 0)

                pygame.draw.aaline(screen, color , v.loc, ((a + p)/ 2, SHEIGHT / 2))

                if animated:
                    sleep(0.01)
                    pygame.display.flip()
        
        pygame.display.flip()

    def drawPartners(self, matched):
        self.draw()
        self.showData(matched)
        for v in self.first:
            if v.partner == None:
                continue
            (x, y) = v.loc
            (a, b) = v.partner.loc

            # How much does v rank their partner 
            fact = (255 - 100) / SIZE
            vpref = v.preferences.index(v.partner.index)
            ppref = v.partner.preferences.index(v.index)
            comp = 255 - int(vpref * fact)
            romp = 255 - int(ppref * fact)
            color1 = (comp, comp, comp)
            color2 = (romp, romp, romp)

            pygame.draw.aaline(screen, color1, v.loc, ((x + a) / 2, SHEIGHT / 2))
            pygame.draw.aaline(screen, color2, v.partner.loc, ((x + a) / 2, SHEIGHT / 2))

        pygame.display.flip()
        sleep(0.01)
        

    def galeShapeley(self):
        unengaged = [v for v in self.first]

        answer = Bipartite()
        ctr = 0
        for v in self.first:
            v.proposeList *= 0 
            for q in v.preferences:
                v.proposeList.append(self.second[q])

        for v in self.first:
            v.partner = None
        for v in self.second:
            v.partner = None
            

        while len(unengaged) > 0:
            man = unengaged.pop(0)
            woman = man.proposeList.pop(0)

            if woman.partner == None: 
                man.partner = woman
                woman.partner = man
            elif woman.preferences[woman.partner.index] < woman.preferences[man.index]:
                unengaged.append(woman.partner)
                woman.partner.partner = None
                woman.partner = man
                man.partner = woman
            else:
                unengaged.append(man)
                continue
                
            self.drawPartners(len(unengaged))


                


def main():
    graph = Bipartite()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                graph.draw()
                pygame.display.flip()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    graph = Bipartite()
                    graph.draw()
                    pygame.display.flip()
                if e.key == pygame.K_e:
                    graph.draw()
                    graph.drawConnections(True)
                if e.key == pygame.K_g:
                    graph.draw()
                    graph.galeShapeley()

        

main()
            
        