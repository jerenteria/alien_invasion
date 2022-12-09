import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_game):
        """Initialize the alien and set it's starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        # An alien is at the right edge if the right attribute of its rect is greater than the screens rect 
        # It's at the left edge if its less than or equal to 0
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True


    def update(self):
        """Move alien to the right or left"""
        # Allows motion to the left or right by multiplying the aliens speed by the val of fleet_direction
        # If fleet_direction = 1 val of alien_speed will be added to aliens current position, moving to the right; if fleet val
        # is -1, the val will be subtracted from aliens position, moving alien to the left
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        # Set the speed to alien_speed in alien settings
        self.x += self.settings.alien_speed
        # Use the val of self.x to update the position of the aliens rect
        self.rect.x = self.x
    

