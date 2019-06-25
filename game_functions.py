# Simplify run_game and isolate the event management loop

import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        # Create a new bullet and add it to the bullets group.
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # response the keypresses and mouse events
    #Watch for keyboard and mouse events. An event is an action that the user performs, such as pressing a key or moving the mouse.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """ start a new game when the player clicks Play. """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset the game settings.
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scorecard image.
        sb.prep_score()
        sb.prep_level()
        sb.prep_high_score()
        sb.prep_ships()

        # empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # draw the score information.
    sb.show_score()

    # draw the play button if`the game is inactive
    if not stats.game_active:
        play_button.draw_button()
    # Make the most recently draw screen visible
    pygame.display.flip()

def update_ship(ship):
    ship.update()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Update bullets position
    bullets.update()

    # Get rid of bullets that have disappreared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            # print(len(bullets))

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # check for any bullets that have hit aliens
    # if so, get rid of the bullet and the alien_number
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # destroy existing bullets and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """ determine the number of aliens that fit in a row """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x/(2 * alien_width))
    return number_aliens_x

def get_number_aliens_y(ai_settings, ship_height, alien_height):
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y/(2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # create the first row of aliens
    """ create an alien and place it in the row. """
    alien = Alien(ai_settings, screen)
    alien.rect.x = alien.rect.width + 2 * alien.rect.width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """ Create a full fleet of aliens """
    # create an alien and find the number of aliens in a row
    # spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_aliens_y(ai_settings, ship.rect.height, alien.rect.height)

    # create the fleet of aliens
    for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """ respond appropiately if any aliens have reached an edge """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """ drop the entire fleet and change the fleet's direction. """
    for alien in aliens.sprites():
        alien.rect.y +=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """ respond to ship being hit by alien. """
    if stats.ship_left > 1:
        # decrement ships_left
        stats.ship_left -= 1

        # Update Scoreboard
        sb.prep_ships()

        # empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        # create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """
    check if the fleet is at an edge, and
    update the positions of all aliens in the fleet """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, sb,screen, ship, aliens, bullets)

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """ check if any aliens have reached the bottom of the screen """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """ check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
