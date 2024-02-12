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
        self.memory = []  # Memory of food locations
        self.bad_memory = []  # Memory of locations with no food
        self.danger_memory = []  # Memory of dangerous locations
        self.crowd_memory = []  # Memory of crowded locations
        self.mistake_memory = []  # Memory of actions that led to negative outcomes
        self.exploration_rate = INITIAL_EXPLORATION_RATE  # Probability of exploring new areas

    def move(self, dx: int, dy: int) -> tuple[int, int]:
        return (self.x + dx, self.y + dy)

    def action(self, world, other_ants):
        self.step_count += 1
        # If energy is low, prioritize finding food
        if self.energy < ENERGY_THRESHOLD:
            # Check memory for food locations
            if self.memory:
                remembered_x, remembered_y = self.memory.pop(0)
                dx = remembered_x - self.x
                dy = remembered_y - self.y
                return self.move(dx, dy)
        # Check the surrounding cells (up, down, left, right)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            new_x, new_y = self.move(dx, dy)
            # If there's danger or a crowd in a cell, remember its location and avoid it
            if world[new_y][new_x] == DANGER or len([ant for ant in other_ants if ant.x == new_x and ant.y == new_y]) > CROWD_THRESHOLD:
                self.danger_memory.append((new_x, new_y))
                self.crowd_memory.append((new_x, new_y))
                self.mistake_memory.append((dx, dy))  # Remember the action that led to this situation
                continue
            # If there's food in a cell, move to that cell and remember its location
            if world[new_y][new_x] == FRUIT:
                self.memory.append((new_x, new_y))
                return self.move(dx, dy)
        # If no other ants know about food locations, follow the strongest pheromone trail or move towards known food locations
        if world[self.y][self.x].pheromone > 0:
            dx, dy = max(directions, key=lambda d: world[self.y + d[1]][self.x + d[0]].pheromone)
            return self.move(dx, dy)
        elif self.memory:
            remembered_x, remembered_y = self.memory.pop(0)
            dx = remembered_x - self.x
            dy = remembered_y - self.y
            return self.move(dx, dy)
        # If no other ants know about food locations, ask other ants for food locations
        for ant in other_ants:
            if ant.memory:
                food_x, food_y = ant.memory[0]
                dx = food_x - self.x
                dy = food_y - self.y
                return self.move(dx, dy)
        # If there's no pheromone trail, move randomly but avoid locations with no food, danger, or crowds, and avoid repeating mistakes
        while True:
            dx: int = random.choice([-1, 0, 1])
            dy: int = random.choice([-1, 0, 1])
            new_x, new_y = self.move(dx, dy)
            if (new_x, new_y) not in self.bad_memory and (new_x, new_y) not in self.danger_memory and (new_x, new_y) not in self.crowd_memory and (dx, dy) not in self.mistake_memory:
                return self.move(dx, dy)
            else:
                self.bad_memory.append((new_x, new_y))
                self.danger_memory.append((new_x, new_y))
                self.crowd_memory.append((new_x, new_y))

    def reproduce(self, old_x, old_y) -> "Ant | None":
        # Only reproduce if energy is above a certain threshold and there's food in memory
        return Ant(old_x, old_y, 5, 1) if self.step_count >= 5 and self.energy > REPRODUCTION_THRESHOLD and self.memory else None

    def update_exploration_rate(self, food_availability):
        # If food is scarce, increase exploration rate
        if food_availability < FOOD_THRESHOLD:
            self.exploration_rate = min(self.exploration_rate + EXPLORATION_INCREMENT, MAX_EXPLORATION_RATE)
        else:
            self.exploration_rate = max(self.exploration_rate - EXPLORATION_INCREMENT, MIN_EXPLORATION_RATE)


