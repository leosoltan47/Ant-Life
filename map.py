import random
import time
import msvcrt

BOUNDARY_X = 15
BOUNDARY_Y = 15

def select_entity(ant_mod: float = 0.1, fruit_mod: float = 0.2, space_mod: float = 0.6) -> str:
    ant_chance: float = random.random() * ant_mod
    fruit_chane: float = random.random() * fruit_mod
    if ant_chance == fruit_chane:
        return ' '

    space_chance: float = random.random() * space_mod

    chosen: float = max(ant_chance, fruit_chane, space_chance)
    if chosen == ant_chance:
        return 'A'
    elif chosen == fruit_chane:
        return 'F'
    else :
        return ' '
    
world: list[list[str]] = [[select_entity() for _ in range(BOUNDARY_X) ] for _ in range(BOUNDARY_Y)]
for line in world:
    print(line)

