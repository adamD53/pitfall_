import pygame, os

from barrel import Barrel
from image import Image
from button import Button

class Game:
    BUTTON_PLAY_INDEX = 0
    BUTTON_STORE_INDEX = 1
    BUTTON_QUIT_INDEX = 2
    
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock() 
        
        self.screen_width = 1080
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        self.game_state = "MENU" 
        
        self.images: list[Image] = []
        self.buttons: list[Button] = [] 
        
        self.dt = 0
        
        self.load_images()
        self.load_buttons()

    def load_images(self) -> None:
        background_path = os.path.join("Sprites", "Background.png")
        
        self.background = Image(background_path, pygame.Vector2(0, 0))
        
        floor_path = os.path.join("Sprites", "Environment", "Floor.png")
        self.floor = Image(floor_path, pygame.Vector2(0, self.screen.get_height() - 250))
        
        self.images.append(self.background)
        self.images.append(self.floor)

        barrel = Barrel(500, self.floor.get_image_pos().y)
        self.images.append(barrel)
    
    def load_buttons(self) -> None:
        center_x = self.screen_width // 2
        path_prefix = os.path.join("Sprites", "Menu")
        
        # 1. Przycisk PLAY
        btn_play = Button(
            x=center_x - 100,
            y=200, 
            normal_path=os.path.join(path_prefix, "Play.png"),
            selected_path=os.path.join(path_prefix, "Play-Selected.png")
        )
        
        # 2. Przycisk STORE
        btn_store = Button(
            x=center_x - 100, 
            y=350, 
            normal_path=os.path.join(path_prefix, "Store.png"),
            selected_path=os.path.join(path_prefix, "Store-Selected.png")
        )

        # 3. Przycisk QUIT
        btn_quit = Button(
            x=center_x - 100, 
            y=500, 
            normal_path=os.path.join(path_prefix, "Quit.png"),
            selected_path=os.path.join(path_prefix, "Quit-Selected.png")
        )

        self.buttons.append(btn_play)   # Index 0
        self.buttons.append(btn_store)  # Index 1
        self.buttons.append(btn_quit)   # Index 2
   
    def on_draw(self) -> None:
        self.screen.fill((0, 0, 0)) 

        if self.game_state == "GAME":
            for image in self.images:
                self.screen.blit(image.get_surface(), image.get_image_pos())
        
        elif self.game_state == "MENU":
            self.screen.blit(self.background.get_surface(), self.background.get_image_pos())
            self.screen.blit(self.floor.get_surface(), self.floor.get_image_pos())
            mouse_pos = pygame.mouse.get_pos() 
            for btn in self.buttons:
                btn.update(mouse_pos) 
                btn.draw(self.screen)

    def handle_input(self) -> None:
       if self.game_state == "GAME":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.game_state = "MENU"   
    
    def load_music(self) -> None:
        music_path = os.path.join("Sounds","background.wav")
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Nie udało się załadować muzyki: {e}")

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.game_state == "MENU":
                    # Sprawdzamy każdy przycisk
                    # PLAY - Button indeks 0
                    if self.buttons[self.BUTTON_PLAY_INDEX].is_clicked(event):
                        self.game_state = "GAME"
                    
                    # STORE - Button indeks 1
                    elif self.buttons[self.BUTTON_STORE_INDEX].is_clicked(event):
                        print("Otwieram sklep... (tu dodaj logikę sklepu)")
                    
                    # QUIT - Button indeks 2
                    elif self.buttons[self.BUTTON_QUIT_INDEX].is_clicked(event):
                        running = False
            
            self.on_draw();
            self.handle_input();

            pygame.display.flip()

            self.dt = self.clock.tick(60) / 1000
