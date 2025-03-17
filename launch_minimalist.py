#!/usr/bin/env python3
"""
Launch Minimalist Tic-Tac-Toe GUI

This script launches the Tic-Tac-Toe GUI with a minimalist black and white design.
"""

import os
import sys
import tkinter as tk

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the GUI components
    from gui.tictactoe_gui import TicTacToeGUI
    from gui.minimalist_style import MinimalistStyle, create_minimalist_board
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("\nPlease make sure you have the correct directory structure:")
    print("- gui/")
    print("  - tictactoe_gui.py")
    print("  - minimalist_board.py")
    print("  - minimalist_style.py")
    print("- tictactoe/ (and other required modules)")
    sys.exit(1)

def main():
    """Launch the minimalist Tic-Tac-Toe GUI."""
    print("Starting Minimalist Tic-Tac-Toe GUI...")
    
    # Create root window
    root = tk.Tk()
    root.title("Tic-Tac-Toe")
    
    # Create the GUI application
    app = TicTacToeGUI(root)
    
    # Apply minimalist styling
    MinimalistStyle.apply_to_app(app)
    
    # Replace regular board with minimalist board
    create_minimalist_board(app)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()