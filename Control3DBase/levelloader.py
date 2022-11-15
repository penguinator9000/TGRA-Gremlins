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
                            print(ycount*self.ySize + self.ySize/2)
                            if wall: toAppend = GraphicalObject(cube,pos = (xcount*self.xSize + self.xSize/2,(ycount-1)*self.ySize + self.ySize/2,zcount*self.zSize+self.zSize/2), size =(self.xSize,self.ySize,self.zSize))
                            self.layout[ycount][zcount].append(toAppend) #exchange this for object at some point.
                            if toAppend:self.walls.append(toAppend)
                            xcount +=1
                        wall = not wall
                    zcount += 1
        valid, msg = self.validateLayouyt()
        print(msg)
        if(not valid): return False
        with open(self.root+"/"+levelDir+"/objects.json",'r') as objects:
            self.objects = json.load(objects)
        return [self.layout, self.objects]
    def draw (self,shader):
        """
            Draws the entire level with all objects 
        """
        for i in self.walls:
            i.draw(shader)
        pass
    def pDraw( self, portalId):
        """
            Draws the level in respect to the portal passed as so that a frame buffer can be made.
        """
        pass
    def queryLevel():
        """
            Query the level returning wether the point is above floor colliding with a wall or
        """
        pass
    def queryObjects():
        """
            Query the level and return any objects found to inhibit that cell
        
        """
        pass
    
    def changeRoot(self,location):
        self.root = location
        #maybe clear data later. also function might be useless
class button:
    def __init__(self, button_dict):
        pass
    def press(self):
        pass
    def nullState(self):
        pass
class portal:
    def __init__(self, portalDict):
        pass

class smallWall:
    def __init__(self, portalDict):
        pass






if __name__ == "__main__":
    ll = LevelLoader(sys.path[0]+"/levels")
    ll.load("buttons")
    print(ll.validateLayouyt())
    print(ll.layout)