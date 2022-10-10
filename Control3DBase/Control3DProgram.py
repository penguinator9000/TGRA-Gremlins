
# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time

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
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()
        self.model_matrix.load_identity()
        self.model_matrix.push_matrix()

        self.projection_view_matrix = ProjectionViewMatrix()
        self.projection_matrix = ProjectionMatrix()
        self.view_matrix = ViewMatrix()
        self.projection_view_matrix.new_proj_view((0,0,0),self.projection_matrix, self.view_matrix)
       


        self.shader.set_projection_view_matrix(self.projection_view_matrix.get_matrix())
        c = Cube()
        self.objects = [GraphicalObject(c),GraphicalObject(c,color =(1,0,1),pos=(2,0,-1))]
        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.UP_key_down = False  ## --- ADD CONTROLS FOR OTHER KEYS TO CONTROL THE CAMERA --- ##

        self.white_background = False

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time
        # if angle > 2 * pi:
        #     angle -= (2 * pi)
        if self.UP_key_down:
            self.white_background = True
        else:
            self.white_background = False
        self.model_matrix.pop_matrix()
        self.model_matrix.add_nothing()
    

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###
        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        glViewport(0, 0, 800, 600)

        

          ### --- ADD PROPER TRANSFORMATION OPERATIONS --- ###
        #self.model_matrix.load_identity()
       # self.model_matrix.add_translation(0,0,-3)
        for obj in self.objects:
            obj.draw(self.shader)


        self.model_matrix.push_matrix()

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

                elif event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        self.UP_key_down = False
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()