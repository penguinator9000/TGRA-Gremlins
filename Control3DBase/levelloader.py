import csv
import json
import sys

from Complex3DObjects import *

def lerp(a,b,t):
    return (1-t)*a+t*b
class LevelLoader():
    def __init__(self,location):
        self.root = location
        self.levelDir = ""
        self.layout = None
        self.objects = None
        self.xSize = 1
        self.ySize = 2
        self.zSize = 1
        self.walls = []
    def validateLayouyt(self):
        count = 1
        if self.layout:
            if (len(self.layout) != self.yMax): 
                return False, "unexpected y values"
            for i in self.layout:
                if (len(i) != self.zMax):
                    return False, "unexpected z values expected "+ str(self.zMax)+ " got "+str(len(i))+" at line "+str(count)  
                for j in i:
                    count += 1
                    if (len(j) != self.xMax): 
                        print(j)
                        return False, "unexpected x values expected "+ str(self.xMax)+ " got "+str(len(j))+" at line "+str(count)
            return True, "Layout valid" 
        else: return False, "No layout"
    def load(self,levelDir):
        if self.levelDir == levelDir:
            return "already loaded"
        cube = Cube()
        self.levelDir = levelDir
        print(levelDir+"/layout.csv")
        with open(self.root+"/"+levelDir+"/layout.csv",'r') as layoutFile:
            csvreader = csv.reader(layoutFile)
            first = True
            ycount = 0
            zcount = 0
            
            for row in csvreader:
                if first: 
                    first =False
                    self.zMax,self.xMax,self.yMax = row
                    self.zMax = int(self.zMax)
                    self.xMax = int(self.xMax)
                    self.yMax = int(self.yMax)
                    self.layout = [[[]for j in range(self.zMax)] for i in range(self.yMax)]
                else:
                    wall = True
                    if self.zMax == zcount:
                        zcount = 0
                        ycount += 1
                    xcount = 0
                    for i in  row:
                        for j in range(int(i)):
                            toAppend = None
                            #print(ycount*self.ySize + self.ySize/2)
                            if wall: toAppend = GraphicalObject(cube,pos = (xcount*self.xSize + self.xSize/2,(ycount-1)*self.ySize + self.ySize/2,zcount*self.zSize+self.zSize/2), size =(self.xSize,self.ySize,self.zSize))
                            self.layout[ycount][zcount].append(toAppend) #exchange this for object at some point.
                            if toAppend:self.walls.append(toAppend)
                            xcount +=1
                        wall = not wall
                    zcount += 1
        valid, msg = self.validateLayouyt()
        print(msg)
        if(not valid): return False
        self.buttons = {}
        self.portals = {}
        self.smallWalls = {}
        self.objectList = []
        self.objectLevelreference = {}
        with open(self.root+"/"+levelDir+"/objects.json",'r') as objects:
            self.objects = json.load(objects)
        for id, dict in self.objects["buttons"].items():
            tmp = Button(id,dict,self.xSize,self.ySize,self.zSize)
            self.objectList.append(tmp)
            self.buttons[id] = tmp
            locationRef = (dict["box-x"],dict["box-y"],dict["box-z"])
            if locationRef not in self.objectLevelreference:
                self.objectLevelreference[locationRef] = [tmp]
            else: 
                self.objectLevelreference[locationRef].append(tmp)
        
        for id, dict in self.objects["portals"].items():
            tmp = Portal(id,dict,self.xSize,self.ySize,self.zSize)
            self.objectList.append(tmp)
            self.portals[id] = tmp
            
            locationRef = (dict["location"]["box-x"],dict["location"]["box-y"],dict["location"]["box-z"])
            if locationRef not in self.objectLevelreference:
                self.objectLevelreference[locationRef] = [tmp]
            else: 
                self.objectLevelreference[locationRef].append(tmp)

        for id, dict in self.objects["smallWalls"].items():
            tmp = SmallWall(id,dict,self.xSize,self.ySize,self.zSize)
            self.objectList.append(tmp)
            self.smallWalls[id] = tmp
            """
            #fix me fucked shit yaknow
            locationRef = (dict["box-x"],dict["box-y"],dict["box-z"])
            if locationRef not in self.objectLevelreference:
                self.objectLevelreference[locationRef] = [tmp]
            else: 
                self.objectLevelreference[locationRef].append(tmp)
            """

        return [self.layout, self.objects]
    def draw (self,shader):
        """
            Draws the entire level with all objects 
        """
        for i in self.walls:
            pass
            i.draw(shader)
        for obj in self.objectList:
            obj.draw(shader)
        
    def pDraw( self, portalId):
        """
            Draws the level in respect to the portal passed as so that a frame buffer can be made.
        """
        pass
    def queryLevel(self,x,z,y = 1):
        x = x//self.xSize
        z = z//self.zSize
        y = (y+2)//self.ySize
        if x >= self.xMax or x < 0: return 0
        if z >= self.zMax or z < 0: return 0 
        return self.layout[y][z][x]
        """
            Query the level returning wether the point is above floor colliding with a wall or
        """
        return 
    def queryObjects(self,x,y,z):
        x = x//self.xSize
        z = z//self.zSize
        y = (y+2)//self.ySize
        """
            Query the level and return any objects found to inhibit that cell
        
        """
        try: return self.objectLevelreference[(x,y,z)]
        except: return None
    
    def changeRoot(self,location):
        self.root = location
        #maybe clear data later. also function might be useless
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
        self.xpos = self.cordCalcs(button_dict["box-x"],xSize,button_dict['placement']["x-offset"])
        self.ypos = button_dict["box-y"]*ySize+self.height/2
        self.zpos = self.cordCalcs(button_dict["box-z"],zSize,button_dict['placement']["z-offset"])
        self.actions = button_dict['action']
        self.colors = button_dict['color']
        self.pillar = GraphicalObject(Cube(),size = (buttonsize,self.height,buttonsize),pos=(self.xpos,self.ypos,self.zpos),color=(0.5,0.2,0.5))
        self.button = GraphicalObject(Cube(),size=(buttonsize*0.7,0.045,buttonsize*0.7),pos=(self.xpos,self.ypos+self.height/2,self.zpos),color=(0.1,0.6,0.6),rotation=(0,45,0) )
        #print(button_dict["box-x"],button_dict["box-y"],button_dict["box-z"])
        #print(self.xpos,self.ypos,self.zpos)

    def press(self):
        pass
    def nullState(self):
        pass
    def draw(self,shader):
        self.pillar.draw(shader)
        self.button.draw(shader)
