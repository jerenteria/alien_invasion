import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

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

        # Create an instance(object of the class Ship) of Ship after the screen has been created
        # argument self refers to current instance of AlienInvasion; gives Ship access to games resources, such as the screen object
        # We assign this ship instance to self.ship 
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # set background color
        self.bg_color = (230, 230, 230)
    
    # Loops through all these methods throughout the whole game
    def run_game(self):
        # Starts the loop for the actual game
        while(True):
            # watch for keyboard and mouse events 
            # pygame.event.get() returns list of events that has taken place since function was last called
            self._check_events()
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
            # Print how many bullets are still in the game and verify that bullets are being deleted
            # comment out the print statement because it takes up a lot of time and will slow down game over time
            # print(len(self.bullets))
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
        # Create an instance of Bullet called new_bullet
        new_bullet = Bullet(self)
        # .add() works like append() but written specifically for pygame; adds new bullet
        self.bullets.add(new_bullet)

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
        # Make the most recently drawn screen visible
        # pygame.display.flip() continually updates display to show the new positions of game elements and hides the old ones
        # creating the illusion of smooth movements 
        pygame.display.flip()
    

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game() 