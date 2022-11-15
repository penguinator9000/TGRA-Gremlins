import random
from random import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
from math import *

from Matrices import *


class GraphicalObject:
    def __init__(self, shape, size = (1,1,1),pos = (0,0,0), rotation =(0,0,0), color =Color(0.6,0.6,0.6) ):
        self.object = shape
        self.model_matrix = ModelMatrix()
        self.model_matrix.load_identity()
        self.model_matrix.add_translation(pos[0],pos[1],pos[2])
        self.model_matrix.add_scale(size[0],size[1],size[2])
        self.model_matrix.add_rotation(rotation[0],rotation[1],rotation[2])
        self.model_matrix.push_matrix()
        self.color = color
        self.pos=Point(pos[0],pos[1],pos[2])
        self.size=Vector(size[0],size[1],size[2])
        self.diffuse = Color(1,1,1)
        self.ambiance = Color(0.5,0.5,0.5)
        self.specular = Color(0.5,0.5,0.5)
        self.shiny = 1

    def draw(self, shader):
        r,g,b = self.color
        rd,gd,bd = self.diffuse
        ra,ga,ba = self.ambiance
        rs,gs,bs = self.specular
        shader.set_model_matrix(self.model_matrix.matrix)
        shader.set_material_diffuse(r*rd,g*gd,b*bd)
        shader.set_material_specular(r*rs,g*gs,b*bs, self.shiny)
        shader.set_material_ambient(r*ra,g*ga,b*ba)
        self.object.draw(shader)
        
    def update(self, size = 0 ,pos = 0, rotation =0, color =0):
        if color: self.color = color 
        if pos:
            self.model_matrix.add_translation(pos[0],pos[1],pos[2])
            self.pos+=Point(pos[0]*self.size.x,pos[1]*self.size.y,pos[2]*self.size.z)
        if size:
            self.model_matrix.add_scale(size[0],size[1],size[2])
            self.size=Point(self.size.x*size[0],self.size.y*size[1],self.size.z*size[2])
        if rotation:
            self.model_matrix.add_rotation(rotation[0],rotation[1],rotation[2])
    def reset(self):
        self.model_matrix.pop_matrix()
        self.model_matrix.push_matrix()
    def copy(self):
        cpy = GraphicalObject(self.object,color=Color(self.color[0],self.color[1],self.color[2]))
        cpy.model_matrix.matrix = self.model_matrix.copy_matrix()
        cpy.ambiance = self.ambiance
        cpy.diffuse = self.diffuse
        cpy.specular = self.specular
        cpy.shiny = self.shiny
        return cpy        

class BOI(GraphicalObject):
    boingPlaces = Vector(1,0,1)
    radius = Vector(0.25,0.25,0.25).__len__()
    spins = Vector(1,1.2,1.1)
    comboSpins = Vector(0,0,0)
    rgb =Color(0,0,0)
    def spinny(self, dtime):
        self.comboSpins += self.spins*dtime 
        sinComSpin = Vector(sin(self.comboSpins.x),sin(self.comboSpins.y),sin(self.comboSpins.z))
        self.model_matrix.add_rotation(sinComSpin.x,sinComSpin.y,sinComSpin.z)
        sinComSpin2 = Vector((sinComSpin.x+1)/2,(sinComSpin.y+1)/2,(sinComSpin.z+1)/2)

        self.diffuse  =Color(sinComSpin2.x,sinComSpin2.y,sinComSpin2.z)
        self.ambiance =Color(sinComSpin2.y,sinComSpin2.z,sinComSpin2.x)
        self.specular =Color(sinComSpin2.z,sinComSpin2.x,sinComSpin2.y)

        self.color = (1,1,1)
    def kill(self, playerPos, proj):
        diff =  playerPos - self.pos
        if diff.__len__() <  Vector(proj.near,proj.top,proj.right).__len__():
            return True
        return False     
    def move(self, dtime):
        moves = self.boingPlaces*dtime
        newpos = self.pos+moves
        self.moveTo(newpos.x,newpos.z)
        return moves
    def moveTo(self, x,z):
        self.reset()
        self.model_matrix.add_translation(x*2,0.25,z*2)
        self.pos = Point(x,0.5,z)
    def randomstart(self,qman):
        x = randint(3,31)
        z = randint(3,31)
        if qman.query_maze(int(x//2),int(z//2)):
            return self.moveTo(x,z)
        self.randomstart(qman)
    def reflect(self,mirVec):
        perpMirVec = Vector(-mirVec.z,0,mirVec.x)
        perpMirVec.normalize() #^n
        dot = self.boingPlaces.dot(perpMirVec)
        #vec = a
        self.boingPlaces.x =self.boingPlaces.x-2*dot*perpMirVec.x
        self.boingPlaces.z =self.boingPlaces.z-2*dot*perpMirVec.z