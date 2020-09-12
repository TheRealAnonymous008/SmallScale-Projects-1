# The following is a proogram which generates a random maze using a modified randomized version of Kruskal's algorithm.
# The algorithm assigns each edge a randomized weight instead of picking a random neigbor

# The maze also comes with a solver utilizng different algorithms, namely:
# Depth First search
# Breadth first search
# Djikstra's algorithm
# A* algorithm
# B* (Best First search)

# The maze also includes portals (which allows the player to jump from one location to another as long as they are connected)


import pygame
import sys
import random
import copy
import heapq
from time import sleep
from operator import attrgetter

(SWIDTH, SHEIGHT) = (600, 600)
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0 , 255)
BLENGTH = 50
BHEIGHT = 50
ULENGTH = SWIDTH / BLENGTH
UWIDTH = SHEIGHT / BHEIGHT
RANDREM = 0
RANDADD = 50
PORTALS = 0

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []

        # walls correspond to North, South, East West
        self.walls = [False, False, False, False]
        self.parent = self

        # For pathfinder
        self.pre = None
        self.fscore = 0
        self.gscore = 100000000
        self.hscore = 0

    def draw(self, color = white):
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

        for n in self.neighbors:
            (a, b) = (self.x * ULENGTH , self.y * UWIDTH)
            (c, d) = (n.x * ULENGTH , n.y * UWIDTH)
            x = (a + c) / 2
            y = (b + d) / 2

            if a == c:
                pygame.draw.rect(screen, color, (x, y, ULENGTH / 2, UWIDTH))
            elif b == d:
                pygame.draw.rect(screen, color, (x, y, ULENGTH, UWIDTH / 2))

        pygame.draw.rect(screen, color, (self.x * ULENGTH, self.y * UWIDTH, ULENGTH / 2, UWIDTH / 2))

    def __lt__(self, other):
        if self.fscore < other.fscore:
            return self

class Edge:
    def __init__(self, v1, v2, adj = False):
        self.v1 = v1
        self.v2 = v2
        self.adj = adj
        self.weight = random.randint(0, 10)
        v1.neighbors.append(v2)
        v2.neighbors.append(v1)
    
    def draw(self, color = (255, 255, 255)):
        

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
        (a, b) = (self.v1.x * ULENGTH , self.v1.y * UWIDTH)
        (c, d) = (self.v2.x * ULENGTH , self.v2.y * UWIDTH)
        x = (a + c) / 2
        y = (b + d) / 2

        
        if self.adj:
            color = (0, 255, 0)
            pygame.draw.rect(screen, color, (a, b, ULENGTH / 2, UWIDTH / 2))
            pygame.draw.rect(screen, color, (c, d, ULENGTH / 2, UWIDTH / 2))
            pygame.draw.line(screen, color, (a, b), (c,d), 3)
            return

        if a == c:
            pygame.draw.rect(screen, color, (x, y, ULENGTH / 2, UWIDTH))
        elif b == d:
            pygame.draw.rect(screen, color, (x, y, ULENGTH, UWIDTH / 2))

        pygame.draw.rect(screen, color, (a, b, ULENGTH / 2, UWIDTH / 2))
        pygame.draw.rect(screen, color, (c, d, ULENGTH / 2, UWIDTH / 2))
    
        pygame.display.flip()

