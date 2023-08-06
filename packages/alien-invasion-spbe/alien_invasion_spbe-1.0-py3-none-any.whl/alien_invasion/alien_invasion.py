import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #making a game screen
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion!!!")

    """make the play button"""
    play_button = Button(ai_settings, screen, "Let's Play!")

    """create instance to store game statistics and create scoreboard"""
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    """make ship"""
    ship = Ship(ai_settings, screen)
    """make alien group"""
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    """store bullets in a group"""
    bullets = Group()

    """main game loop"""
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.m_update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()

