import random
import time
import msvcrt

BOUNDARY_X = 15
BOUNDARY_Y = 15

class GameBoard:

    class Ant:
        pass

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.world = [[self.select_entity() for _ in range(self.width)] for _ in range(self.height)]
        self.antList = self.position(True)
        self.fruitList = self.position(False)
    
    def select_entity(self, ant_mod: float = 0.15, fruit_mod: float = 0.25, space_mod: float = 0.6) -> str:
        ant_chance: float = random.random() * ant_mod
        fruit_chance: float = random.random() * fruit_mod
        if ant_chance == fruit_chance:
            return ' '
        space_chance: float = random.random() * space_mod
        chosen: float = max(ant_chance, fruit_chance, space_chance)
        if chosen == ant_chance:
            return 'A'
        elif chosen == fruit_chance:
            return 'F'
        else:
            return ' '
    
    def position(self, bool1):
        
        fruitList = [[None for _ in range(BOUNDARY_Y)] for _ in range(BOUNDARY_X)]
        antList = [[None for _ in range(BOUNDARY_Y)] for _ in range(BOUNDARY_X)]

        for row in range(len(self.world)):
            for col in range(len(self.world[row])):
                if self.world[row][col] == "F":
                    fruitList[row][col] = True
                elif self.world[row][col] == "A":
                    antList[row][col] = True
    
        if bool1 == True:
            return antList
        else:
            return fruitList
                 
    def print_world(self):
        for line in self.world:
            print(line)
        print("-"*(self.width*5))
    
    def move_ant(self, direction): # Task Cemre (SIRA SIRA ANT MOVEMENT)
        pass


World = GameBoard(BOUNDARY_X, BOUNDARY_Y)

while True:  # Main Code
    World.print_world()
    #move_ant(world, antList, fruitList)
    
    key = msvcrt.getch()
    #print(key)
    if key == b'\xe0' and False:
        key = msvcrt.getch()
        if key == b'K':
            world, antList, fruitList = World.move_ant('a')  # Left arrow
        elif key == b'M':
            world, antList, fruitList = World.move_ant('d')  # Right arrow
        elif key == b'H':
            world, antList, fruitList = World.move_ant('w')  # Up arrow
        elif key == b'P':
            world, antList, fruitList = World.move_ant('s')  # Down arrow
    #else:
       # key = key.decode("utf-8").lower()
       # world, antList, fruitList = World.move_ant(key)

    time.sleep(0.1)  
    


