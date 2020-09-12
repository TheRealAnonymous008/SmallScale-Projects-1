# The following python program serves as a visualizer for networks and graph based algorithms (undirected graphs). Thehe focus is on spanning
# Trees. These include the following graph algorithms:

# DFS -> Depth First Search
# BFS -> Breadth First Search
# Kruskal's Minimum Spanning Tree Algorithm
# Prim's Minimum Spanning Tree Algorithm

import pygame
import math
import sys
import random
import copy
import heapq
from time import sleep
from operator import attrgetter
from collections import deque


# Initialize everything
pygame.init()
(SWIDTH, SHEIGHT) = (800, 600)
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))
RES = 100
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
VERTMAX = 100
EDGEMAX = 100

# Vetex class contains information about graph vertices, namely its location on the grid and its neighbors (which are also vertices)
# The program assumes that all nodes are on a grid 
class Vertex:
    def __init__(self, x = 0, y = 0):
        self.loc = (int(x), int(y))
        self.neighbors = set()
        self.incidentedges = []
        self.index = -1
        self.place = -1
        self.fav = None

        # Seeds will prevent three vertices from being collinear
        self.seedx = random.randint(0, RES / 2)
        self.seedy = random.randint(0, RES / 2)

    def assignIndex(self, index):
        # For Kruskal's algorithm. Index is what changes. place stays fixed
        self.index = index
        self.place = index


    def draw(self, color = blue):
        if self.loc != (None, None):
            (x, y) = self.loc
            x = x * RES + self.seedx
            y = y * RES + self.seedy
            pygame.draw.circle(screen, color, (int(x), int(y)), int(max(1, RES / 20)))
            return (int(x), int(y))

    def __lt__(self, other):
        return self.index < other.index

# Edge class contains information about edges. An edge will always connect two vertices. 
class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        (x, y) = self.v1.loc
        (a, b) = self.v2.loc
        self.w = (x - a ) * (x - a) + (y - b) * (y - b)
    
    def draw(self, color = white, update = False) :
        loc1 = self.v1.draw()
        loc2 = self.v2.draw()

        pygame.draw.aaline(screen, color, loc1, loc2, 10)

        if update:
            pygame.display.flip()

# The Graph class. It contains methods on graphs including its edge set and its vertex set
class Graph:
    def __init__(self):
        self.length = int(SWIDTH / RES)
        self.height = int(SHEIGHT / RES)
        self.edges = []
        self.vertices = []

    # We prioritize adding edges since we assume that each vertex is connected to another vertex. 
    
    def addEdges(self, v1, v2):

        # Check if v1 and v2 are both in vertices. This is to avoid creating the same vertices again and again

        for x in self.vertices:
            if v1.loc == x.loc:
                v1 = x
            if v2.loc == x.loc:
                v2 = x

        # Check if there is already an edge between these two vertices. If there is return. We assume a simple graph
        if v2 in v1.neighbors or v1 in v2.neighbors:
            return False

        # Add everything to their respective arrays
        e = Edge(v1, v2)
        self.edges.append(e)
        v1.neighbors.add(v2)
        v2.neighbors.add(v1)
        v1.incidentedges.append(e)
        v2.incidentedges.append(e)

        if v1 not in self.vertices:
            self.vertices.append(v1)
        if v2 not in self.vertices:
            self.vertices.append(v2)

        return True

    def draw(self, animate = False):
        # Draw all edges. The edges contain a method to draw their respective vertice
        for e in self.edges:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if not animate:
                e.draw()
            else:
                e.draw(green, True)
                sleep(0.5)

    def bfs(self):
        stack = []
        edges = []
        visited = set()

        stack.append(self.vertices[0])
        prev = self.vertices[0]
        graph = Graph()

        while len(stack) != 0:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
            
            if len(edges) != 0:
                e = edges.pop(0)
                v1 = e.v1
                v2 = e.v2
                
                e.draw((0, 0, 0 , 0), True)
                if not (v1 in visited and v2 in visited):
                    e.draw(green, True)
                    x = copy.deepcopy(v1)
                    y = copy.deepcopy(v2)
                    graph.addEdges(x, y)


            x = stack.pop(0)
            if x not in visited:
                visited.add(x)
                for neighbor in x.neighbors:
                    if neighbor not in visited:
                        stack.append(neighbor)
                        edges.append(Edge(x, neighbor))
                    visited.add(x)
            
            sleep(0.01)
        return graph

    def dfs(self):
        stack = deque()
        edges = deque()
        visited = set()

        stack.append(self.vertices[0])
        prev = self.vertices[0]
        graph = Graph()

        while len(stack) != 0:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()

            if len(edges) != 0:
                e = edges.pop()
                v1 = e.v1
                v2 = e.v2  

                e.draw((0, 0, 0 ), True)

                if not (v1 in visited and v2 in visited):
                    e.draw(green, True)
                    x = copy.deepcopy(v1)
                    y = copy.deepcopy(v2)
                    graph.addEdges(x, y)

            x = stack.pop()
            if x not in visited:
                visited.add(x)
                for neighbor in x.neighbors:
                    if neighbor not in visited:
                        stack.append(neighbor)
                        edges.append(Edge(x, neighbor))
                    visited.add(x)

            sleep(0.01)

        return graph

    def kruskal(self):
        
        for i in range(0, len(self.vertices)):
            v = self.vertices[i]
            v.assignIndex(i)

        
        edgelist = [e for e in self.edges]
        edgelist.sort(key = attrgetter('w'))
        graph = Graph()

        for e in edgelist:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Map x to y
            ptr = e.v2
            while ptr.place != ptr.index:
                ptr = self.vertices[ptr.index]
            ctr = e.v1
            while ctr.place != ctr.index:
                ctr = self.vertices[ctr.index]

            if ptr != ctr: 
                # Unite them if they're disjoint
                e.draw(green, True)
                x = copy.deepcopy(ptr)
                y = copy.deepcopy(ctr)
                graph.addEdges(x, y)
            else:
                e.draw((0, 0 ,0), True)
            self.vertices[ctr.index].index = ptr.index
        
        return graph

    def prim(self):
        graph = Graph()
        arr = [v for v in self.vertices]

        for v in arr:
            v.index = 1000000
        self.vertices[0].index = 0

        heapq.heapify(arr)

        tree = []
        while len(tree) < len(self.vertices):
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            choice = heapq.heappop(arr)
            tree.append(choice)
            for edge in choice.incidentedges:
                edge.draw((0, 0,0) ,True)
            if choice.fav != None:
                choice.fav.draw(green, True)
                a = copy.deepcopy(choice.fav.v1)
                b = copy.deepcopy(choice.fav.v2)
                graph.addEdges(a, b)

            for edge in choice.incidentedges:
                v1 = edge.v1
                v2 = edge.v2
                node = None
                if v1 == choice:
                    node = v2
                else:
                    node = v1
                if node not in tree:
                    if edge.w < node.index:
                        node.fav = edge
                    node.index = min(node.index, edge.w)

            heapq.heapify(arr)

        return graph

            
