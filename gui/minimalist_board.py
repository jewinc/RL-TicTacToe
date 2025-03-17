import tkinter as tk
from tkinter import Canvas
from tictactoe.board import Symbol
from tictactoe.move import MoveType
import time


class MinimalistBoardCanvas(Canvas):
    """
    A minimalist board visualization using Canvas with sleek black and white design.
    """
    
    def __init__(self, parent, board_size=450, **kwargs):
        # Create canvas with white background
        super().__init__(parent, width=board_size, height=board_size, 
                         bg="white", highlightthickness=1, 
                         highlightbackground="#e0e0e0", **kwargs)
        
        self.board_size = board_size
        self.cell_size = board_size // 3
        
        # Colors
        self.bg_color = "white"
        self.grid_color = "#000000"  # Pure black
        self.x_color = "#000000"     # Pure black
        self.o_color = "#000000"     # Pure black
        self.highlight_color = "#e6e6e6"  # Light gray for highlighting
        
        # Line width
        self.grid_width = 3
        self.symbol_width = 6
        
        # Symbol padding (percentage of cell size)
        self.symbol_padding = 0.2
        
        # Animation speed
        self.animation_speed = 10  # milliseconds between animation frames
        
        # Mapping from coordinates to MoveType
        self.coords_to_move = {
            (0, 0): MoveType.HG, (0, 1): MoveType.HM, (0, 2): MoveType.HD,
            (1, 0): MoveType.MG, (1, 1): MoveType.MM, (1, 2): MoveType.MD,
            (2, 0): MoveType.BG, (2, 1): MoveType.BM, (2, 2): MoveType.BD
        }
        
        # Board click handler
        self.click_handler = None
        
        # Draw grid
        self.draw_grid()
        
        # Bind click event
        self.bind("<Button-1>", self.on_click)
        
        # Bind resize event - maintain aspect ratio
        self.bind("<Configure>", self.on_resize)
        
    def on_resize(self, event):
        """Handle canvas resize events to maintain square aspect ratio."""
        # Only respond to our own canvas size changes
        if event.widget == self:
            # Keep the board square
            new_size = min(event.width, event.height)
            self.board_size = new_size
            self.cell_size = new_size // 3
            
            # Redraw everything
            self.delete("all")  # Clear canvas
            self.draw_grid()
        
    def draw_grid(self):
        """Draw the tic-tac-toe grid lines."""
        # Vertical lines
        for i in range(1, 3):
            x = i * self.cell_size
            self.create_line(x, 0, x, self.board_size, 
                            width=self.grid_width, fill=self.grid_color,
                            tags="grid")
        
        # Horizontal lines
        for i in range(1, 3):
            y = i * self.cell_size
            self.create_line(0, y, self.board_size, y, 
                            width=self.grid_width, fill=self.grid_color,
                            tags="grid")
    
    def draw_board(self, board):
        """Update the canvas to reflect the current board state."""
        self.delete("symbol")  # Remove all previous symbols
        
        board_state = board.get_board()
        for row in range(3):
            for col in range(3):
                symbol = board_state[row][col]
                if symbol != Symbol.EMPTY:
                    self.draw_symbol(row, col, symbol)
    
    def draw_symbol(self, row, col, symbol):
        """Draw an X or O in the specified cell with minimalist design and simple animation."""
        x0 = col * self.cell_size
        y0 = row * self.cell_size
        padding = self.cell_size * self.symbol_padding  # padding for aesthetics
        
        if symbol == Symbol.X:
            # Animate X drawing
            self.animate_x(x0, y0, padding)
        elif symbol == Symbol.O:
            # Animate O drawing
            self.animate_o(x0, y0, padding)
    
    def animate_x(self, x0, y0, padding):
        """Animate the drawing of an X symbol."""
        # Calculate endpoints
        x1 = x0 + padding
        y1 = y0 + padding
        x2 = x0 + self.cell_size - padding
        y2 = y0 + self.cell_size - padding
        
        # First diagonal animation
        self.animate_line(x1, y1, x2, y2, "x_line1")
        
        # Schedule second diagonal animation to start after first one completes
        self.after(self.animation_speed * 10, lambda: 
            self.animate_line(x2, y1, x1, y2, "x_line2"))
    
    def animate_o(self, x0, y0, padding):
        """Animate the drawing of an O symbol using multiple arcs."""
        # Calculate coordinates for circle
        x1 = x0 + padding
        y1 = y0 + padding
        x2 = x0 + self.cell_size - padding
        y2 = y0 + self.cell_size - padding
        
        # Animate drawing circle in segments
        segments = 8  # Number of segments to draw
        arc_angle = 360 // segments
        
        for i in range(segments):
            start_angle = i * arc_angle
            tag = f"o_arc_{i}"
            
            # Schedule each segment to appear after a delay
            self.after(i * self.animation_speed * 5, lambda angle=start_angle, tag=tag: 
                self.create_arc(x1, y1, x2, y2, 
                              start=angle, extent=arc_angle,
                              style="arc",
                              width=self.symbol_width, 
                              outline=self.o_color,
                              tags=("symbol", tag)))
    
    def animate_line(self, x1, y1, x2, y2, tag_name, steps=10):
        """Animate a line drawing from (x1,y1) to (x2,y2)."""
        # Calculate step sizes
        dx = (x2 - x1) / steps
        dy = (y2 - y1) / steps
        
        # Create recursive animation function
        def draw_step(step):
            if step <= steps:
                # Calculate current endpoint
                curr_x = x1 + dx * step
                curr_y = y1 + dy * step
                
                # Delete previous line segment
                self.delete(tag_name)
                
                # Draw new line segment
                self.create_line(
                    x1, y1, curr_x, curr_y,
                    width=self.symbol_width, fill=self.x_color, 
                    tags=("symbol", tag_name)
                )
                
                # Schedule next step
                self.after(self.animation_speed, lambda: draw_step(step + 1))
        
        # Start animation
        draw_step(1)
            
    def highlight_win(self, winning_line):
        """Highlight the winning cells with a subtle background and animation."""
        self.delete("highlight")  # Clear previous highlights
        
        # Create highlight rectangles with fade-in effect
        for i, move in enumerate(winning_line):
            row, col = move.row, move.col
            x0 = col * self.cell_size
            y0 = row * self.cell_size
            
            # Schedule each cell to be highlighted with a slight delay
            self.after(i * 100, lambda x=x0, y=y0: 
                self.create_rectangle(
                    x, y, x + self.cell_size, y + self.cell_size,
                    fill=self.highlight_color, 
                    tags="highlight", 
                    outline=""
                )
            )
            
        # Redraw symbols on top of highlights after delay
        self.after(350, lambda: self.lift("symbol"))
            
    def clear_highlights(self):
        """Clear any win highlights."""
        self.delete("highlight")
    
    def on_click(self, event):
        """Handle click events on the board."""
        if not self.click_handler:
            return
            
        # Calculate which cell was clicked
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        # Make sure it's a valid cell
        if 0 <= row < 3 and 0 <= col < 3:
            move = self.coords_to_move[(row, col)]
            self.click_handler(move)
    
    def set_click_handler(self, handler):
        """Set the function to call when a cell is clicked."""
        self.click_handler = handler