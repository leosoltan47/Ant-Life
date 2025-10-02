"""
Performance Testing Script for Ant Simulation
Demonstrates the performance improvements made to the codebase
"""
import time
import psutil
import os
from game_engine import GameBoard

def measure_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def benchmark_game_board_creation(size, iterations=100):
    """Benchmark GameBoard creation performance"""
    print(f"Benchmarking GameBoard creation ({size}x{size}) - {iterations} iterations")
    
    start_time = time.time()
    start_memory = measure_memory_usage()
    
    boards = []
    for _ in range(iterations):
        board = GameBoard(size, size)
        boards.append(board)
    
    end_time = time.time()
    end_memory = measure_memory_usage()
    
    total_time = end_time - start_time
    avg_time = total_time / iterations
    memory_used = end_memory - start_memory
    
    print(f"  Total time: {total_time:.4f}s")
    print(f"  Average time per board: {avg_time:.6f}s")
    print(f"  Memory used: {memory_used:.2f} MB")
    print(f"  Memory per board: {memory_used/iterations:.4f} MB")
    
    return avg_time, memory_used / iterations

def benchmark_ant_movement(board, iterations=1000):
    """Benchmark ant movement performance"""
    print(f"Benchmarking ant movement - {iterations} iterations")
    
    start_time = time.time()
    
    for _ in range(iterations):
        board.move_ants()
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / iterations
    
    print(f"  Total time: {total_time:.4f}s")
    print(f"  Average time per move: {avg_time:.6f}s")
    print(f"  Moves per second: {1/avg_time:.0f}")
    
    return avg_time

def benchmark_stats_calculation(board, iterations=10000):
    """Benchmark statistics calculation performance"""
    print(f"Benchmarking stats calculation - {iterations} iterations")
    
    start_time = time.time()
    
    for _ in range(iterations):
        stats = board.get_stats()
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / iterations
    
    print(f"  Total time: {total_time:.4f}s")
    print(f"  Average time per stats call: {avg_time:.8f}s")
    print(f"  Stats calls per second: {1/avg_time:.0f}")
    
    return avg_time

def benchmark_fruit_location_search(board, iterations=1000):
    """Benchmark fruit location search performance"""
    print(f"Benchmarking fruit location search - {iterations} iterations")
    
    start_time = time.time()
    
    for _ in range(iterations):
        location = board.get_new_fruit_location(0, 0)
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / iterations
    
    print(f"  Total time: {total_time:.4f}s")
    print(f"  Average time per search: {avg_time:.8f}s")
    print(f"  Searches per second: {1/avg_time:.0f}")
    
    return avg_time

def run_performance_tests():
    """Run comprehensive performance tests"""
    print("=" * 60)
    print("ANT SIMULATION PERFORMANCE BENCHMARKS")
    print("=" * 60)
    
    # Test different board sizes
    sizes = [5, 10, 20]
    
    for size in sizes:
        print(f"\n{'='*20} BOARD SIZE: {size}x{size} {'='*20}")
        
        # Board creation benchmark
        creation_time, creation_memory = benchmark_game_board_creation(size, 50)
        
        # Create a board for other tests
        board = GameBoard(size, size)
        
        # Movement benchmark
        movement_time = benchmark_ant_movement(board, 100)
        
        # Stats benchmark
        stats_time = benchmark_stats_calculation(board, 1000)
        
        # Fruit location benchmark
        fruit_time = benchmark_fruit_location_search(board, 100)
        
        # Performance summary
        print(f"\n--- PERFORMANCE SUMMARY FOR {size}x{size} BOARD ---")
        print(f"Board creation: {creation_time:.6f}s ({creation_memory:.4f} MB)")
        print(f"Ant movement:   {movement_time:.6f}s")
        print(f"Stats calc:     {stats_time:.8f}s")
        print(f"Fruit search:   {fruit_time:.8f}s")
        
        # Calculate efficiency metrics
        efficiency_score = 1 / (creation_time + movement_time + stats_time + fruit_time)
        print(f"Efficiency score: {efficiency_score:.2f}")

def demonstrate_optimizations():
    """Demonstrate specific optimizations made"""
    print("\n" + "=" * 60)
    print("OPTIMIZATION DEMONSTRATIONS")
    print("=" * 60)
    
    board = GameBoard(10, 10)
    
    print("\n1. MEMORY EFFICIENCY:")
    print("   - Using dataclasses for Ant objects (reduced memory footprint)")
    print("   - Caching empty positions for O(1) fruit spawning")
    print("   - In-place position updates instead of object creation")
    
    print("\n2. ALGORITHM OPTIMIZATION:")
    print("   - Pre-calculated boundary checks in get_valid_moves()")
    print("   - Efficient list comprehensions with early termination")
    print("   - Reduced nested loops and redundant calculations")
    
    print("\n3. DATA STRUCTURE OPTIMIZATION:")
    print("   - Enum for entity types (memory efficient)")
    print("   - Optimized 2D array access patterns")
    print("   - Cached statistics for performance monitoring")
    
    print("\n4. GUI OPTIMIZATION:")
    print("   - Incremental canvas updates (no full redraw)")
    print("   - Pre-created canvas items for faster rendering")
    print("   - Non-blocking simulation loop with tkinter.after()")
    
    # Show current stats
    stats = board.get_stats()
    print(f"\nCurrent simulation stats: {stats}")

if __name__ == "__main__":
    try:
        run_performance_tests()
        demonstrate_optimizations()
        
        print("\n" + "=" * 60)
        print("PERFORMANCE TESTING COMPLETE")
        print("=" * 60)
        
    except ImportError:
        print("psutil not available. Install with: pip install psutil")
        print("Running basic performance tests without memory monitoring...")
        
        # Basic tests without psutil
        board = GameBoard(10, 10)
        
        start_time = time.time()
        for _ in range(1000):
            board.move_ants()
        end_time = time.time()
        
        print(f"1000 move iterations took: {end_time - start_time:.4f}s")
        print(f"Average time per move: {(end_time - start_time)/1000:.6f}s")