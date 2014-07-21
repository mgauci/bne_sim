# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 06:29:37 2014

@author: mgauci
"""

from geometry import *

SCALE = 1920/0.5092700
GRAVITY = 9.80665*SCALE # 9.81 m/s^2 to pixels/s^2

class Disk(Circle):
    def __init__(self, 
                 init_pos,
                 radius, 
                 mass, 
                 init_vel = Vec(0.0, 0.0), 
                 coeff_rest = 1.0):
        Circle.__init__(self, init_pos, radius)
        self.mass = mass
        self.vel = init_vel
        self.coeff_rest = coeff_rest
    def apply_gravity(self, dt, gravity):
        self.vel += dt*gravity
    def update_pos(self, dt):
        self.pos += dt*self.vel
    def kinetic_energy(self):
        return 0.5*self.mass*(self.vel.norm()**2)
        
        
def DiskWallCollision(disk, wall):
    if CircleLineIntersection(disk, wall):
        normal = LineToCircleUnitNormal(wall, disk)
#       Only apply collision resolution if the velocity of the
#       disk is pointing towards the wall.
        if disk.vel.dot(normal) < 0.0:
            vel_normal = disk.vel.dot(normal)*normal
            vel_tangent = disk.vel - vel_normal
            new_vel_normal = -1.0*disk.coeff_rest*vel_normal

            # TODO 
            
#            new_vel_normal = -1.0*vel_normal
#            new_vel_tangent_norm = vel_tangent.norm() - 0.001*1.0*GRAVITY
#            new_vel_tangent = (new_vel_tangent_norm/vel_tangent.norm())*vel_tangent
            new_vel_tangent = 0.5*vel_tangent
            disk.vel = new_vel_normal + new_vel_tangent

def DiskDiskCollision(disk_1, disk_2):
    if CircleCircleIntersection(disk_1, disk_2):
        normal = disk_2.pos - disk_1.pos # normal points from 1 to 2
        normal /= normal.norm()
        if (disk_2.vel - disk_1.vel).dot(normal) < 0.0:
            CR = min(disk_1.coeff_rest, disk_2.coeff_rest)
            m_1 = disk_1.mass
            m_2 = disk_2.mass
            u_1 = disk_1.vel.dot(normal)
            u_2 = disk_2.vel.dot(normal)
            
            v_1 = (m_1*u_1 + m_2*u_2 + m_2*CR*(u_2 - u_1))/(m_1 + m_2)
            v_2 = (m_2*u_2 + m_1*u_1 + m_1*CR*(u_1 - u_2))/(m_1 + m_2)
            
            disk_1.vel = (disk_1.vel - u_1*normal) + v_1*normal
            disk_2.vel = (disk_2.vel - u_2*normal) + v_2*normal
            
def DiskWallPositionCorrection(disk, wall):
    penetration = CircleLinePenetration(disk, wall)
    if penetration > 0.0*disk.radius:
        normal = LineToCircleUnitNormal(wall, disk)
        disk.pos += 0.5*penetration*normal
        
def DiskDiskPositionCorrection(disk_1, disk_2):
    penetration = CircleCirclePenetration(disk_1, disk_2)
    if penetration > 0.01*min(disk_1.radius, disk_2.radius):
        normal = disk_2.pos - disk_1.pos # normal points from 1 to 2
        normal /= normal.norm()
        correction = (0.8*penetration/(disk_1.mass + disk_2.mass))*normal
        disk_1.pos -= disk_1.mass*correction
        disk_2.pos += disk_2.mass*correction

class World:
    def __init__(self, bottom_left_corner, top_right_corner, disks = []):
        self.walls = Square(bottom_left_corner, top_right_corner)
        self.disks = disks
    def add_disk(self, disk):
        self.disks.append(disk)
    def step(self, dt):
#       Disk to Wall collisions.
        for disk in self.disks:
            DiskWallCollision(disk, self.walls.bottom_line)
            DiskWallCollision(disk, self.walls.top_line)
            DiskWallCollision(disk, self.walls.left_line)
            DiskWallCollision(disk, self.walls.right_line)
        
        for i in range(0, len(self.disks)):
            for j in range(0, i):
                if j != i:    
                    DiskDiskCollision(self.disks[i], self.disks[j])
            
            
        for disk in self.disks:
            disk.apply_gravity(dt, Vec(0.0, -GRAVITY))
            disk.update_pos(dt)
            
        for disk in self.disks:
            DiskWallPositionCorrection(disk, self.walls.bottom_line)
            DiskWallPositionCorrection(disk, self.walls.top_line)
            DiskWallPositionCorrection(disk, self.walls.left_line)
            DiskWallPositionCorrection(disk, self.walls.right_line)
            
        for i in range(0, len(self.disks)):
            for j in range(0, i):
                if j != i:    
                    DiskDiskPositionCorrection(self.disks[i], self.disks[j])
            
            