import random

#WORLDSIZE = "20x20"

BOUNDARY_X = 48
BOUNDARY_Y = 120

def generateWorld(X, Y):
    for i in range(0,X):
        for j in range(0,Y):
            if (j == 0 or j == Y-1) and i != 0 :
              print("|",end='')
              continue
            elif i == 0 or i == X-1:
                print("_",end='')
                continue
            print(" ",end="")
        print('')

def AntLife():
    generateWorld(BOUNDARY_X,BOUNDARY_Y)

if __name__ == "__main__":
    AntLife()

