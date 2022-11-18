import random
from random import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
from math import *

from Matrices import *

def lerp(a,b,t):
    t=max(0,min(t,1))
    return a*(1-t)+b*t

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
        self.texture=None
        self.spectexture=None

    def draw(self, shader,skipSides=[]):
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
        
            
        r,g,b = self.color
        rd,gd,bd = self.diffuse
        ra,ga,ba = self.ambiance
        rs,gs,bs = self.specular
        shader.set_model_matrix(self.model_matrix.matrix)
        shader.set_material_diffuse(r*rd,g*gd,b*bd)
        shader.set_material_specular(r*rs,g*gs,b*bs, self.shiny)
        shader.set_material_ambient(r*ra,g*ga,b*ba)
        if skipSides:
            self.object.draw(shader,skipSides)
        else:
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


# class GOPortals:#nvm
#     def __init__(self):
#         self.yRotation=0
#         self.view_matrix=ViewMatrix()
#         self.projection_matrix=ProjectionMatrix()
#         self.pos=Point(0,0,0)
#     def set_view_matrix(self,playerVM):
#         self.view_matrix.eye = playerVM.eye-self.pos
        
          

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
        #if qman.query_maze(int(x//2),int(z//2)):
        return self.moveTo(x,z)
        self.randomstart(qman)
    def reflect(self,mirVec):
        perpMirVec = Vector(-mirVec.z,0,mirVec.x)
        perpMirVec.normalize() #^n
        dot = self.boingPlaces.dot(perpMirVec)
        #vec = a
        self.boingPlaces.x =self.boingPlaces.x-2*dot*perpMirVec.x
        self.boingPlaces.z =self.boingPlaces.z-2*dot*perpMirVec.z


class Button:
    def cordCalcs(self,corner,size,offset):
        start = corner*size+self.buttonSize
        end =  corner*size+size-self.buttonSize
        return lerp(start,end,offset)
        pass
    def __init__(self,id, button_dict,xSize,ySize,zSize,buttonsize = 0.1):
        self.buttonSize = buttonsize
        self.id = id
        self.height = 0.433
        x = button_dict["box-x"]
        y = button_dict["box-y"]
        z = button_dict["box-z"]
        self.boxXYZ=(x,y,z)
        self.xpos = self.cordCalcs(button_dict["box-x"],xSize,button_dict['placement']["x-offset"])
        self.ypos = button_dict["box-y"]*ySize+self.height/2
        self.zpos = self.cordCalcs(button_dict["box-z"],zSize,button_dict['placement']["z-offset"])
        self.point = (self.xpos,self.ypos,self.zpos)
        self.actions = button_dict['action']
        self.colors = button_dict['color']
        self.pillar = GraphicalObject(Cube(),size = (buttonsize,self.height,buttonsize),pos=(self.xpos,self.ypos,self.zpos),color=(0.5,0.2,0.5))
        self.button = GraphicalObject(Cube(),size=(buttonsize*0.7,0.045,buttonsize*0.7),pos=(self.xpos,self.ypos+self.height/2,self.zpos),color=(0.1,0.6,0.6),rotation=(0,45,0) )
        self.proxMargin = 0.5
        self.state = -1
        self.colorState = -1
        #print(button_dict["box-x"],button_dict["box-y"],button_dict["box-z"])
        #print(self.xpos,self.ypos,self.zpos)
    def proximity_test(self,p):
        """if p - pos length is within the margins defined by the button return true"""
        x,y,z = self.xpos,self.ypos,self.zpos
        v = Vector(-x,-y,-z)+p
        if(v.__len__()<self.proxMargin): return True
        return False
    def press(self):
        if self.state == -1: 
            self.state = 0
            self.colorState = 0
        else: 
            self.state +=1
            self.colorState +=1
            if self.state == len(self.actions): self.state = 0
            if self.colorState == len(self.colors): self.colorState = 0
        #print(self.colorState,len(self.colors))
        self.button.color = self.colors[self.colorState]
        return self.actions[self.state]
        
    def nullState(self):
        pass
    def draw(self,shader):
        self.pillar.draw(shader)
        self.button.draw(shader)
