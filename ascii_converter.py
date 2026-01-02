"""
ASCII Converter Module
Converts images to ASCII art with distance and angle calculations
"""

from PIL import Image, ImageEnhance, ImageOps
import numpy as np


class ASCIIConverter:
    # Extended ASCII set (Reverse ordered for Black BG)
    # Fixed escape sequence warning with double backslash
    ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    ASCII_CHARS = ASCII_CHARS[::-1]

    def __init__(self, target_width=250, target_height=100):
        self.target_width = target_width
        self.target_height = target_height
        
    def brightness_to_char(self, brightness):
        char_index = int((brightness / 255) * (len(self.ASCII_CHARS) - 1))
        return self.ASCII_CHARS[char_index]
    
    def calculate_distances(self):
        center_x = self.target_width / 2
        center_y = self.target_height / 2
        Y, X = np.indices((self.target_height, self.target_width))
        distances = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        return distances
    
    def calculate_angles(self):
        center_x = self.target_width / 2
        center_y = self.target_height / 2
        Y, X = np.indices((self.target_height, self.target_width))
        angles = np.arctan2(Y - center_y, X - center_x)
        angles = np.mod(angles, 2 * np.pi)
        return angles
    
    def image_to_ascii_data(self, image_path):
        try:
            image = Image.open(image_path)
            image = image.convert('L')
            
            # High Contrast for Hacker Look
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.8) 
            
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.5)

            font_aspect_ratio = 6 / 12  
            image_aspect_ratio = image.height / image.width
            new_height = int(self.target_width * image_aspect_ratio * font_aspect_ratio)
            self.target_height = new_height
            
            image = image.resize((self.target_width, new_height), Image.Resampling.LANCZOS)
            
        except Exception as e:
            raise Exception(f"Error loading image: {str(e)}")
        
        pixels = np.array(image)
        ascii_chars = []
        for y in range(self.target_height):
            row = []
            for x in range(self.target_width):
                brightness = pixels[y, x]
                row.append(self.brightness_to_char(brightness))
            ascii_chars.append(row)
        
        distances = self.calculate_distances()
        angles = self.calculate_angles()
        
        return {
            'ascii_chars': ascii_chars,
            'distances': distances,
            'angles': angles,
            'max_distance': np.max(distances),
            'width': self.target_width,
            'height': self.target_height
        }
