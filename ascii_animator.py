"""
ASCII Animator Module
Handles Pygame animation with Hacker/Matrix Theme
"""

import pygame
import sys
import numpy as np


class ASCIIAnimator:
    def __init__(self, ascii_data, mode='Matrix', duration_seconds=8):
        self.ascii_chars = ascii_data['ascii_chars']
        self.distances = ascii_data['distances']
        self.angles = ascii_data['angles']
        self.width = ascii_data['width']
        self.height = ascii_data['height']
        self.duration = duration_seconds
        self.mode = mode
        
        pygame.init()
        
        try:
            self.font = pygame.font.SysFont('courier', 10, bold=True)
        except:
            self.font = pygame.font.Font(pygame.font.match_font('courier'), 10)
            
        self.char_width, self.char_height = self.font.size("A")
        
        self.window_width = self.width * self.char_width
        self.window_height = self.height * self.char_height
        
        # Limit window size
        display_info = pygame.display.Info()
        max_w = display_info.current_w - 50
        max_h = display_info.current_h - 100
        if self.window_width > max_w: self.window_width = max_w
        if self.window_height > max_h: self.window_height = max_h

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("TERMINAL ACCESS - " + mode.upper())
        
        self.bg_color = (0, 0, 0)
        # Revert to WHITE as requested
        self.text_color = (255, 255, 255) 
        
        unique_chars = set(char for row in self.ascii_chars for char in row)
        self.char_cache = {}
        for char in unique_chars:
            self.char_cache[char] = self.font.render(char, True, self.text_color)
            
        self.generate_score_grid()
        
        self.progress = 0.0
        self.animation_complete = False
        self.fps = 60
        
        total_frames = self.duration * self.fps
        self.speed_per_frame = self.max_score / total_frames

    def generate_score_grid(self):
        if self.mode == 'Matrix':
            # Enhanced Matrix Rain Logic
            Y, X = np.indices((self.height, self.width))
            # Random column speeds
            col_speeds = np.random.rand(self.width) * 1.5 + 0.5
            # Random offsets (negative Y to start above screen)
            col_offsets = np.random.rand(self.width) * self.height * 1.5
            
            # Score = Time to arrive
            self.score_grid = (Y.astype(float) + col_offsets) / col_speeds
            
        elif self.mode == 'Circular':
            self.score_grid = self.distances
        elif self.mode == 'Spiral':
            norm_angle = self.angles / (2 * np.pi)
            self.score_grid = self.distances + (1.0 - norm_angle) * 15.0
        elif self.mode == 'Vertical':
            Y, _ = np.indices((self.height, self.width))
            self.score_grid = Y.astype(float)
        elif self.mode == 'Radar':
            self.score_grid = self.angles
        elif self.mode == 'Dissolve':
            self.score_grid = np.random.rand(self.height, self.width) * 100.0
        else:
            self.score_grid = self.distances
            
        self.max_score = np.max(self.score_grid)

    def draw_frame(self):
        self.screen.fill(self.bg_color)
        
        cols_visible = int(self.window_width / self.char_width)
        rows_visible = int(self.window_height / self.char_height)
        
        # Draw visible portion based on scroll
        for y in range(min(self.height, rows_visible)):
            for x in range(min(self.width, cols_visible)):
                if self.score_grid[y, x] <= self.progress:
                    char = self.ascii_chars[y][x]
                    if char in self.char_cache:
                        self.screen.blit(self.char_cache[char], (x * self.char_width, y * self.char_height))
        
        pygame.display.flip()
    
    def run_animation(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        self.progress = 0
                        self.animation_complete = False
            
            if not self.animation_complete:
                self.progress += self.speed_per_frame
                if self.progress >= self.max_score:
                    self.progress = self.max_score
                    self.animation_complete = True
            
            self.draw_frame()
            clock.tick(self.fps)
        
        pygame.quit()
