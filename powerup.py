import pygame
import logging


class PowerUp:
    def __init__(self, x, y, powerup_type):
        self.powerup_type = powerup_type
        self.size = 20
        
        color_map = {
            'blue': (0, 150, 255),
            'green': (0, 255, 0),
            'red': (255, 0, 0),
            'yellow': (255, 255, 0)
        }
        
        if powerup_type not in color_map:
            logging.error("Unknown power-up type: {}".format(powerup_type))
            powerup_type = 'blue'
        
        color = color_map[powerup_type]
        
        try:
            image_path = "images/powerup_{}.png".format(powerup_type)
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        except (pygame.error, IOError) as e:
            logging.warning("Failed to load power-up image '{}': {}".format(image_path, e))
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
