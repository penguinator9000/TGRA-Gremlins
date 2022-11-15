
# from OpenGL.GL import *
# from OpenGL.GLU import *
from ctypes import pointer
from math import *
from msilib.schema import Class
from shutil import move
from turtle import Screen, color, pos, position
import random

import pygame
from pygame.locals import *

from levelloader import LevelLoader
import sys
import time
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
from Shaders import *
from Matrices import *
from Complex3DObjects import *

MAZE_Max=17
MAZE_ofset=1

import csv
global WIN
WIN=False



class GraphicsProgram3D:
    def __init__(self):
        # B=BayesianCurve4P(p1 = Point(15, 2.75, 2), p2 = Point(10, 2.5, 2), p3 = Point(5, 2, 2), p4 = Point(0, 2.3, 2))
        
        # L=LoopBayesianCurves4P(B,4)
        # L.ControlePoints[0]=L.ControlePoints[0]*(0.125)
        # L.ControlePoints[1]=L.ControlePoints[1]*(0.125)
        # L.ControlePoints[9]=L.ControlePoints[9]*(8)
        
        # L.BuildFromControle()

        pygame.init() 
        pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()
        self.shader.set_global_ambiance(0.4,0.4,0.4)

        # self.model_matrix = ModelMatrix()
        # self.model_matrix.load_identity()
        # self.model_matrix.push_matrix()

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(fov=120,aspect=(SCREEN_WIDTH/SCREEN_HEIGHT),N=0.25,F=50)
        self.light1 = Light(Point(6,10,6),Color(0.9,0.9,0.9),reach= 12, ambiance=Color(0.2,0.2,0.2))
        self.light2 = Light(Point(2,2,2),diffuse=Color(0.5,0,0), ambiance=Color(0.1,0.1,0.1),specular=Color(0.8,0,0.8),reach = 5)
        #self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 30)
        
        self.view_matrix = ViewMatrix()
        #self.projection_view_matrix.new_proj_view((0,0,0),self.projection_matrix, self.view_matrix)
        self.view_matrix.look(Point(0,0,-1),Vector(0,1,0))
        self.view_matrix.eye=Point(2+MAZE_ofset,0.5,2+MAZE_ofset)
        self.shader.set_view_matrix(self.view_matrix.get_matrix(),self.view_matrix.eye)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        
        self.shader.set_material_specular(0.2,0.2,0.2,1)

        self.view_matrix_3P = ViewMatrix()
        
        self.mini_map_projection_matrix = ProjectionMatrix()
        self.mini_map_projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 100)
        self.mini_map_view_matrix = ViewMatrix()
        self.mini_map_view_matrix.eye = Point(2+MAZE_ofset,3,2+MAZE_ofset)
        self.mini_map_view_matrix.look(self.view_matrix.eye,self.view_matrix.n)

        c = Cube()
        self.ll = LevelLoader(sys.path[0]+"/levels")
        self.ll.load("buttons")
        self.portalLink = PortalLink(self.ll)
        self.portalLink.update("reset","1","2")


        self.Guy= GraphicalObject(D8(),color=Color(0,0.5,1))
        self.Guy.ambiance = Color(0.7,0.7,0.7)
        self.GuyRotation = 0
        self.GuyBop = 0
        self.Guy2= self.Guy.copy()
        self.Guy2update=[(0.75,0.75,0.75),(0,0.25,0),(0,0,0),Color(0.5,0,1)]
        p= GraphicalObject(Plane(),color=Color(0,1,0.5),pos=(0,-0.51,0),size=(1000,1,1000))
        p.ambiance=Color(1,1,1)
        self.objects = [GraphicalObject(c,pos=(0,0,3)),GraphicalObject(c,color =Color(1,0,1),pos=(2,0,-1),size=(0.5,0.5,0.5)),p]
        initialroatate = pi*1.25
        self.view_matrix.yaw(initialroatate)
        self.Guy.update(rotation=(0,-initialroatate,0))
        self.BOI = BOI(c,size=(0.5,0.5,0.5), color = Color(0.9,0.6,0.6))
        #self.BOI.randomstart(self)
        self.objects.append(self.BOI)
        #meshTest=Mesh(2,60,Point(3,-100,3),Color(1,0,0),"2")
        #meshTest.PointMatrix=[[Point(m/10+3,L[m/10+n/3].y-2.5, n+2) for m in range(60) ] for n in [1,2]]

        
        #self.objects.append(meshTest)

        '''
        for i in range(20):
            self.objects.append(GraphicalObject(c,pos=(i-(i%2),0,i-((i+1)%2)),size=(1,3,1)))
        '''
        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.perspective_max=2
        self.perspective_view=0

        ## --- ADD CONTROLS FOR OTHER KEYS TO CONTROL THE CAMERA --- ##
        self.UP_key_down = False  
        self.DOWN_key_down = False
        self.RIGHT_key_down = False
        self.LEFT_key_down = False

        self.w_key_down = False
        self.a_key_down = False
        self.s_key_down = False
        self.d_key_down = False

        self.q_key_down = False
        self.e_key_down = False
        self.r_key_down = False
        self.f_key_down = False


    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.movement=Vector(0,0,0)
        
        if self.q_key_down:
            self.view_matrix.yaw(delta_time)
            self.GuyRotation+=-delta_time
            
        if self.e_key_down:
            self.view_matrix.yaw(-delta_time)
            self.GuyRotation+=delta_time
            
        if self.w_key_down:
            self.movement+=self.view_matrix.slide(delN=-delta_time*2)
        
        if self.s_key_down:
            self.movement+=self.view_matrix.slide(delN=delta_time*2)
        
        if self.a_key_down:
            self.movement+=self.view_matrix.slide(delU=-delta_time*2)
        
        if self.d_key_down:
            self.movement+=self.view_matrix.slide(delU=delta_time*2)
        
        if self.movement!=Vector(0,0,0):
            pass
            self.maze_collision(self.view_matrix.eye, self.movement)


        self.GuyRotation=self.GuyRotation%(pi*2)
        self.GuyBop += self.movement.__len__()
        bopSpeed=3
        self.GuyBop= self.GuyBop%(6.28/bopSpeed)
        bopy = (sin(self.GuyBop*bopSpeed-sin(self.GuyBop*bopSpeed/2))+1)/(16/(self.perspective_view+1)) 
        self.Guy.reset()
        self.Guy.update(rotation=(0,self.GuyRotation,0),pos=(self.view_matrix.eye.x,bopy,self.view_matrix.eye.z))
        if self.perspective_view==0:
            self.view_matrix.eye.y=bopy+0.5
        self.mini_map_view_matrix.eye=self.view_matrix.eye
        self.mini_map_view_matrix.slide(delN=0.5)
        self.mini_map_view_matrix.look(self.view_matrix.eye,(self.view_matrix.n*(-1)))
        self.view_matrix_3P.eye=self.view_matrix.eye+(self.view_matrix.n*0.5)+(self.view_matrix.v*0.5)
        self.maze_collision(self.view_matrix_3P.eye, (self.view_matrix.n*0.5)+(self.view_matrix.v*0.5))
        self.view_matrix_3P.look(self.view_matrix.eye,Vector(0,1,0)+(self.view_matrix.n*(-0.01)))


        self.Guy2 = self.Guy.copy()
        self.Guy2.update(self.Guy2update[0],self.Guy2update[1],self.Guy2update[2],self.Guy2update[3])

        self.light1.pos= Point( self.view_matrix.eye.x ,self.view_matrix.eye.y+2 ,self.view_matrix.eye.z)

        boiWentVec = self.BOI.move(delta_time)
        collided = self.maze_collision(self.BOI.pos,boiWentVec,self.BOI.radius)
        #print(self.BOI.pos)
        if collided:
            self.BOI.moveTo(self.BOI.pos.x,self.BOI.pos.z)
            boiWentVec.normalize()
            # side = q.pos-pNow + (vector*rad)
            #print(collided.pos)
            side = collided.pos-self.BOI.pos + (boiWentVec*self.BOI.radius)
            if abs(side.x) < abs(side.z):
                self.BOI.reflect(Vector(1,0,0))
                #print("x",self.BOI.boingPlaces,side)
            else:
                self.BOI.reflect(Vector(0,0,1))
        self.BOI.spinny(delta_time)
        if self.BOI.kill(self.view_matrix.eye,self.projection_matrix): 
            self.view_matrix.eye.x = 3
            self.view_matrix.eye.z = 3
            pass
        if self.ll.queryLevel(int(self.BOI.pos.x),int(self.BOI.pos.z)) == 0:
            self.BOI.randomstart(self)
        if self.ll.queryLevel(int(self.view_matrix.eye.x),int(self.view_matrix.eye.z//2)) == 0:
            global WIN
            WIN=True
            #return True
        self.light2.pos= Point( self.BOI.pos.x,self.BOI.pos.y+0.5,self.BOI.pos.z)

        return False 
        
        

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###
        
        glClearColor(0.05, 0.0, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###
        
        glViewport(int(SCREEN_WIDTH-SCREEN_HEIGHT/4)-5, int(SCREEN_HEIGHT-SCREEN_HEIGHT/4)-5, int(SCREEN_HEIGHT/4), int(SCREEN_HEIGHT/4))

        self.shader.set_lights([self.light1,self.light2])

        self.shader.set_view_matrix(self.mini_map_view_matrix.get_matrix(),self.mini_map_view_matrix.eye)
        self.shader.set_projection_matrix(self.mini_map_projection_matrix.get_matrix())

        for obj in self.objects:
            obj.draw(self.shader)
        self.ll.draw(self.shader)
        #for obj in self.mazeObjects:
        #    obj.draw(self.shader)
        self.Guy2.draw(self.shader)
        self.Guy.draw(self.shader)
        
        glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        if self.perspective_view == 1:
            self.shader.set_view_matrix(self.view_matrix_3P.get_matrix(),self.view_matrix_3P.eye)
            self.Guy.draw(self.shader)
            self.Guy2.draw(self.shader)
        elif self.perspective_view==2:
            self.shader.set_view_matrix(self.mini_map_view_matrix.get_matrix(),self.mini_map_view_matrix.eye)
            self.Guy.draw(self.shader)
            self.Guy2.draw(self.shader)
        else:
            self.shader.set_view_matrix(self.view_matrix.get_matrix(),self.view_matrix.eye)
            
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        for obj in self.objects:
            obj.draw(self.shader)
        self.ll.draw(self.shader)
        #for obj in self.mazeObjects:
        #    obj.draw(self.shader)
       
        pygame.display.flip()
        

    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True

                    if event.key == K_SPACE:
                        self.perspective_view = (self.perspective_view+1)%self.perspective_max 
                    if event.key == K_UP:
                        self.UP_key_down = True
                    if event.key == K_DOWN: 
                        self.DOWN_key_down = True
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = True
                    if event.key == K_LEFT:
                        self.LEFT_key_down = True
                    if event.key == K_w:
                        self.w_key_down = True
                    if event.key == K_a:
                        self.a_key_down = True
                    if event.key == K_s:
                        self.s_key_down = True
                    if event.key == K_d:
                        self.d_key_down = True
                    if event.key == K_q:
                        self.q_key_down = True
                    if event.key == K_e:
                        self.e_key_down = True
                    if event.key == K_r:
                        self.r_key_down = True
                    if event.key == K_f:
                        self.f_key_down = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        self.UP_key_down = False
                    if event.key == K_DOWN: 
                        self.DOWN_key_down = False
                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = False
                    if event.key == K_LEFT:
                        self.LEFT_key_down = False
                    if event.key == K_w:
                        self.w_key_down = False
                    if event.key == K_a:
                        self.a_key_down = False
                    if event.key == K_s:
                        self.s_key_down = False
                    if event.key == K_d:
                        self.d_key_down = False
                    if event.key == K_q:
                        self.q_key_down = False
                    if event.key == K_e:
                        self.e_key_down = False
                    if event.key == K_r:
                        self.r_key_down = False
                    if event.key == K_f:
                        self.f_key_down = False
            if not exiting:
                exiting = self.update()
                self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()
    
    def query_maze(self,x,z):
        R=range(0,MAZE_Max+1)
        if x in R and z in R:
            pass
            #return self.maze[x][z]
        else:
            return 0
    
    def maze_collision(self,pNow,vector, rad = 0):
        """The point is were you want to be vector is how you got there"""
        pWas = pNow+(vector*(-1))
        X= int(pWas.x)
        Z= int(pWas.z)
        #leeway = 0.25
        if not rad:
            rad = Vector(self.projection_matrix.near,self.projection_matrix.top,self.projection_matrix.right).__len__()
        
        if vector.x<0: vx=-1
        elif vector.x>0: vx=1
        else: vx=0
        #XL = int((pWas.x+vx*leeway)//2)
        XR = int((pWas.x+vx*rad))
        XV = int((pNow.x+vx*rad))
        xtru = XR == XV or True

        if vector.z<0: vz=-1
        elif vector.z>0: vz=1
        else: vz=0
        #ZL = int((pWas.z+vz*leeway)//2)
        ZR = int((pWas.z+vz*rad))
        ZV = int((pNow.z+vz*rad))
        ztru = ZR == ZV or True

        #print("cam here ",pNow)
        #print("index: ",X,Z)
        #print(self.query_maze(X,Z))
        quacko = None
        didcolision=False
        if xtru:
            q = self.ll.queryLevel(XV,Z)
            if q:
                #print("Collision x at ",XV,Z,q)
                #print("q.pos",q.pos,"pNow.x",pNow.x)
                pNow.x = q.pos.x + q.size.x*(-vx)*(0.5) + rad*(-vx)
                didcolision=True
                quacko = q

                #print("q.pos",q.pos,"pNow.x",pNow.x)
                
                
        if ztru:
            q = self.ll.queryLevel(X,ZV)
            if q:
                #print("Collision z at ", X, ZV,q)
                #print("q.pos",q.pos,"pNow.z",pNow.z)
                pNow.z = q.pos.z + q.size.z*(-vz)*(0.5) + rad*(-vz)
                didcolision=True
                #print("q.pos",q.pos,"pNow.z",pNow.z)
                quacko = q
    
                
    
        if not didcolision:
            q = self.ll.queryLevel(XV,ZV)
            if q:
                #print("Collision xz at ", XV, ZV,q)
                vector.normalize()
                side = q.pos-pNow + (vector*rad)
                if not quacko:
                    quacko = q
                if side.x >= side.z:
                    pNow.x = q.pos.x + q.size.x*(-vx)*(0.5) + rad*(-vx)
                else:
                    pNow.z = q.pos.z + q.size.z*(-vz)*(0.5) + rad*(-vz)
        return quacko


                
        ''' 
        ret = []
            if vx and vz:
            for t in [(X+vx,Z+vz),(X,Z+vz),(X+vx)]:
                q = self.query_maze(t[0],t[1])
                if q:
                    ret.append(q)
        else:
            q = self.query_maze(X+vx,Z+vz)
            if q:
                ret.append(q)
        return ret'''
   

            




if __name__ == "__main__":
    GraphicsProgram3D().start()
    if WIN:
        amazing="""    _             _ _ _ 
     /\                                   (_)           | | | |
    /  \   _ __ ___   __ _  __ _  __ _ _____ _ __   __ _| | | |
   / /\ \ | '_ ` _ \ / _` |/ _` |/ _` |_  / | '_ \ / _` | | | |
  / ____ \| | | | | | (_| | (_| | (_| |/ /| | | | | (_| |_|_|_|
 /_/    \_\_| |_| |_|\__,_|\__,_|\__,_/___|_|_| |_|\__, (_|_|_)
                                                    __/ |      
                                                   |___/"""
        print('WOOOOOW you made it out of the maaaaze',amazing)
    if not WIN:
        over = """   _____                         ____                 
  / ____|                       / __ \                
 | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ 
 | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|
 | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   
  \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|"""
        print(over)

