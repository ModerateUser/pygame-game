import logging


class HighScoreManager:
    def __init__(self, filename="highscore.txt"):
        self.filename = filename
        self.high_score = self._load()
    
    def _load(self):
        try:
            with open(self.filename, 'r') as f:
                return int(f.read().strip())
        except (IOError, ValueError) as e:
            logging.info("Failed to load high score from '{}': {}".format(self.filename, e))
            return self._create_default_file()
    
    def _create_default_file(self):
        try:
            with open(self.filename, 'w') as f:
                f.write('0')
            return 0
        except IOError as e:
            logging.error("Failed to create high score file '{}': {}".format(self.filename, e))
            return 0
    
    def get_high_score(self):
        return self.high_score
    
    def save(self, score):
        if score > self.high_score:
            self.high_score = score
            try:
                with open(self.filename, 'w') as f:
                    f.write(str(score))
                logging.info("New high score: {}".format(score))
            except IOError as e:
                logging.error("Failed to save high score to '{}': {}".format(self.filename, e))
    
    def reset(self):
        self.high_score = 0
        try:
            with open(self.filename, 'w') as f:
                f.write('0')
            logging.info("High score reset")
        except IOError as e:
            logging.error("Failed to reset high score in '{}': {}".format(self.filename, e))
