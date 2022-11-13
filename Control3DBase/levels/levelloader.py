import csv
import json

class LevelLoader():
    def __init__(self,location):
        self.root = location
    def load(self,levelDir):
        if self.levelDir != levelDir:
            self.levelDir = levelDir
        else: return "already loaded"
        layoutFile = open(leveldir+"/layout.csv",'r')

        with open(sys.path[0] + "/maze.csv", 'r') as file:
            csvreader = csv.reader(file)
            first = True
            for row in csvreader:
                if first: 
                    first =False
                    self.zMax,self.xMax,self.yMax = row
                else:
                    x,z = [(int(val)) for val in row]
                    temp = GraphicalObject(c,pos=(x*2+MAZE_ofset,1,z*2+MAZE_ofset),size=(2,3,2),color=Color((x)/MAZE_Max,1-min(1,((x)/MAZE_Max+(z)/MAZE_Max)),(z)/MAZE_Max))
                    self.mazeObjects.append(temp)
                    self.maze[x][z]=temp    


    def changeRoot(self,location):
        self.root = location
        #maybe clear data later. also function might be useless
