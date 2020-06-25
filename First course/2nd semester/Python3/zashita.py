import pygame, sys
import time
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (117, 90, 0)
BLUE = (135,255,255)

pygame.init()
size = (700, 500)
screen = pygame.display.set_mode((size))
    
def draw_ball(x_ball, x1,y1, x2,y2):
    pygame.draw.circle(screen,BROWN,(x_ball,y_ball),30)
    pygame.draw.circle(screen,WHITE,(x_ball,y_ball),15)
    pygame.draw.line(screen,BLACK,(x1,y1),(x2,y2),2)
    pygame.draw.line(screen,BLACK,(x1,y1),(x2,y2),2)

def rotate_lines(x,y):
    
    x1 = x
    x = x_ball + (x - x_ball) * math.cos(0.5) + ((y - y_ball) * math.sin(0.5)) 
    y = y_ball + (y - y_ball) * math.cos(0.5) - ((x1 - x_ball) * math.sin(0.5)) 
    return x,y

x1, y1 = 40, 270
x2,y2 = 60,270
x_tire, y_tire = 40, 270
x_ball = 50
y_ball = 270

go = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(BLUE)
    pygame.draw.line(screen,(0,0,0),(0,300),(700,300),4)
    draw_ball(x_ball, x1,y1, x2,y2)
    x_ball += 1
 

    x1,y1 = rotate_lines(x1,y1)
    x2,y2 = rotate_lines(x2,y2)
    
    time.sleep(0.05)
    pygame.display.update()
pygame.quit()
sys.exit()