# The following method randomly creates a path. The path may not necessarily be the shortest path.
def createPath(graph, edges):
    
    prev = None
    safety = 0

    for i in range(0, edges) :
        h = graph.height - 1
        w = graph.length - 1
        x = random.randint(0, w)
        y = random.randint(0, h)
        a = random.randint(0, w)
        b = random.randint(0, h)
        v1 = Vertex(x,y )
        v2 = Vertex(a, b)
        if i > 0:
            v2 = prev
        prev = v1
        
        if graph.addEdges(v1, v2):
            edges += 1
            safety += 1
        else:
            safety = 0
        
        if safety == 100:
            break

    return graph

# The following method creates a random graph from an ALREADY existing graph. It does this by making more edges
def createRandom(graph, edges):
    safety = 0
    for i in range(0, edges):
        x = random.randint(0, len(graph.vertices) - 1)
        y = random.randint(0, len(graph.vertices) - 1)
        
        v1 = graph.vertices[x]
        v2 = graph.vertices[y]

        
        if graph.addEdges(v1, v2):
            edges += 1
            safety += 1
        else:
            safety = 0
        
        if safety == 100:
            break

    return graph

def main():
    # Initialize everything here
    graph = Graph()
    graph = createPath(graph, VERTMAX)
    graph = createRandom(graph, EDGEMAX)

    ograph = None
    # Main loop
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                screen.fill((0, 0, 0))
                graph.draw()
                pygame.display.flip()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_b:
                    screen.fill((0, 0, 0))
                    graph.draw()
                    ograph = graph.bfs()
                    pygame.display.flip()
                elif e.key == pygame.K_d:
                    screen.fill((0, 0, 0))
                    graph.draw()
                    ograph = graph.dfs()
                    pygame.display.flip()
                elif e.key == pygame.K_r:
                    graph = Graph() 
                    ograph = None
                    V = random.randint(1, VERTMAX)
                    E = random.randint(1, EDGEMAX)
                    graph = createPath(graph, V)
                    graph = createRandom(graph, E)
                    screen.fill((0,0, 0 ))
                    graph.draw()
                    pygame.display.flip()
                elif e.key == pygame.K_o:
                    if ograph != None:
                        screen.fill((0,0 ,0))
                        ograph.draw(True)
                        pygame.display.flip()

                elif e.key == pygame.K_k:
                    screen.fill((0, 0, 0))
                    graph.draw()
                    ograph = graph.kruskal()
                    pygame.display.flip()
                elif e.key == pygame.K_p:
                    screen.fill((0, 0, 0))
                    graph.draw()
                    ograph = graph.prim()
                    pygame.display.flip()

main()
