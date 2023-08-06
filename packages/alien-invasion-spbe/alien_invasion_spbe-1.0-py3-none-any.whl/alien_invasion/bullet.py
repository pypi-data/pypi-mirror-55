import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """manage bullets fired from ship"""

    def __init__(self, ai_settings, screen, ship):
        """create bullet at currect position"""
        super(Bullet, self).__init__()
        self.screen = screen

        """create bullet and set at correct position"""
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        """store bullet position as decimal"""
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
    def update(self):
        """moves the bullet up the screen"""
        self.y -= self.speed_factor
        self.rect.y = self.y
    def draw_bullet(self):
        """draw the bullet"""
        pygame.draw.rect(self.screen, self.color, self.rect)