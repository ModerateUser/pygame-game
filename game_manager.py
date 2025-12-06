import pygame
import random
from entities import Player, Enemy
from collision_handler import CollisionHandler
from highscore_manager import HighScoreManager
from powerup import PowerUp
from config import GameConfig

config = GameConfig()


class GameManager:
    _instance = None
    
    def __init__(self):
        self.screen = pygame.display.set_mode((config.width, config.height))
        pygame.display.set_caption("Pygame Survival Game")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont(None, config.ui.FONT_SIZE_NORMAL)
        self.big_font = pygame.font.SysFont(None, config.ui.FONT_SIZE_LARGE)
        
        self.entities = []
        self.powerups = []
        self.state = "menu"
        self.score = 0
        
        self.spawn_timer = 0
        self.powerup_spawn_timer = 0
        self.difficulty = 1.0
        
        self.red_powerup_timer = 0
        self.blue_powerup_timer = 0
        self.yellow_powerup_timer = 0
        
        self.collision_handler = CollisionHandler(self)
        self.highscore_manager = HighScoreManager()
    
    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = GameManager()
        return cls._instance
    
    def add_entity(self, entity):
        self.entities.append(entity)
    
    def reset_game(self):
        self.entities = []
        self.powerups = []
        self.score = 0
        self.spawn_timer = 0
        self.powerup_spawn_timer = 0
        self.difficulty = 1.0
        self.red_powerup_timer = 0
        self.blue_powerup_timer = 0
        self.yellow_powerup_timer = 0
        
        player = Player(config.width // 2, config.height // 2)
        self.add_entity(player)
    
    def update(self):
        if self.state != "game":
            return
        
        self.score += 1
        
        self._update_timers()
        
        self._handle_enemy_spawning()
        
        self._handle_powerup_spawning()
        
        for entity in self.entities:
            entity.update(self)
        
        self.collision_handler.check_all_collisions()
        self.check_powerup_collisions()
    
    def _update_timers(self):
        self.spawn_timer += 1
        self.powerup_spawn_timer += 1
        
        if self.red_powerup_timer > 0:
            self.red_powerup_timer -= 1
        
        if self.blue_powerup_timer > 0:
            self.blue_powerup_timer -= 1
        
        if self.yellow_powerup_timer > 0:
            self.yellow_powerup_timer -= 1
    
    def _handle_enemy_spawning(self):
        spawn_rate = config.spawn.RATE_BASE - int(self.difficulty * config.spawn.DIFFICULTY_MULTIPLIER)
        spawn_rate = max(config.spawn.RATE_MIN, spawn_rate)
        
        if self.spawn_timer > spawn_rate:
            self.spawn_enemy()
            self.spawn_timer = 0
            self.difficulty += config.spawn.DIFFICULTY_INCREASE
    
    def _handle_powerup_spawning(self):
        spawn_rate = random.randint(config.spawn.POWERUP_SPAWN_MIN, config.spawn.POWERUP_SPAWN_MAX)
        
        if self.powerup_spawn_timer > spawn_rate:
            self.spawn_powerup()
            self.powerup_spawn_timer = 0
    
    def draw(self, surface):
        if self.state == "menu":
            self._draw_menu(surface)
        elif self.state == "game":
            self._draw_game(surface)
        elif self.state == "gameover":
            self._draw_game(surface)
            self._draw_gameover(surface)
    
    def _draw_menu(self, surface):
        title = self.big_font.render("PRESS SPACE TO START", True, config.ui.COLOR_TEXT)
        title_rect = title.get_rect(center=(config.width // 2, config.height // 2 - 40))
        surface.blit(title, title_rect)
        
        high_score_text = "High Score: {}".format(self.highscore_manager.get_high_score())
        high_score = self.font.render(high_score_text, True, config.ui.COLOR_TEXT)
        high_score_rect = high_score.get_rect(center=(config.width // 2, config.height // 2 + 40))
        surface.blit(high_score, high_score_rect)
    
    def _draw_game(self, surface):
        for entity in self.entities:
            entity.draw(surface)
        
        for powerup in self.powerups:
            powerup.draw(surface)
        
        self._draw_ui(surface)
    
    def _draw_gameover(self, surface):
        game_over = self.big_font.render("GAME OVER", True, (255, 50, 50))
        game_over_rect = game_over.get_rect(center=(config.width // 2, config.height // 2 - 60))
        surface.blit(game_over, game_over_rect)
        
        restart = self.font.render("Press SPACE to restart", True, config.ui.COLOR_TEXT)
        restart_rect = restart.get_rect(center=(config.width // 2, config.height // 2 + 20))
        surface.blit(restart, restart_rect)
    
    def _draw_ui(self, surface):
        player = self.get_player()
        if player is None:
            return
        
        self._draw_bar(
            surface,
            config.ui.HEALTH_BAR_X,
            config.ui.HEALTH_BAR_Y,
            config.ui.HEALTH_BAR_WIDTH,
            config.ui.HEALTH_BAR_HEIGHT,
            player.health / float(player.max_health),
            config.ui.COLOR_HEALTH_BG,
            config.ui.COLOR_HEALTH_FG
        )
        
        self._draw_bar(
            surface,
            config.ui.STAMINA_BAR_X,
            config.ui.STAMINA_BAR_Y,
            config.ui.STAMINA_BAR_WIDTH,
            config.ui.STAMINA_BAR_HEIGHT,
            player.stamina / float(player.max_stamina),
            config.ui.COLOR_STAMINA_BG,
            config.ui.COLOR_STAMINA_FG
        )
        
        score_text = self.font.render("Score: {}".format(self.score), True, config.ui.COLOR_TEXT)
        score_x = config.width - config.ui.SCORE_MARGIN - score_text.get_width()
        surface.blit(score_text, (score_x, config.ui.SCORE_MARGIN))
        
        self._draw_powerup_timers(surface)
    
    def _draw_bar(self, surface, x, y, width, height, fill_ratio, bg_color, fg_color):
        pygame.draw.rect(surface, bg_color, (x, y, width, height))
        
        fill_width = int(width * max(0.0, min(1.0, fill_ratio)))
        pygame.draw.rect(surface, fg_color, (x, y, fill_width, height))
    
    def _draw_powerup_timers(self, surface):
        y_offset = config.ui.POWERUP_TIMER_Y_START
        
        if self.red_powerup_timer > 0:
            seconds = self.red_powerup_timer // config.fps
            text = self.font.render("RED: {}".format(seconds), True, config.enemy.COLOR_RED)
            text_rect = text.get_rect(center=(config.width // 2, y_offset))
            surface.blit(text, text_rect)
            y_offset += config.ui.POWERUP_TIMER_Y_OFFSET
        
        if self.blue_powerup_timer > 0:
            seconds = self.blue_powerup_timer // config.fps
            text = self.font.render("BLUE: {}".format(seconds), True, config.player.COLOR)
            text_rect = text.get_rect(center=(config.width // 2, y_offset))
            surface.blit(text, text_rect)
            y_offset += config.ui.POWERUP_TIMER_Y_OFFSET
        
        if self.yellow_powerup_timer > 0:
            seconds = self.yellow_powerup_timer // config.fps
            text = self.font.render("YELLOW: {}".format(seconds), True, (255, 255, 0))
            text_rect = text.get_rect(center=(config.width // 2, y_offset))
            surface.blit(text, text_rect)
    
    def get_player(self):
        for entity in self.entities:
            if isinstance(entity, Player):
                return entity
        return None
    
    def game_over(self):
        self.highscore_manager.save(self.score)
        self.state = "gameover"
    
    def spawn_enemy(self):
        rand = random.random()
        
        if rand < config.enemy.SPAWN_PROB_RED:
            color = config.enemy.COLOR_RED
            speed = config.enemy.SPEED_SLOW
            enemy_type = "bounce"
        elif rand < config.enemy.SPAWN_PROB_RED + config.enemy.SPAWN_PROB_ORANGE:
            color = config.enemy.COLOR_ORANGE
            speed = config.enemy.SPEED_FAST
            enemy_type = "bounce"
        elif rand < config.enemy.SPAWN_PROB_RED + config.enemy.SPAWN_PROB_ORANGE + config.enemy.SPAWN_PROB_GREEN:
            color = config.enemy.COLOR_GREEN
            speed = config.enemy.SPEED_SLOW
            enemy_type = "track"
        else:
            color = config.enemy.COLOR_PURPLE
            speed = config.enemy.SPEED_FAST
            enemy_type = "bounce"
        
        side = random.choice(["top", "bottom", "left", "right"])
        
        if side == "top":
            x, y = random.randint(0, config.width), 0
        elif side == "bottom":
            x, y = random.randint(0, config.width), config.height - config.entity.SIZE
        elif side == "left":
            x, y = 0, random.randint(0, config.height)
        else:
            x, y = config.width - config.entity.SIZE, random.randint(0, config.height)
        
        self.add_entity(Enemy(x, y, color, speed, enemy_type))
    
    def spawn_powerup(self):
        margin = config.powerup.SPAWN_MARGIN
        x = random.randint(margin, config.width - margin)
        y = random.randint(margin, config.height - margin)
        
        rand = random.random()
        
        if rand < config.powerup.SPAWN_PROB_BLUE:
            powerup_type = "blue"
        elif rand < config.powerup.SPAWN_PROB_BLUE + config.powerup.SPAWN_PROB_GREEN:
            powerup_type = "green"
        elif rand < config.powerup.SPAWN_PROB_BLUE + config.powerup.SPAWN_PROB_GREEN + config.powerup.SPAWN_PROB_RED:
            powerup_type = "red"
        else:
            powerup_type = "yellow"
        
        self.powerups.append(PowerUp(x, y, powerup_type))
    
    def check_powerup_collisions(self):
        player = self.get_player()
        if player is None:
            return
        
        powerups_to_remove = []
        
        for powerup in self.powerups:
            if player.rect.colliderect(powerup.rect):
                self.apply_powerup(player, powerup.powerup_type)
                powerups_to_remove.append(powerup)
        
        for powerup in powerups_to_remove:
            self.powerups.remove(powerup)
    
    def apply_powerup(self, player, powerup_type):
        if powerup_type == "blue":
            self.blue_powerup_timer = config.powerup.DURATION
        
        elif powerup_type == "green":
            enemies_to_remove = [
                entity for entity in self.entities
                if isinstance(entity, Enemy) and entity.color == config.enemy.COLOR_GREEN
            ]
            for enemy in enemies_to_remove:
                self.entities.remove(enemy)
        
        elif powerup_type == "yellow":
            self.yellow_powerup_timer = config.powerup.DURATION
        
        elif powerup_type == "red":
            self.red_powerup_timer = config.powerup.DURATION
