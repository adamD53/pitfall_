from game import Game
import sys, pygame

def main() -> None:
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
