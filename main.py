"""
ASCII Art Generator - Main GUI Application
GUI-based control panel for selecting images and launching animations
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
import os
import threading
from ascii_converter import ASCIIConverter
from ascii_animator import ASCIIAnimator


class ASCIIArtGUI:
    def __init__(self, root):
        """
        Initialize the main GUI window
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("ASCII Art Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Variables
        self.selected_file = None
        self.current_color = (255, 255, 255)  # Default white
        # Increased resolution for clarity (250 width base)
        self.converter = ASCIIConverter(target_width=250)
        
        # Configure style
        self.setup_styles()
        
        # Create GUI elements
        self.create_widgets()
        
    def setup_styles(self):
        """
        Setup custom styles for the GUI
        """
        self.root.configure(bg='#1a1a1a')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Button style
        style.configure('Custom.TButton',
                       background='#00ff00',
                       foreground='black',
                       font=('Arial', 12, 'bold'),
                       padding=10)
        
    def create_widgets(self):
        """
        Create all GUI widgets
        """
        # Title
        title_label = tk.Label(
            self.root,
            text="ASCII ART GENERATOR",
            font=('Courier', 24, 'bold'),
            bg='#1a1a1a',
            fg='#00ff00'
        )
        title_label.pack(pady=30)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="Transform your images into animated ASCII art",
            font=('Arial', 10),
            bg='#1a1a1a',
            fg='#888888'
        )
        subtitle_label.pack(pady=5)
        
        # Select Image Button
        self.select_btn = tk.Button(
            self.root,
            text="📁 SELECT IMAGE FROM DEVICE",
            font=('Arial', 14, 'bold'),
            bg='#00ff00',
            fg='black',
            activebackground='#00cc00',
            activeforeground='black',
            command=self.select_image,
            cursor='hand2',
            padx=20,
            pady=15,
            relief=tk.RAISED,
            bd=3
        )
        self.select_btn.pack(pady=30)
        
        # Selected file display
        self.file_label = tk.Label(
            self.root,
            text="No file selected",
            font=('Arial', 10),
            bg='#1a1a1a',
            fg='#00ff00',
            wraplength=500
        )
        self.file_label.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Status: Ready",
            font=('Courier', 11),
            bg='#1a1a1a',
            fg='#00ff00'
        )
        self.status_label.pack(pady=20)
        
        # Animation settings frame
        settings_frame = tk.Frame(self.root, bg='#1a1a1a')
        settings_frame.pack(pady=10)
        
        # Duration control
        speed_label = tk.Label(
            settings_frame,
            text="Duration (seconds):",
            font=('Arial', 10),
            bg='#1a1a1a',
            fg='#888888'
        )
        speed_label.grid(row=0, column=0, padx=10)
        
        self.duration_var = tk.IntVar(value=8)  # Default 8 seconds
        duration_slider = tk.Scale(
            settings_frame,
            from_=5,
            to=20,
            orient=tk.HORIZONTAL,
            variable=self.duration_var,
            bg='#1a1a1a',
            fg='#00ff00',
            highlightbackground='#1a1a1a',
            troughcolor='#333333',
            activebackground='#00ff00'
        )
        duration_slider.grid(row=0, column=1, padx=10)

        # Animation Mode Selection
        anim_label = tk.Label(
            settings_frame,
            text="Animation Style:",
            font=('Arial', 10),
            bg='#1a1a1a',
            fg='#888888'
        )
        anim_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.animation_var = tk.StringVar(value="Matrix")
        anim_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.animation_var,
            values=["Circular", "Spiral", "Radar", "Matrix", "Vertical", "Dissolve"],
            state="readonly",
            width=15
        )
        anim_combo.grid(row=1, column=1, padx=10, pady=10)
        
        # Color Selection
        color_label = tk.Label(
            settings_frame,
            text="ASCII Color:",
            font=('Arial', 10),
            bg='#1a1a1a',
            fg='#888888'
        )
        color_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.color_btn = tk.Button(
            settings_frame,
            text="Choose Color",
            font=('Arial', 9),
            bg='#00ff00',
            fg='black',
            command=self.choose_color,
            cursor='hand2',
            padx=10,
            pady=5
        )
        self.color_btn.grid(row=2, column=1, padx=10, pady=10)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Press ESC to close animation | Press R to restart",
            font=('Arial', 8),
            bg='#1a1a1a',
            fg='#555555'
        )
        instructions.pack(side=tk.BOTTOM, pady=10)
        
    def select_image(self):
        """
        Open file dialog to select an image
        """
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("PNG Files", "*.png"),
                ("BMP Files", "*.bmp"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.selected_file = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=f"Selected: {filename}")
            self.status_label.config(text="Status: Image selected, processing...")
            
            # Start animation in separate thread to avoid freezing GUI
            threading.Thread(target=self.start_animation, daemon=True).start()
    
    def start_animation(self):
        """
        Process image and start animation
        """
        try:
            # Update status
            self.status_label.config(text="Status: Converting to ASCII...")
            
            # Convert image to ASCII
            ascii_data = self.converter.image_to_ascii_data(self.selected_file)
            
            # Update status
            self.status_label.config(text=f"Status: Starting {self.animation_var.get()} animation...")
            
            # Create and run animator
            animator = ASCIIAnimator(
                ascii_data, 
                mode=self.animation_var.get(),
                duration_seconds=self.duration_var.get(),
                color=self.current_color
            )
            
            # Update status
            self.status_label.config(text="Status: Animation running...")
            
            # Run animation (this will block until window is closed)
            animator.run_animation()
            
            # Animation finished
            self.status_label.config(text="Status: Animation completed")
            
        except Exception as e:
            # Show error message
            self.status_label.config(text=f"Status: Error - {str(e)}")
            messagebox.showerror("Error", f"Failed to process image:\n{str(e)}")
    
    def choose_color(self):
        """
        Open color chooser dialog to select ASCII color
        """
        color = colorchooser.askcolor(
            title="Choose ASCII Color",
            initialcolor=self.current_color
        )
        
        if color[0]:  # color[0] is RGB tuple, color[1] is hex
            self.current_color = tuple(int(c) for c in color[0])
            # Update button color to show selected color
            hex_color = color[1]
            self.color_btn.config(bg=hex_color)
            # Change text color based on brightness for readability
            brightness = sum(self.current_color) / 3
            text_color = 'black' if brightness > 127 else 'white'
            self.color_btn.config(fg=text_color)


def main():
    """
    Main entry point
    """
    root = tk.Tk()
    app = ASCIIArtGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
