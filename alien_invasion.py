# Description of gameplay:
# In Alien Invasion, the player controls a ship that apprears at the bottom centerr of the screen. The player can move the ship right and left using the arrow keys and shoot bullets using the spacebar.When the game begins, a fleet of aliens fills the sky and moves across and down the screen. The player shoots and destroys the aliens.
#
# If the player shoots all the aliens, a new fleet apprears that moves faster than the previous fleet.
# If any alien hits the player's ship or reaches the bottom of the screen, the player loses a ship.
# If the player loses three ships, the game ends.
#
# Installing Pygame:
# python -m pip install --upgrade pipk
# pip install wheel
# C:\Users\80951\OneDrive - Underwriters Laboratories\Code\Aerthis\python_work\alien_invasion>pip install pygame-1.9.6-cp37-cp37m-win32.whl

import pygame #contains the functionality needed to make a game
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # Initialize background setting and create a screen object.
    pygame.init()

    # create an instance of Settings and store it in ai_settingsa after making the call to pygame.init()
    ai_settings = Settings()
    # screen = pygame.display.set_mode(
    #    (ai_settings.screen_width, ai_settings.screen_height))
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))

    #screen object is called a surface. A surface in Pygame is a part of the screen where you display a game element. Each element in the game, like the aliens or the ship, is a surface.
    # screen = pygame.display.set_mode((1200, 800)) #Argument(1200, 800) is a tuple.
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button
    play_button = Button(ai_settings, screen, "Play")

    # create an instance to store game statistics
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship
    ship = Ship(ai_settings, screen)
    # alien = Alien(ai_settings, screen)

    # make a group to store bullets in
    bullets = Group()
    aliens = Group()

    # create a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)


    # Start the main loop for the game: the loop contains an event loop and code that manages screen updates.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            gf.update_ship(ship)
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
