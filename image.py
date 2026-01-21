import pygame

class Image:
    def __init__(self, path: str, pos: pygame.Vector2) -> None:

        self.surface = pygame.image.load(path).convert_alpha()
        self.pos = pos
        
        self.rect = self.surface.get_rect(topleft=(round(self.pos.x), round(self.pos.y)))

    def get_surface(self) -> pygame.Surface:
        return self.surface

    def get_image_pos(self) -> tuple[int, int]:
        return self.rect.topleft