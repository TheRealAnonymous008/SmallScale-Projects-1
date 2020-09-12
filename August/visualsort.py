# The following program visualizes sorting algorithms using a bar graph.
# So far the following sorting algorithms have been built in
# selSort -> selection Sort
# sheSort -> shellsort / insertion sort
# qSort -> quickSort
# mSort -> mergeSort
# rSortL -> radix sort, LSD
# rSortM -> radix sort, MSD

import pygame
import sys
import random
import copy
import heapq
from time import sleep

# Initialize pygame
pygame.init()
(SWIDTH, SHEIGHT) = (800, 600)
screen = pygame.display.set_mode((SWIDTH, SHEIGHT))

white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

NUMBERS =50

# Draw function
def draw(numarray, swap1 = NUMBERS + 20, swap2 = NUMBERS + 30):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
    screen.fill((0, 0, 0))
    ulength = SWIDTH / NUMBERS
    uheight = SHEIGHT / NUMBERS
    for i in range(0, len(numarray)):
        color = white
        if i == swap1 and swap1 <= NUMBERS:
            color = green
        if i == swap2 and swap2 <= NUMBERS:
            color = red
        num = numarray[i]
        pygame.draw.rect(screen, color, (ulength * i, SHEIGHT - num * uheight,ulength, num * uheight) )
    pygame.display.flip()

# Swapping of two values within the numarray
def swap(numarray, i, j):
    temp = numarray[j]
    numarray[j] = numarray[i]
    numarray[i] = temp
    swap1 = i
    swap2 = j

    draw(numarray, swap1, swap2)
    return numarray


# Define the sorting algorithm here

def qSort(numarray, l, r):
    if not l < r:
        return numarray

    pivot = numarray[r]
    left = l - 1

    for i in range(l , r):
        if numarray[i] <= pivot:
            left += 1
            swap(numarray, left, i)

    left += 1
    swap(numarray, left, r)


    qSort(numarray, l, left - 1)
    qSort(numarray, left + 1, r)
        

    return numarray

def mSort( numarray, l, r):
    if r - l < 1:
        return numarray

    middle = int((l + r) / 2)

    mSort(numarray, l, middle)
    mSort(numarray, middle + 1, r)

    lptr = l
    rptr = middle + 1
    curr = l
    numcopy = copy.deepcopy(numarray)

    while lptr <= middle and rptr <= r:
        if numcopy[lptr] < numcopy[rptr]: 
            draw(numarray, lptr, curr)
            numarray[curr] = numcopy[lptr]
            lptr += 1
        else:
            draw(numarray, rptr, curr)
            numarray[curr] = numcopy[rptr]
            rptr += 1 

        curr += 1

    while lptr <= middle:
        draw(numarray, lptr, curr)
        numarray[curr] = numcopy[lptr]
        curr += 1
        lptr += 1

    while rptr <= r:
        draw(numarray, rptr, curr)
        numarray[curr] = numcopy[rptr]
        curr += 1
        rptr += 1

    return numarray


def rSortL(numarray, l, r, depth = 16):
    left = l
    right = r

    if right > left and depth >= 0:
        while left < right:
            while True:
                num = numarray[left]
                bit = num >> depth & ~(~0 << 1)

                if bit == 1 or right <= left:
                    break

                left += 1

            while True :
                num = numarray[right]
                bit = num >> depth & ~(~0 << 1)

                if bit == 0 or right <= left :
                    break

                right -= 1
            
            swap(numarray, left, right)

        num = numarray[right]
        bit = num >> depth & ~(~0 << 1)

        if bit == 0:
            right += 1

        rSortL(numarray, l, right - 1, depth - 1)
        rSortL(numarray, right, r, depth - 1)

    return numarray

def rSortM(numarray, l, r, depth = 0):
    middle = 0
    bin1 = []
    bin2 = []
    for i in range(l, r + 1):
        num = numarray[i]
        if num >> depth & ~ (~0 << 1) == 0:
            middle += 1
            bin1.append(num)
        else:
            bin2.append(num)
    ctr = l

    if len(bin2) == 0:
        return

    for x in bin1:
        numarray[ctr] = x
        ctr += 1
        draw(numarray, ctr)
    for y in bin2:
        numarray[ctr] = y
        ctr += 1
        draw(numarray, ctr)

    rSortM(numarray, l, r, depth + 1)


    return numarray

def selSort(numarray, l, r):
    for i in range(l ,r + 1):
        for j in range(i, r + 1):
            if numarray[i] > numarray[j]:
                swap(numarray, i, j)
    return numarray

def sheSort(numarray, l, r):
    n = r - l
    gaps = []
    gap = 1
    while gap < n / 9:
        gaps.append(gap)
        gap = gap * 3 + 1

    gaps.reverse()
        
    for gap in gaps:
        for x in range(gap - 1, r + 2):
            temp = numarray[x - 1]
            y = x
            while y - 1 >= gap  and numarray[y- gap - 1] > temp:
                swap(numarray, y - 1, y -gap - 1)
                y = y - gap 

            numarray[y - 1] = temp
            draw(numarray, y, x)

    return numarray




def mySort(numarray):
    numarray = qSort(numarray, 0, len(numarray) - 1)

    draw(numarray)




def main():
    numarray = [ i for i in range(1, NUMBERS) ] 

    random.shuffle(numarray)
    play = False 
    looped = False

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                play = True

        # Draw the shuffled board . Start with calculating the unit length and height
        if not play:
            draw(numarray)

        elif play and not looped: 
            looped = True
            mySort(numarray)


        pygame.display.flip()

main()
