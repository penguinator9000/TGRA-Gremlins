import csv
import json
import sys

from Complex3DObjects import *


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
        self.lava = None
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
    def load(self,levelDir,wallTexture = None ,specWallTexture = None):
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
                            if toAppend:
                                self.walls.append(toAppend)
                                toAppend.portals = []
                                toAppend.texture = wallTexture
                                toAppend.spectexture = specWallTexture
                                toAppend.boxXYZ=(xcount,ycount,zcount)
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
            x,y,z = dict["location"]["box-x"],dict["location"]["box-y"],dict["location"]["box-z"]
            locationRef = (x,y,z)
            self.layout[y][z][x].portals.append(tmp)
            if locationRef not in self.objectLevelreference:
                self.objectLevelreference[locationRef] = [tmp]
            else: 
                self.objectLevelreference[locationRef].append(tmp)

        for id, dict in self.objects["smallWalls"].items():
            tmp = SmallWall(id,dict,self.xSize,self.ySize,self.zSize)
            self.objectList.append(tmp)
            self.smallWalls[id] = tmp
            x,y,z = dict["location"]["box-x"],dict["location"]["box-y"],dict["location"]["box-z"]
            locationRef = (x,y,z)
            if locationRef not in self.objectLevelreference:
                self.objectLevelreference[locationRef] = [tmp]
            else:
                self.objectLevelreference[locationRef].append(tmp)


        return [self.layout, self.objects]
    def draw (self,shader):
        """
            Draws the entire level with all objects 
        """
        for i in self.walls:
            skipSides=[]
            for portal in i.portals:
                if portal.active:
                    skipSides.append(portal.face)
            pass
            i.draw(shader,skipSides)
        for obj in self.objectList:
            obj.draw(shader)
        if self.lava: self.lava.draw(shader)
        
    def pDraw( self,shader, portalId):
        """
            Draws the level in respect to the portal passed as so that a frame buffer can be made.
        """
        portal = self.portals[portalId]
        Px,Py,Pz=portal.boxXYZ
        xd,yd,zd = portal.direction
        dirV=Vector(xd,yd,zd)
        portPosV= Vector(Px,Py,Pz)
        portDirV=portPosV.axWiseMult(dirV)
        portDirSum=sum(portDirV.list())

        for i in self.walls:
            xi,yi,zi=i.boxXYZ
            iSum = sum(Vector(xi,yi,zi).axWiseMult(dirV).list())
            #print(portDirSum,iSum,portDirSum<iSum)
            if portDirSum<iSum:
                skipSides=[]
                for portal in i.portals:
                    if portal.active:
                        skipSides.append(portal.face)
                pass
                i.draw(shader,skipSides)
            #else:
                #print("woop")
        for obj in self.objectList:
            xi,yi,zi=obj.boxXYZ
            iSum = sum(Vector(xi,yi,zi).axWiseMult(dirV).list())
            if portDirSum<iSum:
                obj.draw(shader)
            
        if self.lava: self.lava.draw(shader)#might be not good
        
    def queryLevel(self,x,z,y = 1):
        x = int(x//self.xSize)
        z = int(z//self.zSize)
        y = int((y+2)//self.ySize)
        #print(x,y,z)
        if x >= self.xMax or x < 0: return 0
        if z >= self.zMax or z < 0: return 0 
        return self.layout[y][z][x]
        """
            Query the level returning wether the point is above floor colliding with a wall or
        """
        return 
    def queryObjects(self,x,z,y):
        x = int(x//self.xSize)
        z = int(z//self.zSize)
        y = int((y+2)//self.ySize)
        """
            Query the level and return any objects found to inhibit that cell
        
        """
        ret = None
        try:
            ret = self.objectLevelreference[(x,y,z)] 
        except: return ret
        return ret
    def queryPortal(self,x,z,y = 1):
        x = x//self.xSize
        z = z//self.zSize
        y = (y+2)//self.ySize
        if x >= self.xMax or x < 0: return 0
        if z >= self.zMax or z < 0: return 0 
        if self.layout[y][z][x]:
            return self.layout[y][z][x].portal
        return None
    def createLava(self,lava_tex1,lava_tex2):
        B=BayesianCurve4P(p1 = Point(0, 0, 1), p2 = Point(0, 1, 0), p3 = Point(1, 1, 1), p4 = Point(1, 0, 0))
        
        L=LoopBayesianCurves4P(B,8)
        
        L.BuildFromControle()
        self.lava=Lava(L,10,10,Point(0,-2,0),Point(self.xMax,-1.5,self.zMax),Color(1,0,0),Color(0.5,0.5,0),5,5,30,273.272,texture=lava_tex1,spectexture=lava_tex2)
    def changeRoot(self,location):
        self.root = location
        #maybe clear data later. also function might be useless





if __name__ == "__main__":
    ll = LevelLoader(sys.path[0]+"/levels")
    ll.load("buttons")
    print(ll.validateLayouyt())
    #print(ll.layout)
    print(ll.queryLevel(0,0))