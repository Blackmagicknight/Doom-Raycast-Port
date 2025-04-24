#=======================================================================================================================#

#IMPORTS#

import pygame
from pygame.locals import *
from math import *
import os
import button



#=======================================================================================================================#

#PYGAME SETTINGS#

mainClock = pygame.time.Clock()
pygame.init()

res = 1
WIDTH, HEIGHT = 640 * res, 400 * res
pygame.display.set_caption("Cube")
screen = pygame.display.set_mode((WIDTH, HEIGHT), SCALED | FULLSCREEN)

#load button images
rot_img = pygame.image.load(os.path.join(os.path.dirname(__file__), 'Images/ROT.svg')).convert_alpha()

#create button instances
rot_button = button.Button(10, 10, rot_img, 0.1)

target_path = os.path.join(os.path.dirname(__file__), 'Fonts/impact.ttf')



#=======================================================================================================================#

#CLASSES#

class player:
    def __init__(self, x, y, z, a, i):
        self.x = x #player position
        self.y = y #player position
        self.z = z #player position
        self.a = a #rotate player
        self.i = i #look up player



#=======================================================================================================================#

#VARIABLES#

#-----------------------#
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
#-----------------------#

Player = player(70, -110, 20, 0, 0)
sw = WIDTH
sh = HEIGHT
origin = [WIDTH/2, HEIGHT/2] #x, y (Changes the cubes position) (Is centered)

framerate = 60
font = pygame.font.Font(target_path, 32)
clock = pygame.time.Clock()

press_w = False
press_a = False
press_s = False
press_d = False
press_LEFT = False
press_RIGHT = False
press_UP = False
press_DOWN = False

Turn_Speed = 2
Walk_Speed = 0.5



#=======================================================================================================================#

#ROTATION LOGIC#

v = 0

sin1 = [0] * 360
cos1 = [0] * 360
print(sin1)

def Rotation_LOG():
    global v
    v = 0

    def iteration1():
        global v

        if (v < 360):
            cos1[v] = cos(v / 180 * pi)
            sin1[v] = sin(v / 180 * pi)

            v += 1
            iteration1()

    if ( v < 360):
        iteration1()



#=======================================================================================================================#

#DRAW LOGIC#

def clip_behind_player(x1, y1, z1, x2, y2, z2):
    global clipx1, clipy1, clipz1

    da = y1 #distance plain -> point a
    db = y2 #distance plain -> point b
    d = da - db

    if (d == 0):
        d = 1

    s = da / (da - db)  #intersection factor (between 0 and 1)
    x1 = x1 + s * (x2 - x1)
    y1 = y1 + s * (y2 - y1)

    if (y1 == 0):   #prevent divide by zero
        y1 = 1

    z1 = z1 + s * (z2 - z1)

    clipx1 = x1
    clipy1 = y1
    clipz1 = z1





#draw x verticle lines
def draw_wall(x1, x2, b1, b2, t1, t2):
    global x
    
    #hold the differences
    dyb = b2 - b1   #y distance of bottome line
    dyt = t2 - t1   #y distance of top line
    dx = x2 - x1    #x distance
    if (dx == 0):   
        dx = 1
    xs = x1         #hold initial x1 starting position

    #clip x
    if (x1 < 1): x1 = 1 #clip left
    if (x2 < 1): x2 = 1 #clip left
    if (x1 > sw - 1): x1 = sw - 1   #clip right
    if (x2 > sw - 1): x2 = sw - 1   #clip right

    x = x1

    def iteration2():
        global x, y, y2

        if (x < x2):
            y1 = dyb * (x - xs + 0.5) / dx + b1 #y bottom point
            y2 = dyt * (x - xs + 0.5) / dx + t1 #y bottom point

            #clip y
            if (y1 < 1): y1 = 1 #clip y
            if (y2 < 1): y2 = 1 #clip y
            if (y1 > sh - 1): y1 = sh - 1   #clip y
            if (y2 > sh - 1): y2 = sh - 1   #clip y

            y = y1
            if (y < y2):
                pygame.draw.line(screen, BLACK, (x, y1), (x, y2))

            x += 1
            iteration2()

    if (x < x2):
        iteration2()
                