class Board:
    def __init__(self):
        self.board = [[Vertex(i, j) for i in range(0, BLENGTH) ] for j in range(0, BHEIGHT)]
        self.edges = []
        for i in range(0, BHEIGHT ):
            for j in range(0, BLENGTH ):
                    v1 = self.board[i][j]
                    if i < BHEIGHT - 1:
                        v2 = self.board[i + 1][j]
                        self.edges.append(Edge(v1, v2))
                    if j < BLENGTH -1 :
                        v2 = self.board[i][j + 1]
                        self.edges.append(Edge(v1, v2))



    def draw(self):
        for e in self.edges:
            e.draw()
        
      
    def generateKruskal(self):

        path = []
        self.edges.sort(key = attrgetter('weight'))

        for v in self.board:
            for q in v:
                q.neighbors *= 0

        for edge in self.edges:
                
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
            v1 = edge.v1
            v2 = edge.v2

            ptr = v1
            ctr = v2
            while ptr.parent != ptr:
                ptr = ptr.parent

            while ctr.parent != ctr:
                ctr = ctr.parent

            if ptr != ctr:
                ptr.parent = ctr
                path.append(edge)

        self.edges *= 0
        for e in path:
            (v1, v2) = e.v1, e.v2
            edge = Edge(v1, v2)
            self.edges.append(edge)

        for i in range(0, RANDREM):
            choose = random.choice(self.edges)
            (v1, v2) = choose.v1, choose.v2
            v1.neighbors.remove(v2)
            v2.neighbors.remove(v1)
            self.edges.remove(choose)

        for i in range(0, RANDADD):
            x = random.randint(0, BHEIGHT - 1)
            y = random.randint(0, BLENGTH - 1)
            choice = random.randint(0, 1)

            v1 = self.board[x][y]

            if choice == 0 and x < BHEIGHT - 1:
                v2 = self.board[x + 1][y]
                self.edges.append(Edge(v1, v2))
            
            elif choice == 0 and x == BHEIGHT - 1:
                v2 = self.board[x - 1][y]
                self.edges.append(Edge(v1, v2))

            
            elif choice == 1 and y < BLENGTH - 1:
                v2 = self.board[x][y + 1]
                self.edges.append(Edge(v1, v2))
            
            elif choice == 1 and y ==BLENGTH - 1:
                v2 = self.board[x][y - 1]
                self.edges.append(Edge(v1, v2))
        
        for i in range(0, PORTALS):
            c1 = random.choice(self.edges)
            c2 = random.choice(self.edges)

            v1 = c1.v1
            v2 = c2.v2

            edge = Edge(v1, v2, True)
            self.edges.append(edge)


    def solveBFS(self, start = (0, 0), end = (BLENGTH - 1, BHEIGHT - 1)):
        (x, y) = start
        (dx, dy) = end
        stack = [self.board[x][y]]
        visited = []
        current = self.board[x][y]
        destination = self.board[dx][dy]
        destination.draw((255, 255, 0))
        start = current
        start.draw((255, 0, 255))

        while current != destination and len(stack) > 0:
            
            current = stack.pop(0)
            current.draw(blue)
            if current not in visited:
                visited.append(current)
                for n in current.neighbors:
                    if n not in visited:
                        stack.append(n)
                        n.draw(red)
                        n.pre = current
            start.draw((255, 0, 255))
            destination.draw((255, 255, 0))
            pygame.display.flip()

        # Draw the path
        
        if(current != destination):
            return
        current = destination
        while current.pre != start:
            
            (x1, y1) = current.x, current.y
            (x2, y2) = current.pre.x, current.pre.y
            edge = Edge(Vertex(x1, y1), Vertex(x2, y2))
            edge.draw(green)
            current = current.pre
            pygame.display.flip()

    
    def solveDFS(self, start = (0, 0), end = (BLENGTH - 1, BHEIGHT - 1)):
        (x, y) = start
        (dx, dy) = end
        stack = [self.board[x][y]]
        visited = []
        current = self.board[x][y]
        destination = self.board[dx][dy]
        destination.draw((255, 255, 0))
        start = current
        start.draw((255, 0, 255))


        while current != destination and len(stack) > 0:
            
            current = stack.pop()
            current.draw(blue)
            if current not in visited:
                visited.append(current)
                for n in current.neighbors:
                    if n not in visited:
                        stack.append(n)
                        n.draw(red)
                        n.pre = current
            start.draw((255, 0, 255))
            destination.draw((255, 255, 0))
            pygame.display.flip()

        # Draw the path
        
        if(current != destination):
            return
        current = destination
        while current.pre != start:
            
            (x1, y1) = current.x, current.y
            (x2, y2) = current.pre.x, current.pre.y
            edge = Edge(Vertex(x1, y1), Vertex(x2, y2))
            edge.draw(green)
            current = current.pre
            pygame.display.flip()

    def solveDjikstra(self, start = (0, 0), end = (BLENGTH - 1, BHEIGHT - 1)):
        (x, y) = start
        (dx, dy) = end
        visited = []
        unvisited = []
        examine = []

        for i in self.board:
            for j in i:
                j.gscore = 10000000
                j.fscore = 10000000
                unvisited.append(j)
        
        current = self.board[x][y]
        destination = self.board[dx][dy]
        destination.draw((255, 255, 0))
        start = current
        examine.append(start)
        start.draw((255, 0, 255))
        start.gscore = 0

        while current != destination and len(unvisited) > 0 and len(examine) > 0:

            current = heapq.heappop(examine)
            current.draw(blue)
            if current in unvisited:
                unvisited.remove(current)

            for neighbor in current.neighbors:
                if neighbor  in unvisited:
                    alt = current.gscore + 1
                    if alt < neighbor.gscore:
                        neighbor.gscore = alt
                        neighbor.fscore = alt
                        neighbor.pre = current
                        examine.append(neighbor)

            
                    neighbor.draw(red)
                    pygame.display.flip()

            heapq.heapify(examine) 

        # Draw the path
        examine *= 0
        
        if(current != destination):
            return
        current = destination
        while current.pre != start:
            (x1, y1) = current.x, current.y
            (x2, y2) = current.pre.x, current.pre.y
            edge = Edge(Vertex(x1, y1), Vertex(x2, y2))
            edge.draw(green)
            current = current.pre
            pygame.display.flip()

    def solveAstar(self, start = (0, 0), end = (BLENGTH - 1, BHEIGHT - 1)):
        (x, y) = start
        (dx, dy) = end
        unvisited = []
        examine = []

        for i in self.board:
            for j in i:
                unvisited.append(j)
                j.gscore = 10000000
                j.fscore = 10000000
        
        current = self.board[x][y]
        destination = self.board[dx][dy]
        destination.draw((255, 255, 0))
        start = current
        examine.append(start)
        start.draw((255, 0, 255))
        start.gscore = 0

        while len(examine) > 0 and current != destination:
            current = heapq.heappop(examine)
            current.draw(red)
            for neighbor in current.neighbors:
                hscore = abs(destination.x - neighbor.x) + abs(destination.y - neighbor.y)
                tentative = current.gscore + 1
                neighbor.draw(blue)
                if tentative < neighbor.gscore: 
                    neighbor.gscore = tentative
                    neighbor.pre = current
                    neighbor.fscore = tentative + hscore
                    if neighbor not in examine: 
                        examine.append(neighbor)

            heapq.heapify(examine)

            pygame.display.flip()

        examine *= 0
        if(current != destination):
            return
        current = destination
        while current.pre != start:
            
            (x1, y1) = current.x, current.y
            (x2, y2) = current.pre.x, current.pre.y
            edge = Edge(Vertex(x1, y1), Vertex(x2, y2))
            edge.draw(green)
            current = current.pre
            pygame.display.flip()
                    

    def solveBstar(self, start = (0, 0), end = (BLENGTH - 1, BHEIGHT - 1)):
        (x, y) = start
        (dx, dy) = end
        unvisited = []
        examine = []

        for i in self.board:
            for j in i:
                unvisited.append(j)
                j.gscore = 10000000
                j.fscore = 10000000
        
        current = self.board[x][y]
        destination = self.board[dx][dy]
        destination.draw((255, 255, 0))
        start = current
        examine.append(start)
        start.draw((255, 0, 255))
        start.gscore = 0
        
        while len(examine) > 0 and current != destination:
            current = heapq.heappop(examine)
            current.draw(red)
            for neighbor in current.neighbors:
                hscore = abs(destination.x - neighbor.x) + abs(destination.y - neighbor.y)
                tentative = current.gscore + 1
                neighbor.draw(blue)
                if tentative < neighbor.gscore: 
                    neighbor.gscore = tentative
                    neighbor.pre = current
                    neighbor.fscore = hscore
                    if neighbor not in examine: 
                        examine.append(neighbor)


            heapq.heapify(examine)
            pygame.display.flip()

        examine *= 0
        
        if(current != destination):
            return
        current = destination
        while current.pre != start:
            
            (x1, y1) = current.x, current.y
            (x2, y2) = current.pre.x, current.pre.y
            edge = Edge(Vertex(x1, y1), Vertex(x2, y2))
            edge.draw(green)
            current = current.pre
            pygame.display.flip()
    

        

