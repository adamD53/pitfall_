import pygame

class Image:
    def __init__(self, path: str, pos: pygame.Vector2) -> None:
        self.path = path
        self.image_surface = pygame.image.load(self.path)
        self.pos = pos

    def get_surface(self) -> pygame.Surface:
        return self.image_surface
    
    def get_image_pos(self) -> pygame.Vector2:
        return self.pos
