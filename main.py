import pygame
import sys
import logging
from game_manager import GameManager
from config import GameConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

config = GameConfig()


def initialize_pygame():
    try:
        pygame.init()
        pygame.mixer.init()
        return True
    except pygame.error as e:
        logging.error("Failed to initialize pygame: {}".format(e))
        return False


def handle_events(game_manager):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            if game_manager.state == "menu" and event.key == pygame.K_SPACE:
                game_manager.reset_game()
                game_manager.state = "game"
            
            elif game_manager.state == "gameover" and event.key == pygame.K_SPACE:
                game_manager.reset_game()
                game_manager.state = "game"
            
            elif event.key == pygame.K_ESCAPE:
                return False
    
    return True


def main():
    if not initialize_pygame():
        return 1
    
    try:
        game_manager = GameManager.get()
        game_manager.state = "menu"
        
        logging.info("Game started successfully")
        
        running = True
        while running:
            running = handle_events(game_manager)
            
            if game_manager.state == "game":
                game_manager.update()
            
            game_manager.screen.fill(config.display.BACKGROUND_COLOR)
            game_manager.draw(game_manager.screen)
            pygame.display.flip()
            
            game_manager.clock.tick(config.fps)
        
        logging.info("Game closed normally")
        return 0
    
    except Exception as e:
        logging.error("Unexpected error in main game loop: {}".format(e), exc_info=True)
        return 1
    
    finally:
        pygame.quit()


if __name__ == "__main__":
    sys.exit(main())
