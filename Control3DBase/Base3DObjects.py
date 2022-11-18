
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
    
    def normalize(self,out=False):
        length = self.__len__()
        if length!=0 and not out:
            self.x /= length
            self.y /= length
            self.z /= length
        elif length!=0 :
            return Vector(self.x / length,self.y / length,self.z / length)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)
    def __str__(self) -> str:
        return "|x:"+str(self.x)+", y:"+str(self.y)+", z:"+str(self.z)+" |"
    
    def list(self):
        return [self.x,self.y,self.z]
    
    def axWiseMult(self,other):
        return Vector(self.x * other.x , self.y * other.y , self.z * other.z)
    
    def copy(self):
        return Vector(self.x*1 ,self.y*1 ,self.z*1 )


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
        return Color(self.r * other.r, self.g * other.g, self.b * other.b, self.a * other.a)
    
    def __add__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b, self.a + other.a)

    def __str__(self):
        return"RGBA - "+str(self.r)+", "+str(self.g)+", "+str(self.b)+", "+str(self.a)
    
    def intensity(self,scalar):
        return Color(self.r * scalar, self.g * scalar, self.b * scalar, self.a * scalar)

        
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
        # self.uv_array = [1.0, 1.0,
        #                  0.0, 0.0,
        #                  1.0, 1.0,
        #                  0.0, 0.0]*12
        self.uv_array = [0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0]*12
        
        
    def draw(self, shader,skipSides=[]):
        
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)
        
        for i in range(6):
            if not(i in skipSides):
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
                         0.0, 0.0]*16
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
                         1.0, 0.0]*2
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
    def __str__(self) -> str:
        L=[str(self.pos) ,
        str(self.color ),
        str(self.diffuse) ,
        str(self.ambiance) ,
        str(self.specular ),
        str(self.reach) ]
        return "L* - "+str(L)
    
    def copy(self):
        return Light(self.pos ,
        self.color,
        self.diffuse,
        self.ambiance,
        self.specular,
        self.reach)    

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
    def __init__(self,Curve1=BayesianCurve4P(Point(1,1,1),Point(1,1,1),Point(1,1,1),Point(1,1,1)),repetitions=2,d=1):
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
        self.duration=d

    def __getitem__(self,t):
        t=t%self.length
        i=int(t//1)
        it=t%1
        return self.Curvelist[i][it]
    
    def getPoint(self,f):
        """frame of duration"""
        t=(f/self.duration)*self.length
        return self.__getitem__(t)

    def BuildFromControle(self,ControlePoints=[]):
        if ControlePoints != []: self.ControlePoints=ControlePoints
        for i in range(self.length):
            p1, v2, p4, v3 = self.ControlePoints[i*2:i*2+4]
            if i == self.length-1:
                p4,v3=self.ControlePoints[0:2]
            C = BayesianCurve4P(p1,v2,v3,p4)
            self.Curvelist[i]=C

def det(M2x2):
    a,b,c,d = M2x2
    return (a*d)-(b*c)
def det3(M3x3):
    top=M3x3[:3]
    mid=M3x3[3:6]
    bot=M3x3[3:6]
    a=top[0]*det(mid[:2]+bot[:2])
    b=top[1]*det([mid[0],mid[2],bot[0],bot[2]])
    c=top[2]*det(mid[1:]+bot[1:])
    return a-b+c
class Mesh:
    def __init__(self,n,m,pos=Point(0,0,0),color=Color(),vertex="1",texture="triangle"):
        self.PointMatrix=[[pos]*m]*n
        self.ColorMatrix=[[color]*m]*n
        
        self.pos=pos
        self.DrawingMode={"vertex":vertex,"texture":texture}
        #self.position_array=[Point(0,0,0)]*m*n
        #self.normal_array=[Point(0,0,0)]*m*n
        self.nm=(n,m)
        self.color=color
        self.diffuse = Color(1,1,1)
        self.ambiance = Color(0.5,0.5,0.5)
        self.specular = Color(0.5,0.5,0.5)
        self.shiny = 1
        
        self.model_matrix=[ 1, 0, 0, 0,
                            0, 1, 0, 0,
                            0, 0, 1, 0,
                            0, 0, 0, 1 ]
        self.texture=None
        self.spectexture=None
        self.LastDrawInfo=[None]*7
    
    def draw(self,shader):
        n,m=self.nm
        v=Vector(0,0,0)
        shader.set_model_matrix(self.model_matrix)
        
        
        position_array=[]
        normal_array=[]
        uv_array = []
        color_array=[]
        triangle_uv_array = [1.0, 0.5,
                             0.0, 1.0,
                             0.0, 0.0]
        many=0
        if self.texture != None:
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D,self.texture)
            shader.set_material_texture(1)
        else:
            shader.set_material_texture(0)
        if self.spectexture != None:
            glActiveTexture(GL_TEXTURE2)
            glBindTexture(GL_TEXTURE_2D,self.spectexture)
            shader.set_material_specular_texture(2)
        else:
            shader.set_material_specular_texture(0)

        if  self.LastDrawInfo[:3] == [self.PointMatrix,self.DrawingMode,self.ColorMatrix]:
            position_array=self.LastDrawInfo[3]
            normal_array=self.LastDrawInfo[4]
            uv_array = self.LastDrawInfo[5]
            many= self.LastDrawInfo[6]
            color_array= self.LastDrawInfo[7]
        elif n>1 and m>1:
            for ni in range(n-1):
                for mi in range(m-1):
                    if self.DrawingMode["vertex"] == "1":
                        p1 = v+(self.PointMatrix[ni][mi])
                        p2 = v+(self.PointMatrix[ni+1][mi])
                        p3 = v+(self.PointMatrix[ni][mi+1])
                        p4 = v+(self.PointMatrix[ni+1][mi+1])
                        c1 = (self.ColorMatrix[ni][mi])
                        c2 = (self.ColorMatrix[ni+1][mi])
                        c3 = (self.ColorMatrix[ni][mi+1])
                        c4 = (self.ColorMatrix[ni+1][mi+1])
                        if self.DrawingMode["texture"]=="squere":
                            squere_uv_array=[0,0,
                                             1,0,
                                             0,1,
                                             1,1]
                        elif self.DrawingMode["texture"]=="All":
                            squere_uv_array=[ni/n,mi/m,
                                             (ni+1)/n,mi/m,
                                             ni/n,(mi+1)/m,
                                             (ni+1)/n,(mi+1)/m]
                    elif self.DrawingMode["vertex"] == "2":
                        p1 = v+(self.PointMatrix[ni+1][mi])
                        p2 = v+(self.PointMatrix[ni][mi])
                        p3 = v+(self.PointMatrix[ni+1][mi+1])
                        p4 = v+(self.PointMatrix[ni][mi+1])
                        c1 = (self.ColorMatrix[ni+1][mi])
                        c2 = (self.ColorMatrix[ni][mi])
                        c3 = (self.ColorMatrix[ni+1][mi+1])
                        c4 = (self.ColorMatrix[ni][mi+1])
                        if self.DrawingMode["texture"]=="squere":
                            squere_uv_array=[1,0,
                                             0,0,
                                             1,1,
                                             0,1]
                        elif self.DrawingMode["texture"]=="All":
                            squere_uv_array=[(ni+1)/n,mi/m,
                                             ni/n,mi/m,
                                             (ni+1)/n,(mi+1)/m,
                                             ni/n,(mi+1)/m]
                    
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

                    for l in [[p1,p2,p3,c1,c2,c3],[p2,p3,p4,c2,c3,c4]]:
                        l1,l2,l3,k1,k2,k3=l
                        position_array+=l1.list()+l2.list()+l3.list()
                        v1=l1-l3
                        v2=l2-l3
                        facingv=l1-self.pos+l2-self.pos+l3-self.pos
                        
                        nv=Vector(det([v1.y,v1.z,v2.y,v2.z]),det([v1.x,v1.z,v2.x,v2.z]),det([v1.x,v1.y,v2.x,v2.y]))
                        nv.normalize()
                        facingv.normalize()
                        sign=facingv.dot(nv)
                        #print(sign)
                        #if sign>0:nv=nv*(-1)
                        # print("lol") 
                        # if 1+nv.y>0:
                        #     nv*(-1)
                        #     print("woop")
                        
                        color_array.append(k1.intensity(1/3)+k2.intensity(1/3)+k3.intensity(1/3))
                        if self.DrawingMode["texture"]=="triangle":
                            #shader.set_uv_attribute(triangle_uv_array)
                            uv_array +=triangle_uv_array
                            if sign<=0:nv=nv*(-1)#def wrong
                        elif self.DrawingMode["texture"]=="squere" or self.DrawingMode["texture"]=="All":
                            if l3==p3:
                                #shader.set_uv_attribute(squere_uv_array[:-1])
                                uv_array +=squere_uv_array[:-1]
                                
                            else:
                                #shader.set_uv_attribute(squere_uv_array[1:])
                                uv_array +=squere_uv_array[1:]
                                nv=nv*(-1)
                        else:
                            if sign>0:nv=nv*(-1)#def wrong

                        normal_array+=nv.list()*3
                        many+=1    
                        
        shader.set_position_attribute(position_array)
        shader.set_normal_attribute(normal_array)
        shader.set_uv_attribute(uv_array)
        for i in range(many):
            C=color_array[i]
            rd,gd,bd = self.diffuse*C
            ra,ga,ba = self.ambiance*C
            rs,gs,bs = self.specular*C
            shader.set_material_diffuse(rd,gd,bd)
            shader.set_material_specular(rs,gs,bs, self.shiny)
            shader.set_material_ambient(ra,ga,ba)
            glDrawArrays(GL_TRIANGLE_FAN, i*3, 3)
        self.LastDrawInfo=[self.PointMatrix.copy(),self.DrawingMode.copy(),self.ColorMatrix.copy(),position_array,normal_array,uv_array,many,color_array]


