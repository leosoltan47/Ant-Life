import random
import time
import msvcrt

class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_alive = True

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Fruit:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def spawn_fruit():
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    return Fruit(x, y)

def get_key():
    return msvcrt.getch().decode('utf-8').lower()


ant = Ant(5, 5)
fruits = [spawn_fruit() for _ in range(5)]

def print_game():
    for row in range(15):
        for col in range(15):
            if ant.x == col and ant.y == row:
                print("A", end=" ") 
            elif any(fruit.x == col and fruit.y == row for fruit in fruits):
                print("F", end=" ")  
            else:
                print(".", end=" ") 
        print()

while True:
    print_game()

    key = get_key()
    if key == 'w' or key == 'up':
        ant.move(0, -1)  
    elif key == 's' or key == 'down':
        ant.move(0, 1)   
    elif key == 'a' or key == 'left':
        ant.move(-1, 0) 
    elif key == 'd' or key == 'right':
        ant.move(1, 0)   


    for fruit in fruits:
        if ant.x == fruit.x and ant.y == fruit.y:
            fruits.remove(fruit)
            fruits.append(spawn_fruit())

    time.sleep(0.5)  