def draw_3D():
    global Player, clipx1, clipy1, clipz1
    
    wx = [0] * 4
    wy = [0] * 4
    wz = [0] * 4
    cs = cos1[Player.a]
    sn = sin1[Player.a]

    #offset points by player
    x1 = 40 - Player.x
    y1 = 10 - Player.y
    x2 = 40 - Player.x
    y2 = 290 - Player.y

    #world x position
    wx[0] = (x1 * cs) - (y1 * sn)
    wx[1] = (x2 * cs) - (y2 * sn)
    wx[2] = wx[0]                   #top line has same x
    wx[3] = wx[1]

    #world y position (depth)
    wy[0] = (y1 * cs) + (x1 * sn)
    wy[1] = (y2 * cs) + (x2 * sn)
    wy[2] = wy[0]                   #top line has same y
    wy[3] = wy[1]

    #world z height
    wz[0] = 0 - Player.z + ((Player.i * wy[0]) / 32)
    wz[1] = 0 - Player.z + ((Player.i * wy[1]) / 32)
    wz[2] = wz[0] + 40              #top line has new z
    wz[3] = wz[1] + 40

    #dont draw behind the player
    if (wy[0] < 1 and wy[1] < 1):   #wall behind player (dont draw)
        return

    #if point 1 behind player (clip)
    if (wy[0] < 1):
        clip_behind_player(wx[0], wy[0], wz[0], wx[1], wy[1], wz[1])    #bottom line
        wx[0] = clipx1
        wy[0] = clipy1
        wz[0] = clipz1
        clip_behind_player(wx[2], wy[2], wz[2], wx[3], wy[3], wz[3])    #top line
        wx[2] = clipx1
        wy[2] = clipy1
        wz[2] = clipz1

    #if point 2 behind player (clip)
    if (wy[1] < 1):
        clip_behind_player(wx[1], wy[1], wz[1], wx[0], wy[0], wz[0])    #bottom line
        wx[1] = clipx1
        wy[1] = clipy1
        wz[1] = clipz1
        clip_behind_player(wx[3], wy[3], wz[3], wx[2], wy[2], wz[2])    #top line
        wx[3] = clipx1
        wy[3] = clipy1
        wz[3] = clipz1

    #screen x and y position
    wx[0] = wx[0] * 200 / wy[0] + origin[0]
    wy[0] = wz[0] * 200 / wy[0] + origin[1]
    wx[1] = wx[1] * 200 / wy[1] + origin[0]
    wy[1] = wz[1] * 200 / wy[1] + origin[1]
    
    wx[2] = wx[2] * 200 / wy[2] + origin[0]
    wy[2] = wz[2] * 200 / wy[2] + origin[1]
    wx[3] = wx[3] * 200 / wy[3] + origin[0]
    wy[3] = wz[3] * 200 / wy[3] + origin[1]

    #draw points
    draw_wall(wx[0], wx[1], wy[0], wy[1], wy[2], wy[3])



#=======================================================================================================================#

#SCREEN LOGIC#

def clear():
    screen.fill(WHITE)

def draw_text(text, font, colour, surface, x, y):
    textobj = font.render(text, 1, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def delta():
    clock.tick()
    Frames = round(clock.get_fps())
    draw_text('{0}'.format(Frames), font, RED, screen, 15, 60)


def move_player():
    global press_w, press_a, press_s, press_d, press_LEFT, press_RIGHT, press_UP, press_DOWN

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_w:         #move forward
                press_w = True
            if event.key == pygame.K_a:         #move left
                press_a = True
            if event.key == pygame.K_s:         #move backward
                press_s = True
            if event.key == pygame.K_d:         #move right
                press_d = True
            if event.key == pygame.K_LEFT:      #look left
                press_LEFT = True
            if event.key == pygame.K_RIGHT:     #look right
                press_RIGHT = True
            if event.key == pygame.K_UP:        #look up
                press_UP = True
            if event.key == pygame.K_DOWN:      #look down
                press_DOWN = True
            if event.key == pygame.K_o:         #move up
                Player.i += 1
            if event.key == pygame.K_l:         #move down
                Player.i -= 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:         #move forward
                press_w = False
            if event.key == pygame.K_a:         #move left
                press_a = False
            if event.key == pygame.K_s:         #move backward
                press_s = False
            if event.key == pygame.K_d:         #move right
                press_d = False
            if event.key == pygame.K_LEFT:      #look left
                press_LEFT = False
            if event.key == pygame.K_RIGHT:     #look right
                press_RIGHT = False
            if event.key == pygame.K_UP:        #look up
                press_UP = False
            if event.key == pygame.K_DOWN:      #look down
                press_DOWN = False



#=======================================================================================================================#

#PYGAME LAUNCH#

while True:
    dx = sin1[Player.a] * 10
    dy = cos1[Player.a] * 10

    #================================#

    clear()
    
    Rotation_LOG()
    move_player()
    draw_3D()

    delta()

    #================================#

    if press_w:
        Player.x += dx * Walk_Speed
        Player.y += dy * Walk_Speed
    if press_a:
        Player.x -= dy * Walk_Speed
        Player.y += dx * Walk_Speed
    if press_s:
        Player.x -= dx * Walk_Speed
        Player.y -= dy * Walk_Speed
    if press_d:
        Player.x += dy * Walk_Speed
        Player.y -= dx * Walk_Speed
    if press_LEFT:
        Player.a -= 1 * Turn_Speed
        if (Player.a < 0):
            Player.a += 360
    if press_RIGHT:
        Player.a += 1 * Turn_Speed
        if (Player.a > 359):
            Player.a -= 360
    if press_UP:
        Player.z -= 1 * Turn_Speed
    if press_DOWN:
        Player.z += 1 * Turn_Speed

    if rot_button.draw(screen):
        e = 0

    # update stuff
    pygame.display.update()
    mainClock.tick(framerate)
    


#=======================================================================================================================#
