#!/usr/bin/env python2.7

from physics import *

import pygame
#import sys
from pygame.locals import *
import random

SCALE = 1080/0.286258  # 1080 pixels, 23" screen height = 0.28 meters.
SCALE = 1920/0.5092700 # Same story.

WORLD_X = 0.25*SCALE
WORLD_Y = 0.25*SCALE

pygame.init()
screen = pygame.display.set_mode((int(WORLD_X), int(WORLD_Y))) #Screen size
clock = pygame.time.Clock()

blue = (0,0,255)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255,255,255)

world = World(Vec(0.0, 0.0), Vec(WORLD_X, WORLD_Y))

pos = Vec(0.05*SCALE, 0.2*SCALE)
vel = Vec(1.5*SCALE, 0.0*SCALE) # converts 10m/sec to pixels/sec
d = Disk(pos, 0.02*SCALE, 100.0, init_vel = vel, coeff_rest = 0.75)
world.add_disk(d)

pos += Vec(0.1*SCALE, -0.1*SCALE)
vel = Vec(3.0*SCALE, 0.0)
d = Disk(pos, 0.005*SCALE, 12.5, init_vel = vel, coeff_rest = 0.75)
world.add_disk(d)
    

t = 0
main_loop = True 
while main_loop:
    t += 0.01
    clock.tick(1000) #FPS
    
#===============================================================================
#   CONTROL
#===============================================================================
#   Check for events (key presses, mouse movement etc.).
    for event in pygame.event.get():
#       X button pressed in the pygame window.
        if event.type == pygame.QUIT:
            main_loop = False
#       Escape key pressed on keyboard.
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            main_loop = False
            
#===============================================================================
#   MODEL
#===============================================================================
    world.step(0.001)
    KE = 0
    for disk in world.disks:
        KE += disk.kinetic_energy()

#===============================================================================
#   VIEW
#===============================================================================
#   Start with a blank screen.
    screen.fill(white)
    
    for i,disk in enumerate(world.disks):
        pos = [disk.pos.x, WORLD_Y - disk.pos.y]
        pos = map(int, pos)
        radius = int(disk.radius)
        if i < 100:
            col = blue
        else:
            col = red
#       Draw a circle (screen, color, position, radius, width = 0).
        pygame.draw.circle(screen, col, pos, radius, 0) 
         
#       Draw onto the display.
        pygame.display.flip()
    
        print KE

pygame.quit()
