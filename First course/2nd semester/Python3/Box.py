import pygame
from math import pi, cos, sin, radians
import time
import sys

FPS = 1020
fpsClock = pygame.time.Clock()
y_box = 350
x_box= 200
y_ball = 400
x_ball= 450
dir_box = 0.04
dir_ball = 0.04
alpha_box = 0
alpha_ball = 0
running = 1
width = 640
height = 480
screen = pygame.display.set_mode((width, height))

#colors
red = 255, 0, 0
bgcolor = 1, 0, 0
darkBlue = (0,0,128)
yellow = (255, 255, 128)
angle = 0
angle2 = 0

#function to build and rotate the lines inside the circle
def rotate(x_center,y_center, x_obj, y_obj, angle, color):
    startP = pygame.math.Vector2(int(x_center), int(y_center))
    endP = pygame.math.Vector2(x_obj, y_obj)
    current_endP = startP + endP.rotate(angle)
    pygame.draw.line(screen, color, startP, current_endP, 2)


while running:
    fpsClock.tick(FPS)
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0

    screen.fill(bgcolor)

    pygame.draw.circle(screen, yellow, (550, 100), 50)

    #draw circle
    pygame.draw.circle(screen,yellow, (int(x_ball), int(y_ball)), 12)
    # draw the box
    pygame.draw.rect(screen, darkBlue, pygame.Rect((100, 350), (100, 100)), 10)
    # draw the box top
    pygame.draw.line(screen, red, (100, 350), (x_box, y_box),10)

    #angle of the box top movement
    alpha_box += pi/75*dir_box

    #Move the box top (arc movement)
    x_box = 100 + (100 * cos(alpha_box))
    y_box = 350 - (100 * sin(alpha_box))

    #move the box top from 0 to 90 degrees
    if alpha_box >=pi/2 or alpha_box <= 0:
        dir_box *= -1
    pygame.draw.circle(screen, (243,79,79), (100,350), 12)

    #move the ball on trajectory 0 to 90 degrees
    if alpha_ball < pi/2:
        alpha_ball += pi / 50 * dir_ball
        x_ball = 200 + (190 * cos(alpha_ball))
        y_ball = 450 - (125 * sin(alpha_ball))

    #change trajectory to circle with smaller radius (move the center of movement)
    if alpha_ball >= pi / 2:
        alpha_ball += pi / 23 * dir_ball
        x_ball = 200 + (75 * cos(alpha_ball))
        y_ball = 425 - (100 * sin(alpha_ball))
        if alpha_ball >= pi+0.1:
            dir_ball *= -1
    if alpha_ball <= 0:
        dir_ball *= -1

    #draw and rotate line in the middle of the circle
    angle = (angle + 20 * dir_ball) % 360
    angle2 = (angle2+0.1) % 360
    rotate(int(x_ball), int(y_ball), 8, 0, angle,darkBlue)
    rotate(int(x_ball), int(y_ball), -8, 0, angle,darkBlue)
    rotate(int(x_ball), int(y_ball), 0, 8, angle,darkBlue)
    rotate(int(x_ball), int(y_ball), 0, -8, angle,darkBlue)
    rotate(550, 100, 120, 50, angle2,yellow)
    rotate(550, 100, 120, 50, angle2 +50,yellow)

    rotate(550, 100, 120, 50, angle2 + 100,yellow)

    rotate(550, 100, 120, 50, angle2 + 150,yellow)

    rotate(550, 100, 120, 50, angle2 + 200,yellow)
    rotate(550, 100, 120, 50, angle2 + 250,yellow)
    rotate(550, 100, 120, 50, angle2 + 300,yellow)




    pygame.display.update()
    pygame.display.flip()
