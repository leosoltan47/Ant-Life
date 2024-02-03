import random
import time
import msvcrt

BOUNDARY_X = 15
BOUNDARY_Y = 15

class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Fruit:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GameBoard:
    def init(self, width, height):
        self.width = width
        self.height = height
        self.world = [[self.select_entity() for _ in range(self.width)] for _ in range(self.height)]

    def place_ant(self, ant, x, y):
        if self.world[y][x] is None:
            self.world[y][x] = ant
            ant.x = x
            ant.y = y
    
    def select_entity(self, ant_mod: float = 0.15, fruit_mod: float = 0.25, space_mod: float = 0.6) -> str:
        ant_chance: float = random.random() * ant_mod
        fruit_chance: float = random.random() * fruit_mod
        if ant_chance == fruit_chance:
            return ' '
        space_chance: float = random.random() * space_mod
        chosen: float = max( fruit_chance, space_chance)
        if chosen == ant_chance:
            return 'A'
        if chosen == fruit_chance:
            return 'F'
        else:
            return ' '
    
    def print_world(self):
        for line in self.world:
            print(line)
        print("-"*(self.width*5))


