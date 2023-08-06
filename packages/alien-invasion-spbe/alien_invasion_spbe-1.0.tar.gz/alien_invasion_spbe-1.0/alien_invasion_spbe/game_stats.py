class GameStats():
    """tracking statistics for ship hits and scoring points"""

    def __init__(self, ai_settings):
        """Initial statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        """start game active"""
        self.game_active = False
        """high score will not be reset"""
        self.high_score = 0

    def reset_stats(self):
        """initialize statistics that change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1