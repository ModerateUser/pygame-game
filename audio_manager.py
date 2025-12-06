import pygame
import logging


class AudioManager:
    _instance = None
    
    def __init__(self):
        self.sounds = {}
        self._load_sounds()
    
    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = AudioManager()
        return cls._instance
    
    def _load_sounds(self):
        sound_files = {
            'die_enemy': 'sounds/die_enemy.wav',
            'die_player': 'sounds/die_player.wav',
            'hurt_player': 'sounds/hurt_player.wav',
        }
        
        for sound_name, file_path in sound_files.items():
            try:
                self.sounds[sound_name] = pygame.mixer.Sound(file_path)
            except (pygame.error, IOError) as e:
                logging.warning("Failed to load sound '{}' from '{}': {}".format(sound_name, file_path, e))
    
    def play(self, sound_name, volume=1.0):
        if sound_name not in self.sounds:
            logging.warning("Sound '{}' not found".format(sound_name))
            return False
        
        try:
            sound = self.sounds[sound_name]
            sound.set_volume(volume)
            sound.play()
            return True
        except pygame.error as e:
            logging.warning("Failed to play sound '{}': {}".format(sound_name, e))
            return False
    
    def stop(self, sound_name):
        if sound_name not in self.sounds:
            return False
        
        try:
            self.sounds[sound_name].stop()
            return True
        except pygame.error as e:
            logging.warning("Failed to stop sound '{}': {}".format(sound_name, e))
            return False
    
    def stop_all(self):
        pygame.mixer.stop()
    
    def set_volume(self, sound_name, volume):
        if sound_name not in self.sounds:
            return False
        
        try:
            self.sounds[sound_name].set_volume(max(0.0, min(1.0, volume)))
            return True
        except pygame.error as e:
            logging.warning("Failed to set volume for '{}': {}".format(sound_name, e))
            return False
    
    def set_master_volume(self, volume):
        volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(volume)
