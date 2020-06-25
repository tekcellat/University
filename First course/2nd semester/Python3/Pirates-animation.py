#Author Hasanzade UI7-26
import pygame
from pygame import *
from math   import *

WIN_WIDTH = 900;  WIN_HEIGHT = 640
BACKGROUND_COLOR ='#00BFFF'
sea_width = 0
sea_size = Rect((0,round(WIN_HEIGHT*(2/3))),(WIN_WIDTH,WIN_HEIGHT))  
island_size = Rect((round(WIN_WIDTH*(1/3)),370),(round(WIN_WIDTH*(1/3)),160))

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
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
    pygame.display.set_caption('Возможно здесь должен быть заголовок')
    
    bg=Surface((WIN_WIDTH,WIN_HEIGHT))   

    def SKY():
        global sky
        sky = Surface((200,100),SRCALPHA)
        draw.ellipse(sky,Color('white'),Rect((50,15),(100,40)),0)
        draw.ellipse(sky,Color('white'),Rect((100,40),(100,40)),0)
        draw.ellipse(sky,Color('white'),Rect((50,65),(100,40)),0)
        draw.ellipse(sky,Color('white'),Rect((0,40),(100,40)),0)
        draw.ellipse(sky,Color('white'),Rect((20,55),(100,40)),0)
        draw.ellipse(sky,Color('white'),Rect((20,30),(100,40)),0)
        draw.ellipse(sky,Color('white'),Rect((85,30),(100,40)),0)
        draw.ellipse(sky,Color('white'),Rect((85,55),(100,40)),0)
    def BOAT():
        global boat
        boat = Surface((300,200),SRCALPHA)
        draw.polygon(boat,Color('#FF8C00'),[(50,150),(260,150),(260,130),(295,130),(295,190),(90,190)],0)
        draw.line(boat,Color('#FF8C00'),(50,150),(0,140),3)
        draw.line(boat,Color('#FF8C00'),(120,30),(120,150),4)
        draw.line(boat,Color('#FF8C00'),(200,10),(200,150),4)
        draw.line(boat,Color('#FF8C00'),(292,120),(292,130),4)
        draw.polygon(boat,Color('red'),[(200,10),(220,10),(215,15),(220,20),(200,20)],0)
        x=75
        for i in range(12):          
           draw.ellipse(boat,Color('#2F4F4F'),Rect((x,160),(15,15)),0)
           x+=17
        draw.lines(boat,Color('black'),False,[(0,140),(120,30),(200,30),(292,120)],2)
        draw.arc(boat,Color('White'),[142,30,120,120],pi/2,3*pi/2,5)
        draw.arc(boat,Color('White'),[90,30,75,120],pi/2,3*pi/2,5)
        draw.arc(boat,Color('White'),[0,120,55,50],pi/180*170,pi/180*(350),5)

    def FISH():
        global fish
        fish = Surface((100,100),SRCALPHA)    
       # fish.fill(Color('white'))
        draw.ellipse(fish,Color('#008080'),Rect((20,30),(80,40)),0)
        draw.polygon(fish,Color('#008080'),[(0,30),(30,40),(30,60),(0,70),(18,50)],0)
        draw.polygon(fish,Color('#008080'),[(0,30),(30,40),(30,60),(0,70),(18,50)],0)
        draw.polygon(fish,Color('#008080'),[(50,15),(50,35),(80,35)],0)
        draw.polygon(fish,Color('#008080'),[(40,60),(40,80),(70,60)],0)
        draw.polygon(fish,Color('#0000CD'),[(80,55),(100,50),(100,60)],0)
        draw.ellipse(fish,Color('black'),Rect((80,40),(10,10)),0)
    t = 0
    x = 0
    flag = True
    SKY(); BOAT(); FISH()
    while flag:
        for e in event.get(): 
            if e.type == QUIT:  flag = False   
        screen.blit(bg, (0,0))
        
        draw.rect(bg, Color(BACKGROUND_COLOR), Rect(0,0,WIN_WIDTH, WIN_HEIGHT) , 0)

        #солнце
        draw.ellipse(bg,Color('yellow'),Rect((750,30),(80,80)),0)
        g = 0
        while g<=pi*2:
               draw.line(bg,Color('yellow'),(130*cos(g)+790,130*sin(g)+70),\
                                          (790,70),2)
               g+=(pi*2)/8
    
        p = pi*2/16    
        while p<=pi*2:
               draw.line(bg,Color('yellow'),(100*cos(p)+790,100*sin(p)+70),(790,70),\
                                                   2)
               p+=pi*2/16
        
        bg.blit(sky,(t/4,20))
        bg.blit(sky,(1000-t/4,130))
        
        draw.ellipse(bg,Color('#FFD700'),island_size,sea_width)
        draw.rect(bg, Color('#0000CD'), sea_size, sea_width)
        
        y1=350; y2=370
        for i in range(11):
           draw.polygon(bg,Color('#CD853F'),[(435,y1),(465,y1),(460,y2),(440,y2)],sea_width)
           y1-=20;y2-=20
        draw.polygon(bg,Color('#7FFF00'),[(450,150),(550,70),(530,100),(600,90),(540,120),(590,120),(530,130),(570,140)],sea_width)
        draw.polygon(bg,Color('#7FFF00'),[(450,150),(350,70),(380,100),(310,90),(370,120),(330,120),(380,130),(350,140)],sea_width)
        draw.polygon(bg,Color('#7FFF00'),[(450,150),(550,160),(530,170),(570,180),(550,190),(600,220),(540,210)],sea_width)
        draw.polygon(bg,Color('#7FFF00'),[(450,150),(350,160),(370,170),(330,180),(350,190),(300,220),(360,210)],sea_width)

        draw.lines(bg,Color('#000000'),False,[(480,380),(485,380),(490,360),(495,380),(500,380)],3)
        draw.lines(bg,Color('#000000'),False,[(481,365),(482,350),(498,350),(501,335)],3)
        draw.line(bg,Color('#000000'),(490,350),(490,360),3)
        draw.ellipse(bg,Color('#000000'),Rect((483,338),(15,15)),3)

        bg.blit(rot_center(fish, 50*cos(0.02*t)), (t/3, 460+50*atan(-50*sin(0.02*t)*0.02)))
        draw.rect(bg,Color('#0000CD'),Rect((0,510),(WIN_WIDTH,WIN_HEIGHT)),0)
               
        bg.blit(boat,(900-t/3,400))        
    
        t += 0.5
        if t > 5000:
            t = 0
        
        display.update()
            
main()
