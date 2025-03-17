import tkinter as tk
from tkinter import ttk, messagebox, IntVar, StringVar
import os
import sys
import time
import threading
import logging

# Add the parent directory to the path so we can import the tictactoe modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the required modules from the tictactoe package
from tictactoe.board import Board, Symbol
from tictactoe.player import Player, PlayerType, HumanPlayer
from tictactoe.move import MoveType
from tictactoe.player_manager import PlayerManager
from tictactoe.agents_collection.random_agent import RandomAgent
from tictactoe.agents_collection.minimax_agent import MinimaxAgent
from tictactoe.agents_collection.reinforcement_agent import ReinforcementAgent, ModelDifficulty

# Import the minimalist board visualization
from gui.minimalist_board import MinimalistBoardCanvas

# Import the configuration and player options
from config import Config


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Demonstration")
        self.root.geometry(Config.WINDOW_SIZE)
        self.root.resizable(True, True)
        
        # Set theme and styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colors
        self.bg_color = Config.BG_COLOR
        self.accent_color = Config.ACCENT_COLOR
        self.x_color = Config.X_COLOR
        self.o_color = Config.O_COLOR
        
        self.root.configure(bg=self.bg_color)
        
        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 11))
        self.style.configure('Header.TLabel', font=('Arial', 22, 'bold'))
        self.style.configure('Subheader.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Status.TLabel', font=('Arial', 14))
        
        # Game state initialization
        self.board = Board()
        self.player_types = {
            "Human": lambda name: HumanPlayer(name),
            "Random Agent": lambda _: RandomAgent(),
            "Minimax Agent": lambda _: MinimaxAgent(use_alpha_beta=False),
            "Minimax Agent (Alpha-Beta)": lambda _: MinimaxAgent(use_alpha_beta=True),
            "RL Agent (Easy)": lambda _: ReinforcementAgent(ModelDifficulty.EASY),
            "RL Agent (Medium)": lambda _: ReinforcementAgent(ModelDifficulty.MEDIUM),
            "RL Agent (Hard)": lambda _: ReinforcementAgent(ModelDifficulty.HARD)
        }
        self.game_active = False
        self.auto_play = False
        self.auto_play_thread = None
        self.stop_auto_play = False
        self.current_player = None
        self.player_manager = None
        self.game_stats = {
            "X_wins": 0,
            "O_wins": 0,
            "Draws": 0,
            "Games": 0
        }
        
        # Winning line coordinates for highlighting
        self.winning_lines = {
            "H_row": MoveType.H_row(),
            "M_row": MoveType.M_row(),
            "B_row": MoveType.B_row(),
            "G_col": MoveType.G_col(),
            "M_col": MoveType.M_col(),
            "D_col": MoveType.D_col(),
            "H_diag": MoveType.H_diag(),
            "D_diag": MoveType.D_diag()
        }
        
        # Auto-play settings
        self.max_games = IntVar(value=10)
        self.delay_between_moves = IntVar(value=500)  # milliseconds
        self.delay_between_games = IntVar(value=1000)  # milliseconds
        
        # Create the widgets
        self.create_widgets()
        
        # Bind resize event to handle resizing properly
        self.root.bind("<Configure>", self.on_resize)
        
    def create_widgets(self):
        # Main container with padding that expands
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Main frame with padding - centered
        self.main_frame = ttk.Frame(self.main_container, padding=20)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title
        self.title_label = ttk.Label(self.main_frame, 
                               text="Tic-Tac-Toe Demonstration", 
                               style='Header.TLabel')
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel - Settings & Stats
        self.left_panel = ttk.Frame(self.main_frame, padding=10)
        self.left_panel.grid(row=1, column=0, sticky="n", padx=(0, 30))
        
        # Player Selection Frame
        self.player_frame = ttk.LabelFrame(self.left_panel, text="Player Setup", padding=10)
        self.player_frame.pack(fill="x", pady=(0, 20))
        
        # Player X setup
        self.player_x_label = ttk.Label(self.player_frame, text="Player X:")
        self.player_x_label.grid(row=0, column=0, sticky="w", pady=5)
        
        self.player_x_var = tk.StringVar(value="Human")
        self.player_x_combo = ttk.Combobox(self.player_frame, 
                                          textvariable=self.player_x_var,
                                          values=list(self.player_types.keys()),
                                          width=15)
        self.player_x_combo.grid(row=0, column=1, padx=5, pady=5)
        
        self.player_x_name_label = ttk.Label(self.player_frame, text="Name:")
        self.player_x_name_label.grid(row=0, column=2, sticky="w", padx=(10, 5), pady=5)
        
        self.player_x_name_var = tk.StringVar(value="Player X")
        self.player_x_name_entry = ttk.Entry(self.player_frame, 
                                           textvariable=self.player_x_name_var,
                                           width=15)
        self.player_x_name_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Player O setup
        self.player_o_label = ttk.Label(self.player_frame, text="Player O:")
        self.player_o_label.grid(row=1, column=0, sticky="w", pady=5)
        
        self.player_o_var = tk.StringVar(value="Random Agent")
        self.player_o_combo = ttk.Combobox(self.player_frame, 
                                          textvariable=self.player_o_var,
                                          values=list(self.player_types.keys()),
                                          width=15)
        self.player_o_combo.grid(row=1, column=1, padx=5, pady=5)
        
        self.player_o_name_label = ttk.Label(self.player_frame, text="Name:")
        self.player_o_name_label.grid(row=1, column=2, sticky="w", padx=(10, 5), pady=5)
        
        self.player_o_name_var = tk.StringVar(value="Player O")
        self.player_o_name_entry = ttk.Entry(self.player_frame, 
                                           textvariable=self.player_o_name_var,
                                           width=15)
        self.player_o_name_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Auto-play settings
        self.auto_frame = ttk.LabelFrame(self.left_panel, text="Auto-Play Settings", padding=10)
        self.auto_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(self.auto_frame, text="Max Games:").grid(row=0, column=0, sticky="w", pady=5)
        max_games_entry = ttk.Entry(self.auto_frame, textvariable=self.max_games, width=5)
        max_games_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(self.auto_frame, text="Move Delay (ms):").grid(row=1, column=0, sticky="w", pady=5)
        move_delay_entry = ttk.Entry(self.auto_frame, textvariable=self.delay_between_moves, width=5)
        move_delay_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(self.auto_frame, text="Game Delay (ms):").grid(row=2, column=0, sticky="w", pady=5)
        game_delay_entry = ttk.Entry(self.auto_frame, textvariable=self.delay_between_games, width=5)
        game_delay_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Game controls
        self.controls_frame = ttk.LabelFrame(self.left_panel, text="Game Controls", padding=10)
        self.controls_frame.pack(fill="x", pady=(0, 20))
        
        # Game buttons row 1
        self.controls_row1 = ttk.Frame(self.controls_frame)
        self.controls_row1.pack(fill="x", pady=(0, 5))
        
        self.start_button = ttk.Button(self.controls_row1, 
                                    text="Start Game", 
                                    command=self.start_game)
        self.start_button.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 2))
        
        self.stop_button = ttk.Button(self.controls_row1, 
                                    text="Stop Game", 
                                    command=self.stop_game,
                                    state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, fill="x", expand=True, padx=(2, 0))
        
        # Game buttons row 2
        self.controls_row2 = ttk.Frame(self.controls_frame)
        self.controls_row2.pack(fill="x", pady=5)
        
        self.reset_board_button = ttk.Button(self.controls_row2, 
                                          text="Reset Board", 
                                          command=self.reset_board,
                                          state=tk.DISABLED)
        self.reset_board_button.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 2))
        
        self.reset_stats_button = ttk.Button(self.controls_row2, 
                                          text="Reset Stats", 
                                          command=self.reset_stats)
        self.reset_stats_button.pack(side=tk.RIGHT, fill="x", expand=True, padx=(2, 0))
        
        # Auto-play button
        self.auto_play_button = ttk.Button(self.controls_frame, 
                                         text="Start Auto-Play", 
                                         command=self.toggle_auto_play)
        self.auto_play_button.pack(fill="x", pady=(5, 0))
        
        # Game Statistics
        self.stats_frame = ttk.LabelFrame(self.left_panel, text="Game Statistics", padding=10)
        self.stats_frame.pack(fill="x")
        
        # Stats labels
        self.turn_label = ttk.Label(self.stats_frame, 
                                  text="Current Turn:", 
                                  font=('Arial', 12, 'bold'))
        self.turn_label.pack(anchor="w", pady=(0, 5))
        
        self.turn_value = ttk.Label(self.stats_frame, text="-")
        self.turn_value.pack(anchor="w", pady=(0, 10))
        
        self.stats_label = ttk.Label(self.stats_frame, 
                                   text="Results:", 
                                   font=('Arial', 12, 'bold'))
        self.stats_label.pack(anchor="w", pady=(0, 5))
        
        # Stats table (grid)
        self.stats_frame_inner = ttk.Frame(self.stats_frame)
        self.stats_frame_inner.pack(fill="x")
        
        ttk.Label(self.stats_frame_inner, text="X Wins:").grid(row=0, column=0, sticky="w", pady=2)
        self.x_wins_label = ttk.Label(self.stats_frame_inner, text="0")
        self.x_wins_label.grid(row=0, column=1, sticky="e", pady=2)
        
        ttk.Label(self.stats_frame_inner, text="O Wins:").grid(row=1, column=0, sticky="w", pady=2)
        self.o_wins_label = ttk.Label(self.stats_frame_inner, text="0")
        self.o_wins_label.grid(row=1, column=1, sticky="e", pady=2)
        
        ttk.Label(self.stats_frame_inner, text="Draws:").grid(row=2, column=0, sticky="w", pady=2)
        self.draws_label = ttk.Label(self.stats_frame_inner, text="0")
        self.draws_label.grid(row=2, column=1, sticky="e", pady=2)
        
        ttk.Label(self.stats_frame_inner, text="Total Games:").grid(row=3, column=0, sticky="w", pady=2)
        self.total_games_label = ttk.Label(self.stats_frame_inner, text="0")
        self.total_games_label.grid(row=3, column=1, sticky="e", pady=2)
        
        # Progress indicator for auto-play
        self.progress_frame = ttk.Frame(self.stats_frame)
        self.progress_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Label(self.progress_frame, text="Auto-Play Progress:").pack(anchor="w", pady=(0, 5))
        
        self.progress_var = StringVar(value="0 / 0")
        self.progress_label = ttk.Label(self.progress_frame, textvariable=self.progress_var)
        self.progress_label.pack(anchor="w", pady=(0, 5))
        
        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(fill="x", pady=(0, 5))
        
        # Right panel - Game Board
        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.grid(row=1, column=1, sticky="nsew")
        
        # Create minimalist board
        self.board_canvas = MinimalistBoardCanvas(self.right_panel, board_size=450)
        self.board_canvas.pack(pady=(0, 20))
        self.board_canvas.set_click_handler(self.handle_board_click)
        
        # Status message with improved readability
        status_frame = ttk.Frame(self.right_panel)
        status_frame.pack(fill="x", expand=True)
        
        self.status_var = tk.StringVar(value="Welcome to Tic-Tac-Toe! Configure players and click 'Start Game'.")
        self.status_label = ttk.Label(status_frame, 
                                    textvariable=self.status_var,
                                    style="Status.TLabel",
                                    wraplength=450,
                                    justify="center",
                                    background="#f0f0f0",  # Light background for better readability
                                    relief="groove",  # Slight border for emphasis
                                    padding=10)      # More padding for better readability
        self.status_label.pack(fill="x", expand=True)
        
        # Configure grid weights to make the UI responsive
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Set up event handlers
        self.player_x_combo.bind("<<ComboboxSelected>>", self.update_player_name_entry)
        self.player_o_combo.bind("<<ComboboxSelected>>", self.update_player_name_entry)
        
        # Initialize state
        self.update_player_name_entry()
    
    def on_resize(self, event):
        """Handle window resize events to keep the UI centered."""
        # Only respond to window size changes, not internal widget resizes
        if event.widget == self.root:
            # Recenter the main frame in the container
            self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def update_player_name_entry(self, event=None):
        """Enable or disable name entry based on player type selection."""
        # Player X
        if self.player_x_var.get() == "Human":
            self.player_x_name_entry.configure(state="normal")
        else:
            self.player_x_name_entry.configure(state="disabled")
            
        # Player O
        if self.player_o_var.get() == "Human":
            self.player_o_name_entry.configure(state="normal")
        else:
            self.player_o_name_entry.configure(state="disabled")
            
        # Enable auto-play button if both players are agents
        if self.player_x_var.get() != "Human" and self.player_o_var.get() != "Human":
            self.auto_play_button.configure(state="normal")
        else:
            self.auto_play_button.configure(state="disabled")

    def start_game(self):
        """Start a new game with the configured players."""
        # Reset the board
        self.board = Board()
        self.board_canvas.draw_board(self.board)
        self.board_canvas.clear_highlights()
        
        # Create players
        player_x_type = self.player_x_var.get()
        player_o_type = self.player_o_var.get()
        
        player_x_name = self.player_x_name_var.get() if player_x_type == "Human" else player_x_type
        player_o_name = self.player_o_name_var.get() if player_o_type == "Human" else player_o_type
        
        player_x = self.player_types[player_x_type](player_x_name)
        player_o = self.player_types[player_o_type](player_o_name)
        
        # Set up player manager
        self.player_manager = PlayerManager(player_x, player_o)
        
        # Enable/disable buttons
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        self.reset_board_button.configure(state=tk.NORMAL)
        self.player_x_combo.configure(state=tk.DISABLED)
        self.player_o_combo.configure(state=tk.DISABLED)
        self.player_x_name_entry.configure(state=tk.DISABLED)
        self.player_o_name_entry.configure(state=tk.DISABLED)
        
        # Update auto-play button state
        if not self.auto_play:
            self.auto_play_button.configure(state=tk.DISABLED)
        
        # Start game
        self.game_active = True
        self.status_var.set("Game started! " + self.get_turn_message())
        
        # Update turn indicator
        self.update_turn_indicator()
        
        # If first player is an agent, make its move
        self.check_agent_turn()

    def stop_game(self):
        """Stop the current game."""
        if self.auto_play:
            self.stop_auto_play = True
            self.auto_play = False
            self.auto_play_button.configure(text="Start Auto-Play")
            self.status_var.set("Auto-play stopped.")
            
            # Reset the board
            if self.game_active:
                self.board.reset()
                self.board_canvas.draw_board(self.board)
                self.board_canvas.clear_highlights()
                self.game_active = False
                
            # Re-enable UI elements
            self._reset_after_stop()
        else:
            self.end_game()
            self.status_var.set("Game stopped.")

    def reset_board(self):
        """Reset the game board but keep the same players."""
        # Reset the board
        self.board.reset()
        self.board_canvas.draw_board(self.board)
        self.board_canvas.clear_highlights()
        
        # Reset player manager
        if self.player_manager:
            self.player_manager.reset()
        
        self.game_active = True
        self.status_var.set("Board reset. " + self.get_turn_message())
        
        # Update turn indicator
        self.update_turn_indicator()
        
        # If first player is an agent, make its move
        self.check_agent_turn()

    def reset_stats(self):
        """Reset all game statistics."""
        self.game_stats = {
            "X_wins": 0,
            "O_wins": 0,
            "Draws": 0,
            "Games": 0
        }
        
        # Update labels
        self.x_wins_label.configure(text="0")
        self.o_wins_label.configure(text="0")
        self.draws_label.configure(text="0")
        self.total_games_label.configure(text="0")
        
        # Reset progress
        self.progress_var.set("0 / 0")
        self.progress["value"] = 0
        
        self.status_var.set("Statistics reset.")

    def toggle_auto_play(self):
        """Toggle auto-play mode for agent vs agent games."""
        if self.auto_play:
            # Stop auto-play
            self.stop_auto_play = True
            self.auto_play_button.configure(text="Start Auto-Play")
            self.status_var.set("Stopping auto-play...")
        else:
            # Start auto-play
            if self.player_x_var.get() == "Human" or self.player_o_var.get() == "Human":
                messagebox.showwarning("Auto-Play", "Auto-play is only available for agent vs agent games.")
                return
            
            # Get max games value
            try:
                max_games = self.max_games.get()
                if max_games <= 0:
                    messagebox.showwarning("Auto-Play", "Maximum games must be a positive number.")
                    return
            except:
                messagebox.showwarning("Auto-Play", "Invalid maximum games value.")
                return
            
            # Disable controls
            self.start_button.configure(state=tk.DISABLED)
            self.reset_board_button.configure(state=tk.DISABLED)
            self.player_x_combo.configure(state=tk.DISABLED)
            self.player_o_combo.configure(state=tk.DISABLED)
            self.player_x_name_entry.configure(state=tk.DISABLED)
            self.player_o_name_entry.configure(state=tk.DISABLED)
            
            # Enable stop button
            self.stop_button.configure(state=tk.NORMAL)
            
            # Update button text and state
            self.auto_play_button.configure(text="Stop Auto-Play")
            
            # Start auto-play
            self.auto_play = True
            self.stop_auto_play = False
            
            # Reset progress
            self.progress["maximum"] = max_games
            self.progress["value"] = 0
            self.progress_var.set(f"0 / {max_games}")
            
            # Start auto-play using Tkinter's after method instead of a thread
            self.status_var.set("Starting auto-play...")
            self.root.after(100, lambda: self.run_auto_play_iteration(0, max_games))

    def run_auto_play(self):
        """Run multiple games automatically for agent vs agent play."""
        max_games = self.max_games.get()
        move_delay = self.delay_between_moves.get() / 1000
        game_delay = self.delay_between_games.get() / 1000
        
        games_played = 0
        
        while games_played < max_games and not self.stop_auto_play:
            # If there's no active game, start a new one
            if not self.game_active:
                # Start a new game (use the main thread to ensure thread safety)
                self.root.after(0, self.start_game)
                
                # Wait for game to start
                time.sleep(0.1)
            
            # Wait until game ends or we're asked to stop
            while self.game_active and not self.stop_auto_play:
                time.sleep(0.1)
                
            # If auto-play was stopped, break out of the loop
            if self.stop_auto_play:
                break
                
            # Update progress
            games_played += 1
            self.root.after(0, lambda count=games_played, total=max_games: self.update_progress(count, total))
            
            # Delay between games
            time.sleep(game_delay)
        
        # End auto-play
        if not self.stop_auto_play:
            self.root.after(0, self.end_auto_play)
        else:
            # Make sure UI is properly reset if stopped manually
            self.root.after(0, self._reset_after_stop)

    def _reset_after_stop(self):
        """Reset UI after auto-play is manually stopped."""
        self.auto_play = False
        self.auto_play_button.configure(text="Start Auto-Play")
        self.stop_button.configure(state=tk.DISABLED)
        self.start_button.configure(state=tk.NORMAL)
        self.player_x_combo.configure(state=tk.NORMAL)
        self.player_o_combo.configure(state=tk.NORMAL)
        self.update_player_name_entry()
        
        # Set status
        self.status_var.set(f"Auto-play stopped after {self.game_stats['Games']} games.")

    def update_progress(self, current, total):
        """Update the progress display for auto-play."""
        self.progress_var.set(f"{current} / {total}")
        self.progress["value"] = current

    def run_auto_play_iteration(self, games_played, max_games):
        """Run a single iteration of auto-play using Tkinter's after method."""
        if games_played >= max_games or self.stop_auto_play:
            self.end_auto_play()
            return
        
        # Reset board for a new game if needed
        if not self.game_active:
            self.reset_board()
            # Add a small delay before starting to process agent moves
            self.root.after(100, lambda: self.process_auto_play_game(games_played, max_games))
        else:
            # Game is already active, just process it
            self.process_auto_play_game(games_played, max_games)

    def process_auto_play_game(self, games_played, max_games):
        """Process a single auto-play game until completion."""
        if not self.game_active or self.stop_auto_play:
            # Either game ended or auto-play was stopped
            if self.stop_auto_play:
                self.end_auto_play()
            else:
                # Game ended naturally, update progress and start next game
                games_played += 1
                self.update_progress(games_played, max_games)
                # Delay before starting next game
                self.root.after(self.delay_between_games.get(), 
                            lambda: self.run_auto_play_iteration(games_played, max_games))
            return
        
        # Process current player's move if it's an agent
        current_player = self.player_manager.current_player
        if current_player.player_type == PlayerType.AGENT:
            try:
                # Choose and execute the move
                move = current_player.choose_move(self.board)
                self.make_move(move)
                
                # Schedule next check after a delay
                self.root.after(self.delay_between_moves.get(), 
                            lambda: self.process_auto_play_game(games_played, max_games))
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during auto-play: {e}")
                self.stop_auto_play = True
                self.end_auto_play()
        else:
            # If it's somehow a human player's turn during auto-play, move to next game
            messagebox.showwarning("Auto-Play", "Human player detected during auto-play. Ending current game.")
            self.end_game()
            self.root.after(100, lambda: self.run_auto_play_iteration(games_played, max_games))

    def end_auto_play(self):
        """End auto-play mode and update UI."""
        self.auto_play = False
        self.auto_play_button.configure(text="Start Auto-Play")
        self.stop_button.configure(state=tk.DISABLED)
        self.start_button.configure(state=tk.NORMAL)
        self.player_x_combo.configure(state=tk.NORMAL)
        self.player_o_combo.configure(state=tk.NORMAL)
        self.reset_board_button.configure(state=tk.NORMAL)
        self.update_player_name_entry()
        
        # Set status
        games_played = self.game_stats['Games']
        if self.stop_auto_play:
            self.status_var.set(f"Auto-play stopped after {games_played} games.")
        else:
            self.status_var.set(f"Auto-play completed: {games_played} games played.")
        
        # Reset flags
        self.stop_auto_play = False
        
    def get_turn_message(self):
        """Get a message about whose turn it is."""
        if not self.game_active or not self.player_manager:
            return ""
            
        current_player = self.player_manager.current_player
        return f"It's {current_player}'s turn ({current_player.symbol.value})."

    def update_turn_indicator(self):
        """Update the turn indicator in the UI."""
        if not self.game_active or not self.player_manager:
            self.turn_value.configure(text="-")
            return
            
        current_player = self.player_manager.current_player
        symbol = current_player.symbol.value
        
        # Change text color based on player symbol
        if symbol == "X":
            self.turn_value.configure(text=f"{symbol} - {current_player}", foreground=self.x_color)
        else:
            self.turn_value.configure(text=f"{symbol} - {current_player}", foreground=self.o_color)

    def handle_board_click(self, move):
        """Handle a click on the board canvas."""
        if not self.game_active or self.auto_play:
            return
            
        current_player = self.player_manager.current_player
        
        # Only process clicks if it's a human player's turn
        if current_player.player_type == PlayerType.HUMAN and self.board.is_move_valid(move):
            self.make_move(move)

    def make_move(self, move):
        """Make a move on the board."""
        if not self.game_active:
            return
            
        current_player = self.player_manager.current_player
        
        # Make sure the move is valid
        if not self.board.is_move_valid(move):
            if not self.auto_play:  # Only show message if not in auto-play mode
                messagebox.showwarning("Invalid Move", "That move is not valid. Please try again.")
            return False
        
        try:
            # Make the move
            self.board.set_move(move, current_player.symbol)
            self.board_canvas.draw_board(self.board)
            
            # Check for win or draw
            if self.check_game_end():
                return True
            
            # Switch player
            self.player_manager.switch_player()
            self.update_turn_indicator()
            self.status_var.set(self.get_turn_message())
            
            # If next player is an agent, make its move
            self.check_agent_turn()
            return True
        except Exception as e:
            logging.error(f"Error making move: {e}")
            if not self.auto_play:  # Only show message if not in auto-play mode
                messagebox.showerror("Error", f"An error occurred while making a move: {e}")
            return False

    def check_agent_turn(self):
        """Check if it's an agent's turn and make a move if it is."""
        if not self.game_active:
            return
            
        current_player = self.player_manager.current_player
        
        # If it's an agent's turn
        if current_player.player_type == PlayerType.AGENT:
            # Set status
            self.status_var.set(f"{current_player} is thinking...")
            self.root.update_idletasks()  # Force update UI
            
            # Add a delay for better presentation/visualization
            if self.auto_play:
                delay = min(self.delay_between_moves.get(), 100)  # Faster for auto-play
            else:
                delay = self.delay_between_moves.get()
                
            # Check again if game is still active before scheduling the agent move
            if self.game_active:
                self.root.after(delay, self.execute_agent_move)

    def execute_agent_move(self):
        """Execute an agent's move after a delay."""
        # Check again if the game is still active
        if not self.game_active or self.stop_auto_play:
            return
            
        current_player = self.player_manager.current_player
        
        # Make sure it's still an agent's turn
        if current_player.player_type == PlayerType.AGENT:
            try:
                # Get the move
                move = current_player.choose_move(self.board)
                
                # Check again if game is still active
                if not self.game_active or self.stop_auto_play:
                    return
                    
                # Make the move
                success = self.make_move(move)
                
                # If the move wasn't successful and we're in auto-play mode,
                # we should end the game to avoid getting stuck
                if not success and self.auto_play:
                    self.status_var.set(f"Invalid move from {current_player}. Ending game.")
                    self.end_game()
                    
            except Exception as e:
                error_msg = f"An error occurred during the agent's move: {e}"
                logging.error(error_msg)
                
                if self.game_active:  # Only show error if game is still active
                    if not self.auto_play:  # Only show dialog if not in auto-play
                        messagebox.showerror("Error", error_msg)
                    self.end_game()

    def end_game(self):
        """End the current game and update UI."""
        self.game_active = False
        
        # Keep stop button enabled during auto-play
        if not self.auto_play:
            self.stop_button.configure(state=tk.DISABLED)
            self.start_button.configure(state=tk.NORMAL)
            self.player_x_combo.configure(state=tk.NORMAL)
            self.player_o_combo.configure(state=tk.NORMAL)
            self.reset_board_button.configure(state=tk.NORMAL)
            self.update_player_name_entry()

    def check_game_end(self):
        """Check if the game has ended and update the UI accordingly."""
        is_won, winner_symbol = self.board.has_winner()
        
        if is_won:
            winner = self.player_manager.get_player_from_symbol(winner_symbol)
            
            # Update stats
            if winner_symbol == Symbol.X:
                self.game_stats["X_wins"] += 1
                self.x_wins_label.configure(text=str(self.game_stats["X_wins"]))
            else:
                self.game_stats["O_wins"] += 1
                self.o_wins_label.configure(text=str(self.game_stats["O_wins"]))
            
            self.game_stats["Games"] += 1
            self.total_games_label.configure(text=str(self.game_stats["Games"]))
            
            # Find and highlight the winning line
            self.highlight_winning_line(winner_symbol)
            
            # Show winner message
            if not self.auto_play:
                self.status_var.set(f"{winner} wins!")
                self.turn_value.configure(text="Game Over")
            
            # End the game
            self.end_game()
            return True
            
        elif self.board.is_full():
            # Update draw stats
            self.game_stats["Draws"] += 1
            self.draws_label.configure(text=str(self.game_stats["Draws"]))
            
            self.game_stats["Games"] += 1
            self.total_games_label.configure(text=str(self.game_stats["Games"]))
            
            # Show draw message
            if not self.auto_play:
                self.status_var.set("It's a draw!")
                self.turn_value.configure(text="Game Over")
            
            # End the game
            self.end_game()
            return True
            
        return False

    def highlight_winning_line(self, winner_symbol):
        """Identify and highlight the winning line on the board."""
        board_state = self.board.get_board()
        
        # Check rows
        for row_idx, row_name in enumerate(["H_row", "M_row", "B_row"]):
            if all(board_state[row_idx][col] == winner_symbol for col in range(3)):
                self.board_canvas.highlight_win(self.winning_lines[row_name])
                return
                
        # Check columns
        for col_idx, col_name in enumerate(["G_col", "M_col", "D_col"]):
            if all(board_state[row][col_idx] == winner_symbol for row in range(3)):
                self.board_canvas.highlight_win(self.winning_lines[col_name])
                return
                
        # Check diagonals
        if board_state[0][0] == board_state[1][1] == board_state[2][2] == winner_symbol:
            self.board_canvas.highlight_win(self.winning_lines["H_diag"])
            return
            
        if board_state[0][2] == board_state[1][1] == board_state[2][0] == winner_symbol:
            self.board_canvas.highlight_win(self.winning_lines["D_diag"])
            return

    def end_game(self):
        """End the current game and update UI."""
        self.game_active = False
        
        # Keep stop button enabled during auto-play
        if not self.auto_play:
            self.stop_button.configure(state=tk.DISABLED)
            self.start_button.configure(state=tk.NORMAL)
            self.player_x_combo.configure(state=tk.NORMAL)
            self.player_o_combo.configure(state=tk.NORMAL)
            self.reset_board_button.configure(state=tk.NORMAL)
            self.update_player_name_entry()
            
        # If auto-play is active, this will trigger the next game in the sequence
        # The auto-play thread is waiting for game_active to become False


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()