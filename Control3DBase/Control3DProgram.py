
# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *
from turtle import Screen

import pygame
from pygame.locals import *

import sys
import time
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
from Shaders import *
from Matrices import *

class GraphicalObject:
    def __init__(self, shape, size = (1,1,1),pos = (0,0,0), rotation =(0,0,0), color =(0.6,0.6,0.6) ):
        self.object = shape
        self.model_matrix = ModelMatrix()
        self.model_matrix.load_identity()
        self.model_matrix.add_scale(size[0],size[1],size[2])
        self.model_matrix.add_translation(pos[0],pos[1],pos[2])
        self.model_matrix.add_rotation(rotation[0],rotation[1],rotation[2])
        self.model_matrix.push_matrix()
        self.color = color
        
    def draw(self, shader):
        shader.set_model_matrix(self.model_matrix.matrix)
        shader.set_solid_color(self.color[0],self.color[1],self.color[2])
        self.object.draw(shader)
    def update(self, size = 0 ,pos = 0, rotation =0, color =0):
        if color: self.color = color 
        if size:
            self.model_matrix.add_scale(size[0],size[1],size[2])
        if pos:
            self.model_matrix.add_translation(pos[0],pos[1],pos[2])
        if rotation:
            self.model_matrix.add_rotation(rotation[0],rotation[1],rotation[2])
    def reset(self):
        self.model_matrix.pop_matrix()
        self.model_matrix.push_matrix()
    def copy(self):
        cpy = GraphicalObject(self.object,color=(self.color[0],self.color[1],self.color[2]))
        cpy.model_matrix.matrix = self.model_matrix.copy_matrix()
        return cpy
        

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
        self.projection_matrix.set_perspective(fov=90,aspect=(SCREEN_WIDTH/SCREEN_HEIGHT),N=0.5,F=100)
        
        #self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 30)
        
        self.view_matrix = ViewMatrix()
        #self.projection_view_matrix.new_proj_view((0,0,0),self.projection_matrix, self.view_matrix)
       
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        
        self.mini_map_projection_matrix = ProjectionMatrix()
        self.mini_map_projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 30)
        self.mini_map_view_matrix = ViewMatrix()
        self.mini_map_view_matrix.eye = Point(0,3,0)
        self.mini_map_view_matrix.look(self.view_matrix.eye,self.view_matrix.n)

        c = Cube()
        self.Guy= GraphicalObject(D8(),color=(0,0.5,1))
        self.objects = [self.Guy,GraphicalObject(c,pos=(0,0,3)),GraphicalObject(c,color =(1,0,1),pos=(2,0,-1),size=(0.5,0.5,0.5)),GraphicalObject(Plane(),color=(0,1,0.5),pos=(0,-0.5,0),size=(1000,1,1000))]
        
        self.clock = pygame.time.Clock()
        self.clock.tick()



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

        if self.q_key_down:
            self.view_matrix.yaw(delta_time)
            self.Guy.update(rotation=(0,-delta_time,0))
        if self.e_key_down:
            self.view_matrix.yaw(-delta_time)
            self.Guy.update(rotation=(0,delta_time,0))
        if self.w_key_down:
            self.view_matrix.slide(delN=-delta_time)
            self.Guy.update(pos=(0,0,-delta_time))
        if self.s_key_down:
            self.view_matrix.slide(delN=delta_time)
            self.Guy.update(pos=(0,0,delta_time))
        if self.a_key_down:
            self.view_matrix.slide(delU=-delta_time)
            self.Guy.update(pos=(-delta_time,0,0))
        if self.d_key_down:
            self.view_matrix.slide(delU=delta_time)
            self.Guy.update(pos=(delta_time,0,0))
            

        # if self.UP_key_down:
        #     self.view_matrix.pitch(delta_time)
        # if self.DOWN_key_down:
        #     self.view_matrix.pitch(-delta_time)
        # if self.LEFT_key_down:
        #     self.view_matrix.yaw(delta_time)
        # if self.RIGHT_key_down:
        #     self.view_matrix.yaw(-delta_time)
        # if self.w_key_down:
        #     self.view_matrix.slide(delN=-delta_time)
        # if self.s_key_down:
        #     self.view_matrix.slide(delN=delta_time)
        # if self.a_key_down:
        #     self.view_matrix.slide(delU=-delta_time)
        # if self.d_key_down:
        #     self.view_matrix.slide(delU=delta_time)
        # if self.q_key_down:
        #     self.view_matrix.roll(delta_time)
        # if self.e_key_down:
        #     self.view_matrix.roll(-delta_time)
        # if self.r_key_down:
        #     self.view_matrix.slide(delV=delta_time)
        # if self.f_key_down:
        #     self.view_matrix.slide(delV=-delta_time)
        
        self.mini_map_view_matrix.eye=self.view_matrix.eye
        self.mini_map_view_matrix.slide(delN=3)
        self.mini_map_view_matrix.look(self.view_matrix.eye,(self.view_matrix.n*(-1)))
        

        

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###
        pygame.display.gl_set_attribute(GL_DEPTH_SIZE,8)
        glViewport(int(SCREEN_WIDTH-SCREEN_HEIGHT/4), int(SCREEN_HEIGHT-SCREEN_HEIGHT/4), int(SCREEN_HEIGHT/4), int(SCREEN_HEIGHT/4))
        self.shader.set_view_matrix(self.mini_map_view_matrix.get_matrix())
        self.shader.set_projection_matrix(self.mini_map_projection_matrix.get_matrix())
        for obj in self.objects:
            obj.draw(self.shader)
        print(pygame.display.gl_get_attribute(GL_DEPTH_SIZE))


        pygame.display.gl_set_attribute(GL_DEPTH_SIZE,16)
        glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        print(pygame.display.gl_get_attribute(GL_DEPTH_SIZE))


          ### --- ADD PROPER TRANSFORMATION OPERATIONS --- ###
        #self.model_matrix.load_identity()
       # self.model_matrix.add_translation(0,0,-3)
        
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        for obj in self.objects:
            obj.draw(self.shader)
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
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()