def main():

    x = random.randint(0, BLENGTH - 1)
    y = random.randint(0, BHEIGHT - 1)
    a = random.randint(0, BLENGTH - 1)
    b = random.randint(0, BHEIGHT - 1)
    maze = Board()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_k:
                    screen.fill((0, 0, 0))
                    
                    x = random.randint(0, BLENGTH - 1)
                    y = random.randint(0, BHEIGHT - 1)
                    a = random.randint(0, BLENGTH - 1)
                    b = random.randint(0, BHEIGHT - 1)
                    maze = Board()
                    maze.generateKruskal()
                    maze.draw()
                if e.key == pygame.K_b:
                    maze.solveBFS((x, y), (a, b))
                if e.key == pygame.K_d:
                    maze.solveDFS((x, y), (a, b))
                if e.key == pygame.K_1:
                    maze.solveDjikstra((x, y), (a, b))
                    
                if e.key == pygame.K_a:
                    maze.solveAstar((x, y), (a, b))
                    
                if e.key == pygame.K_2:
                    maze.solveBstar((x, y), (a, b))
                if e.key == pygame.K_r:
                        
                    x = random.randint(0, BLENGTH)
                    y = random.randint(0, BHEIGHT)
                    a = random.randint(0, BLENGTH)
                    b = random.randint(0, BHEIGHT)
                if e.key == pygame.K_c:
                    screen.fill((0, 0, 0))

        pygame.display.flip()

main()