class Portal:
    def __init__(self,id, portalDict,xSize,ySize,zSize):
        r =pi/2
        offset = 0.0
        self.active = False
        self.id = id
        self.direction = portalDict["location"]["direction"]
        xd,yd,zd = self.direction
        self.up = portalDict['location']['up']
        x = portalDict["location"]["box-x"]
        y = portalDict["location"]["box-y"]
        z = portalDict["location"]["box-z"]
        self.boxXYZ=(x,y,z)
        self.xpos = x*xSize+xSize/2 + xd*(xSize+offset)/2
        self.ypos = (y-1)*ySize+ySize/2+ yd*(ySize+offset)/2
        self.zpos = z*zSize+zSize/2 + zd*(zSize+offset)/2
        #print(self.xpos,self.ypos,self.zpos)
        rot = (r*xd,0,r)
        if yd != 0: rot = (2*r,0,0)
        self.portal = GraphicalObject(Plane(),size=(xSize,ySize,zSize),pos=(self.xpos,self.ypos,self.zpos),color=(0,0,1), rotation=rot)  
        c=Cube()
        f=-1
        for i in range(6):
            #print(c.normal_array[i*3*4:i*3*4+3])
            if self.direction == c.normal_array[i*3*4:i*3*4+3]:
                f=i
        self.face=f  

    def draw(self,shader):
        if self.active:
            self.portal.draw(shader)
    def setColor(self,color):
        self.portal.color = color

class SmallWall:
    def __init__(self,id, smallWallDict,xSize,ySize,zSize,pillarcount=3,barcount=1,Smaller=0.2,barUpSmaller=0.1):
        self.id = id
        
        SizeV=Vector(xSize,ySize,zSize)
        BoxPos=Vector(smallWallDict["location"]["box-x"],smallWallDict["location"]["box-y"],smallWallDict["location"]["box-z"])
        posDir=Vector(smallWallDict["location"]["direction"][0]*xSize,smallWallDict["location"]["direction"][1]*ySize,smallWallDict["location"]["direction"][2]*zSize)
        PosSize=posDir.axWiseMult(SizeV)
        PosSizeHalf=PosSize*0.5
        self.pos = Point(BoxPos.x*xSize + xSize/2+PosSizeHalf.x,(BoxPos.y-1)*ySize + ySize/2+PosSizeHalf.y,BoxPos.z*zSize+zSize/2++PosSizeHalf.z)
        self.boxXYZ=BoxPos.list()
        upDir=Vector(smallWallDict["location"]["up"][0],smallWallDict["location"]["up"][1],smallWallDict["location"]["up"][2])
        colliSize=[]
        pillaSize=[]
        bar__Size=[]
        Sizes=SizeV.list()
        smallSize=(SizeV*Smaller).list()
        for i in range(len(smallWallDict["location"]["direction"])):
            d=smallWallDict["location"]["direction"][i]
            u=smallWallDict["location"]["up"][i]
            
            if d == 0:
                if u!=0:
                    bar__Size.append(Sizes[i]*barUpSmaller)
                    pillaSize.append(Sizes[i])
                else:
                    bar__Size.append(Sizes[i])
                    pillaSize.append(sqrt(2*((smallSize[i]*0.5)**2)))#will not be good if x!=z
                colliSize.append(Sizes[i])
                
            else:
                pillaSize.append(sqrt(2*((smallSize[i]*0.5)**2)))#will not be good if x!=z
                bar__Size.append(smallSize[i])
                colliSize.append(smallSize[i])

        self.collisionCube= GraphicalObject(Cube(),colliSize,pos = (self.pos.x,self.pos.y,self.pos.z))
        self.DrawObjects=[]
        upDir.normalize()
        
        sideDir = ((upDir.normalize(True)+posDir.normalize(True))*(-1)+Vector(1,1,1)).normalize(True)
        sideSize = sideDir.axWiseMult(SizeV)
        for i in range(pillarcount):
            rot=upDir*(pi/4)
            
            p=Vector(self.pos.x,self.pos.y,self.pos.z)+sideSize*(-0.5)
            sideSmall = sideSize*Smaller
            ler=lerp(sideSize,Vector(0,0,0),((i+0.5)/pillarcount))
            #print(p,ler,sideSize,(i/pillarcount))
            p=ler+p#+sideSmall
            G=GraphicalObject(Cube(),pillaSize,pos =p.list() )
            G.model_matrix.add_rotation(rot.x,rot.y,rot.z)
            self.DrawObjects.append(G)
            pass
        for i in range(barcount):
            

            G=GraphicalObject(Cube(),bar__Size,pos = (self.pos.x,self.pos.y,self.pos.z))
            self.DrawObjects.append(G)
            pass


    def draw(self,shader):
        
        #self.collisionCube.draw(shader)
        for o in self.DrawObjects:
            o.draw(shader)
        pass

