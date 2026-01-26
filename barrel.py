import pygame
import os
from image import Image

class Barrel(Image):
    def __init__(self, x: float, y: float) -> None:

        path1 = os.path.join("Sprites", "Environment", "Barrel", "1.png")
        path2 = os.path.join("Sprites", "Environment", "Barrel", "2.png")
        
        super().__init__(path1, pygame.Vector2(x, y))

        self.textures = []
        try:
            self.textures.append(pygame.image.load(path1).convert_alpha())
            self.textures.append(pygame.image.load(path2).convert_alpha())
        except FileNotFoundError as e:
            print(f"Błąd ładowania tekstur beczki: {e}")
            self.textures.append(self.surface)

        self.animation_timer = 0
        self.current_frame_index = 0
        self.animation_speed = 0.1 

        self.velocity = pygame.Vector2(-250, 0) 
       

    def update(self, dt: float) -> None:
        self.pos.x += self.velocity.x * dt
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0

            self.current_frame_index = (self.current_frame_index + 1) % len(self.textures)

            self.surface = self.textures[self.current_frame_index]

        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.rect)
