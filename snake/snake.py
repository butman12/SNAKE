import sys
import math
import random
import pygame
import tkinter as tk
from pygame import mixer
import time
################################################################
    #RUNNING A GEME REQUIRES USER TO SET VARIABLE "FOLDER" 
    #USE YOUR OWN DIRECTORY TO DOWNLOADED FOLDER "SNAKE"
################################################################
folder='/Users/michalbutmankiewicz/Desktop'
#grid poits used to build walls,etc. (depending on map choice)
mapa0=[]
mapa1=[(4,7),(4,8),(4,9),(4,10),(4,11),(4,12),(15,7),(15,8),(15,9),(15,10),(15,11),(15,12),(7,4),(8,4),(9,4),(10,4),(11,4),(12,4),(7,15),(8,15),(9,15),(10,15),(11,15),(12,15)]


#set life count and score
life=2
wyniki=[]


#pre-loading graphics
dwa=pygame.image.load(folder+"/snake/grafika/2.png")
jeden=pygame.image.load(folder+"/snake/grafika/1.png")
zero=pygame.image.load(folder+"/snake/grafika/0.png")
bestsc=pygame.image.load(folder+"/snake/grafika/bestsc.png")
sc=pygame.image.load(folder+"/snake/grafika/sc.png")
dwojka=pygame.image.load(folder+"/snake/grafika/dwojka.png")
trojka=pygame.image.load(folder+"/snake/grafika/trojka.png")
czworka=pygame.image.load(folder+"/snake/grafika/czworka.png")
piatka=pygame.image.load(folder+"/snake/grafika/piatka.png")
szostka=pygame.image.load(folder+"/snake/grafika/szostka.png")
siodemka=pygame.image.load(folder+"/snake/grafika/siodemka.png")
osemka=pygame.image.load(folder+"/snake/grafika/osemka.png")
dziewiatka=pygame.image.load(folder+"/snake/grafika/dziewiatka.png")
zero1=pygame.image.load(folder+"/snake/grafika/zero1.png")
jedynka=pygame.image.load(folder+"/snake/grafika/jedynka.png")



