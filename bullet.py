import pygame
from pygame.sprite import Sprite # Sprites allow you to group related elements in your game and act on all grouped elements at once

# Sprites are objects with differect properties like height, width, color, etc
class Bullet(Sprite):
    """Manages bullets fired from ship"""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect attribute at (0,0) and then correct the position
        # We are not using an image for bullets so we have to build from scratch using pygame.Rect() class
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        # Set the bullet's midtop attribute to match the ship's midtop attribute(this will make the bullet merge from top of ship,
        # making it look like the bullet is fired from ship)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    # Manage the bullet's position
    def update(self):
        """Move the bullet up the screen"""
        # Update the decimal position of the bullet
        # When the bullet is fired it moves up the screen which is a decreasing y-value so we subtract the amount stored
        # in settings.bullet_speed from self.y
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
    
    # When we want to draw a bullet we call draw_bullet()
    def draw_bullet(self):
        """Draw the bullet to the screen"""
        # draw.rect() fills the part of the scrreen defined by the bullet's rect with the color stored in self.color
        pygame.draw.rect(self.screen, self.color, self.rect)