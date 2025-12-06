from entities import Player, Enemy
from audio_manager import AudioManager
from config import GameConfig

config = GameConfig()


class CollisionHandler:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.audio_manager = AudioManager.get()
    
    def check_all_collisions(self):
        self.check_player_enemy_collisions()
        self.check_enemy_enemy_collisions()
    
    def check_player_enemy_collisions(self):
        player = self.game_manager.get_player()
        if not player:
            return
        
        for enemy in list(self.game_manager.entities):
            if not isinstance(enemy, Enemy):
                continue
            
            if player.rect.colliderect(enemy.rect):
                died = player.take_damage(config.collision.DAMAGE_AMOUNT)
                
                if died:
                    self.audio_manager.play('die_player')
                    self.game_manager.game_over()
                else:
                    self.audio_manager.play('hurt_player')
                    self._apply_player_knockback(player, enemy)
    
    def check_enemy_enemy_collisions(self):
        enemies = [e for e in self.game_manager.entities if isinstance(e, Enemy)]
        
        for i, enemy1 in enumerate(enemies):
            for enemy2 in enemies[i + 1:]:
                if enemy1.rect.colliderect(enemy2.rect):
                    self._handle_enemy_collision(enemy1, enemy2)
    
    def _apply_player_knockback(self, player, enemy):
        dx = player.rect.centerx - enemy.rect.centerx
        dy = player.rect.centery - enemy.rect.centery
        
        distance = (dx * dx + dy * dy) ** 0.5
        if distance > 0:
            dx = dx / distance
            dy = dy / distance
            
            player.rect.x += int(dx * config.collision.KNOCKBACK_DISTANCE)
            player.rect.y += int(dy * config.collision.KNOCKBACK_DISTANCE)
    
    def _handle_enemy_collision(self, enemy1, enemy2):
        red_powerup_active = self.game_manager.red_powerup_timer > 0
        
        if red_powerup_active:
            if enemy1.color == config.enemy.COLOR_RED and enemy2.color != config.enemy.COLOR_RED:
                self._destroy_enemy(enemy2)
                return
            elif enemy2.color == config.enemy.COLOR_RED and enemy1.color != config.enemy.COLOR_RED:
                self._destroy_enemy(enemy1)
                return
        
        if enemy1.color != enemy2.color:
            self._handle_different_color_collision(enemy1, enemy2)
        else:
            self._handle_same_color_collision(enemy1, enemy2)
    
    def _handle_different_color_collision(self, enemy1, enemy2):
        color_strength = {
            config.enemy.COLOR_PURPLE: 4,
            config.enemy.COLOR_GREEN: 3,
            config.enemy.COLOR_ORANGE: 2,
            config.enemy.COLOR_RED: 1,
        }
        
        strength1 = color_strength.get(enemy1.color, 0)
        strength2 = color_strength.get(enemy2.color, 0)
        
        if strength1 > strength2:
            self._destroy_enemy(enemy2)
        elif strength2 > strength1:
            self._destroy_enemy(enemy1)
    
    def _handle_same_color_collision(self, enemy1, enemy2):
        enemy1.vx = -enemy1.vx
        enemy1.vy = -enemy1.vy
        enemy2.vx = -enemy2.vx
        enemy2.vy = -enemy2.vy
        
        if enemy1.enemy_type == "track":
            enemy1.confuse(config.enemy.CONFUSION_DURATION)
        if enemy2.enemy_type == "track":
            enemy2.confuse(config.enemy.CONFUSION_DURATION)
    
    def _destroy_enemy(self, enemy):
        if enemy in self.game_manager.entities:
            self.game_manager.entities.remove(enemy)
            self.audio_manager.play('die_enemy')
            self._heal_player_for_enemy(enemy)
    
    def _heal_player_for_enemy(self, enemy):
        player = self.game_manager.get_player()
        if not player:
            return
        
        heal_amounts = {
            config.enemy.COLOR_RED: config.collision.HEAL_RED,
            config.enemy.COLOR_ORANGE: config.collision.HEAL_ORANGE,
            config.enemy.COLOR_PURPLE: config.collision.HEAL_PURPLE,
            config.enemy.COLOR_GREEN: config.collision.HEAL_GREEN,
        }
        
        heal_amount = heal_amounts.get(enemy.color, 0)
        if heal_amount > 0:
            player.heal(heal_amount)
