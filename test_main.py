import unittest
from game_engine import GameBoard, Ant, EntityType

class TestGameEngine(unittest.TestCase):
    def test_init_game_board(self):
        """Test GameBoard initialization"""
        game = GameBoard(4, 4)
        self.assertEqual(game.width, 4)
        self.assertEqual(game.height, 4)
        self.assertIsNotNone(game.world)
        self.assertIsNotNone(game.ants)
        self.assertIsNotNone(game.fruits)
    
    def test_ant_creation(self):
        """Test Ant object creation and methods"""
        ant = Ant(1, 2, 5, 1)
        self.assertEqual(ant.x, 1)
        self.assertEqual(ant.y, 2)
        self.assertEqual(ant.energy, 5)
        self.assertEqual(ant.step_count, 1)
        
        # Test move calculation
        new_pos = ant.move(1, 1)
        self.assertEqual(new_pos, (2, 3))
        
        # Test position update
        ant.update_position(3, 4)
        self.assertEqual(ant.x, 3)
        self.assertEqual(ant.y, 4)
    
    def test_ant_reproduction(self):
        """Test ant reproduction logic"""
        ant = Ant(1, 1, 5, 4)
        self.assertFalse(ant.can_reproduce())
        
        ant.step_count = 5
        self.assertTrue(ant.can_reproduce())
        
        new_ant = ant.reproduce(2, 2)
        self.assertIsNotNone(new_ant)
        self.assertEqual(new_ant.x, 2)
        self.assertEqual(new_ant.y, 2)
        self.assertEqual(new_ant.energy, 5)
        self.assertEqual(new_ant.step_count, 1)
    
    def test_game_stats(self):
        """Test game statistics functionality"""
        game = GameBoard(3, 3)
        stats = game.get_stats()
        
        self.assertIn('ants', stats)
        self.assertIn('fruits', stats)
        self.assertIn('total_energy', stats)
        self.assertIn('empty_spaces', stats)
        
        # All values should be non-negative
        for value in stats.values():
            self.assertGreaterEqual(value, 0)
    
    def test_valid_moves(self):
        """Test valid moves calculation"""
        game = GameBoard(3, 3)
        
        # Test moves from center position
        moves = game.get_valid_moves(1, 1)
        self.assertIsInstance(moves, list)
        
        # Should have at most 4 moves (up, down, left, right)
        self.assertLessEqual(len(moves), 4)
    
    def test_world_string(self):
        """Test world string representation"""
        game = GameBoard(2, 2)
        world_str = game.get_world_string()
        
        self.assertIsInstance(world_str, str)
        # Should contain entity symbols
        self.assertTrue(any(entity.value in world_str for entity in EntityType))

if __name__ == "__main__":
    unittest.main()