#game itself-starting with choosen map
def gra(mapa):
    #cube class can be interpreted as snake body
    class cube(object):
        rows = 20
        w = 700
        def __init__(self,start,dirnx=1,dirny=0,color=(100,10,200)):
            self.pos = start
            #directionx (dirnx) = 1 means right, -1 means left
            #same with dirny and up/down
            self.dirnx = 1
            self.dirny = 0
            self.color = color
     
           
        def move(self, dirnx, dirny):
            self.dirnx = dirnx
            self.dirny = dirny
            self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
     
        def draw(self, surface, eyes=False):
            dis = self.w // self.rows
            i = self.pos[0]
            j = self.pos[1]
     
            pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
            #optional eyes-drawing part:
            if eyes:
                centre = dis//2
                radius = 3
                circleMiddle = (i*dis+centre-radius,j*dis+8)
                circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
                pygame.draw.circle(surface, (200,10,100), circleMiddle, radius)
                pygame.draw.circle(surface, (200,10,100), circleMiddle2, radius)
           
    #wall class is (as suspected) a wall ;) 
    class wall(object):
        rows=20
        w=700
        
        def __init__(self,color=(150,50,100),lista=mapa):
            self.color=color
            self.lista=lista
        def draw(self,surface):
            dis=self.w//self.rows
            for k in range(len(self.lista)):
                i=self.lista[k][0]
                j=self.lista[k][1]
                pygame.draw.rect(surface,self.color,(i*dis+1,j*dis+1, dis-2, dis-2))
        
    #previously we had parts of snake, now time to build the whole snake          
    class snake(object):
        body = []
        turns = {}
        def __init__(self, color, pos):
            self.color = color
            self.head = cube(pos)
            self.body.append(self.head)
            self.dirnx = 0
            self.dirny = 1
        #move comands are set to arrow-keys
        def move(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                
     
                keys = pygame.key.get_pressed()
     
                for key in keys:
                    if keys[pygame.K_LEFT]:
                        self.dirnx = -1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
     
                    elif keys[pygame.K_RIGHT]:
                        self.dirnx = 1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
     
                    elif keys[pygame.K_UP]:
                        self.dirnx = 0
                        self.dirny = -1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
     
                    elif keys[pygame.K_DOWN]:
                        self.dirnx = 0
                        self.dirny = 1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    elif keys[pygame.K_ESCAPE]:
                        lvl()
     
            for i, c in enumerate(self.body):
                p = c.pos[:]
                if p in self.turns:
                    turn = self.turns[p]
                    c.move(turn[0],turn[1])
                    if i == len(self.body)-1:
                        self.turns.pop(p)
                #part bellow allows snake to cross borders (going up too much-snake's head pops up at the bottom, etc)
                else:
                    if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                    elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                    elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                    elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                    else: c.move(c.dirnx,c.dirny)
           
        #setting everything back to defoult settings
        def reset(self, pos):
            self.head = cube(pos)
            self.body = []
            self.body.append(self.head)
            self.turns = {}
            self.dirnx = 0
            self.dirny = 1
     
     
        def addCube(self):
 
            
            tail = self.body[-1]
            dx, dy = tail.dirnx, tail.dirny
     #depending on direction of snake's tail, adding a new cube must happen oon the opposite side
            if dx == 1 and dy == 0:
                self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
            elif dx == -1 and dy == 0:
                self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
            elif dx == 0 and dy == 1:
                self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
            elif dx == 0 and dy == -1:
                self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
     
            self.body[-1].dirnx = dx
            self.body[-1].dirny = dy
           
     
        def draw(self, surface):
            for i, c in enumerate(self.body):
                if i ==0:          #with eyes
                    c.draw(surface, True)
                else:              #without eyes
                    c.draw(surface)
     
    #map drawing 
    def drawGrid(w, rows, surface):
        sizeBtwn = w // rows
     
        x = 0
        y = 0
        for l in range(rows):
            x = x + sizeBtwn
            y = y + sizeBtwn
     
            pygame.draw.line(surface, (0,200,10), (x,0),(x,w))
            pygame.draw.line(surface, (0,200,10), (0,y),(w,y))
           
    #refreshing window 
    def redrawWindow(surface):
        global rows, width, s, snack,bestscore,wynik
        f=open(folder+"/snake/bestscore.txt",'r')
        wyniki=[]
        for i in range(10):
            wyniki.append(eval(f.readline()))
        f.close()
        wyniki.sort()
        wyniki.reverse()
        if len(s.body)-1>wyniki[0]:
            bestscore=(len(s.body)-1)
        else:
            bestscore=wyniki[0]
            
        
        f.close()
        surface.fill((0,0,0))
        
        snack.draw(surface)
        if life == 2:
            screen.blit(dwa, [540, 710])
        elif life == 1:
            screen.blit(jeden, [540, 710])
        else:
            screen.blit(zero, [540, 710])
        screen.blit(sc, [0, 710])
        screen.blit(bestsc, [0, 760])
        if (len(s.body)-1)%10 == 0:#last digit
            screen.blit(zero1, [165, 735])
        elif (len(s.body)-1)%10 == 1:
            screen.blit(jedynka, [165, 735])
        elif (len(s.body)-1)%10 == 2:
            screen.blit(dwojka, [165, 735])
        elif (len(s.body)-1)%10 == 3:
            screen.blit(trojka, [165, 735])
        elif (len(s.body)-1)%10 == 4:
            screen.blit(czworka, [165, 735])
        elif (len(s.body)-1)%10 == 5:
            screen.blit(piatka, [165, 735])
        elif (len(s.body)-1)%10 == 6:
            screen.blit(szostka, [165, 735])
        elif (len(s.body)-1)%10 == 7:
            screen.blit(siodemka, [165, 735])
        elif (len(s.body)-1)%10 == 8:
            screen.blit(osemka, [165, 735])
        elif (len(s.body)-1)%10 == 9:
            screen.blit(dziewiatka, [165, 735])
        if (((len(s.body)-1)%100)-(((len(s.body)-1)%10)))/10==0:#middle digit
            screen.blit(zero1, [145, 735])
        elif (((len(s.body)-1)%100)-(((len(s.body)-1)%10)))/10==1:
            screen.blit(jedynka, [145, 735])
        elif (((len(s.body)-1)%100)-(((len(s.body)-1)%10)))/10==2:
            screen.blit(dwojka, [145, 735])
        elif (((len(s.body)-1)%100)-(((len(s.body)-1)%10)))/10==3:
            screen.blit(trojka, [145, 735])
        elif (((len(s.body)-1)%100)-(((len(s.body)-1)%10)))/10==4:
            screen.blit(czworka, [145, 735])
        elif (((len(s.body)-1)%100)-(((len(s.body)-1)%10)))/10==5:
            screen.blit(piatka, [145, 735])
        elif (((len(s.body)-1)%100)-(((len(s.body)-1)%10)))/10==6:
            screen.blit(szostka, [145, 735])
        elif (((len(s.body)-1)%100)-(((len(s.body)-1)%10)))/10==7:
            screen.blit(siodemka, [145, 735])
        elif (((len(s.body)-1)%100)-(((len(s.body)-1)%10)))/10==8:
            screen.blit(osemka, [145, 735])
        elif (((len(s.body)-1)%100)-(((len(s.body)-1)%10)))/10==9:
            screen.blit(dziewiatka, [145, 735])
        if ((len(s.body)-1)-((len(s.body)-1)%100))/100==0:#first digit
            screen.blit(zero1, [125, 735])
        elif ((len(s.body)-1)-((len(s.body)-1)%100))/100==1:
            screen.blit(jedynka, [125, 735])
        elif ((len(s.body)-1)-((len(s.body)-1)%100))/100==2:
            screen.blit(dwojka, [125, 735])
        elif ((len(s.body)-1)-((len(s.body)-1)%100))/100==3:
            screen.blit(trojka, [125, 735])
        elif ((len(s.body)-1)-((len(s.body)-1)%100))/100==4:
            screen.blit(czworka, [125, 735])
        elif ((len(s.body)-1)-((len(s.body)-1)%100))/100==5:
            screen.blit(piatka, [125, 735])
        elif ((len(s.body)-1)-((len(s.body)-1)%100))/100==6:
            screen.blit(szostka, [125, 735])
        elif ((len(s.body)-1)-((len(s.body)-1)%100))/100==7:
            screen.blit(siodemka, [125, 735])
        elif ((len(s.body)-1)-((len(s.body)-1)%100))/100==8:
            screen.blit(osemka, [125, 735])
        elif ((len(s.body)-1)-((len(s.body)-1)%100))/100==9:
            screen.blit(dziewiatka, [125, 735])
################################################################################################################
#WHILE COMMENTING THIS CODE, I NOTICED THAT THERES MUCH SIMPLER AND ELEGANT SOLUTION TO THIS, MAY CHANGE IT SOON
################################################################################################################

#same with bestscore

        if bestscore%10 == 0:
            screen.blit(zero1, [260, 785])
        elif bestscore%10 == 1:
            screen.blit(jedynka, [260, 785])
        elif bestscore%10 == 2:
            screen.blit(dwojka, [260, 785])
        elif bestscore%10 == 3:
            screen.blit(trojka, [260, 785])
        elif bestscore%10 == 4:
            screen.blit(czworka, [260, 785])
        elif bestscore%10 == 5:
            screen.blit(piatka, [260, 785])
        elif bestscore%10 == 6:
            screen.blit(szostka, [260, 785])
        elif bestscore%10== 7:
            screen.blit(siodemka, [260, 785])
        elif bestscore%10== 8:
            screen.blit(osemka, [260, 785])
        elif bestscore%10 == 9:
            screen.blit(dziewiatka, [260, 785])
        if ((bestscore%100)-(bestscore%10))/10==0:
            screen.blit(zero1, [240, 785])
        elif ((bestscore%100)-(bestscore%10))/10==1:
            screen.blit(jedynka, [240, 785])
        elif ((bestscore%100)-(bestscore%10))/10==2:
            screen.blit(dwojka, [240, 785])
        elif ((bestscore%100)-(bestscore%10))/10==3:
            screen.blit(trojka, [240, 785])
        elif ((bestscore%100)-(bestscore%10))/10==4:
            screen.blit(czworka, [240, 785])
        elif ((bestscore%100)-(bestscore%10))/10==5:
            screen.blit(piatka, [240, 785])
        elif ((bestscore%100)-(bestscore%10))/10==6:
            screen.blit(szostka, [240, 785])
        elif ((bestscore%100)-(bestscore%10))/10==7:
            screen.blit(siodemka, [240, 785])
        elif ((bestscore%100)-(bestscore%10))/10==8:
            screen.blit(osemka, [240, 785])
        elif ((bestscore%100)-(bestscore%10))/10==9:
            screen.blit(dziewiatka, [240, 785])
        if (bestscore-(bestscore%100))/100==0:
            screen.blit(zero1, [220, 785])
        elif (bestscore-(bestscore%100))/100==1:
            screen.blit(jedynka, [220, 785])
        elif (bestscore-(bestscore%100))/100==2:
            screen.blit(dwojka, [220, 785])
        elif (bestscore-(bestscore%100))/100==3:
            screen.blit(trojka, [220, 785])
        elif (bestscore-(bestscore%100))/100==4:
            screen.blit(czworka, [220, 785])
        elif (bestscore-(bestscore%100))/100==5:
            screen.blit(piatka, [220, 785])
        elif (bestscore-(bestscore%100))/100==6:
            screen.blit(szostka, [220, 785])
        elif (bestscore-(bestscore%100))/100==7:
            screen.blit(siodemka, [220, 785])
        elif (bestscore-(bestscore%100))/100==8:
            screen.blit(osemka, [220, 785])
        elif (bestscore-(bestscore%100))/100==9:
            screen.blit(dziewiatka, [220, 785])

        sciana.draw(surface)
        s.draw(surface)
        drawGrid(width,rows, surface)
        pygame.display.update()
     
    #snacks
    def randomSnack(rows, item):
     
        positions = item.body
     
        while True:
            x = random.randrange(rows)
            y = random.randrange(rows)
            if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0 or (x,y) in sciana.lista:
                continue
            else:
                break
        return (x,y)
           
    def main():
        
        global width, rows, s, snack,life,sciana,bestscore,wyniki
        width = 700
        rows = 20
        wyniki=[]
        sciana=wall((150,50,100),mapa)
        win = pygame.display.set_mode((width, 850))
        s = snake((255,0,0), (10,10))
        snack = cube(randomSnack(rows, s), color=(0,255,0))
        flag = True
        clock = pygame.time.Clock()
       
        while flag:
            pygame.time.delay(50)
            clock.tick(10)
            s.move()
            if s.body[0].pos == snack.pos:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(folder+"/snake/muzyka/snack.wav"))
                s.addCube()
                snack = cube(randomSnack(rows, s), color=(0,255,0))
            if len(sciana.lista)>1:#with existing map
                
                
                for x in range(len(s.body)):
                    if s.body[0].pos in list(map(lambda z:z.pos,s.body[1:])) or s.body[0].pos in sciana.lista:#head hit the wall
                        #condition bellow allows crossig wall without losing more than 1 health
                        if (s.dirny == -1 and (s.body[0].pos[0] == 4 or s.body[0].pos[0] == 15) and s.body[0].pos[1]<12) or (s.dirny == 1 and (s.body[0].pos[0] == 4 or s.body[0].pos[0] == 15) and s.body[0].pos[1]>7) or (s.dirnx == 1 and (s.body[0].pos[1] == 4 or s.body[0].pos[1] == 15) and s.body[0].pos[0]>7) or (s.dirnx == -1 and (s.body[0].pos[1] == 4 or s.body[0].pos[1] == 15) and s.body[0].pos[0]<12):
                            pass
                        else:
                            if life>0:#if snake still has health points one is taken away
                                life=life-1
                                pygame.mixer.Channel(1).play(pygame.mixer.Sound(folder+"/snake/muzyka/-1.wav"))
                                time.sleep(0.5)
                            else:#if snake had only one health point, game ends
                                
                                
                                   
                                pygame.mixer.Channel(1).play(pygame.mixer.Sound(folder+"/snake/muzyka/gameover.wav"))
                                screen.blit(zero, [550, 700])
                                time.sleep(3)
                                life=2
                                f=open(folder+"/snake/bestscore.txt",'r')
                                wyniki=[]
                                for i in range(10):
                                    wyniki.append(eval(f.readline()))
                                f.close()
                                wyniki.append(len(s.body)-1)
                                wyniki.sort()
                                wyniki.reverse()
                                
                                f=open(folder+"/snake/bestscore.txt",'w')
                                for i in range(10):
                                    f.write(str(wyniki[i]) + "\n")
                                f.close()
                                lvl()
                            break
            else:#when there is no wall
                for x in range(len(s.body)):
                    if s.body[0].pos in list(map(lambda z:z.pos,s.body[1:])):
                        if life>0:
                                life=life-1
                                pygame.mixer.Channel(1).play(pygame.mixer.Sound(folder+"/snake/muzyka/-1.wav"))
                                time.sleep(0.5)
                        else:
                                   
                                pygame.mixer.Channel(1).play(pygame.mixer.Sound(folder+"/snake/muzyka/gameover.wav"))
                                screen.blit(zero, [550, 700])
                                time.sleep(3)
                                life=2
                                
                                f=open(folder+"/snake/bestscore.txt",'r')
                                wyniki=[]
                                for i in range(10):
                                    wyniki.append(eval(f.readline()))
                                f.close()
                                wyniki.append(len(s.body)-1)
                                wyniki.sort()
                                wyniki.reverse()
                                
                                f=open(folder+"/snake/bestscore.txt",'w')
                                for i in range(10):
                                    f.write(str(wyniki[i]) + "\n")
                                f.close()
                                lvl()
                                
                        break
                
          
            redrawWindow(win)   
        pass
     
    main()

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.display.set_caption('snake')
screen = pygame.display.set_mode((700, 850),0,32)
#MENU GRAPHICS
lvlimage = pygame.image.load(folder+"/snake/grafika/mapa.png")
background_image = pygame.image.load(folder+"/snake/grafika/Bez nazwy.png")
infoimage=pygame.image.load(folder+"/snake/grafika/info.png")                           
creditsimage=pygame.image.load(folder+"/snake/grafika/credits.png")
mixer.music.load(folder+"/snake/muzyka/menumusic.wav")


 
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
click = False