class PortalLink:
    def __init__(self, ll,f1,t1,f2,t2):
        self.ll = ll
        self.p1 = None
        self.p2 = None
        self.buttonID = None
        self.f1=f1
        self.t1=t1
        self.f2=f2
        self.t2=t2
    def update(self,buttonId,p1_Id, p2_Id):
        if self.buttonID:
            if self.buttonID != buttonId:
                self.ll.buttons[self.buttonID].nullState()
        if self.p1 or self.p2:
            self.clear()
        self.buttonID = buttonId
        self.p1 = self.ll.portals[p1_Id]
        self.p1.active = True
        self.p2 = self.ll.portals[p2_Id]
        self.p2.active = True
        self.p1.portal.color=Color(1, 0.5, 0, 1)
        self.p2.portal.color=Color(0, 0.5, 1, 1)
        self.p1.portal.texture=None
        self.p2.portal.texture=None
        
        
    def clear(self):
        self.p1.active = False
        self.p2.active = False
        self.p1 = None
        self.p2 = None
    def teleport(self,inPortal,toPort,matrix):
        """
            use the input portal to return the new position of the object
        """
        if self.p1 and self.p2:
            if self.p1.id == inPortal.id: outPortal = self.p2
            else: outPortal = self.p1
            x,y,z = outPortal.direction
            toPort.x = outPortal.xpos + x*0.25
            toPort.y = outPortal.ypos + y*0.25
            toPort.z = outPortal.zpos + z*0.25
            
            look = Vector(outPortal.xpos,outPortal.ypos,outPortal.zpos)+Vector(x,y,z)
            a,b,c = outPortal.up
            matrix.look(look,Vector(a,b,c))
        else: print("Bro portals aint got no conenctions right now")

    def gibRot(self,d1,d2):
        if d1 == d2:
            return pi
        elif d1+d2 == Vector(0,0,0):
            return 0
        if d1.x:
            boy=d2.z
        else:
            boy=d2.x
        return boy*pi/2

    
    def portalTexturUpdate(self,shader,viewMatrixObj,projectionMatrixObj,objects):
        
        if self.p1 and self.p2:
            if  self.p1.active and self.p2.active:
                
                veiw1 = viewMatrixObj.copy()
                veiw2 = viewMatrixObj.copy()

                self.p1.portal.color=Color(1,1,1)
                self.p2.portal.color=Color(1,1,1)

                d1x,d1y,d1z = self.p1.direction
                d2x,d2y,d2z = self.p2.direction

                d1 = Vector(d1x,d1y,d1z)
                d2 = Vector(d2x,d2y,d2z)

                rot=self.gibRot(d1,d2)

                p1v=Vector(self.p1.xpos,0,self.p1.zpos)
                p2v=Vector(self.p2.xpos,0,self.p2.zpos)

                v1=((p1v*(-1))+viewMatrixObj.eye)
                v2=((p2v*(-1))+viewMatrixObj.eye)

                vv1=Vector(v1.x*cos(rot) -v1.z*sin(rot) ,v1.y,v1.x*sin(rot) +v1.z*cos(rot))
                rot2=-rot
                vv2=Vector(v2.x*cos(rot) -v2.z*sin(rot) ,v2.y,v2.x*sin(rot) +v2.z*cos(rot))
                n=viewMatrixObj.n
                nn =Vector(n.x*cos(rot) -n.z*sin(rot) ,n.y,v2.x*sin(rot) +n.z*cos(rot))

                veiw1.eye=veiw1.eye+vv2
                veiw2.eye=veiw2.eye+vv1
                u1x,u1y,u1z = self.p1.up
                veiw1.look(veiw1.eye-nn,Vector(u1x,-u1y,u1z))
                #veiw1.look(p1v,Vector(u1x,-u1y,u1z))
                u2x,u2y,u2z = self.p2.up
                veiw2.look(veiw2.eye-nn,Vector(u2x,-u2y,u2z))
                #veiw2.look(p2v,Vector(u2x,-u2y,u2z))
                glBindFramebuffer(GL_FRAMEBUFFER, self.f1)
                glClearColor(1, 0.5, 0, 1)
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)# // we're not using the stencil buffer now
                glEnable(GL_DEPTH_TEST)
                shader.set_view_matrix(veiw1.get_matrix(),veiw1.eye)
                shader.set_projection_matrix(projectionMatrixObj.get_matrix())#need to edit
                for obj in objects:
                    obj.draw(shader)
                self.ll.pDraw(shader,self.p2.id)
                self.p1.portal.texture=self.t1
                glBindFramebuffer(GL_FRAMEBUFFER,0)
                glBindFramebuffer(GL_FRAMEBUFFER, self.f2)
                glClearColor(0, 0.5, 1, 1)
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)# // we're not using the stencil buffer now
                glEnable(GL_DEPTH_TEST)
                shader.set_view_matrix(veiw2.get_matrix(),veiw2.eye)
                shader.set_projection_matrix(projectionMatrixObj.get_matrix())#need to edit
                for obj in objects:
                    obj.draw(shader)
                self.ll.pDraw(shader,self.p1.id)
                self.p2.portal.texture=self.t2
                glBindFramebuffer(GL_FRAMEBUFFER,0)

if __name__ == "__main__":
    from leveltest import *
    GraphicsProgram3D().start() 
                    
