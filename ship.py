import pygame

class Ship:
    """A class to manage the ship """

    # Giving ai_game is a reference to the current instance of the AlienInvasion class(will give class Ship access to all the game
    # resources defined in AlienInvasion class)
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        # Assign screen to an attribute of Ship to access it easily in all the methods in this class
        self.screen = ai_game.screen
        self.settings = ai_game.settings
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

        # Store a decimal value for the ships horizontal position
        # Store the decimal value here because a rect will only keep the integer portion of the value
        self.x = float(self.rect.x)

        # Set the moving right to False by default because we dont want to start the game moving to the right
            # Movement Flag
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Update the ship's position based on the movement flag"""
        # Checks position of the ship before changing the value of self.x
        # self.rect.right returns x coordinate of the right edge of the ship's rect if this val is less than the val returned by
        # self.screen_rect.right, the ship has not reached the left side of the screen
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        # Use if instead of elif b/c elif would give right arrow priority when user is switching arrows keys
        # Ensures ship is within bounds these bounds before before adjusting the value of self.x 
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        # Update rect object from self.x 
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)