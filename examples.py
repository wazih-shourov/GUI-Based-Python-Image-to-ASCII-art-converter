"""
ASCII Art Generator - Usage Examples
"""

# Example 1: Using the converter directly
from ascii_converter import ASCIIConverter

converter = ASCIIConverter(target_width=80, target_height=40)
ascii_data = converter.image_to_ascii_data('test_image.png')

print("ASCII Art Preview:")
for row in ascii_data['ascii_chars'][:10]:  # First 10 rows
    print(''.join(row))

# Example 2: Custom settings
converter_large = ASCIIConverter(target_width=150, target_height=80)

# Example 3: Different character sets
# You can modify ASCII_CHARS in ascii_converter.py for different effects:
# Dense: "@#8&%*+=:-. "
# Simple: "@%#*+=-:. "
# Minimal: "█▓▒░ "
