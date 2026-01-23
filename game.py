import pygame, os
import random
from datetime import datetime
from enum import Enum

from barrel import Barrel
from image import Image
from button import Button
from player import Player
from hole import Hole
from rope import Rope

class GameState(Enum):
    MENU = 0
    GAME = 1
    GAME_OVER = 2

class Game:
    BUTTON_PLAY_INDEX = 0
    BUTTON_QUIT_INDEX = 1

    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock() 
        
        self.screen_width = 1080
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 60, bold=True)
        
        self.game_state = GameState.MENU 
        
        self.images: list[Image] = []
        self.barrels: list[Barrel] = []
        self.buttons: list[Button] = [] 
        
 
        self.ropes: list[Rope] = []
        self.holes: list[Hole] = []

        
        self.dt = 0
        self.level = 1
        
        self.lives = 3
        self.score = 0
        self.score_timer = 0.0
        self.damage_cooldown = 0.0

        self.load_images()
        self.load_buttons()
        self.play_music("metallica.wav")
        
        floor_y_pos = self.floor.get_image_pos()[1]
        self.player = Player(50, floor_y_pos - 100, floor_y_pos)

    def start_new_game(self):
        self.level = 1
        self.lives = 3
        self.score = 0
        self.score_timer = 0
        self.damage_cooldown = 0
        self.setup_level()
        self.play_music("background.wav")

    def save_score_to_file(self):
        """Zapisuje wynik i datę do pliku tekstowego"""
        try:
            now = datetime.now()
            date_string = now.strftime("%Y-%m-%d %H:%M:%S")
            line = f"Data: {date_string} | Wynik: {self.score} pkt | Poziom: {self.level}\n"
            
            with open("wyniki.txt", "a", encoding="utf-8") as f:
                f.write(line)
            print("Zapisano wynik do pliku.")
        except Exception as e:
            print(f"Błąd zapisu pliku: {e}")

    def setup_level(self):
        """Generuje poziom - proceduralnie lub według scenariusza"""

        self.barrels.clear()
        self.holes.clear()
        self.ropes.clear()
        

        self.player.holes = self.holes
        
        floor_y_pos = self.floor.get_image_pos()[1]
        self.player.pos.x = 50
        self.player.pos.y = floor_y_pos - 100
        self.player.velocity = pygame.Vector2(0, 0)
        self.player.is_swinging = False

        print(f"Generowanie poziomu: {self.level}")

        if self.level == 1:
            self.add_rope(self.screen_width // 2)
            self.spawn_barrel(count=1)

        elif self.level == 2:
            self.add_rope(self.screen_width // 2)
            self.spawn_barrel(count=3, interval=350)

        elif self.level == 3:
            hole_x = (self.screen_width // 2) - 50
            self.add_hole(hole_x)
            self.add_rope(self.screen_width // 2)
            

            barrel = Barrel(self.screen_width - 200, floor_y_pos - 55)
            barrel.velocity = pygame.Vector2(0, 0)
            self.barrels.append(barrel)

        else:
            scenario = random.choice(["barrels", "holes", "parkour"])
            
            if scenario == "barrels":
                print("Scenariusz: Deszcz Beczek")
                self.add_rope(self.screen_width // 2)
                count = random.randint(4, 5)
                self.spawn_barrel(count=count, interval=250)
            
            elif scenario == "holes":
                print("Scenariusz: Szwajcarski Ser")
                x1 = random.randint(300, 500)
                x2 = random.randint(700, 900)
                self.add_hole(x1)
                self.add_hole(x2)

                self.add_rope(x1 + 50)
                self.add_rope(x2 + 50)
                self.spawn_barrel(count=2, interval=400)

            elif scenario == "parkour":
                print("Scenariusz: Parkour")
                self.add_hole(400)
                self.add_hole(800)
                self.add_rope(450)
                self.add_rope(850)
                
                barrel = Barrel(self.screen_width + 100, floor_y_pos - 55)
                barrel.velocity.x = -450 
                self.barrels.append(barrel)

    def add_rope(self, x):
        floor_y = self.floor.get_image_pos()[1]
        length = floor_y - 150
        self.ropes.append(Rope(x, 0, length))

    def add_hole(self, x):
        floor_y = self.floor.get_image_pos()[1]
        self.holes.append(Hole(x, floor_y))

    def spawn_barrel(self, count=1, interval=0):
        floor_y = self.floor.get_image_pos()[1]
        barrel_y = floor_y - 55
        for i in range(count):
            start_x = self.screen_width + 50 + (i * interval)
            self.barrels.append(Barrel(start_x, barrel_y))

    def load_images(self) -> None:
        background_path = os.path.join("Sprites", "Background.png")
        self.background = Image(background_path, pygame.Vector2(0, 0))
        floor_path = os.path.join("Sprites", "Environment", "Floor.png")
        self.floor = Image(floor_path, pygame.Vector2(0, self.screen.get_height() - 250))
        self.images.append(self.background)
        self.images.append(self.floor)

    def load_buttons(self) -> None:
        center_x = self.screen_width // 2
        path_prefix = os.path.join("Sprites", "Menu")
        btn_play = Button(center_x - 100, 300, 
                          os.path.join(path_prefix, "Play.png"), 
                          os.path.join(path_prefix, "Play-Selected.png"))
        btn_quit = Button(center_x - 100, 400, 
                          os.path.join(path_prefix, "Quit.png"), 
                          os.path.join(path_prefix, "Quit-Selected.png"))
        self.buttons.append(btn_play)   
        self.buttons.append(btn_quit)   

    def draw_hud(self):
        score_text = self.font.render(f"Wynik: {self.score}", True, (255, 255, 255))
        lives_text = self.font.render(f"Życia: {self.lives}", True, (255, 50, 50))
        level_text = self.font.render(f"Poziom: {self.level}", True, (200, 200, 255))
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(lives_text, (20, 55))
        self.screen.blit(level_text, (20, 90))

    def draw_game_over(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.big_font.render("KONIEC GRY", True, (255, 0, 0))
        score_text = self.font.render(f"Twój wynik końcowy: {self.score}", True, (255, 255, 255))
        restart_text = self.font.render("Naciśnij SPACJĘ, aby zagrać ponownie", True, (200, 200, 200))
        saved_text = self.font.render("(Wynik zapisano do wyniki.txt)", True, (100, 255, 100))

        go_rect = game_over_text.get_rect(center=(self.screen_width/2, self.screen_height/2 - 50))
        sc_rect = score_text.get_rect(center=(self.screen_width/2, self.screen_height/2 + 20))
        rs_rect = restart_text.get_rect(center=(self.screen_width/2, self.screen_height/2 + 80))
        sv_rect = saved_text.get_rect(center=(self.screen_width/2, self.screen_height/2 + 130))

        self.screen.blit(game_over_text, go_rect)
        self.screen.blit(score_text, sc_rect)
        self.screen.blit(restart_text, rs_rect)
        self.screen.blit(saved_text, sv_rect)

    def on_draw(self) -> None:
        self.screen.fill((0, 0, 0)) 

        if self.game_state == GameState.GAME or self.game_state == GameState.GAME_OVER:
            for image in self.images:
                self.screen.blit(image.get_surface(), image.get_image_pos())
            
            for hole in self.holes:
                hole.draw(self.screen)
            
            for rope in self.ropes:
                rope.draw(self.screen)
            
            for barrel in self.barrels:
                barrel.draw(self.screen)

            if self.game_state == GameState.GAME:
                if self.damage_cooldown <= 0 or (self.damage_cooldown * 10) % 2 > 1:
                    self.player.draw(self.screen)
                self.draw_hud()
            elif self.game_state == GameState.GAME_OVER:
                self.draw_game_over()
        
        elif self.game_state == GameState.MENU:
            self.screen.blit(self.background.get_surface(), self.background.get_image_pos())
            self.screen.blit(self.floor.get_surface(), self.floor.get_image_pos())
            mouse_pos = pygame.mouse.get_pos() 
            for btn in self.buttons:
                btn.update(mouse_pos) 
                btn.draw(self.screen)

    def handle_input(self) -> None:
       keys = pygame.key.get_pressed()

       if self.game_state == GameState.GAME_OVER:
           if keys[pygame.K_SPACE]:
               self.start_new_game()
               self.game_state = GameState.GAME
           elif keys[pygame.K_ESCAPE]:
               self.game_state = GameState.MENU
               self.play_music("metallica.wav")
           return

       if self.game_state == GameState.GAME:
            self.score_timer += self.dt
            if self.score_timer >= 1.0:
                self.score += 10
                self.score_timer = 0
            
            if self.damage_cooldown > 0:
                self.damage_cooldown -= self.dt

            for hole in self.holes:
                hole.update(self.dt)
            
            for rope in self.ropes:
                rope.update(self.dt)
                if (self.player.rect.colliderect(rope.rect) 
                    and not self.player.on_ground 
                    and self.player.rope_cooldown <= 0):
                    
                    self.player.is_swinging = True
                    self.current_rope = rope 

            if self.player.is_swinging and hasattr(self, 'current_rope'):
                rope_x, rope_y = self.current_rope.get_end_pos()
                self.player.pos.x = rope_x - (self.player.rect.width / 2)
                self.player.pos.y = rope_y
            
            
            if not self.player.is_swinging:
                self.current_rope = None

            self.player.speed = 300 
            for barrel in self.barrels:
                barrel.update(self.dt)
                if self.player.rect.colliderect(barrel.rect):
                    self.player.speed = 100
                    if self.damage_cooldown <= 0:
                        self.score -= 5
                        self.damage_cooldown = 1.0
                
                
                if barrel.velocity.x < 0: 
                    if barrel.pos.x < -100:
                        max_x = max([b.pos.x for b in self.barrels]) if self.barrels else 0
                        new_x = max(max_x + 350, self.screen_width + 50)
                        barrel.pos.x = new_x

            self.player.update(self.dt)
            
            
            if self.player.pos.y > self.screen_height:
                self.lives -= 1
                if self.lives > 0:
                    self.setup_level()
                else:
                    self.save_score_to_file() 
                    self.game_state = GameState.GAME_OVER
                    self.play_music("metallica.wav")

            
            if self.player.pos.x > self.screen_width:
                self.level += 1
                self.score += 50 
                self.setup_level()

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
            print(f"Błąd muzyki: {e}")

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.game_state == GameState.MENU:
                    if self.buttons[self.BUTTON_PLAY_INDEX].is_clicked(event):
                        self.start_new_game()
                        self.game_state = GameState.GAME
                    elif self.buttons[self.BUTTON_QUIT_INDEX].is_clicked(event):
                        running = False
            
            self.on_draw()
            self.handle_input()
            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000