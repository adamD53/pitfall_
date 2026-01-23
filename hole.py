import pygame
import os
from image import Image

class Hole(Image):
    def __init__(self, x: float, y: float) -> None:

        path_prefix = os.path.join("Sprites", "Environment", "Pit")
        

        path1 = os.path.join(path_prefix, "1.png")
        
        super().__init__(path1, pygame.Vector2(x, y))

        self.textures = []
        self.load_textures(path_prefix)


        self.animation_timer = 0
        self.current_frame_index = 0
        self.animation_speed = 0.1 

    def load_textures(self, prefix: str) -> None:

        for i in range(1, 9):
            path = os.path.join(prefix, f"{i}.png")
            try:
                texture = pygame.image.load(path).convert_alpha()
                self.textures.append(texture)
            except FileNotFoundError:
                print(f"Błąd: Nie znaleziono grafiki dziury: {path}")
        

        if not self.textures:
            self.textures.append(self.surface)

    def update(self, dt: float) -> None:
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            

            self.current_frame_index = (self.current_frame_index + 1) % len(self.textures)

            self.surface = self.textures[self.current_frame_index]

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.rect)