class Lava():
    def __init__(self,Wave,N,M,p1,p2,botColor,topColor,xWaveScale,yWaveScale,zWaveScale,animationSpeed=1,yWaveRange=None,texture=None,spectexture=None):
        if Wave == None:
            Wave=LoopBayesianCurves4P()
        self.Wave=Wave
        self.nm=(N,M)
        self.animationSpeed=animationSpeed
        v=Vector(0,0,0)
        x1,y1,z1 = (v+p1).list()
        x2,y2,z2 = (v+p2).list()
        self.Xrange=(x1,x2)
        self.Yrange=(y1,y2)
        self.Zrange=(z1,z2)
        self.mesh=Mesh(N,M,Point((x1+x2)/2,(y1+y2)/2-10000000,(z1+z2)/2),topColor,texture="triangle")
        self.mesh.texture=texture
        self.mesh.spectexture=spectexture
        self.timeElapsed = 0
        if yWaveRange==None:
            yWaveMin=self.Wave.ControlePoints[0].y
            yWaveMax=self.Wave.ControlePoints[0].y
            temp=self.Wave.ControlePoints[0].y
            for i in range(len(self.Wave.ControlePoints)):
                P=self.Wave.ControlePoints[i].y
                if i%2:
                    temp=self.Wave.ControlePoints[i].y
                    if P>yWaveMax:
                        yWaveMax=P
                    elif P<yWaveMin:
                        yWaveMin=P
                else:
                    P1=temp+self.Wave.ControlePoints[i].y
                    if P1>yWaveMax:
                        yWaveMax=P1
                    elif P<yWaveMin:
                        yWaveMin=P1
                    P2=temp-self.Wave.ControlePoints[i].y
                    if P1>yWaveMax:
                        yWaveMax=P2
                    elif P<yWaveMin:
                        yWaveMin=P2
            self.yWaveRange=(yWaveMin,yWaveMax)
        else:
            self.yWaveRange=yWaveRange

        self.WaveScale=Vector(xWaveScale,yWaveScale,zWaveScale)
        self.Colors=(botColor,topColor)
        self.update(0)

    def update(self,dtime):
        #return None
        self.timeElapsed +=dtime/1000
        
        N,M = self.nm
        xMin,xMax=self.Xrange
        yMin,yMax=self.Yrange
        zMin,zMax=self.Zrange
        yPs=[]
        def X(m):return xMin + (m/(M-1))*(xMax-xMin)
        def Y(n,m):
            time=self.timeElapsed*self.animationSpeed
            xW=self.Wave[(n+time)/self.WaveScale.x].x
            zW=self.Wave[(n+time)/self.WaveScale.z].z
            yW=self.Wave[(m+time)/self.WaveScale.y+xW+zW].y
            yWaveMin,yWaveMax =self.yWaveRange
            yP = ( (yW-yWaveMin)/(yWaveMax-yWaveMin) )
            yPs.append(yP)
            y = yMin +yP *(yMax-yMin)
            return y 
        def Z(n):return zMin + (n/(N-1))*(zMax-zMin)
        self.mesh.PointMatrix=[ [ Point(X(n),Y(n,m),Z(m)) for m in range(M) ] for n in range(N)]
        botColor,topColor=self.Colors
        self.mesh.ColorMatrix=[[ (botColor.intensity(1-yPs[m+n*M]))+(topColor.intensity(yPs[m+n*M])) for m in range(M) ] for n in range(N)]
    
    def draw(self,shader):
        #return None
        self.mesh.draw(shader)




if __name__ == "__main__":
    from leveltest import *
    GraphicsProgram3D().start() 
                    
                        
        
        
    