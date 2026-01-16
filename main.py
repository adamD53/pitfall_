import pygame, os

class Image:
    def __init__(self, path: str, pos: tuple) -> None:
        self.path: str = path
        self.image_surface = pygame.image.load(self.path)
        self.pos: tuple = pos

    def get_image_surface(self) -> pygame.Surface:
        return self.image_surface
    
    def get_image_pos(self) -> tuple:
        return self.pos


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1080, 720))
        self.images: list[Image] = []
        self.dt = 0
        self.load_images()

    def load_images(self) -> None:
        background_path = os.path.join("Sprites", "Background.png");
        background = Image(background_path, (0, 0));
        floor_path = os.path.join("Sprites", "Environment", "Floor.png");
        floor = Image(floor_path, (100, self.screen.get_height() - 250));
        self.images.append(background)
        self.images.append(floor)
   
    def on_draw(self) -> None:
        for image in self.images:
            self.screen.blit(image.get_image_surface(), image.get_image_pos());

    def handle_input(self) -> None:
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_w]:
        #     player_pos.y -= 300 * self.dt
        # if keys[pygame.K_s]:
        #     player_pos.y += 300 * self.dt
        # if keys[pygame.K_a]:
        #     player_pos.x -= 300 * self.dt
        # if keys[pygame.K_d]:
        #     player_pos.x += 300 * self.dt
        pass

    def run(self) -> None:
        running = True
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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

if __name__ == "__main__":
    main()
