import pygame, sys
import time
import math

pygame.init()
screen = pygame.display.set_mode((720,480),0,32)
pygame.display.set_caption("Balls")

def road():
    pygame.draw.line(screen,(0,0,0),(0,420),(350,420),8)
    pygame.draw.line(screen,(0,0,0),(0,420),(720,420),8)

def ball(x,y):
    xr = x
    pygame.draw.circle(screen,(223,162,14),(x,y), 30)
    pygame.draw.line(screen,(0,0,0),(x,y),(x+30,y),2)
    pygame.draw.line(screen,(0,0,0),(x,y),(x-30,y),2)
        
def ballse(x,y):
    xr = x
    pygame.draw.circle(screen,(223,162,14),(x,y), 30)
    pygame.draw.line(screen,(0,0,0),(x,y),(x+30,y),2)
    pygame.draw.line(screen,(0,0,0),(x,y),(x-30,y),2)

    

enter = False
ballx ,bally =0,390
ballsex, ballsey =780,390
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if enter :
        ball(40,235)
        ballse(50, 245)
    else:
        ball(ballx,bally)
        ballse(ballsex, ballsey)

        ballx += 12
        ballsex -= 12
        
    time.sleep(0.06)

    pygame.draw.rect(screen,(108,204,204),(0,0,720,480))
    road()
    ball(ballx,bally)
    ballse(ballsex, ballsey)
    pygame.display.update()
    pygame.display.flip()

pygame.quit()
sys.exit() 
