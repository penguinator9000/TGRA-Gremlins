
from OpenGL.GL import *
from math import * # trigonometry
import numpy as np

import sys

from Base3DObjects import *

class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc			= glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc			    = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)

        self.modelMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc	= glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")
        
        #self.colorLoc= glGetUniformLocation(self.renderingProgramID, "u_color")
        self.lightCouVerLoc			= glGetUniformLocation(self.renderingProgramID, "u_light_count_vert")
        self.lightCouFraLoc			= glGetUniformLocation(self.renderingProgramID, "u_light_count_frag")
        self.all_lights=[Light()]*10

        self.lightPosLoc			=[0]*10
        self.lightDifLoc			=[0]*10
        self.lightAmbLoc			=[0]*10
        self.lightSpeLoc			=[0]*10
        self.lightReach             =[0]*10
        
        for i in range(10): 
            self.lightPosLoc[i]			= glGetUniformLocation(self.renderingProgramID, "u_light_position["+str(i)+"]")
            self.lightDifLoc[i]			= glGetUniformLocation(self.renderingProgramID, "u_light_diffuse["+str(i)+"]")
            self.lightAmbLoc[i]			= glGetUniformLocation(self.renderingProgramID, "u_light_ambient["+str(i)+"]")
            self.lightSpeLoc[i]			= glGetUniformLocation(self.renderingProgramID, "u_light_specular["+str(i)+"]")
            self.lightReach[i]          = glGetUniformLocation(self.renderingProgramID, "u_light_reach["+str(i)+"]")   

        self.matDifLoc	            = glGetUniformLocation(self.renderingProgramID, "u_material_diffuse")
        self.matAmbLoc	            = glGetUniformLocation(self.renderingProgramID, "u_material_ambient")
        self.matSpeLoc	            = glGetUniformLocation(self.renderingProgramID, "u_material_specular")
        self.matShiLoc	            = glGetUniformLocation(self.renderingProgramID, "u_material_shiny")

        self.eyePosLoc              = glGetUniformLocation(self.renderingProgramID, "u_eye_position") 
        self.globalAmbiance         = glGetUniformLocation(self.renderingProgramID, "u_global_ambiance")    

        self.light2PosLoc			= glGetUniformLocation(self.renderingProgramID, "u_light2_position")
        self.light2DifLoc			= glGetUniformLocation(self.renderingProgramID, "u_light2_diffuse")
        self.light2AmbLoc			= glGetUniformLocation(self.renderingProgramID, "u_light2_ambient")
        self.light2SpeLoc			= glGetUniformLocation(self.renderingProgramID, "u_light2_specular")
        self.light2Reach            = glGetUniformLocation(self.renderingProgramID, "u_light2_reach")   
 


    def use(self):
        try:
            glUseProgram(self.renderingProgramID)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array,matrix_eye_pos):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)
        glUniform4f(self.eyePosLoc,matrix_eye_pos.x,matrix_eye_pos.y,matrix_eye_pos.z,1)

    def set_global_ambiance(self,r,g,b):
        glUniform4f(self.globalAmbiance,r,g,b,0)
    

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)
    
    #def set_solid_color(self,r,g,b):
    #    glUniform4f(self.colorLoc, r, g, b, 1.0)

    def set_lights(self,lights):
        
        L_lights=lights+[Light()]*(10-len(lights))
        count=min(10,len(lights))
        glUniform1f(self.lightCouVerLoc,count)
        glUniform1f(self.lightCouFraLoc,count)

        #np.array()?
        v=Vector(0,0,0)
        L_poss=[l.pos for l in L_lights]
        L_diffuses=[(l.color*l.diffuse) for l in L_lights]
        L_ambiances=[(l.color*l.ambiance) for l in L_lights]
        L_speculars=[(l.color*l.specular) for l in L_lights]
        L_reachs=[l.reach for l in L_lights]

        for i in range(count):
            l = self.all_lights[i]
            if L_poss[i] != l.pos:
                glUniform4f(self.lightPosLoc[i],L_poss[i].x,L_poss[i].y,L_poss[i].z,0)
            if L_diffuses[i] != (l.color*l.diffuse):
                glUniform4f(self.lightDifLoc[i],L_diffuses[i].r,L_diffuses[i].g,L_diffuses[i].b,L_diffuses[i].a)
            if L_ambiances[i] != (l.color*l.ambiance):
                glUniform4f(self.lightAmbLoc[i],L_ambiances[i].r,L_ambiances[i].g,L_ambiances[i].b,L_ambiances[i].a)
            if L_speculars[i] != (l.color*l.specular):
                glUniform4f(self.lightSpeLoc[i],L_speculars[i].r,L_speculars[i].g,L_speculars[i].b,L_speculars[i].a)
            if L_reachs[i] != l.reach:
                glUniform1f(self.lightReach[i],L_reachs[i])

        self.all_lights= L_lights




        
    


    def set_material_diffuse(self,r,g,b):
        glUniform4f(self.matDifLoc, r, g, b,0)
    
    def set_material_ambient(self,r,g,b):
        glUniform4f(self.matAmbLoc,r,g,b,0)

    def set_material_specular(self,r,g,b,shiny):
        glUniform4f(self.matSpeLoc,r,g,b,0)
        glUniform1f(self.matShiLoc,shiny)
    
    
    def set_light2_position(self,x,y,z):
        glUniform4f(self.light2PosLoc,x,y,z,1)
        
    def set_light2_diffuse(self,r,g,b):
        glUniform4f(self.light2DifLoc,r,g,b,0)
    
    def set_light2_ambient(self,r,g,b):
        glUniform4f(self.light2AmbLoc,r,g,b,0)
    
    def set_light2_specular(self,r,g,b):
        glUniform4f(self.light2SpeLoc,r,g,b,0)
    def set_light2_reach(self,reach):
        glUniform1f(self.light2Reach,reach)
    
