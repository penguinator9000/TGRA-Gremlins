import csv
import json
import sys
class LevelLoader():
    def __init__(self,location):
        self.root = location
        self.levelDir = ""
    def load(self,levelDir):
        if self.levelDir == levelDir:
            return "already loaded"
        
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
                    for i in  row:
                        for j in range(int(i)):
                            self.layout[ycount][zcount].append(wall) #exchange this for object at some point.
                        wall = not wall
                    zcount += 1
        with open(self.root+"/"+levelDir+"/objects.json",'r') as objects:
            self.objects = json.load(objects)
        return [self.layout, self.objects]

                       


    def changeRoot(self,location):
        self.root = location
        #maybe clear data later. also function might be useless


if __name__ == "__main__":
    ll = LevelLoader(sys.path[0])
    print(ll.load("buttons"))