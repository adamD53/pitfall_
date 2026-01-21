import pygame, os
from image import Image

class Player(Image):
    def __init__(self, x: float, y: float, ground_y: int) -> None:
        
        path = os.path.join("Sprites", "Player", "Idle", "1.png")
        super().__init__(path, pygame.Vector2(x, y))
        
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 300
        self.gravity = 1200
        self.jump_force = -600
        self.on_ground = False
        self.jump_sound = None
        sound_path = os.path.join("Sounds", "jump.wav")
        self.jump_sound = pygame.mixer.Sound(sound_path)
        self.jump_sound.set_volume(0.3) 

        self.ground_y = ground_y 

        self.facing_right = True
        
        self.walking_animation_textures: list[pygame.Surface] = []
        self.flipped_walking_animation_textures: list[pygame.Surface] = []
        
        self.idle_image = self.surface  
        self.flipped_idle_image = pygame.transform.flip(self.idle_image, True, False)
        
        self.timer = 0
        self.current_animation_frame_index = 0
        self.load_walking_animation_textures()

    def load_walking_animation_textures(self) -> None:
        for i in range(1, 6):
            try:
                path = os.path.join("Sprites", "Player", "Running", f"{i}.png")
                texture = pygame.image.load(path).convert_alpha() 
                self.walking_animation_textures.append(texture)
            except FileNotFoundError:
                print(f"Nie znaleziono pliku: {path}") 

        for texture in self.walking_animation_textures:
            self.flipped_walking_animation_textures.append(
                pygame.transform.flip(texture, True, False)
            )

    def play_walking_animation(self, dt) -> None:
        if self.current_animation_frame_index >= len(self.walking_animation_textures):
            self.current_animation_frame_index = 0
        
        if self.facing_right:
            self.surface = self.walking_animation_textures[self.current_animation_frame_index]
        else:
            self.surface = self.flipped_walking_animation_textures[self.current_animation_frame_index]

        if self.timer > 0.1:
            self.current_animation_frame_index += 1
            self.timer = 0
        self.timer += dt

    def apply_gravity(self, dt) -> None:
        self.velocity.y += self.gravity * dt
        self.pos.y += self.velocity.y * dt

        current_height = self.surface.get_height()

        if self.pos.y + current_height >= self.ground_y:
            self.pos.y = self.ground_y - current_height 
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def input(self, dt) -> None:
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.facing_right = False
            self.play_walking_animation(dt)
            
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.facing_right = True
            self.play_walking_animation(dt)

        else:
            self.surface = self.idle_image if self.facing_right else self.flipped_idle_image

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity.y = self.jump_force
            self.on_ground = False
            
            if self.jump_sound:
                self.jump_sound.play()

    def update(self, dt) -> None:
        self.input(dt)
        self.apply_gravity(dt)
        
        self.pos.x += self.velocity.x * dt
        
        if hasattr(self, 'rect'):
            self.rect = self.surface.get_rect(topleft=(round(self.pos.x), round(self.pos.y)))
    
    def draw(self, screen) -> None:
        screen.blit(self.surface, self.rect)