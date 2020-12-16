from key import check_checksum
import sys
from tkinter import *
from tkinter import messagebox as mb
import pygame
import random

if not check_checksum("license.key"):
    mb.showerror("error", "U don't have a license 😞 ")
    sys.exit()
else:
    pygame.init()
    
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    
    SIZE = [400, 400]
    
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Snow Animation")
    snow_list = []
    
    for i in range(200):
        x = random.randrange(0, 400)
        y = random.randrange(0, 400)
        snow_list.append([x, y])
    
    clock = pygame.time.Clock()
    
    done = False
    while not done:
    
        for event in pygame.event.get():  
            if event.type == pygame.QUIT: 
                done = True   
    
        screen.fill(BLACK)
    
        for i in range(len(snow_list)):
    
            pygame.draw.circle(screen, WHITE, snow_list[i], 2)
    
            snow_list[i][1] += 1
    
            if snow_list[i][1] > 400:
                y = random.randrange(-50, -10)
                snow_list[i][1] = y
                x = random.randrange(0, 400)
                snow_list[i][0] = x
    
        pygame.display.flip()
        clock.tick(60)