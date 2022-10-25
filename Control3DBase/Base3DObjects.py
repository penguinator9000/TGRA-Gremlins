
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
    
    def list(self):
        return [self.x,self.y,self.z]

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
    
    def __mul__(self, other):
        return Color(self.r * other.r, self.g * other.g, self.b * other.b,self.a*other.a)
    
        
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
        self.uv_array = [0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0]*6
        
    def draw(self, shader):
        
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)
        
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
        self.uv_array = [1.0, 0.5,
                         0.0, 1.0,
                         0.0, 0.0]*8
    def draw(self, shader):
        
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)
        
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
        self.uv_array = [0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0]
    def draw(self, shader):
        
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)
        
        for i in range(1):
            glDrawArrays(GL_TRIANGLE_FAN, i*4, 4)

class Light():
    def __init__(self, pos = Point(4,10,4), color = Color(1,1,1),diffuse= Color(1,1,1), ambiance = Color(0.5,0.5,0.5),specular = Color(0.25,0.25,0.25), reach=0):
        self.pos = pos
        self.color = color
        self.diffuse = diffuse
        self.ambiance = ambiance
        self.specular = specular
        self.reach = reach
    
        

class BayesianCurve4P:
    def __init__(self,p1,p2,p3,p4,d=1):
        v=Vector(0,0,0)
        self.p1=v+p1
        if type(p2)==type(v):
            self.p2=self.p1+p2
            self.p1p2vec = p2
        else:
            self.p2=v+p2
            self.p1p2vec = self.p2-self.p1
        self.p4=v+p4
        if type(p3)==type(Vector(0,0,0)):
            self.p3=self.p4+(p3*(-1))
            self.p3p4vec = p3
        else:
            self.p3=v+p3
            self.p3p4vec = self.p4-self.p3
        self.duration = d
        
    
    def __getitem__(self,t):
        #v=Vector(1,1,1)
        #print(Vector(1,0,0)*((1-t)**3)+Vector(0,1,0)*((3*((1-t)**2))*t)+Vector(0,0,1)*(3*(1-t)*(t**2))+Vector(0,0,0)*(t**3))
        return self.p1*((1-t)**3)+self.p2*((3*((1-t)**2))*t)+self.p3*(3*(1-t)*(t**2))+self.p4*(t**3)
    
    def getPoint(self,f):
        """frame of duration"""
        t=f/self.duration
        return self.__getitem__(t)

