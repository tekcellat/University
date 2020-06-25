import pygame
import math
from pygame.locals import *
SIZE = 800, 800
pygame.init()
screen = pygame.display.set_mode(SIZE)
FPSCLOCK = pygame.time.Clock()
done = False
screen.fill((0, 0, 0))
degree=0
while not done:
    screen.fill(0)
    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            done = True
            break
    for x in range(1,400,10):
        pygame.draw.circle(screen,(255,255,255),(400,400),x,1)    
    radar = (400,400)
    radar_len = 400
    x = radar[0] + math.cos(math.radians(degree)) * radar_len
    y = radar[1] + math.sin(math.radians(degree)) * radar_len

    # then render the line radar->(x,y)
    pygame.draw.line(screen, Color("red"), radar, (x,y), 1)
    pygame.display.flip()   
    degree+=5
    FPSCLOCK.tick(40)
