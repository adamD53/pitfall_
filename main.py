import pygame, os
import sys

class Image:
    def __init__(self, path: str, pos: tuple) -> None:
        self.path: str = path
        self.image_surface = pygame.image.load(self.path)
        self.pos: tuple = pos

    def get_image_surface(self) -> pygame.Surface:
        return self.image_surface
    
    def get_image_pos(self) -> tuple:
        return self.pos

class Barrel(Image):
    def __init__(self, x: int, y: int) -> None:
        # Ustalamy ścieżkę do pliku na sztywno wewnątrz klasy
        path = os.path.join("Sprites","Environment","Barrel","1.png")
        
        # Wywołujemy konstruktor klasy nadrzędnej (Image), żeby załadował grafikę
        super().__init__(path, (x, y))

    # Tutaj w przyszłości możesz dodać metody specyficzne dla beczki,
    # np. def wybuchnij(self): ...
class Button:
    def __init__(self, x: int, y: int, normal_path: str, selected_path: str) -> None:
        # Ładujemy oba obrazki
        self.img_normal = pygame.image.load(normal_path)
        self.img_selected = pygame.image.load(selected_path)
        
        # Tworzymy prostokąt (rect) na podstawie obrazka, żeby łatwo wykrywać kolizje z myszką
        self.rect = self.img_normal.get_rect(topleft=(x, y))
        self.is_hovered = False

    def update(self, mouse_pos: tuple) -> None:
        # Sprawdzamy, czy kursor jest nad przyciskiem
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

    def draw(self, screen: pygame.Surface) -> None:
        # Rysujemy odpowiedni obrazek w zależności od tego, czy jest najechany
        if self.is_hovered:
            screen.blit(self.img_selected, self.rect)
        else:
            screen.blit(self.img_normal, self.rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        # Sprawdzamy czy był klik i czy był na tym przycisku
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # 1 to lewy przycisk
            if self.is_hovered:
                return True
        return False   
class Game:
    def __init__(self) -> None:
        pygame.init()
        # TEJ LINIJKI BRAKUJE lub jest źle wcięta:
        self.clock = pygame.time.Clock() 
        
        self.screen_width = 1080
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # Ustawiamy stan początkowy na MENU
        self.game_state = "MENU" 
        
        self.images: list[Image] = []
        self.buttons: list[Button] = [] 
        
        self.dt = 0
        
        # Ładujemy grafiki
        self.load_images()
        self.load_buttons()

    def load_images(self) -> None:
        background_path = os.path.join("Sprites", "Background.png")
        
        # ZMIANA: Zapisujemy tło jako atrybut klasy (self.background), 
        # żeby mieć do niego dostęp w on_draw
        self.background = Image(background_path, (0, 0))
        
        floor_path = os.path.join("Sprites", "Environment", "Floor.png")
        self.floor = Image(floor_path, (0, self.screen.get_height() - 250))
        
        # Dodajemy tło do listy images, żeby rysowało się podczas gry (tak jak wcześniej)
        self.images.append(self.background)
        self.images.append(self.floor)

        floor_y = self.screen.get_height() - 175
        floor = Image(floor_path, (0, floor_y))
        barrel = Barrel(500, floor_y - 80)
        self.images.append(barrel)
    
    def load_buttons(self) -> None:
        # Środek ekranu w poziomie
        center_x = self.screen_width // 2
        
        # Definiujemy ścieżki do plików (dostosuj foldery jeśli masz inne!)
        # Zakładam strukturę: Sprites/Menu/Play.png itd.
        path_prefix = os.path.join("Sprites", "Menu")
        
        # 1. Przycisk PLAY
        btn_play = Button(
            x=center_x - 100, # Przesuwamy w lewo o połowę szerokości (około), żeby wyśrodkować
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

        self.buttons.append(btn_play)
        self.buttons.append(btn_store)
        self.buttons.append(btn_quit)
   
    def on_draw(self) -> None:
        # Zawsze czyścimy ekran przed rysowaniem nowej klatki
        self.screen.fill((0, 0, 0)) 

        if self.game_state == "GAME":
            # Rysujemy grę (wszystkie obiekty: tło, podłoga, beczki)
            for image in self.images:
                self.screen.blit(image.get_image_surface(), image.get_image_pos())
        
        elif self.game_state == "MENU":
            # Rysujemy menu
            
            # NOWE: Rysujemy tło z gry pod przyciskami
            # Używamy self.background, które stworzyliśmy w load_images
            self.screen.blit(self.background.get_image_surface(), self.background.get_image_pos())
            self.screen.blit(self.floor.get_image_surface(), self.floor.get_image_pos())
            mouse_pos = pygame.mouse.get_pos() 
            for btn in self.buttons:
                btn.update(mouse_pos) 
                btn.draw(self.screen)

    def handle_input(self) -> None:
       if self.game_state == "GAME":
            keys = pygame.key.get_pressed()
            # Tutaj np. obsługa chodzenia
            if keys[pygame.K_ESCAPE]:
                self.game_state = "MENU" # Powrót do menu klawiszem ESC
    # def load_music(self) -> None:
    #     music_path = os.path.join("Sounds","background.wav")
    #     try:
    #         pygame.mixer.music.load(music_path)
    #         pygame.mixer.music.set_volume(0.5)
    #         pygame.mixer.music.play(-1)
    #     except pygame.error as e:
    #         print(f"Nie udało się załadować muzyki: {e}")
    def run(self) -> None:
        running = True
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.game_state == "MENU":
                    # Sprawdzamy każdy przycisk
                    # PLAY - Button indeks 0
                    if self.buttons[0].is_clicked(event):
                        self.game_state = "GAME"
                    
                    # STORE - Button indeks 1
                    elif self.buttons[1].is_clicked(event):
                        print("Otwieram sklep... (tu dodaj logikę sklepu)")
                    
                    # QUIT - Button indeks 2
                    elif self.buttons[2].is_clicked(event):
                        running = False
            # fill the screen with a color to wipe away anything from last frame
            
            self.on_draw();
            self.handle_input();

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60s
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000




def main() -> None:
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
