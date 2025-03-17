import tkinter as tk
from tkinter import font as tkfont


class MinimalistStyle:
    """
    A class to apply a minimalist black and white style to the TicTacToe GUI.
    """
    
    @staticmethod
    def apply_to_app(app):
        """Apply minimalist styling to a TicTacToeGUI instance."""
        root = app.root
        style = app.style
        
        # Define colors
        colors = {
            "bg": "white",
            "fg": "black",
            "accent": "#f0f0f0",
            "border": "#e0e0e0",
            "highlight": "#f8f8f8",
            "disabled": "#cccccc",
        }
        
        # Set app colors
        app.bg_color = colors["bg"]
        app.accent_color = colors["accent"]
        app.x_color = "black"
        app.o_color = "black"
        
        # Configure root window
        root.configure(bg=colors["bg"])
        
        # Create custom fonts
        title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        header_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
        body_font = tkfont.Font(family="Helvetica", size=11)
        
        # Configure ttk styles
        style.configure("TFrame", background=colors["bg"])
        style.configure("TLabel", background=colors["bg"], foreground=colors["fg"], font=body_font)
        style.configure("TButton", 
                        font=body_font,
                        relief="flat",
                        borderwidth=1)
        
        style.map("TButton",
                 background=[("active", colors["accent"]), ("disabled", colors["disabled"])],
                 foreground=[("disabled", "#666666")])
        
        style.configure("Header.TLabel", font=header_font)
        style.configure("Title.TLabel", font=title_font)
        
        # LabelFrame styling
        style.configure("TLabelframe", background=colors["bg"])
        style.configure("TLabelframe.Label", background=colors["bg"], foreground=colors["fg"], font=body_font)
        
        # Entry styling
        style.configure("TEntry", fieldbackground="white")
        
        # Combobox styling
        style.configure("TCombobox", 
                        background=colors["bg"], 
                        fieldbackground="white",
                        selectbackground=colors["accent"],
                        selectforeground=colors["fg"])
        
        # Progressbar styling
        style.configure("TProgressbar", background="black", troughcolor=colors["border"])
        
        # Don't try to recursively style widgets - this was causing the error
        
        return app

def create_minimalist_board(app):
    """Replace the regular board with a minimalist board."""
    from gui.minimalist_board import MinimalistBoardCanvas
    
    # Remove old board
    if hasattr(app, 'board_canvas'):
        app.board_canvas.pack_forget()
    
    # Create new minimalist board
    app.board_canvas = MinimalistBoardCanvas(app.right_panel, board_size=450)
    app.board_canvas.pack(pady=(0, 20))
    app.board_canvas.set_click_handler(app.handle_board_click)
    
    return app