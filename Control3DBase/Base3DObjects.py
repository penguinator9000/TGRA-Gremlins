
import random
from random import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
from math import *


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    def __str__(self) -> str:
        return "|x:"+str(self.x)+", y:"+str(self.y)+", z:"+str(self.z)+" |"

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __len__(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def normalize(self):
        length = self.__len__()
        if length!=0:
            self.x /= length
            self.y /= length
            self.z /= length

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)
    def __str__(self) -> str:
        return "|x:"+str(self.x)+", y:"+str(self.y)+", z:"+str(self.z)+" |"

class Color:
    def __init__(self,r=0,g=0,b=0,a=1):
        self.r=r
        self.g=g
        self.b=b
        self.a=a
        self.rgb=(r,g,b)
        self.rgba=(r,g,b,a)
    
    def __getitem__(self,i):
        return self.rgb[i]
    
        
class Cube:
    def __init__(self):
        self.position_array = [-0.5, -0.5, -0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, 0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, 0.5, -0.5]
        self.normal_array = [0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0]
    def draw(self, shader):
        
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        
        for i in range(6):
            glDrawArrays(GL_TRIANGLE_FAN, i*4, 4)

class D8:
    def __init__(self):
        self.position_array=[ 0.5, 0.0, 0.0,
                              0.0, 0.5, 0.0,
                              0.0, 0.0, 0.5,
                             -0.5, 0.0, 0.0,
                              0.0, 0.5, 0.0,
                              0.0, 0.0, 0.5,
                              0.5, 0.0, 0.0,
                              0.0,-0.5, 0.0,
                              0.0, 0.0, 0.5,
                              0.5, 0.0, 0.0,
                              0.0, 0.5, 0.0,
                              0.0, 0.0,-0.5,
                             -0.5, 0.0, 0.0,
                              0.0,-0.5, 0.0,
                              0.0, 0.0, 0.5,
                              0.5, 0.0, 0.0,
                              0.0,-0.5, 0.0,
                              0.0, 0.0,-0.5,
                             -0.5, 0.0, 0.0,
                              0.0, 0.5, 0.0,
                              0.0, 0.0,-0.5,
                             -0.5, 0.0, 0.0,
                              0.0,-0.5, 0.0,
                              0.0, 0.0,-0.5,]

        self.normal_array= [ 1, 1, 1,
                             1, 1, 1,
                             1, 1, 1,
                            -1, 1, 1,
                            -1, 1, 1,
                            -1, 1, 1,
                             1,-1, 1,
                             1,-1, 1,
                             1,-1, 1,
                             1, 1,-1,
                             1, 1,-1,
                             1, 1,-1,
                            -1,-1, 1,
                            -1,-1, 1,
                            -1,-1, 1,
                             1,-1,-1,
                             1,-1,-1,
                             1,-1,-1,
                            -1, 1,-1,
                            -1, 1,-1,
                            -1, 1,-1,
                            -1,-1,-1,
                            -1,-1,-1,
                            -1,-1,-1 ]
        
    def draw(self, shader):
        
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        
        for i in range(8):
            glDrawArrays(GL_TRIANGLE_FAN, i*3, 3)

class Plane:
    def __init__(self):
        self.position_array = [-0.5, 0,-0.5,
                               -0.5, 0, 0.5,
                                0.5, 0, 0.5,
                                0.5, 0,-0.5,
                            ]
        self.normal_array = [0.0,1.0,0.0,
                             0.0,1.0,0.0,
                             0.0,1.0,0.0,
                             0.0,1.0,0.0,
                            ]
    def draw(self, shader):
        
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        
        for i in range(1):
            glDrawArrays(GL_TRIANGLE_FAN, i*4, 4)
        