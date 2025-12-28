# ASCII Art Generator

A beautiful GUI-based ASCII art generator with circular animation effects.

## Features

✨ **GUI-Based Control Panel** - Easy-to-use interface for selecting images  
🎨 **Circular Animation** - Stunning reveal effect from center outward  
⏱️ **Adjustable Duration** - Control animation time (5-15 seconds)  
🖼️ **Multiple Format Support** - Works with JPG, PNG, BMP, GIF  
🎮 **Interactive Controls** - Press R to restart, ESC to close  

## Installation

1. Install required libraries:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Click "SELECT IMAGE FROM DEVICE"
3. Choose an image from your computer
4. Watch the ASCII animation automatically start!

## Controls

- **ESC** - Close animation window
- **R** - Restart animation
- **Duration Slider** - Adjust ensure smooth slow animation (default 8s)

## Technical Details

- **Image Processing**: Pillow (PIL)
- **GUI**: Tkinter
- **Animation**: Pygame
- **Math**: NumPy

## Project Structure

```
ASCII art/
├── main.py              # Main GUI application
├── ascii_converter.py   # Image to ASCII conversion
├── ascii_animator.py    # Animation engine
└── requirements.txt     # Dependencies
```

## How It Works

1. **Image Loading**: Converts image to grayscale and resizes
2. **Character Mapping**: Maps pixel brightness to ASCII characters
3. **Distance Calculation**: Calculates each pixel's distance from center
4. **Circular Animation**: Reveals ASCII art from center outward

---

**Created with ❤️ for ASCII art lovers**