class GameBoard:
    def __init__(self, width: int, height: int, initial_energy: int = 5 , initial_step: int = 1) -> None:
        self.width: int = width
        self.height: int = height
        self.world: list[list[str]] = [[self.select_entity() for _ in range(self.width)] for _ in range(self.height)]
        self.ants: list[list[Ant | None]] = [
                [Ant(row, col, initial_energy, initial_step) if tile == ANT else None for col, tile in enumerate(line)]
                for row, line in enumerate(self.world)
                ]
        self.fruits: list[list[bool]] = [ [tile == FRUIT for tile in line] for line in self.world ]
    
    def select_entity(self, ant_mod: float = 0.2, fruit_mod: float = 0.5, space_mod: float = 0.5) -> str:
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
    
    def get_new_fruit_location(self, new_row: int, new_col: int, ants: list[list[Ant | None]]) -> tuple[int, int] | None:
        available_locations = [
            (x, y)
            for x, line in enumerate(self.world)
            for y, line in enumerate(line)
            if x != new_row and y != new_col
            if not ants[x][y] and not self.fruits[x][y]
        ]

        if available_locations:
            return random.choice(available_locations)
        else:
            return None
       
    def print_world(self) -> None:
        system('cls')
        for line in self.world:
            print(line)

    def update_fruit(self, ants: list[list[Ant|None]], new_row: int, new_col:int) -> None:
        if self.fruits[new_row][new_col]:
            ants[new_row][new_col].energy += 3 # 1 fruit gives 3 energy

            self.fruits[new_row][new_col] = False 

            respawn_location = self.get_new_fruit_location(new_row, new_col, ants)
            if respawn_location is not None:
                respawn_row, respawn_col = respawn_location
                self.fruits[respawn_row][respawn_col] = True
                self.world[respawn_row][respawn_col] = FRUIT

    def reproduce_ant(self, ants: list[list[Ant|None]], row: int, col: int, new_row: int, new_col:int) -> None:
        if ants[new_row][new_col].energy == 0:
            ants[new_row][new_col] = None # Ant's Energy died
            self.world[new_row][new_col] = EMPTY

        if (ants[new_row][new_col] is not None) and (ants[new_row][new_col].step_count % 6 == 0) and (ants[row][col] is None):
            new_ant = ants[new_row][new_col].reproduce(row, col)
            if new_ant is not None:
                ants[new_ant.x][new_ant.y] = new_ant
                self.world[new_ant.x][new_ant.y] = ANT
    
    def move_ants(self):
        ants: list[list[Ant | None]] = [
                [Ant(ant.x, ant.y, ant.energy, ant.step_count) if ant is not None else None for ant in row]
                for row in self.ants
                ]
        for row in range(len(self.world)):
            for col in range(len(self.world[row])):
                if self.ants[row][col] is None: 
                    continue
                possible_moves: list = []

                if row - 1 >= 0 and (ants[row - 1][col] is None):
                    possible_moves.append((row - 1, col))
                if row + 1 < len(self.world) and (ants[row + 1][col] is None):
                    possible_moves.append((row + 1, col))
                if col - 1 >= 0 and (ants[row][col - 1] is None):
                    possible_moves.append((row, col - 1))
                if col + 1 < len(self.world[row]) and (ants[row][col + 1] is None):
                    possible_moves.append((row, col + 1)) 

                if len(possible_moves) == 0:
                    continue
                new_row, new_col = random.choice(possible_moves)
                

                ants[row][col].step_count += 1
                ants[row][col].energy -= 1  # 1 movement cost 1 energy
                old_ant = ants[row][col]
                self.world[row][col] = EMPTY
                ants[new_row][new_col] = Ant(old_ant.x, old_ant.y, old_ant.energy, old_ant.step_count)
                ants[row][col] = None
                self.world[new_row][new_col] = ANT

                self.update_fruit(ants, new_row, new_col)
                self.reproduce_ant(ants, row, col, new_row, new_col)
        self.ants = ants

def main() -> None:
    World: GameBoard = GameBoard(BOUNDARY_X, BOUNDARY_Y)
    while True:
        World.print_world()
        World.move_ants()
        time.sleep(1)  

if __name__ == "__main__":
    main()
