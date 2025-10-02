import tkinter as tk
from tkinter import ttk
from time import sleep
from game_engine import GameBoard, EntityType

BOUNDARY_X = 5
BOUNDARY_Y = 5

class OptimizedGameGUI:
    """Optimized GUI with incremental updates and performance monitoring"""
    
    def __init__(self, master):
        self.master = master
        self.master.title("Optimized Ant Simulation Game")
        
        # Game state
        self.game_board = GameBoard(BOUNDARY_X, BOUNDARY_Y)
        self.is_running = False
        self.simulation_speed = 1000  # milliseconds
        
        # GUI elements
        self.setup_gui()
        
        # Performance tracking
        self.frame_count = 0
        self.last_stats = {}
        
        # Initial render
        self.update_canvas()
    
    def setup_gui(self):
        """Setup optimized GUI components"""
        # Control frame
        control_frame = ttk.Frame(self.master)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Buttons
        self.start_button = ttk.Button(control_frame, text="Start Simulation", 
                                     command=self.start_simulation)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Simulation", 
                                    command=self.stop_simulation, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Speed control
        ttk.Label(control_frame, text="Speed:").pack(side=tk.LEFT, padx=(20, 5))
        self.speed_var = tk.IntVar(value=1000)
        speed_scale = ttk.Scale(control_frame, from_=100, to=2000, 
                               variable=self.speed_var, orient=tk.HORIZONTAL,
                               command=self.update_speed)
        speed_scale.pack(side=tk.LEFT, padx=5)
        
        # Canvas with optimized settings
        self.canvas = tk.Canvas(self.master, width=BOUNDARY_X * 50, height=BOUNDARY_Y * 50,
                               bg='white', highlightthickness=0)
        self.canvas.pack(padx=5, pady=5)
        
        # Stats frame
        stats_frame = ttk.Frame(self.master)
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stats_label = ttk.Label(stats_frame, text="", font=("Arial", 10))
        self.stats_label.pack()
        
        # Store canvas items for incremental updates
        self.canvas_items = {}
        self._initialize_canvas_items()
    
    def _initialize_canvas_items(self):
        """Initialize canvas items for incremental updates"""
        for row in range(BOUNDARY_Y):
            for col in range(BOUNDARY_X):
                x1, y1 = col * 50, row * 50
                x2, y2 = x1 + 50, y1 + 50
                center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
                
                # Create invisible text items
                item_id = self.canvas.create_text(center_x, center_y, text="", 
                                                font=("Arial", 16), fill="white")
                self.canvas_items[(row, col)] = item_id
    
    def update_canvas(self):
        """Optimized canvas update with incremental rendering"""
        for row in range(BOUNDARY_Y):
            for col in range(BOUNDARY_X):
                entity = self.game_board.world[row][col]
                item_id = self.canvas_items[(row, col)]
                
                # Update text and color based on entity type
                if entity == EntityType.ANT:
                    self.canvas.itemconfig(item_id, text=EntityType.ANT.value, fill="black")
                elif entity == EntityType.FRUIT:
                    self.canvas.itemconfig(item_id, text=EntityType.FRUIT.value, fill="green")
                else:
                    self.canvas.itemconfig(item_id, text="", fill="white")
        
        # Update stats
        self.update_stats()
    
    def update_stats(self):
        """Update statistics display"""
        stats = self.game_board.get_stats()
        self.stats_label.config(
            text=f"Ants: {stats['ants']} | Fruits: {stats['fruits']} | "
                 f"Total Energy: {stats['total_energy']} | Empty: {stats['empty_spaces']} | "
                 f"Frames: {self.frame_count}"
        )
        self.last_stats = stats
    
    def update_speed(self, value):
        """Update simulation speed"""
        self.simulation_speed = int(value)
    
    def start_simulation(self):
        """Start the simulation with optimized loop"""
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.simulation_loop()
    
    def stop_simulation(self):
        """Stop the simulation"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def simulation_loop(self):
        """Optimized simulation loop"""
        if not self.is_running:
            return
            
        # Update game state
        self.game_board.move_ants()
        
        # Update display
        self.update_canvas()
        self.frame_count += 1
        
        # Schedule next update
        self.master.after(self.simulation_speed, self.simulation_loop)
def main() -> None:
    """Main function for GUI application"""
    root = tk.Tk()
    game_gui = OptimizedGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()