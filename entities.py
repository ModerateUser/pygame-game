import pygame
import random
from config import GameConfig

config = GameConfig()


class Entity:
    def __init__(self, x, y, color=(200, 200, 200)):
        self.image = pygame.Surface((config.entity.SIZE, config.entity.SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def update(self, game_manager):
        pass
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, config.player.COLOR)
        self.speed = config.player.SPEED_NORMAL
        self.max_health = config.player.MAX_HEALTH
        self.health = config.player.MAX_HEALTH
        self.max_stamina = config.player.MAX_STAMINA
        self.stamina = config.player.MAX_STAMINA
        self.damage_cooldown = 0
    
    def update(self, game_manager):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
        
        blue_active = game_manager.blue_powerup_timer > 0
        
        keys = pygame.key.get_pressed()
        move_x, move_y = self._get_movement_input(keys)
        
        speed = self._calculate_speed(move_x, move_y, blue_active)
        
        self._apply_movement(move_x, move_y, speed)
        
        self._clamp_to_screen()
    
    def _get_movement_input(self, keys):
        move_x = 0
        move_y = 0
        
        if keys[pygame.K_w]:
            move_y -= 1
        if keys[pygame.K_s]:
            move_y += 1
        if keys[pygame.K_a]:
            move_x -= 1
        if keys[pygame.K_d]:
            move_x += 1
        
        return move_x, move_y
    
    def _calculate_speed(self, move_x, move_y, blue_active):
        is_moving = move_x != 0 or move_y != 0
        
        if is_moving:
            if self.stamina > 0:
                drain = config.player.STAMINA_DRAIN_RATE / 2.0 if blue_active else config.player.STAMINA_DRAIN_RATE
                self.stamina -= drain
                
                boost = 4 if blue_active else 2
                return self.speed + boost
            else:
                boost = 2 if blue_active else 0
                return self.speed + boost
        else:
            if self.stamina < self.max_stamina:
                regen = config.player.STAMINA_REGEN_RATE * 2.5 if blue_active else config.player.STAMINA_REGEN_RATE
                self.stamina = min(self.max_stamina, self.stamina + regen)
            return self.speed
    
    def _apply_movement(self, move_x, move_y, speed):
        self.rect.x += int(move_x * speed)
        self.rect.y += int(move_y * speed)
    
    def _clamp_to_screen(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > config.width:
            self.rect.right = config.width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > config.height:
            self.rect.bottom = config.height
    
    def take_damage(self, damage):
        if self.damage_cooldown > 0:
            return False
        
        self.health -= damage
        self.damage_cooldown = config.player.DAMAGE_COOLDOWN
        return self.health <= 0
    
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)


class Enemy(Entity):
    def __init__(self, x, y, color, speed, enemy_type):
        super().__init__(x, y, color)
        self.color = color
        self.speed = speed
        self.enemy_type = enemy_type
        self.damage = config.collision.DAMAGE_AMOUNT
        self.confused = 0
        
        if enemy_type == "bounce":
            self.vx = random.choice([-1, 1]) * speed
            self.vy = random.choice([-1, 1]) * speed
        else:
            self.vx = 0
            self.vy = 0
    
    def update(self, game_manager):
        if self.enemy_type == "track":
            self._update_tracking(game_manager)
        
        yellow_active = game_manager.yellow_powerup_timer > 0
        speed_multiplier = 0.5 if yellow_active else 1.0
        
        self.rect.x += int(self.vx * speed_multiplier)
        self.rect.y += int(self.vy * speed_multiplier)
        
        self._handle_wall_collisions()
    
    def _update_tracking(self, game_manager):
        if self.confused > 0:
            self.confused -= 1
            return
        
        player = game_manager.get_player()
        if not player:
            return
        
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        
        if abs(dx) > abs(dy):
            self.vx = self.speed if dx > 0 else -self.speed
            self.vy = 0
        else:
            self.vy = self.speed if dy > 0 else -self.speed
            self.vx = 0
    
    def _handle_wall_collisions(self):
        if self.rect.left <= 0:
            self.rect.left = 0
            self.vx = abs(self.vx)
        if self.rect.right >= config.width:
            self.rect.right = config.width
            self.vx = -abs(self.vx)
        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy = abs(self.vy)
        if self.rect.bottom >= config.height:
            self.rect.bottom = config.height
            self.vy = -abs(self.vy)
    
    def confuse(self, duration):
        self.confused = duration
