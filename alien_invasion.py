import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    # constructor class
    def __init__(self):
        """ Overall class to manage game assets and behavior """
        pygame.init()

        # Creates an instance of settings and assign it to self.settings
        self.settings = Settings()
        # Pass a size of (0,0) and tell pygame to go fullscreen b/c we dont know the screen size ahead of time
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics 
        self.stats = GameStats(self)
        # Create an instance to create a scoreboard
        self.sb = Scoreboard(self)

        # Create an instance(object of the class Ship) of Ship after the screen has been created
        # argument self refers to current instance of AlienInvasion; gives Ship access to games resources, such as the screen object
        # We assign this ship instance to self.ship 
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()


        # Make the play button
        self.play_button = Button(self, "Play")

        # set background color
        self.bg_color = (230, 230, 230)
    
    # Loops through all these methods throughout the whole game
    def run_game(self):
        # Starts the loop for the actual game
        while(True):
            # watch for keyboard and mouse events 
            # pygame.event.get() returns list of events that has taken place since function was last called
            self._check_events()
            # Print how many bullets are still in the game and verify that bullets are being deleted
            # comment out the print statement because it takes up a lot of time and will slow down game over time
            # print(len(self.bullets))
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # call sys.exit() to exit the game
                sys.exit()
                # Check if the event type is a key being pressed down
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)  
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            # Check if the player clicks mouse on screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of x and y coordinates when mouse is being clicked
                mouse_pos = pygame.mouse.get_pos()
                # Send these values to the new method _check_play_button()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play"""
        # Use rect method collidepoint() to check whether the point of the mouse click overlaps the region defined by the
            # Play button's rect
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # Only start the game if Play is clicked and the game is not currently active
        if button_clicked and not self.stats.game_active:
            # Reset the game settings after new start
            self.settings.initialize_dynamic_settings()
            # Reset the game stats
            self.stats.reset_stats()
            # If so set game_active to True and start the game 
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    # Respond to keypresses
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # Change moving_right in ship.py to True so the ship can move to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # Press q to quit game
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    # Respond to key releases
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            # Switch moving_right back to False to stop the ship from moving
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        # If there are less than bullets allowed create a new bullet but if 3 bullets are already active nothing happens when pressing space
        # This allows the player to only shoot bullets in groups of 3
        if len(self.bullets) < self.settings.bullets_allowed:
            # Create an instance of Bullet called new_bullet
            new_bullet = Bullet(self)
            # .add() works like append() but written specifically for pygame; adds new bullet
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Happens after we check for events and before the screen updates so the screen updates with the players movement
        self.ship.update()
        # When you call update() on a group, the group automatically calls update() for each Sprite in the group
        # self.bullets.update() calls bullet.update() for each bullet we place in the group bullets
        self.bullets.update()
        # Get rid of bullets that have dissapeared
        # Copy() allows us to modidfy bullets inside the loop since we cannot remove items in a list/group within a for loop
        # By looping over a copy of the group
        for bullet in self.bullets.copy():
            # Check each bullet if its dissapeared at the top of screen
            if bullet.rect.bottom <= 0:
                # If bullet disppeared remove it
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        # Check for any bullets that have hit aliens
        # If so, get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        # Update score
        if collisions:
            # Loop through all the aliens(values in the dictionary)
            for aliens in collisions.values():
                # Set the score to be the amount of points * the amount of aliens hit
                self.stats.score += self.settings.alien_points * len(aliens)
                # Update the score
            self.sb.prep_score()
            # Everytime a alien is hit check the score to see if its higher than the current high score
            self.sb.check_high_score()
        # check if aliens group is empty
        if not self.aliens:
            # If it is get rid of existing bullets using empty()
            self.bullets.empty()
            # Refill screen with new fleet of aliens
            self._create_fleet()
            # Call increase_speed in settings.py to increase the speed everytime all the aliens have been shot down to lvl up!
            self.settings.increase_speed()
            # Increase level
            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):
        """Check if the fleet is at an edge then update the positions if all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        # Look for alien-ship collisions
        # spritecollideany() function takes two arguments, a sprite and a group and looks for any member of the group that has 
        # collided with the sprite
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen; if there is an alien at bottom of screen a new fleet will appear
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien first before we perform calculations 
        alien = Alien(self)
        # Get width/height of alien by creating tuple(used to store multiple items in a single variable) .size is the tuple
        alien_width, alien_height = alien.rect.size
        # Calculate the horizontal space available for aliens and the number of aliens that can fit into that space
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        # find available vertical space by subtracting the alien height from the top, ship height from the bottom, and two alien
        # heights from the bottom of the screen
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens
        # The outter loop counts from 0 to the number of rows we want
        for row_number in range(number_rows):
            # Loop that counts from 0 to the number of aliens we need to make
            # Inner loop creates aliens for one row
            for alien_number in range(number_aliens_x):
                # Include argument for row number so each row can be further down the screen
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create alien and place it in the row"""
        # Create an alien 
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # Set aliens x coordinate val to place it in the row
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        # Change aliens y-coordinate when its not in the first row to create empty space at top of screen
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached edge"""
        # Loop through the fleet and call check_edges
        for alien in self.aliens.sprites():
            # If check_edges() returns True, we know an alien is at an edge and the whole fleet needs to change direction
            if alien.check_edges():
                # Call _change_fleet_direction()
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        # Loop through all the aliens
        for alien in self.aliens.sprites():
            # Drop each alien using fleet_drop_speed
            alien.rect.y += self.settings.fleet_drop_speed
            # Change the value of fleet_direction by multiplying is current val by -1. The line that changes the fleets direction
            # isn't part of the for loop, we want to change each alien's vertical position, but change fleet's direction only once
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        # If the # of ships that are left is greater than 0 do the following and keep the game going
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1
            # After removing a ship display the correct amount of remaining ships on the screen
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # Pause 
            sleep(0.5)
        # Switch the game_active to False and end the game if player has ran out of ships
        else:
            self.stats.game_active = False
            # Bring back mouse cursor when game ends
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this like when the ships get hit
                self._ship_hit()
                break

    def _update_screen(self):
        # The surface(part of the screen where a game element can be displayed)
        # Each element in the game(ship/alien) is its own surface
        # Screen itself is a surface
        # Redraw the screen during each pass through the loop
        # Fills screen with background color
        self.screen.fill(self.settings.bg_color)
        # Call ship.blitme() after filling the screen so the ship appears on top of the background
        self.ship.blitme()
        # bullets.sprites() returns a list of all sprites in the group bullets
        # To draw bullets on screen we loop through the sprites in bullets and call draw_bullet() on each one 
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # when you call draw() on a group pygame draws each element in the group position defined by its rect attribute
        # draw() requires one argument: a surface to draw elements
        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        # pygame.display.flip() continually updates display to show the new positions of game elements and hides the old ones
        # creating the illusion of smooth movements 
        pygame.display.flip()
    

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game() 