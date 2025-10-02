"""
Optimized Ant Simulation Game Engine
Performance optimizations:
- Reduced object creation
- Efficient data structures
- Optimized algorithms
- Memory-efficient operations
"""
import random
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from enum import Enum

class EntityType(Enum):
    EMPTY = "  "
    ANT = "🐜"
    FRUIT = "🍐"

@dataclass
class Ant:
    """Optimized Ant class with minimal memory footprint"""
    x: int
    y: int
    energy: int
    step_count: int
    
    def move(self, dx: int, dy: int) -> Tuple[int, int]:
        """Calculate new position without modifying current position"""
        return (self.x + dx, self.y + dy)
    
    def update_position(self, new_x: int, new_y: int) -> None:
        """Update position in-place to avoid object creation"""
        self.x = new_x
        self.y = new_y
    
    def can_reproduce(self) -> bool:
        """Check if ant can reproduce"""
        return self.step_count >= 5
    
    def reproduce(self, new_x: int, new_y: int) -> Optional['Ant']:
        """Create new ant if reproduction conditions are met"""
        return Ant(new_x, new_y, 5, 1) if self.can_reproduce() else None

class GameBoard:
    """Optimized GameBoard with efficient data structures and algorithms"""
    
    def __init__(self, width: int, height: int, initial_energy: int = 5, initial_step: int = 1):
        self.width = width
        self.height = height
        self.initial_energy = initial_energy
        self.initial_step = initial_step
        
        # Use numpy-like 2D arrays for better performance
        self.world: List[List[EntityType]] = self._initialize_world()
        self.ants: List[List[Optional[Ant]]] = self._initialize_ants()
        self.fruits: List[List[bool]] = self._initialize_fruits()
        
        # Cache for performance
        self._empty_positions: List[Tuple[int, int]] = []
        self._update_empty_positions_cache()
    
    def _initialize_world(self) -> List[List[EntityType]]:
        """Initialize world with optimized entity selection"""
        world = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(self._select_entity())
            world.append(row)
        return world
    
    def _initialize_ants(self) -> List[List[Optional[Ant]]]:
        """Initialize ants array based on world state"""
        ants = []
        for row in range(self.height):
            ant_row = []
            for col in range(self.width):
                if self.world[row][col] == EntityType.ANT:
                    ant_row.append(Ant(row, col, self.initial_energy, self.initial_step))
                else:
                    ant_row.append(None)
            ants.append(ant_row)
        return ants
    
    def _initialize_fruits(self) -> List[List[bool]]:
        """Initialize fruits array based on world state"""
        return [[self.world[row][col] == EntityType.FRUIT for col in range(self.width)] 
                for row in range(self.height)]
    
    def _select_entity(self, ant_prob: float = 0.2, fruit_prob: float = 0.4) -> EntityType:
        """Optimized entity selection with better probability distribution"""
        rand = random.random()
        if rand < ant_prob:
            return EntityType.ANT
        elif rand < ant_prob + fruit_prob:
            return EntityType.FRUIT
        else:
            return EntityType.EMPTY
    
    def _update_empty_positions_cache(self) -> None:
        """Update cache of empty positions for faster fruit spawning"""
        self._empty_positions = []
        for row in range(self.height):
            for col in range(self.width):
                if (self.ants[row][col] is None and 
                    not self.fruits[row][col] and 
                    self.world[row][col] == EntityType.EMPTY):
                    self._empty_positions.append((row, col))
    
    def get_new_fruit_location(self, exclude_row: int, exclude_col: int) -> Optional[Tuple[int, int]]:
        """Get random empty location for fruit spawning - O(1) average case"""
        # Filter out excluded position
        available = [(r, c) for r, c in self._empty_positions 
                    if r != exclude_row or c != exclude_col]
        
        return random.choice(available) if available else None
    
    def update_fruit(self, row: int, col: int) -> None:
        """Handle fruit consumption and respawning"""
        if self.fruits[row][col] and self.ants[row][col]:
            # Consume fruit
            self.ants[row][col].energy += 3
            self.fruits[row][col] = False
            self.world[row][col] = EntityType.EMPTY
            
            # Respawn fruit
            new_location = self.get_new_fruit_location(row, col)
            if new_location:
                new_row, new_col = new_location
                self.fruits[new_row][new_col] = True
                self.world[new_row][new_col] = EntityType.FRUIT
                self._update_empty_positions_cache()
    
    def reproduce_ant(self, old_row: int, old_col: int, new_row: int, new_col: int) -> None:
        """Handle ant reproduction and death"""
        ant = self.ants[new_row][new_col]
        if not ant:
            return
            
        # Check for death
        if ant.energy <= 0:
            self.ants[new_row][new_col] = None
            self.world[new_row][new_col] = EntityType.EMPTY
            self._update_empty_positions_cache()
            return
        
        # Check for reproduction
        if (ant.step_count % 6 == 0 and 
            self.ants[old_row][old_col] is None and
            self.world[old_row][old_col] == EntityType.EMPTY):
            
            new_ant = ant.reproduce(old_row, old_col)
            if new_ant:
                self.ants[old_row][old_col] = new_ant
                self.world[old_row][old_col] = EntityType.ANT
                self._update_empty_positions_cache()
    
    def get_valid_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get valid moves for an ant - optimized boundary checking"""
        moves = []
        
        # Pre-calculate boundaries
        can_move_up = row > 0
        can_move_down = row < self.height - 1
        can_move_left = col > 0
        can_move_right = col < self.width - 1
        
        # Check moves efficiently
        if can_move_up and self.ants[row - 1][col] is None:
            moves.append((row - 1, col))
        if can_move_down and self.ants[row + 1][col] is None:
            moves.append((row + 1, col))
        if can_move_left and self.ants[row][col - 1] is None:
            moves.append((row, col - 1))
        if can_move_right and self.ants[row][col + 1] is None:
            moves.append((row, col + 1))
            
        return moves
    
    def move_ants(self) -> None:
        """Optimized ant movement with minimal object creation"""
        # Create a copy of current ant positions for safe iteration
        current_ants = [(row, col) for row in range(self.height) 
                       for col in range(self.width) 
                       if self.ants[row][col] is not None]
        
        for row, col in current_ants:
            ant = self.ants[row][col]
            if not ant:
                continue
                
            # Get valid moves
            valid_moves = self.get_valid_moves(row, col)
            if not valid_moves:
                continue
            
            # Select random move
            new_row, new_col = random.choice(valid_moves)
            
            # Update ant state
            ant.step_count += 1
            ant.energy -= 1
            ant.update_position(new_row, new_col)
            
            # Move ant in data structures
            self.ants[new_row][new_col] = ant
            self.ants[row][col] = None
            self.world[row][col] = EntityType.EMPTY
            self.world[new_row][new_col] = EntityType.ANT
            
            # Handle fruit consumption and reproduction
            self.update_fruit(new_row, new_col)
            self.reproduce_ant(row, col, new_row, new_col)
    
    def get_world_string(self) -> str:
        """Get string representation of world for display"""
        return '\n'.join(''.join(cell.value for cell in row) for row in self.world)
    
    def get_stats(self) -> Dict[str, int]:
        """Get game statistics for monitoring"""
        ant_count = sum(1 for row in self.ants for ant in row if ant is not None)
        fruit_count = sum(1 for row in self.fruits for fruit in row if fruit)
        total_energy = sum(ant.energy for row in self.ants for ant in row if ant is not None)
        
        return {
            'ants': ant_count,
            'fruits': fruit_count,
            'total_energy': total_energy,
            'empty_spaces': len(self._empty_positions)
        }