#bestscore table
def punkty():
    while True:
        txt=[]
        font = pygame.font.SysFont(None, 70)
        screen.fill((0,0,0))
        f=open(folder+"/snake/bestscore.txt",'r')
        for i in range(10):
            txt.append(eval(f.readline()))
        txt.sort()
        txt.reverse()
        draw_text("BEST SCORES",font,(255,255,255),screen,170,50)
        for i in range(len(txt)):
            draw_text(str(txt[i]), font, (255,255,255),screen,320,150+i*60)
                
            
        for event in pygame.event.get():
                
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_ESCAPE]:
                    lvl()
        pygame.display.update()
    
#info page
def info():
    while True:
        screen.fill((0,0,0))
        screen.blit(infoimage, [0,0])
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_ESCAPE]:
                    main_menu()
        pygame.display.update()
#credits page
def credit():
    while True:
        screen.fill((0,0,0))
        screen.blit(creditsimage, [0,0])
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_ESCAPE]:
                    main_menu()
        pygame.display.update()
#select map menu
def lvl():
    while True:
        screen.fill((0,0,0))
        screen.blit(lvlimage,[0,0])
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            #przyciski
            if mx<320 and mx>10 and my<600 and my>280 and event.type == MOUSEBUTTONDOWN:
                gra(mapa0)
            elif mx<690 and mx>380 and my<600 and my>280 and event.type == MOUSEBUTTONDOWN:
                gra(mapa1)
            elif my>700 and my<800 and event.type == MOUSEBUTTONDOWN:
                punkty()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_ESCAPE]:
                    main_menu()
        pygame.display.update()
#main menu
def main_menu():
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(folder+"/snake/muzyka/menumusic.wav"))
    while True:
 
        screen.fill((0,0,0))
        screen.blit(background_image, [0, 0])
        

        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            #przyciski
            if mx<440 and mx>240 and my<340 and my>240 and event.type == MOUSEBUTTONDOWN:
                lvl()
            elif mx<440 and mx>240 and my<480 and my>420 and event.type == MOUSEBUTTONDOWN:
                info()
            elif mx<440 and mx>240 and my<750 and my>680 and event.type == MOUSEBUTTONDOWN:
                pygame.quit()
            elif mx<540 and mx>140 and my<600 and my>530 and event.type == MOUSEBUTTONDOWN:
                credit()
 
        click = False
        pygame.display.update()
        mainClock.tick(60)
 

        
 

 
main_menu()


