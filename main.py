import time
import os
from game_engine import GameBoard

BOUNDARY_X = 5
BOUNDARY_Y = 5

def clear_screen() -> None:
    """Cross-platform screen clearing"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_world(world: GameBoard) -> None:
    """Optimized world printing with stats"""
    clear_screen()
    print(world.get_world_string())
    stats = world.get_stats()
    print(f"\nStats: Ants: {stats['ants']}, Fruits: {stats['fruits']}, "
          f"Total Energy: {stats['total_energy']}, Empty: {stats['empty_spaces']}")

def main() -> None:
    """Optimized main game loop"""
    world = GameBoard(BOUNDARY_X, BOUNDARY_Y)
    
    try:
        while True:
            print_world(world)
            world.move_ants()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")

if __name__ == "__main__":
    main()
