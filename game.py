import pygame, os
from enum import Enum

from barrel import Barrel
from image import Image
from button import Button
from player import Player

class GameState(Enum):
    MENU = 0
    GAME = 1

class Game:
    BUTTON_PLAY_INDEX = 0
    BUTTON_QUIT_INDEX = 1

    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock() 
        
        self.screen_width = 1080
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        self.game_state = GameState.MENU 
        
        self.images: list[Image] = []
        self.barrels: list[Barrel] = []
        self.buttons: list[Button] = [] 
        
        self.dt = 0
        
        self.load_images()
        self.load_buttons()
        self.play_music("metallica.wav")
        
        floor_y_pos = self.floor.get_image_pos()[1]
        self.player = Player(50, floor_y_pos - 100, floor_y_pos)

        self.spawn_barrel()

    def load_images(self) -> None:
        background_path = os.path.join("Sprites", "Background.png")
        self.background = Image(background_path, pygame.Vector2(0, 0))
        
        floor_path = os.path.join("Sprites", "Environment", "Floor.png")
        self.floor = Image(floor_path, pygame.Vector2(0, self.screen.get_height() - 250))
        
        self.images.append(self.background)
        self.images.append(self.floor)

    def spawn_barrel(self):
        barrel_y = self.floor.get_image_pos()[1] - 55
        barrel_x = self.screen_width + 50 
        barrel = Barrel(barrel_x, barrel_y)
        self.barrels.append(barrel)
    
    def load_buttons(self) -> None:
        center_x = self.screen_width // 2
        path_prefix = os.path.join("Sprites", "Menu")
        
        btn_play = Button(
            x=center_x - 100,
            y=300, 
            normal_path=os.path.join(path_prefix, "Play.png"),
            selected_path=os.path.join(path_prefix, "Play-Selected.png")
        )

        btn_quit = Button(
            x=center_x - 100, 
            y=400, 
            normal_path=os.path.join(path_prefix, "Quit.png"),
            selected_path=os.path.join(path_prefix, "Quit-Selected.png")
        )

        self.buttons.append(btn_play)   
        self.buttons.append(btn_quit)   
   
    def on_draw(self) -> None:
        self.screen.fill((0, 0, 0)) 

        if self.game_state == GameState.GAME:
            for image in self.images:
                self.screen.blit(image.get_surface(), image.get_image_pos())
            
            for barrel in self.barrels:
                barrel.draw(self.screen)

            self.player.draw(self.screen)
        
        elif self.game_state == GameState.MENU:
            self.screen.blit(self.background.get_surface(), self.background.get_image_pos())
            self.screen.blit(self.floor.get_surface(), self.floor.get_image_pos())
            mouse_pos = pygame.mouse.get_pos() 
            for btn in self.buttons:
                btn.update(mouse_pos) 
                btn.draw(self.screen)

    def handle_input(self) -> None:
       if self.game_state == GameState.GAME:
            keys = pygame.key.get_pressed()
            
            self.player.speed = 300 
            player_rect = self.player.rect


            for barrel in self.barrels:

                barrel.update(self.dt)

 
                if player_rect.colliderect(barrel.rect):
                    self.player.speed = 100
                


                if barrel.pos.x < -100:

                    barrel.pos.x = self.screen_width + 50


            self.player.update(self.dt)
            
            if keys[pygame.K_ESCAPE]:
                self.game_state = GameState.MENU
                self.play_music("metallica.wav")
    
    def play_music(self, filename: str) -> None:
        music_path = os.path.join("Sounds", filename)
        try:
            pygame.mixer.music.unload() 
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1) 
        except pygame.error as e:
            print(f"Nie udało się wczytać muzyki {filename}: {e}")

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.game_state == GameState.MENU:
                    if self.buttons[self.BUTTON_PLAY_INDEX].is_clicked(event):
                        
                        self.game_state = GameState.GAME
                        self.play_music("background.wav")
                    
                    elif self.buttons[self.BUTTON_QUIT_INDEX].is_clicked(event):
                        running = False
            
            self.on_draw()
            self.handle_input()
            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000