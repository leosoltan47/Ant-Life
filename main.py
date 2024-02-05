import random
import time
from os import system

BOUNDARY_X = 5
BOUNDARY_Y = 5

ANT: str = "A"
FRUIT: str = "F"
EMPTY: str = " "


class GameBoard:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.world = [[self.select_entity() for _ in range(self.width)] for _ in range(self.height)]
        self.antList = self._fill_antList()
        self.fruitList = self._fill_fruitList()
        self.current_ant_index = 0
    
    def select_entity(self, ant_mod: float = 0.2, fruit_mod: float = 0.3, space_mod: float = 0.5) -> str:
        ant_chance: float = random.random() * ant_mod
        fruit_chance: float = random.random() * fruit_mod
        if ant_chance == fruit_chance:
            return EMPTY
        space_chance: float = random.random() * space_mod
        chosen: float = max(ant_chance, fruit_chance, space_chance)
        if chosen == ant_chance:
            return ANT
        elif chosen == fruit_chance:
            return FRUIT
        else:
            return EMPTY
    
    def _fill_antList(self) -> list[list[bool]]:
            return [ [tile == ANT for tile in line ] for line in self.world ]

    def _fill_fruitList(self) -> list[list[bool]]:
            return [ [tile == FRUIT for tile in line ] for line in self.world ] 

                 
    def print_world(self):
        for line in self.world:
            print(line)
        print("-"*(self.width*5))
    
    def move_ants(self):
        antList = [row.copy() for row in self.antList]

        for row in range(len(self.world)):
            for col in range(len(self.world[row])):
                if self.antList[row][col]: 
                    possible_moves = []

                    if row - 1 >= 0 and not antList[row - 1][col]:
                        possible_moves.append((row - 1, col))
                    if row + 1 < len(self.world) and not antList[row + 1][col]:
                        possible_moves.append((row + 1, col))
                    if col - 1 >= 0 and not antList[row][col - 1]:
                        possible_moves.append((row, col - 1))
                    if col + 1 < len(self.world[row]) and not antList[row][col + 1]:
                        possible_moves.append((row, col + 1)) 

                    if possible_moves:
                        new_row, new_col = random.choice(possible_moves)

                        antList[row][col] = False
                        self.world[row][col] = EMPTY
                        antList[new_row][new_col] = True
                        self.world[new_row][new_col] = ANT

                        if self.fruitList[new_row][new_col]:
                            #print(f"Ant at ({row}, {col}) ate a fruit!")
                            self.fruitList[new_row][new_col] = False 

                            respawn_row, respawn_col = random.randint(0, len(self.world) - 1), random.randint(0, len(self.world[row]) - 1)

                            while (antList[respawn_row][respawn_col] or (respawn_row == new_row and respawn_col == new_col)) and self.fruitList[respawn_row][respawn_col]:
                                respawn_row, respawn_col = random.randint(0, len(self.world) - 1), random.randint(0, len(self.world[row]) - 1)

                            self.fruitList[respawn_row][respawn_col] = True
                            self.world[respawn_row][respawn_col] = FRUIT

        self.antList = antList


World = GameBoard(BOUNDARY_X, BOUNDARY_Y)

while True:  # Main Code
    World.print_world()
    World.move_ants()
    

    time.sleep(1)  
    system('cls')
