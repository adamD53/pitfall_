import pygame
import math
import os

class Rope:
    def __init__(self, x: int, y: int, length: int) -> None:
        self.pivot_x = x
        self.pivot_y = y
        self.length = length
        
        self.angle = 0
        self.time = 0
        self.swing_speed = 2.0
        self.max_angle = 0.8
        
        self.end_x = x
        self.end_y = y + length
        
        self.rect = pygame.Rect(x - 10, y + length - 10, 20, 20)


        self.segment_surface = self.create_rope_texture()
        self.segment_height = self.segment_surface.get_height()

    def create_rope_texture(self) -> pygame.Surface:

        width = 6
        height = 10
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((139, 69, 19))
        pygame.draw.rect(surface, (100, 50, 10), (0, 0, 2, height)) 
        return surface

    def update(self, dt: float) -> None:
        self.time += dt
        self.angle = math.sin(self.time * self.swing_speed) * self.max_angle
        
        self.end_x = self.pivot_x + math.sin(self.angle) * self.length
        self.end_y = self.pivot_y + math.cos(self.angle) * self.length
        
        self.rect.center = (round(self.end_x), round(self.end_y))

    def draw(self, screen: pygame.Surface) -> None:
        num_segments = int(self.length / self.segment_height)
        
        angle_degrees = math.degrees(self.angle)
        rotated_segment = pygame.transform.rotate(self.segment_surface, -angle_degrees)
        

        dx = math.sin(self.angle) * self.segment_height
        dy = math.cos(self.angle) * self.segment_height
        
        current_x = self.pivot_x
        current_y = self.pivot_y

        for _ in range(num_segments):
            rect = rotated_segment.get_rect(center=(current_x, current_y))
            screen.blit(rotated_segment, rect)
            
            current_x += dx
            current_y += dy

        pygame.draw.circle(screen, (100, 50, 10), (int(self.end_x), int(self.end_y)), 6)

    def get_end_pos(self) -> tuple[float, float]:
        return (self.end_x, self.end_y)