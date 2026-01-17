import pygame

class Button:
    def __init__(self, x: int, y: int, normal_path: str, selected_path: str) -> None:
        self.img_normal = pygame.image.load(normal_path)
        self.img_selected = pygame.image.load(selected_path)
        self.rect = self.img_normal.get_rect(topleft=(x, y))
        self.is_hovered = False

    def update(self, mouse_pos: tuple) -> None:
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

    def draw(self, screen: pygame.Surface) -> None:
        if self.is_hovered:
            screen.blit(self.img_selected, self.rect)
        else:
            screen.blit(self.img_normal, self.rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.is_hovered:
                return True
        return False   
