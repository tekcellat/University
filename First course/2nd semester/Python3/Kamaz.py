import pygame
from pygame import *
from math   import *

WIN_WIDTH = 900;  WIN_HEIGHT = 640
BACKGROUND_COLOR ='#00BFFF'
earth = Rect((0,round(WIN_HEIGHT*(2/3))),(WIN_WIDTH,WIN_HEIGHT))  

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
    
def main():
    pygame.init()
    DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption('Возможно тут должен быть заголовок')
    
    bg=Surface((WIN_WIDTH,WIN_HEIGHT))   
 
    def CAR():
        global car
        car = Surface((300,260),SRCALPHA)
        draw.rect(car,Color('red'),Rect(20,100,200,50),0)
        draw.polygon(car,Color('red'),[(220,150),(290,150),(290,60),(260,40),(220,40)],0)
        draw.polygon(car,Color('#00BFFF'),[(240,50),(260,50),(280,70),(280,80),(240,80)],0)
        draw.line(car,Color('red'),(50,160),(70,150))
        draw.line(car,Color('red'),(80,150),(100,160))
        
        draw.line(car,Color('red'),(220,160),(240,150))
        draw.line(car,Color('red'),(260,150),(280,160))
    def WHEELS():
        global wheel
        wheel = Surface((50,50),SRCALPHA)
        draw.ellipse(wheel,Color('brown'),Rect((5,5),(40,40)),0)
        draw.line(wheel,Color('black'),(11,11),(36,36),3)
        draw.line(wheel,Color('black'),(36,11),(11,36),3)
    def LUGGAGE():
        global luggage
        luggage = Surface((100,50))
        luggage.fill(Color('green'))
    t = 0
    x = 0
    flag = True
    CAR();WHEELS(); LUGGAGE()
    
    while flag:
        temp = 0
        for e in event.get(): 
            if e.type == QUIT:  flag = False   
        screen.blit(bg, (0,0))
        
        draw.rect(bg, Color(BACKGROUND_COLOR), Rect(0,0,WIN_WIDTH, WIN_HEIGHT) , 0)
        draw.rect(bg, Color('gold'), earth,0)
        draw.line(bg,Color('black'),(0,545),(900,545),3)       
        bg.blit(car,(t/2,350))
        bg.blit(rot_center(wheel, 100+t/2), (50+t/2, 500+1*atan(-50*sin(0.02*t)*0.02)))
        bg.blit(rot_center(wheel, 100+t/2), (225+t/2, 500+1*atan(-50*sin(0.02*t)*0.02)))                         
        temp = (20+t/2-t/10)
        if t<1000:
            #temp = (20+t/2-t/10)
            bg.blit(luggage,(temp,400))
            cach = temp
        if t>=1000:
            bg.blit(luggage,(cach,350+temp/9))
    
        t += 1
        
        if t > 3000:
            t = 0
        
        display.update()
            
main()
