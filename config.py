class DisplayConfig:
    WIDTH = 800
    HEIGHT = 600
    BACKGROUND_COLOR = (0, 0, 0)


class EntityConfig:
    SIZE = 30


class PlayerConfig:
    COLOR = (0, 150, 255)
    SPEED_NORMAL = 3
    SPEED_SPRINT = 5
    MAX_HEALTH = 25
    MAX_STAMINA = 100
    STAMINA_DRAIN_RATE = 0.5
    STAMINA_REGEN_RATE = 0.4
    DAMAGE_COOLDOWN = 60


class EnemyConfig:
    COLOR_RED = (255, 0, 0)
    COLOR_ORANGE = (255, 165, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_PURPLE = (128, 0, 128)
    SPEED_SLOW = 2
    SPEED_FAST = 4
    SPAWN_PROB_RED = 0.3
    SPAWN_PROB_ORANGE = 0.3
    SPAWN_PROB_GREEN = 0.2
    SPAWN_PROB_PURPLE = 0.2
    CONFUSION_DURATION = 60
    TRACKING_UPDATE_RATE = 10


class SpawnConfig:
    RATE_BASE = 80
    RATE_MIN = 30
    DIFFICULTY_MULTIPLIER = 8
    DIFFICULTY_INCREASE = 0.08
    POWERUP_SPAWN_MIN = 300
    POWERUP_SPAWN_MAX = 600


class PowerUpConfig:
    DURATION = 300
    SPAWN_MARGIN = 50
    SPAWN_PROB_BLUE = 0.3
    SPAWN_PROB_GREEN = 0.3
    SPAWN_PROB_RED = 0.2
    SPAWN_PROB_YELLOW = 0.2


class CollisionConfig:
    DAMAGE_AMOUNT = 5
    KNOCKBACK_DISTANCE = 10
    HEAL_RED = 1
    HEAL_ORANGE = 1
    HEAL_PURPLE = 1
    HEAL_GREEN = 2


class UIConfig:
    FONT_SIZE_NORMAL = 36
    FONT_SIZE_LARGE = 72
    COLOR_TEXT = (255, 255, 255)
    COLOR_HEALTH_BG = (100, 0, 0)
    COLOR_HEALTH_FG = (255, 0, 0)
    COLOR_STAMINA_BG = (0, 100, 0)
    COLOR_STAMINA_FG = (0, 255, 0)
    HEALTH_BAR_X = 10
    HEALTH_BAR_Y = 10
    HEALTH_BAR_WIDTH = 200
    HEALTH_BAR_HEIGHT = 20
    STAMINA_BAR_X = 10
    STAMINA_BAR_Y = 40
    STAMINA_BAR_WIDTH = 200
    STAMINA_BAR_HEIGHT = 20
    SCORE_MARGIN = 10
    POWERUP_TIMER_Y_START = 100
    POWERUP_TIMER_Y_OFFSET = 30


class GameConfig:
    def __init__(self):
        self.display = DisplayConfig()
        self.entity = EntityConfig()
        self.player = PlayerConfig()
        self.enemy = EnemyConfig()
        self.spawn = SpawnConfig()
        self.powerup = PowerUpConfig()
        self.collision = CollisionConfig()
        self.ui = UIConfig()
        self.width = self.display.WIDTH
        self.height = self.display.HEIGHT
        self.fps = 60
