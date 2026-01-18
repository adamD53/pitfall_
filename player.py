import pygame, os
from image import Image

class Player(Image):
    def __init__(self, x: float, y: float) -> None:
        path = os.path.join("Sprites","Player","Idle","1.png")
        super().__init__(path, pygame.Vector2(x, y))
        self.facing_right = True
        self.walking_animation_textures: list[pygame.Surface] = []
        self.flipped_walking_animation_textures: list[pygame.Surface] = []
        self.idle_image = self.get_surface();
        self.timer = 0
        self.current_animation_frame_index = 0
        self.load_walking_animation_textures()

    # TODO: Przenieść całą logike animacji do osobnego modułu lub klasy
    def load_walking_animation_textures(self) -> None:
        for i in range(1, 6):
            path = os.path.join("Sprites", "Player", "Running", f"{i}.png");
            texture = pygame.image.load(path)
            self.walking_animation_textures.append(texture);

        for i in range(len(self.walking_animation_textures)):
            self.flipped_walking_animation_textures.append(pygame.transform.flip(self.walking_animation_textures[i], True, False))


    def play_walking_animation(self, dt) -> None:
        if self.current_animation_frame_index >= len(self.walking_animation_textures):
            self.current_animation_frame_index = 0
        
        if self.facing_right:
            self.image_surface = self.walking_animation_textures[self.current_animation_frame_index]
        else:
            self.image_surface = self.flipped_walking_animation_textures[self.current_animation_frame_index]

        if self.timer > 0.1:
            self.current_animation_frame_index += 1
            self.timer = 0
        self.timer += dt

    def input(self, dt) -> None:
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_w]:
        #     self.pos.y -= 300 * dt
        # if keys[pygame.K_s]:
        #     self.pos.y += 300 * dt
        
        self.image_surface = self.idle_image if self.facing_right else pygame.transform.flip(self.idle_image, True, False)

        if keys[pygame.K_a]:
            if self.facing_right:
                self.facing_right = False
            self.play_walking_animation(dt)
            self.pos.x -= 300 * dt
                
        if keys[pygame.K_d]:
            if not self.facing_right:
                self.facing_right = True
            self.play_walking_animation(dt)
            self.pos.x += 300 * dt

    def update(self, dt) -> None:
        self.input(dt)

    def draw(self, screen) -> None:
        screen.blit(self.get_surface(), self.get_image_pos())

