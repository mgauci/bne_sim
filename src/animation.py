#!/usr/bin/env python2.7

from physics import *

import pygame
from pygame.locals import *

# 'Hack' to creates an enum-like class in Python.
# See: http://stackoverflow.com/questions/36932/
def enum(**enums):
    return type('Enum', (), enums)

# RGB color definitions.
Colors = enum(
    red   = (255,   0,   0),
    green = (  0, 255,   0),
    blue  = (  0,   0, 255),
    black = (  0,   0,   0),
    white = (255, 255, 255),
)

# 1080 pixels, screen height = 0.28 meters 
# for 23" screen with 16:9 display ratio.
SCALE   = 1080/0.286258
WORLD_X = 0.2*SCALE # 0.2 m.
WORLD_Y = 0.2*SCALE # 0.2 m.

world = World(Vec(0.0, 0.0), Vec(WORLD_X, WORLD_Y))

d = Disk(init_pos   = Vec(0.5*WORLD_X, 0.5*WORLD_Y),
         init_vel   = Vec(2.5*SCALE, 2.5*SCALE),
         radius     = 0.02*SCALE, 
         mass       = 10.0, 
         coeff_rest = 0.75)

world.add_disk(d)

pygame.init()
screen = pygame.display.set_mode((int(WORLD_X), int(WORLD_Y)))
clock = pygame.time.Clock()   

main_loop = True 
while main_loop:
    clock.tick(1000) #FPS
    
#===============================================================================
#   CONTROL
#===============================================================================
#   Check for events (key presses, mouse movement etc.).
    for event in pygame.event.get():
#       X button pressed in the Pygame window.
        if event.type == pygame.QUIT:
            main_loop = False
#       Escape key pressed on keyboard.
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            main_loop = False
            
#===============================================================================
#   MODEL
#===============================================================================
    world.step(0.001)

#===============================================================================
#   VIEW
#===============================================================================
#   Start with a blank screen.
    screen.fill(Colors.white)
    
    for i,disk in enumerate(world.disks):
        col = Colors.blue
        pos = map(int, [disk.pos.x, WORLD_Y - disk.pos.y])
        radius = int(disk.radius)

#       Draw a circle (screen, color, position, radius, width = 0).
        pygame.draw.circle(screen, col, pos, radius, 0) 
         
#   Draw onto the display.
    pygame.display.flip()

pygame.quit()