class LoopBayesianCurves4P:
    def __init__(self,Curve1,repetitions=2):
        self.Curvelist=[Curve1]
        self.ControlePoints=[Curve1.p1,Curve1.p1p2vec,Curve1.p4,Curve1.p3p4vec]
        repetitions+=repetitions%2
        self.length=repetitions
        for i in range(repetitions):
            X=self.Curvelist[i]
            p1, v2, p4, v3 = (X.p1,X.p1p2vec,X.p4,X.p3p4vec)
            C = BayesianCurve4P(p4,v3,v2,p1)
            self.Curvelist.append(C)
            self.ControlePoints+=[p1,v2]
    def __getitem__(self,t):
        t=t%self.length
        i=int(t//1)
        it=t%1
        return self.Curvelist[i][it]   

    def BuildFromControle(self,ControlePoints=[]):
        if ControlePoints == []: ControlePoints=self.ControlePoints
        for i in range(self.length):
            p1, v2, p4, v3 = self.ControlePoints[i*2:i*2+4]
            if i == self.length-1:
                p4,v3=self.ControlePoints[0:2]
            C = BayesianCurve4P(p1,v2,v3,p4)
            self.Curvelist[i]=C

def det(M2x2):
    a,b,c,d = M2x2
    return (a*d)-(b*c)
class Mesh:
    def __init__(self,n,m,pos=Point(0,0,0),color=Color(),DrawingMode="1"):
        self.PointMatrix=[[pos]*m]*n
        self.ColorMatrix=[[color]*m]*n
        
        self.pos=pos
        self.DrawingMode=DrawingMode
        #self.position_array=[Point(0,0,0)]*m*n
        #self.normal_array=[Point(0,0,0)]*m*n
        self.nm=(n,m)
        self.color=color
        self.diffuse = Color(1,1,1)
        self.ambiance = Color(0.5,0.5,0.5)
        self.specular = Color(0.5,0.5,0.5)
        self.shiny = 1
        self.single_uv_array = [1.0, 0.5,
                         0.0, 1.0,
                         0.0, 0.0]
        self.model_matrix=[ 1, 0, 0, 0,
                                  0, 1, 0, 0,
                                  0, 0, 1, 0,
                                  0, 0, 0, 1 ]
        
    
    def draw(self,shader):
        n,m=self.nm
        v=Vector(0,0,0)
        shader.set_model_matrix(self.model_matrix)
        r,g,b = self.color
        rd,gd,bd = self.diffuse
        ra,ga,ba = self.ambiance
        rs,gs,bs = self.specular
        shader.set_material_diffuse(r*rd,g*gd,b*bd)
        shader.set_material_specular(r*rs,g*gs,b*bs, self.shiny)
        shader.set_material_ambient(r*ra,g*ga,b*ba)
        
        position_array=[]
        normal_array=[]

        if n>1 and m>1:
            for ni in range(n-1):
                for mi in range(m-1):
                    if self.DrawingMode == "1":
                        p1 = v+(self.PointMatrix[ni][mi])
                        p2 = v+(self.PointMatrix[ni+1][mi])
                        p3 = v+(self.PointMatrix[ni][mi+1])
                        p4 = v+(self.PointMatrix[ni+1][mi+1])
                    elif self.DrawingMode == "2":
                        p1 = v+(self.PointMatrix[ni+1][mi])
                        p2 = v+(self.PointMatrix[ni][mi])
                        p3 = v+(self.PointMatrix[ni+1][mi+1])
                        p4 = v+(self.PointMatrix[ni][mi+1])
                    
                    # position_array=p1.list()+p2.list()+p3.list()
                    # v1=p2-p1
                    # v2=p3-p1
                    # nv=Vector(det([v1.y,v1.z,v2.y,v2.z]),det([v1.x,v1.z,v2.x,v2.z]),det([v1.x,v1.y,v2.x,v2.y]))
                    # nv.normalize()
                    # facingv=p1-self.pos+p2-self.pos+p3-self.pos
                    # facingv.normalize()
                    # sign=facingv.dot(nv)
                    # if sign<0:nv*(-1) 
                    # normal_array=nv.list()*3
                    # shader.set_position_attribute(position_array)
                    # shader.set_normal_attribute(normal_array)
                    # glDrawArrays(GL_TRIANGLE_FAN, 0, 3)

                    for l in [[p1,p2,p3],[p2,p3,p4]]:
                        l1,l2,l3=l
                        position_array=l1.list()+l2.list()+l3.list()
                        v1=l1-l3
                        v2=l2-l3
                        facingv=l1-self.pos+l2-self.pos+l3-self.pos
                        
                        nv=Vector(det([v1.y,v1.z,v2.y,v2.z]),det([v1.x,v1.z,v2.x,v2.z]),det([v1.x,v1.y,v2.x,v2.y]))
                        nv.normalize()
                        facingv.normalize()
                        sign=facingv.dot(nv)
                        if sign<0:nv=nv*(-1)
                        # print("lol") 
                        # if 1+nv.y>0:
                        #     nv*(-1)
                        #     print("woop")
                        normal_array=nv.list()*3
                        shader.set_position_attribute(position_array)
                        shader.set_normal_attribute(normal_array)
                        shader.set_uv_attribute(self.single_uv_array)
                        glDrawArrays(GL_TRIANGLE_FAN, 0, 3)
        
    
                    
                        
        
        
    