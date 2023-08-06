import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Initializing ship with starting position"""
        self.screen = screen
        super(Ship, self).__init__()

        """loading the ship"""
        self.image = pygame.image.load('images/spaceship.png')
        self.ai_settings = ai_settings
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        """Start ship at bottom center"""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        """ship center location in decimal"""
        self.center = float(self.rect.centerx)

        """movement flags"""
        self.moving_right = False
        self.moving_left = False

    def m_update(self):
        """updates ships position during movement based on center value"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

            """update rect from self center"""
        self.rect.centerx = self.center

    def blitme(self):
        """draw ship at current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """center the ship on the screen"""
        self.center = self.screen_rect.centerx