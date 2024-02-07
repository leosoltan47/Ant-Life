import random
import time
from os import system

BOUNDARY_X = 5
BOUNDARY_Y = 5

ANT = "🐜"
FRUIT = "🍐"
EMPTY = "  "

class Ant:
    def __init__(self, x: int, y: int, energy: int, step_count: int) -> None:
        self.x = x
        self.y = y
        self.energy = energy
        self.step_count = step_count

    def move(self, dx: int, dy: int) -> tuple[int, int]:
        return (self.x + dx, self.y + dy)
    
    def action(self):
        self.step_count += 1
        dx: int = random.choice([-1, 0, 1])
        dy: int = random.choice([-1, 0, 1])
        return self.move(dx, dy)

    def reproduce(self, old_x, old_y) -> "Ant | None":
        return Ant(old_x, old_y, 5, 1) if self.step_count >= 5 else None

class GameBoard:
    def __init__(self, width: int, height: int, initial_energy: int = 5 , initial_step: int = 1) -> None:
        self.width: int = width
        self.height: int = height
        self.world: list[list[str]] = [[self.select_entity() for _ in range(self.width)] for _ in range(self.height)]
        self.antList: list[list[Ant | None]] = [
                [Ant(row, col, initial_energy, initial_step) if tile == ANT else None for col, tile in enumerate(line)]
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
                [Ant(ant.x, ant.y, ant.energy, ant.step_count) if ant is not None else None for ant in row]
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
                        

                        antList[row][col].step_count += 1
                        antList[row][col].energy -= 1  # 1 movement cost 1 energy
                        old_ant = antList[row][col]
                        self.world[row][col] = EMPTY
                        antList[new_row][new_col] = Ant(old_ant.x, old_ant.y, old_ant.energy, old_ant.step_count)
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

                        if (antList[new_row][new_col] is not None) and (antList[new_row][new_col].step_count % 6 == 0) and (antList[row][col] is None):
                            new_ant = antList[new_row][new_col].reproduce(row, col)
                            if new_ant is not None:
                                antList[new_ant.x][new_ant.y] = new_ant
                                self.world[new_ant.x][new_ant.y] = ANT
                    
        self.antList = antList

def main() -> None:
    World: GameBoard = GameBoard(BOUNDARY_X, BOUNDARY_Y)
    while True:
        World.print_world()
        World.move_ants()
        time.sleep(1)  

if __name__ == "__main__":
    main()
