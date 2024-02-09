import random
from time import sleep
import tkinter as tk

BOUNDARY_X = 5
BOUNDARY_Y = 5

ANT = "🐜"
FRUIT = "🍐"
EMPTY = "  "

class GameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Ant Simulation Game")

        self.game_board = GameBoard(BOUNDARY_X, BOUNDARY_Y)

        self.canvas = tk.Canvas(self.master, width=BOUNDARY_X * 50, height=BOUNDARY_Y * 50) 
        self.canvas.pack() # Window Created

        self.start_button = tk.Button(self.master, text="Start Simulation", command= self.start_simulation)
        self.start_button.pack()

        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all") # No more need for os library

        for row in range(len(self.game_board.world)):
            for col in range(len(self.game_board.world[row])):
                x1, y1 = col * 50, row * 50 # Top Left Corner
                x2, y2 = x1 + 50, y1 + 50 # Bottom Right Corner

                if self.game_board.world[row][col] == ANT:
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=ANT, font=("Arial", 16)) # Center of Entry
                elif self.game_board.world[row][col] == FRUIT:
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=FRUIT, font=("Arial", 16))

    def start_simulation(self):
        self.start_button.config(state=tk.DISABLED)

        while True: 
            self.game_board.move_ants()
            self.update_canvas()
            self.master.update()  # Update window
            sleep(1)
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
        self.ants: list[list[Ant | None]] = [
                [Ant(row, col, initial_energy, initial_step) if tile == ANT else None for col, tile in enumerate(line)]
                for row, line in enumerate(self.world)
                ]
        self.fruits: list[list[bool]] = [ [tile == FRUIT for tile in line] for line in self.world ]
    
    def select_entity(self, ant_mod: float = 0.2, fruit_mod: float = 0.4, space_mod: float = 0.5) -> str:
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
    root = tk.Tk()
    game_gui = GameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()