class Portal:
    def __init__(self,id, portalDict,xSize,ySize,zSize):
        r =1.57079633
        offset = 0.01
        self.active = Falses
        self.id = id
        self.direction = portalDict["location"]["direction"]
        xd,yd,zd = self.direction
        self.up = portalDict['location']['up']
        x = portalDict["location"]["box-x"]
        y = portalDict["location"]["box-y"]
        z = portalDict["location"]["box-z"]
        self.xpos = x*xSize+xSize/2 + xd*(xSize+offset)/2
        self.ypos = (y-1)*ySize+ySize/2+ yd*(ySize+offset)/2
        self.zpos = z*zSize+zSize/2 + zd*(zSize+offset)/2
        print(self.xpos,self.ypos,self.zpos)
        rot = (r*xd,0,r)
        if yd != 0: rot = (2*r,0,0)
        self.portal = GraphicalObject(Plane(),size=(xSize,ySize,zSize),pos=(self.xpos,self.ypos,self.zpos),color=(0,0,1), rotation=rot)    

    def draw(self,shader):
        if self.active:
            self.portal.draw(shader)
    def setColor(self,color):
        self.portal.color = color

class SmallWall:
    def __init__(self,id, smallWallDict,xSize,ySize,zSize):
        pass
    def draw(self,shader):
        pass






if __name__ == "__main__":
    ll = LevelLoader(sys.path[0]+"/levels")
    ll.load("buttons")
    print(ll.validateLayouyt())
    #print(ll.layout)
    print(ll.queryLevel(0,0))