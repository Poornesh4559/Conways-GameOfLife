import os
import random
from matplotlib.pyplot import pause, sca
import numpy as np
import pygame
import time
from sklearn import neighbors

from sympy import false, true

os.environ['SDL_VIDEO_CENTERED'] = '1'

width,height = 1920,1080
size = (width,height)

pygame.init()
pygame.display.set_caption("Game-of-life")
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
clock = pygame.time.Clock()

fps = 30

offset = 1
scale = 30


class Grid:
    def __init__(self,width,height,offset,scale):

        self.row = int(width/scale)
        self.col = int(height/scale)
        self.size = (self.row,self.col)

        self.grid_array = np.ndarray(shape=self.size)
        self.offset = offset
        self.scale = scale



    def random_2d_array(self):
        for i in range(self.row):
            for j in range(self.col):
                self.grid_array[i][j] = random.randint(0,0)


    def neighbour(self,x,y):
        total = 0
        for i in range(-1,2):
            for j in range(-1,2):
                x_edge = (x+i+self.row)%self.row
                y_edge = (y+j+self.col)%self.col

                total += self.grid_array[x_edge][y_edge]

        total -= self.grid_array[x][y]
        return total

    def Conway(self,off_color,on_color,screen,pause):
        for x in range(self.row):
            for y in range(self.col):
                x_pos = x*self.scale
                y_pos = y*self.scale


                if self.grid_array[x][y] == 1:
                    pygame.draw.rect(screen,on_color,[x_pos,y_pos,self.scale-self.offset,self.scale- self.offset])

                else:
                    pygame.draw.rect(screen,off_color,[x_pos,y_pos,self.scale-self.offset,self.scale- self.offset])
        next = np.ndarray(shape=self.size)
        if pause == False:
            for x in range(self.row):
                for y in range(self.col):
                    state = self.grid_array[x][y]
                    neighbors = self.neighbour(x,y)
                    if state ==0 and neighbors == 3:
                        next[x][y] = 1
                    elif state ==1 and (neighbors<2 or neighbors>3):
                        next[x][y] = 0
                    else:
                        next[x][y] = state
            self.grid_array = next


    def mouseHandle(self,x,y):
        _x = x//self.scale
        _y = y//self.scale

        if self.grid_array[_x][_y] != None:
            self.grid_array[_x][_y] = 1
                    
            




black = (0,0,0)
blue = (0,14,71)
white = (255, 255, 255)


grid = Grid(width,height,offset,scale)
grid.random_2d_array()


run = True
pause = True


while run:
    clock.tick(fps)
    screen.fill(white)
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                pause = not pause

    grid.Conway(off_color=black, on_color=white, screen=screen, pause=pause)

    if pygame.mouse.get_pressed()[0]:
        mouseX, mouseY = pygame.mouse.get_pos()
        grid.mouseHandle(mouseX, mouseY)
    pygame.display.update()


pygame.quit()
