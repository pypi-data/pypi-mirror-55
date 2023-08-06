class Settings():

    def __init__(self):
        """game initial settings"""
        """screen settings"""
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (44, 53, 57)
        """ship settings"""
        self.ship_limit = 3
        """bullet settings"""
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 183, 65, 14
        self.bullets_allowed = 6
        """Alien settings"""
        self.fleet_drop_speed = 10
        """how quickly the game speeds up after every fleet"""
        self.speedup_scale = 1.1
        """how quickly point values increase between levels"""
        self.score_scale = 1.5

        self.initialize_dynamic_settings

    def initialize_dynamic_settings(self):
        """settings that change while the game is played"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.5
        """1 is right and -1 is left"""
        self.fleet_direction = 1
        """points the aliens are worth"""
        self.alien_points = 25

    def increase_speed(self):
        """increase speed every fleet run and point values"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
