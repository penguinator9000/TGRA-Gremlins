
from math import *


from Base3DObjects import *

class ModelMatrix:
    def __init__(self):
        self.matrix = [ 1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1 ]
        self.stack = []
        self.stack_count = 0
        self.stack_capacity = 0

    def load_identity(self):
        self.matrix = [ 1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1 ]

    def copy_matrix(self):
        new_matrix = [0] * 16
        for i in range(16):
            new_matrix[i] = self.matrix[i]
        return new_matrix

    def add_transformation(self, matrix2):
        counter = 0
        new_matrix = [0] * 16
        for row in range(4):
            for col in range(4):
                for i in range(4):
                    new_matrix[counter] += self.matrix[row*4 + i]*matrix2[col + 4*i]
                counter += 1
        self.matrix = new_matrix

    def add_nothing(self):
        other_matrix = [1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    ## MAKE OPERATIONS TO ADD TRANLATIONS, SCALES AND ROTATIONS ##
    # ---

    def add_translation(self,x=0,y=0,z=0):
        if (x != 0 or y != 0 or z !=0 ):
            other_matrix = [1, 0, 0, x,
                            0, 1, 0, y,
                            0, 0, 1, z,
                            0, 0, 0, 1]
            self.add_transformation(other_matrix)
    
    def add_scale(self,x=1,y=1,z=1):
        if (x != 1 or y != 1 or z !=1 ):
            other_matrix = [x, 0, 0, 0,
                            0, y, 0, 0,
                            0, 0, z, 0,
                            0, 0, 0, 1]
            self.add_transformation(other_matrix)
    
    def add_rotation(self,xt=0,yt=0,zt=0):
        """rotation(radians) function were 
        xt= angle in were x is stationary
        yt= angle in were y is stationary
        zt= angle in were z is stationary """
        if xt:
            cxt=math.cos(xt)
            sxt=math.sin(xt)
            xMatrix =      [1, 0, 0, 0,
                            0, cxt, sxt, 0,
                            0, -sxt, cxt, 0,
                            0, 0, 0, 1]
            self.add_transformation(xMatrix)
        if yt:
            cyt=math.cos(yt)
            syt=math.sin(yt)
            yMatrix =      [cyt, 0, -syt, 0,
                            0, 1, 0, 0,
                            syt, 0, cyt, 0,
                            0, 0, 0, 1]
            self.add_transformation(yMatrix)
        if zt:
            czt=math.cos(zt)
            szt=math.sin(zt)
            zMatrix =      [czt, szt, 0, 0,
                            -szt, czt, 0, 0,
                            0, 0, 1, 0,
                            0, 0, 0, 1]
            self.add_transformation(zMatrix)
    

    # YOU CAN TRY TO MAKE PUSH AND POP (AND COPY) LESS DEPENDANT ON GARBAGE COLLECTION
    # THAT CAN FIX SMOOTHNESS ISSUES ON SOME COMPUTERS
    def push_matrix(self):
        self.stack.append(self.copy_matrix())

    def pop_matrix(self):
        self.matrix = self.stack.pop()

    # This operation mainly for debugging
    def __str__(self):
        ret_str = ""
        counter = 0
        for _ in range(4):
            ret_str += "["
            for _ in range(4):
                ret_str += " " + str(self.matrix[counter]) + " "
                counter += 1
            ret_str += "]\n"
        return ret_str



# The ViewMatrix class holds the camera's coordinate frame and
# set's up a transformation concerning the camera's position
# and orientation

class ViewMatrix:
    def __init__(self):
        self.eye = Point(0, 0, 0)
        self.u = Vector(1, 0, 0)
        self.v = Vector(0, 1, 0)
        self.n = Vector(0, 0, 1)
        self.up = Vector(0, 1, 0)

    ## MAKE OPERATIONS TO ADD LOOK, SLIDE, PITCH, YAW and ROLL ##
    # ---
    def look(self,lookpoint,up):
        self.up = up
        self.n = self.eye - lookpoint
        self.n.normalize()
        self.u = up.cross(self.n)
        self.u.normalize()
        self.v = self.n.cross(self.u)
        self.v.normalize()

    def slide(self, delU=0, delV=0, delN=0):
        self.eye += self.u * delU + self.v * delV + self.n * delN
        return self.u * delU + self.v * delV + self.n * delN

    def roll(self,angle):
        """we use radians!!!"""
        angCos = cos(angle)
        angSin = sin(angle)
        newU=self.u*angCos+self.v*angSin
        newV=self.u*(-angSin)+self.v*angCos
        self.u=newU
        self.v=newV  
    
    def pitch(self,angle):
        """we use radians!!!"""
        angCos = cos(angle)
        angSin = sin(angle)
        newN=self.n*angCos+self.v*angSin
        newV=self.n*(-angSin)+self.v*angCos
        print(angle,newN,newV)
        self.v=newV
        self.n=newN

    def yaw(self,angle):
        """we use radians!!!"""
        angCos = cos(angle)
        angSin = sin(angle)
        newN=self.n*angCos+self.u*angSin
        newU=self.n*(-angSin)+self.u*angCos
        self.n=newN
        self.u=newU
        

    def get_matrix(self):
        minusEye = Vector(-self.eye.x, -self.eye.y, -self.eye.z)
        return [self.u.x, self.u.y, self.u.z, minusEye.dot(self.u),
                self.v.x, self.v.y, self.v.z, minusEye.dot(self.v),
                self.n.x, self.n.y, self.n.z, minusEye.dot(self.n),
                0,        0,        0,        1]


# The ProjectionMatrix class builds transformations concerning
# the camera's "lens"

class ProjectionMatrix:
    def __init__(self):
        self.left = -1
        self.right = 1
        self.bottom = -1
        self.top = 1
        self.near = -1
        self.far = 1

        self.is_orthographic = True

    ## MAKE OPERATION TO SET PERSPECTIVE PROJECTION (don't forget to set is_orthographic to False) ##
    # ---
    def set_perspective(self,fov,aspect,N,F):
        self.is_orthographic = False
        self.top = N*tan((fov * (pi / 180.0))/2)
        self.bottom -self.top
        self.right=self.top*aspect
        self.left=-self.right
        self.near = N
        self.far = F
        

    def set_orthographic(self, left, right, bottom, top, near, far):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.near = near
        self.far = far
        self.is_orthographic = True

    def get_matrix(self):
        if self.is_orthographic:
            A = 2 / (self.right - self.left)
            B = -(self.right + self.left) / (self.right - self.left)
            C = 2 / (self.top - self.bottom)
            D = -(self.top + self.bottom) / (self.top - self.bottom)
            E = 2 / (self.near - self.far)
            F = (self.near + self.far) / (self.near - self.far)

            return [A,0,0,B,
                    0,C,0,D,
                    0,0,E,F,
                    0,0,0,1]

        else:
            A = (2*self.near) / (self.right - self.left)
            B = (self.right + self.left) / (self.right - self.left)
            C = (2*self.near) / (self.top - self.bottom)
            D = (self.top + self.bottom) / (self.top - self.bottom)
            E = -(self.far + self.near) / (self.far - self.near)
            F = -(2 * self.far * self.near) / (self.far - self.near)
            return [A,0,B, 0,
                    0,C,D, 0,
                    0,0,E, F,
                    0,0,-1,0]



# The ProjectionViewMatrix returns a hardcoded matrix
# that is just used to get something to send to the
# shader before you properly implement the ViewMatrix
# and ProjectionMatrix classes.
# Feel free to throw it away afterwards!

class ProjectionViewMatrix:
    def __init__(self):
        self.matrix = [ 0.45052942369783683,  0.0,  -0.15017647456594563,  0.0,
                -0.10435451285616304,  0.5217725642808152,  -0.3130635385684891,  0.0,
                -0.2953940042189954,  -0.5907880084379908,  -0.8861820126569863,  3.082884480118567,
                -0.2672612419124244,  -0.5345224838248488,  -0.8017837257372732,  3.7416573867739413 ]

    def get_matrix(self):
        return self.matrix
    # def add_transformation(self, matrix2):
    #     counter = 0
    #     new_matrix = [0] * 16
    #     for row in range(4):
    #         for col in range(4):
    #             for i in range(4):
    #                 new_matrix[counter] += self.matrix[row*4 + i]*matrix2[col + 4*i]
    #             counter += 1
    #     self.matrix = new_matrix
    # def new_proj_view(self, pos, projection, view):
    #     self.matrix =  [1, 0, 0, pos[0],
    #                     0, 1, 0, pos[1],
    #                     0, 0, 1, pos[2],
    #                     0, 0, 0, 1]
    #     self.add_transformation(view.get_matrix())
    #     self.add_transformation(projection.get_matrix())

# IDEAS FOR OPERATIONS AND TESTING:
# if __name__ == "__main__":
#     matrix = ModelMatrix()
#     matrix.push_matrix()
#     print(matrix)
#     matrix.add_translation(3, 1, 2)
#     matrix.push_matrix()
#     print(matrix)
#     matrix.add_scale(2, 3, 4)
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
    
#     matrix.add_translation(5, 5, 5)
#     matrix.push_matrix()
#     print(matrix)
#     matrix.add_scale(3, 2, 3)
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
    
#     matrix.pop_matrix()
#     print(matrix)
        
#     matrix.push_matrix()
#     matrix.add_scale(2, 2, 2)
#     print(matrix)
#     matrix.push_matrix()
#     matrix.add_translation(3, 3, 3)
#     print(matrix)
#     matrix.push_matrix()
#     matrix.add_rotation_y(pi / 3)
#     print(matrix)
#     matrix.push_matrix()
#     matrix.add_translation(1, 1, 1)
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
    
