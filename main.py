import random
import time
from os import system

BOUNDARY_X = 5
BOUNDARY_Y = 5

ANT = "🐜"
FRUIT = "🍐"
EMPTY = "  "

class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if any(entity.x == new_x and entity.y == new_y for entity in world.entities if entity != self):
            return  # Collision
        if 0 <= new_x < world.width and 0 <= new_y < world.height:
            self.x = new_x
            self.y = new_y

    def action(self):
        self.random_movement()

    def random_movement(self):
        dx, dy = random.choice([-1, 0, 1]), random.choice([-1, 0, 1])
        self.move(dx, dy)

    def gather_food(self):
        # Add logic for gathering food

    def communicate(self):
        # Add logic for communication with other ants
        
class GameBoard:
    def __init__(self, width: int, height: int, initial_energy: int = 5) -> None:
        self.width: int = width
        self.height: int = height
        self.world: list[list[str]] = [[self.select_entity() for _ in range(self.width)] for _ in range(self.height)]
        self.antList: list[list[Ant | None]] = [
                [Ant(row, col, initial_energy) if tile == ANT else None for col, tile in enumerate(line)]
                for row, line in enumerate(self.world)
                ]
        self.fruitList: list[list[bool]] = [ [tile == FRUIT for tile in line] for line in self.world ]
    
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
    
    def get_new_fruit_location(self, new_row: int, new_col: int, antList: list[list[Ant | None]]) -> tuple[int, int]:
        return random.choice([
                (x, y)
                for x, line in enumerate(self.world)
                for y, line in enumerate(line)
                if x != new_row and y != new_col
                if not antList[x][y] and not self.fruitList[x][y]
            ])
                 
    def print_world(self) -> None:
        system('cls')
        for line in self.world:
            print(line)
        #print("-"*(self.width*5))
    
    def move_ants(self):
        antList: list[list[Ant | None]] = [
                [Ant(ant.x, ant.y, ant.energy) if ant is not None else None for ant in row]
                for row in self.antList
                ]
        for row in range(len(self.world)):
            for col in range(len(self.world[row])):
                if self.antList[row][col] is not None: 
                    possible_moves: list = []

                    if row - 1 >= 0 and (antList[row - 1][col] is None):
                        possible_moves.append((row - 1, col))
                    if row + 1 < len(self.world) and (antList[row + 1][col] is None):
                        possible_moves.append((row + 1, col))
                    if col - 1 >= 0 and (antList[row][col - 1] is None):
                        possible_moves.append((row, col - 1))
                    if col + 1 < len(self.world[row]) and (antList[row][col + 1] is None):
                        possible_moves.append((row, col + 1)) 

                    if possible_moves:
                        new_row: int
                        new_col: int
                        new_row, new_col = random.choice(possible_moves)
                        old_ant = antList[row][col]

                        antList[row][col].energy -= 1  # 1 movement cost 1 energy
                        self.world[row][col] = EMPTY
                        antList[new_row][new_col] = Ant(old_ant.x, old_ant.y, old_ant.energy)
                        antList[row][col] = None
                        self.world[new_row][new_col] = ANT

                        if self.fruitList[new_row][new_col]:
                            antList[new_row][new_col].energy += 3 # 1 fruit gives 3 energy

                            self.fruitList[new_row][new_col] = False 

                            respawn_row, respawn_col = self.get_new_fruit_location(new_row, new_col, antList)

                            self.fruitList[respawn_row][respawn_col] = True
                            self.world[respawn_row][respawn_col] = FRUIT
                        
                        if antList[new_row][new_col].energy == 0:
                            antList[new_row][new_col] = None # Ant's Energy died
                            self.world[new_row][new_col] = EMPTY

        self.antList = antList

def main() -> None:
    World: GameBoard = GameBoard(BOUNDARY_X, BOUNDARY_Y)
    while True:
        World.print_world()
        World.move_ants()
        time.sleep(1)  

if __name__ == "__main__":
    main()
