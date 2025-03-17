from tictactoe.agent import Agent, AgentType
from tictactoe.board import Board, Symbol
from tictactoe.move import MoveType


class MinimaxAgent(Agent):
    def __init__(self, use_alpha_beta=True):
        super().__init__(AgentType.MINIMAX)
        self.use_alpha_beta = use_alpha_beta
        
    def choose_move(self, board) -> MoveType:
        """
        Choose the best move using the Minimax algorithm with alpha-beta pruning.
        
        Args:
            board: The current game board
        
        Returns:
            MoveType: The optimal move
        """
        valid_moves = self.get_valid_moves(board)
        
        # If only one move is available, return it (optimization)
        if len(valid_moves) == 1:
            return valid_moves[0]
        
        # Initialize best score to worst possible
        best_score = float('-inf')
        best_move = None
        
        # Try each valid move
        for move in valid_moves:
            # Create a copy of the board to simulate the move
            board_copy = self._copy_board(board)
            board_copy.set_move(move, self.symbol)
            
            # Get score for this move
            if self.use_alpha_beta:
                score = self._minimax_alpha_beta(board_copy, 0, False, float('-inf'), float('inf'))
            else:
                score = self._minimax(board_copy, 0, False)
            
            # Update best move if this move is better
            if score > best_score:
                best_score = score
                best_move = move
                
            # Early exit if we found a winning move (optimization)
            if best_score == 10:
                break
        
        return best_move
    
    def _minimax(self, board, depth, is_maximizing):
        """
        Standard Minimax algorithm implementation.
        
        Args:
            board: The current board state
            depth: Current depth in the game tree
            is_maximizing: Whether it's the maximizing player's turn (AI)
        
        Returns:
            int: The best score for the current player
        """
        # Get opponent's symbol
        opponent_symbol = Symbol.O if self.symbol == Symbol.X else Symbol.X
        
        # Check for terminal states
        is_won, winner_symbol = board.has_winner()
        
        if is_won:
            if winner_symbol == self.symbol:
                return 10 - depth  # Prefer winning in fewer moves
            else:
                return depth - 10  # Avoid losing, but if must lose, prefer losing in more moves
        
        if board.is_full():
            return 0  # Draw
        
        if is_maximizing:
            # AI's turn - maximize score
            best_score = float('-inf')
            for move in MoveType.all_moves():
                if board.is_move_valid(move):
                    board_copy = self._copy_board(board)
                    board_copy.set_move(move, self.symbol)
                    score = self._minimax(board_copy, depth + 1, False)
                    best_score = max(score, best_score)
            return best_score
        else:
            # Opponent's turn - minimize score
            best_score = float('inf')
            for move in MoveType.all_moves():
                if board.is_move_valid(move):
                    board_copy = self._copy_board(board)
                    board_copy.set_move(move, opponent_symbol)
                    score = self._minimax(board_copy, depth + 1, True)
                    best_score = min(score, best_score)
            return best_score
    
    def _minimax_alpha_beta(self, board, depth, is_maximizing, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning for improved performance.
        
        Args:
            board: The current board state
            depth: Current depth in the game tree
            is_maximizing: Whether it's the maximizing player's turn (AI)
            alpha: Best value for maximizing player
            beta: Best value for minimizing player
        
        Returns:
            int: The best score for the current player
        """
        # Get opponent's symbol
        opponent_symbol = Symbol.O if self.symbol == Symbol.X else Symbol.X
        
        # Check for terminal states
        is_won, winner_symbol = board.has_winner()
        
        if is_won:
            if winner_symbol == self.symbol:
                return 10 - depth
            else:
                return depth - 10
        
        if board.is_full():
            return 0
        
        if is_maximizing:
            # AI's turn
            best_score = float('-inf')
            for move in MoveType.all_moves():
                if board.is_move_valid(move):
                    board_copy = self._copy_board(board)
                    board_copy.set_move(move, self.symbol)
                    score = self._minimax_alpha_beta(board_copy, depth + 1, False, alpha, beta)
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break  # Beta cutoff
            return best_score
        else:
            # Opponent's turn
            best_score = float('inf')
            for move in MoveType.all_moves():
                if board.is_move_valid(move):
                    board_copy = self._copy_board(board)
                    board_copy.set_move(move, opponent_symbol)
                    score = self._minimax_alpha_beta(board_copy, depth + 1, True, alpha, beta)
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break  # Alpha cutoff
            return best_score
    
    def _copy_board(self, board):
        """
        Create a deep copy of the board to simulate moves.
        
        Args:
            board: The board to copy
            
        Returns:
            Board: A new board with the same state
        """
        new_board = Board()
        for move in MoveType.all_moves():
            symbol = board.get(move)
            if symbol != Symbol.EMPTY:
                new_board.set_move(move, symbol)
        return new_board
    
    def reset(self):
        """Reset agent state if needed between games"""
        pass
    
    def __str__(self):
        pruning_text = "with α-β pruning" if self.use_alpha_beta else ""
        return f"Minimax Agent {pruning_text} (Perfect)"