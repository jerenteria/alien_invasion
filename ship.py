import pygame

class Ship:
    """A class to manage the ship """

    # Giving ai_game is a reference to the current instance of the AlienInvasion class(will give class Ship access to all the game
    # resources defined in AlienInvasion class)
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        # Assign screen to an attribute of Ship to access it easily in all the methods in this class
        self.screen = ai_game.screen
        # Access the screens rect(rectangle) attribute using the get_rect() method and assign it to self.screen_rect
            # this allows us to place the ship in the correct location on the screen 
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image by giving the location of image
            # This returns a surface(the ship) which we assigned to self.image
        self.image = pygame.image.load('images/ship.bmp')
        # After image is loaded we call self.rect() to access the ships surface's rect attribute so we can later use it to 
        # place the ship
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom of center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)