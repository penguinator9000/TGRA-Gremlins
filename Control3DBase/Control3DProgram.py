
# from OpenGL.GL import *
# from OpenGL.GLU import *
from ctypes import pointer
from math import *
from msilib.schema import Class
from shutil import move
from turtle import Screen, pos, position
import random

import pygame
from pygame.locals import *

import sys
import time
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
from Shaders import *
from Matrices import *

MAZE_Max=17
MAZE_ofset=1

import csv
global WIN
WIN=False

class GraphicalObject:
    def __init__(self, shape, size = (1,1,1),pos = (0,0,0), rotation =(0,0,0), color =(0.6,0.6,0.6) ):
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
        
    def draw(self, shader):
        shader.set_model_matrix(self.model_matrix.matrix)
        shader.set_solid_color(self.color[0],self.color[1],self.color[2])
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
        cpy = GraphicalObject(self.object,color=(self.color[0],self.color[1],self.color[2]))
        cpy.model_matrix.matrix = self.model_matrix.copy_matrix()
        return cpy
class BOI(GraphicalObject):
    boingPlaces = Vector(1,0,1)
    radius = Vector(0.25,0.25,0.25).__len__()
    spins = Vector(1,1.2,1.1)
    comboSpins = Vector(0,0,0)
    rgb = [0,0,0]
    def spinny(self, dtime):
        self.comboSpins += self.spins*dtime 
        self.model_matrix.add_rotation(sin(self.comboSpins.x),
                                        sin(self.comboSpins.y),
                                        sin(self.comboSpins.z))
        self.color = ((sin(self.comboSpins.x)+1)/2,
                                        (sin(self.comboSpins.y)+1)/2,
                                        (sin(self.comboSpins.z)+1)/2)
    def kill(self, playerPos):
        diff =  playerPos - self.pos
        if diff.x > -self.radius and diff.x < self.radius and diff.y > -self.radius and diff.y < self.radius:
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

