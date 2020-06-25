import pygame,  sys
from pygame.locals import *
from pygame import *
#import pygame
from math import cos, sin, pi


gray = (35, 31, 32)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)


pygame.init()
screen = pygame.display.set_mode((738, 800), 0, 32)
pygame.scrap.init()
pygame.display.set_caption('Совушка')
clock = pygame.time.Clock()


def static():
    # тело ------------------------------------------------------------------


    pygame.draw.ellipse(screen, gray, [(53, 10), (641, 759)], 0)
    clock_cen = (370, 532)
    clock_rad = 224
    # pygame.draw.circle(screen, white, clock_cen, clock_rad, 0)
    pygame.draw.ellipse(screen, white, [(120, 320), (500, 420)], 0)

    # ушки  --------------------------------------------------------------

    ear_1_coord = [(106, 0), (155, 130), (256, 43)]
    pygame.draw.polygon(screen, gray, ear_1_coord, 0)
    ear_2_coord = [(479, 48), (607, 2), (574, 135)]
    pygame.draw.polygon(screen, gray, ear_2_coord, 0)

    # глазки -----------------------------------------------------------

    eye_11_cen = (266, 183)
    eye_11_rad = 110
    pygame.draw.circle(screen, white, eye_11_cen, eye_11_rad, 0)
    eye_21_cen = (456, 179)
    eye_21_rad = 110
    pygame.draw.circle(screen, white, eye_21_cen, eye_21_rad, 0)
    # носик -------------------------------------------------------------
    nose_coord = [(325, 232), (390, 232), (360, 307)]
    pygame.draw.polygon(screen, gray, nose_coord, 0)

    nose_coord = [(325, 232), (390, 232), (360, 307)]
    pygame.draw.polygon(screen, white, nose_coord, 4)

    # крылья --------------------------------------------------------------
    ##pygame.draw.circle(screen, white,(113, 526), 120 , 0)

    # лапки ---------------------------------------------------------------


    # цифры --------------------------------------------------------------

    font = pygame.font.SysFont('comicsansms', 64)

    text = font.render('12', True, black)
    screen.blit(text, (335, 325))

    text = font.render('1', True, black)
    screen.blit(text, (445, 350))

    text = font.render('2', True, black)
    screen.blit(text, (510, 400))

    text = font.render('3', True, black)
    screen.blit(text, (550, 480))

    text = font.render('6', True, black)
    screen.blit(text, (363, 650))

    text = font.render('9', True, black)
    screen.blit(text, (162, 500))

    text = font.render('4', True, black)
    screen.blit(text, (510, 580))

    text = font.render('5', True, black)
    screen.blit(text, (445, 630))

    text = font.render('7', True, black)
    screen.blit(text, (280, 630))

    text = font.render('8', True, black)
    screen.blit(text, (217, 580))

    text = font.render('8', True, black)
    screen.blit(text, (217, 580))

    text = font.render('10', True, black)
    screen.blit(text, (174, 415))

    text = font.render('11', True, black)
    screen.blit(text, (240, 350))

    # стрелки -------------------------------------------------------------

    cen_cen = (372, 529)
    cen_rad = 25
    pygame.draw.circle(screen, gray, cen_cen, cen_rad, 0)



    # moving -------------------------------------------------------------

done = False
t = - pi / 2
k = - pi / 2
l = - pi / 2
tick = 0
pos = 1
x = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill((250, 240, 230))
    owl = image.load("owl.jpg")
    owl_rec = owl.get_rect()
    screen.blit(owl, owl_rec)
    static()
    if pos == 1:
        pos = 2
        x = 0
    elif pos == 2:
        pos = 3
        x = 25
    elif pos == 3:
        pos = 4
        x = 50
    elif pos == 4:
        pos = 5
        x = 75
    elif pos == 5:
        pos = -1
        x = 100
    elif pos == -1:
        pos = -2
        x = 75
    elif pos == -2:
        pos = -3
        x = 50
    elif pos == -3:
        pos = -4
        x = 25
    elif pos == -4:
        pos = -5
        x = 0
    elif pos == -5:
        pos = 1
        x = -25

    eye_12_cen = (300 - x, 179)
    eye_12_rad = 42
    pygame.draw.circle(screen, gray, eye_12_cen, eye_12_rad, 0)

    eye_13_cen = (319 - x, 161)
    eye_13_rad = 12
    pygame.draw.circle(screen, white, eye_13_cen, eye_13_rad, 0)

    eye_22_cen = (506 - x, 179)
    eye_22_rad = 42
    pygame.draw.circle(screen, gray, eye_22_cen, eye_22_rad, 0)

    eye_23_cen = (524 - x, 163)
    eye_23_rad = 12
    pygame.draw.circle(screen, white, eye_23_cen, eye_23_rad, 0)



    t += pi / 30
    if t >= 2 * pi:
        t = 0
    # seconds
    pygame.draw.line(screen, red, [372, 529], [372 + cos(t) * 200, 529 + sin(t) * 200], 2)
    tick += 1

    if tick % 60 == 0:
        k += pi / 30
    if k >= 2 * pi:
        k = 0
    # minutes
    pygame.draw.line(screen, gray, [372, 529], [372 + cos(k) * 150, 529 + sin(k) * 150], 5)
    if tick % 3600 == 0:
        l += pi / 6
    if l >= 2 * pi:
        l = 0
    # hours
    pygame.draw.line(screen, gray, [372, 529], [372 + cos(l) * 130, 529 + sin(l) * 130], 8)

    c_cen = (372, 529)
    c_rad = 15
    pygame.draw.circle(screen, white, c_cen, c_rad, 0)

    pygame.display.flip()
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            done = True
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            m = mouse.get_pos()
            print(m)  # выводит в терминал(по желанию)
            s = '(' + str(m[0]) + ', ' + str(m[1]) + ')'
            scrap.put(SCRAP_TEXT, s.encode())  # копирует в буфер обмена
    pygame.display.update()
pygame.quit()
