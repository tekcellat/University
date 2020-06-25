import pygame, sys
import time
import math

def draw_house(x,y):
    #house
    pygame.draw.rect(screen,(255,255,255),(x,y-130,200,130))
    pygame.draw.rect(screen,(0,0,0),(x,y-130,200,130),3)
    pygame.draw.polygon(screen, (0,0,0),[(x,y-130),(x+200,y-130),(x+100,y-200)])
    #door
    pygame.draw.rect(screen,(89,71,0),(x+80,y-60,40,60))
    pygame.draw.rect(screen,(89,71,0),(x+80,y-60,40,60),3)
    #door ruc
    pygame.draw.circle(screen,(255,204,0),(x+112,y-30),4)
    draw_window(x+20,y-40)
    draw_window(x+130,y-40)
 

def draw_tree(x,y):
    #tree trunk (50 wide and 100 tall)
    pygame.draw.rect(screen,(117,90,0),(x,y-100,25,100))
    #leaves are a circle
    pygame.draw.circle(screen,(27,117,0),(x+13,y-120),50)

def draw_window(x,y):
    #glaases
    pygame.draw.rect(screen,(207,229,255),(x,y-50,50,50))
    #burdalar
    pygame.draw.rect(screen,(0,0,0),(x,y-50,50,50),5)
    pygame.draw.rect(screen,(0,0,0),(x+23,y-50,5,50))
    pygame.draw.rect(screen,(0,0,0),(x,y-27,50,5))

def draw_cloud(x,y,size):
    #put int() around any multiplications by decimals to get rid of this warning:
    #DeprecationWarning: integer argument expected, got float
    pygame.draw.circle(screen,(235,235,235),(x,y),int(size*.5))
    pygame.draw.circle(screen,(235,235,235),(int(x+size*.5),y),int(size*.6))
    pygame.draw.circle(screen,(235,235,235),(x+size,int(y-size*.1)),int(size*.4))


def draw_man(x,y):
    #draw hands
    pygame.draw.line(screen,(0,0,0),(x,y+10),(x-20,y+35),5)
    pygame.draw.line(screen,(0,0,0),(x,y+10),(x+20,y+35),5)

    #draw body
    pygame.draw.circle(screen,(0,0,0),(x,y), 10)
    pygame.draw.line(screen,(0,0,0),(x,y+13),(x,y+42),10)

    #draw legs
    pygame.draw.line(screen,(0,0,0),(x,y+35),(x-15,y+70),5)
    pygame.draw.line(screen,(0,0,0),(x,y+35),(x+15,y+70),5)

def draw_dog(x,y):
    #dog body
    pygame.draw.circle(screen,(0,0,0),(x,y), 10)
    pygame.draw.line(screen,(0,0,0),(x+5,y),(x+30,y),9)

    #dog lapkos first
    pygame.draw.line(screen,(0,0,0),(x+2,y+7),(x-5,y+15),7)
    pygame.draw.line(screen,(0,0,0),(x+2,y+7),(x+5,y+15),7)

    #lapkos second
    pygame.draw.line(screen,(0,0,0),(x+30,y+7),(x+23,y+15),7)
    pygame.draw.line(screen,(0,0,0),(x+30,y+7),(x+37,y+15),7)

    
pygame.init()
screen = pygame.display.set_mode((900,580),0,32)
pygame.display.set_caption("Возможно тут должен быть заголовок")

xCloud1, yCloud1 = 60, 120
xCloud2, yCloud2 = 200, 50
xCloud3, yCloud3 = 550, 100

x_dog, y_dog = 550, 500
x_man, y_man = 550, 450
count = 0

running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #green ground
    pygame.draw.rect(screen,(0,155,3),(0,500,900,80))

    #L.blue sky
    pygame.draw.rect(screen,(135,255,255),(0,0,900,500))

    #trees
    draw_tree(650,500)
    draw_tree(780,500)

    draw_dog(x_dog,y_dog)
    x_dog -= 2

    #draw clouds
    draw_cloud(xCloud1,yCloud1,80)
    draw_cloud(xCloud2,yCloud2,40)
    draw_cloud(xCloud3,yCloud3,100)

    xCloud1 += 5
    xCloud2 += 5
    xCloud3 += 5

    if xCloud1 == 900: 
        xCloud1 = 0
    elif xCloud2 == 900:
        xCloud2 = 0
    elif xCloud3 == 900:
        xCloud3 = 0
        
    draw_house(225,500)
    draw_man(x_man,y_man)
    x_man -=1
    count+=1
    if count >=0 and count < 20:
        y_man -= 1
        count += 1
    elif count < 0 and count > -20:
        y_man +=1
        count -= 1
    elif count == 20:
        count == -1
    elif count == -20:
        count == 0  
     
    time.sleep(0.04)
    pygame.display.update()
    pygame.display.flip()

#start
pygame.quit()
sys.exit()