class GraphicsProgram3D:
    def __init__(self):
        pygame.init() 
        pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        # self.model_matrix = ModelMatrix()
        # self.model_matrix.load_identity()
        # self.model_matrix.push_matrix()

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(fov=120,aspect=(SCREEN_WIDTH/SCREEN_HEIGHT),N=0.25,F=50)
        
        #self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 30)
        
        self.view_matrix = ViewMatrix()
        #self.projection_view_matrix.new_proj_view((0,0,0),self.projection_matrix, self.view_matrix)
        self.view_matrix.look(Point(0,0,-1),Vector(0,1,0))
        self.view_matrix.eye=Point(2+MAZE_ofset,0.5,2+MAZE_ofset)
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.view_matrix_3P = ViewMatrix()
        
        self.mini_map_projection_matrix = ProjectionMatrix()
        self.mini_map_projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 100)
        self.mini_map_view_matrix = ViewMatrix()
        self.mini_map_view_matrix.eye = Point(2+MAZE_ofset,3,2+MAZE_ofset)
        self.mini_map_view_matrix.look(self.view_matrix.eye,self.view_matrix.n)

        c = Cube()
        self.maze=[[None for i in range(MAZE_Max+1)] for ii in range(MAZE_Max+1)]
        self.mazeObjects =[]
        with open(sys.path[0] + "/maze.csv", 'r') as file:
            csvreader = csv.reader(file)
            first = True
            for row in csvreader:
                if first: first = False
                else:
                    x,z = [(int(val)) for val in row]
                    temp = GraphicalObject(c,pos=(x*2+MAZE_ofset,1,z*2+MAZE_ofset),size=(2,3,2),color=((x)/MAZE_Max,1-min(1,((x)/MAZE_Max+(z)/MAZE_Max)),(z)/MAZE_Max))
                    self.mazeObjects.append(temp)
                    self.maze[x][z]=temp

        self.Guy= GraphicalObject(D8(),color=(0,0.5,1))
        self.GuyRotation = 0
        self.GuyBop = 0
        self.Guy2= self.Guy.copy()
        self.Guy2update=[(1,1,1),(0,0,0),(0,pi/4,0),(0.5,0,1)]
        self.objects = [self.Guy,GraphicalObject(c,pos=(0,0,3)),GraphicalObject(c,color =(1,0,1),pos=(2,0,-1),size=(0.5,0.5,0.5)),GraphicalObject(Plane(),color=(0,1,0.5),pos=(0,-0.51,0),size=(1000,1,1000))]
        initialroatate = pi*1.25
        self.view_matrix.yaw(initialroatate)
        self.Guy.update(rotation=(0,-initialroatate,0))
        self.BOI = BOI(c,size=(0.5,0.5,0.5), color = (0.9,0.6,0.6))
        self.BOI.randomstart(self)
        self.objects.append(self.BOI)

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
            self.maze_collision(self.view_matrix.eye, self.movement)


        self.GuyRotation=self.GuyRotation%(pi*2)
        self.GuyBop += self.movement.__len__()
        bopSpeed=3
        self.GuyBop= self.GuyBop%(6.28/bopSpeed)
        bopy = (sin(self.GuyBop*bopSpeed-sin(self.GuyBop*bopSpeed/2))+1)/(16/(self.perspective_view+1)) 
        self.Guy.reset()
        self.Guy.update(rotation=(0,self.GuyRotation,0),pos=(self.view_matrix.eye.x,bopy,self.view_matrix.eye.z))
        
        self.mini_map_view_matrix.eye=self.view_matrix.eye
        self.mini_map_view_matrix.slide(delN=0.5)
        self.mini_map_view_matrix.look(self.view_matrix.eye,(self.view_matrix.n*(-1)))
        self.view_matrix_3P.eye=self.view_matrix.eye+(self.view_matrix.n*0.5)+(self.view_matrix.v*0.5)
        self.maze_collision(self.view_matrix_3P.eye, (self.view_matrix.n*0.5)+(self.view_matrix.v*0.5))
        self.view_matrix_3P.look(self.view_matrix.eye,Vector(0,1,0)+(self.view_matrix.n*(-0.01)))


        self.Guy2 = self.Guy.copy()
        self.Guy2.update(self.Guy2update[0],self.Guy2update[1],self.Guy2update[2],self.Guy2update[3])


        boiWentVec = self.BOI.move(delta_time)
        collided = self.maze_collision(self.BOI.pos,boiWentVec,self.BOI.radius)
        print(self.BOI.pos)
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
        if self.BOI.kill(self.view_matrix.eye): 
            self.view_matrix.eye.x = 3
            self.view_matrix.eye.z = 3
        if self.query_maze(int(self.BOI.pos.x//2),int(self.BOI.pos.z//2)) == 0:
            self.BOI.randomstart(self)
        if self.query_maze(int(self.view_matrix.eye.x//2),int(self.view_matrix.eye.z//2)) == 0:
            global WIN
            WIN=True
            return True
        return False 
        

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###
        
        glViewport(int(SCREEN_WIDTH-SCREEN_HEIGHT/4)-5, int(SCREEN_HEIGHT-SCREEN_HEIGHT/4)-5, int(SCREEN_HEIGHT/4), int(SCREEN_HEIGHT/4))
        self.shader.set_view_matrix(self.mini_map_view_matrix.get_matrix())
        self.shader.set_projection_matrix(self.mini_map_projection_matrix.get_matrix())
        for obj in self.objects:
            obj.draw(self.shader)
        for obj in self.mazeObjects:
            obj.draw(self.shader)
        self.Guy2.draw(self.shader)
        
        glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        if self.perspective_view == 1:
            self.shader.set_view_matrix(self.view_matrix_3P.get_matrix())
        elif self.perspective_view==2:
            self.shader.set_view_matrix(self.mini_map_view_matrix.get_matrix())
        else:
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        for obj in self.objects:
            obj.draw(self.shader)
        for obj in self.mazeObjects:
            obj.draw(self.shader)
        self.Guy2.draw(self.shader)
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
            return self.maze[x][z]
        else:
            return 0
    
    def maze_collision(self,pNow,vector, rad = 0):
        """The point is were you want to be vector is how you got there"""
        pWas = pNow+(vector*(-1))
        X= int(pWas.x//2)
        Z= int(pWas.z//2)
        #leeway = 0.25
        if not rad:
            rad = Vector(self.projection_matrix.near,self.projection_matrix.top,self.projection_matrix.right).__len__()
        
        if vector.x<0: vx=-1
        elif vector.x>0: vx=1
        else: vx=0
        #XL = int((pWas.x+vx*leeway)//2)
        XR = int((pWas.x+vx*rad)//2)
        XV = int((pNow.x+vx*rad)//2)
        xtru = XR == XV or True

        if vector.z<0: vz=-1
        elif vector.z>0: vz=1
        else: vz=0
        #ZL = int((pWas.z+vz*leeway)//2)
        ZR = int((pWas.z+vz*rad)//2)
        ZV = int((pNow.z+vz*rad)//2)
        ztru = ZR == ZV or True

        #print("cam here ",pNow)
        #print("index: ",X,Z)
        #print(self.query_maze(X,Z))
        quacko = None
        didcolision=False
        if xtru:
            q = self.query_maze(XV,Z)
            if q:
                #print("Collision x at ",XV,Z,q)
                #print("q.pos",q.pos,"pNow.x",pNow.x)
                pNow.x = q.pos.x + q.size.x*(-vx)*(0.5) + rad*(-vx)
                didcolision=True
                quacko = q

                #print("q.pos",q.pos,"pNow.x",pNow.x)
                
                
        if ztru:
            q = self.query_maze(X,ZV)
            if q:
                #print("Collision z at ", X, ZV,q)
                #print("q.pos",q.pos,"pNow.z",pNow.z)
                pNow.z = q.pos.z + q.size.z*(-vz)*(0.5) + rad*(-vz)
                didcolision=True
                #print("q.pos",q.pos,"pNow.z",pNow.z)
                quacko = q
    
                
    
        if not didcolision:
            q = self.query_maze(XV,ZV)
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
    while WIN:
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

