
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
        self.lightPosLoc			= glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.lightDifLoc			= glGetUniformLocation(self.renderingProgramID, "u_light_diffuse")
        self.lightAmbLoc			= glGetUniformLocation(self.renderingProgramID, "u_light_ambient")
        self.lightSpeLoc			= glGetUniformLocation(self.renderingProgramID, "u_light_specular")
        self.lightReach             = glGetUniformLocation(self.renderingProgramID, "u_light_reach")   

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

    def set_lights(self,light):
        
        count=min(10,1)
        glUniform1f(self.lightCouVerLoc,count)
        glUniform1f(self.lightCouFraLoc,count)
        v=Vector(0,0,0)
        #np.array()?
        p=v+light.pos
        L_poss=(p.list()+[1.0])
        glUniform4f(self.lightPosLoc,L_poss[0],L_poss[1],L_poss[2],L_poss[3])
        
        L_diffuses=list((light.color*light.diffuse).rgba)
        glUniform4f(self.lightDifLoc,L_diffuses[0],L_diffuses[1],L_diffuses[2],L_diffuses[3])
        L_ambiances=list((light.color*light.ambiance).rgba)
        glUniform4f(self.lightAmbLoc,L_ambiances[0],L_ambiances[1],L_ambiances[2],L_ambiances[3])
        L_speculars=list((light.color*light.specular).rgba)
        glUniform4f(self.lightSpeLoc,L_speculars[0],L_speculars[1],L_speculars[2],L_speculars[3])

        L_reachs=light.reach
        glUniform1f(self.lightReach,L_reachs)




        
    


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
    
