import sys
import pygame
from settings import Settings

class AlienInvasion:
    # constructor class
    def __init__(self):
        """ Overall class to manage game assets and behavior """
        pygame.init()

        # Creates an instance of settings and assign it to self.settings
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # set background color
        self.bg_color = (230, 230, 230)
    
    def run_game(self):
        # Starts the loop for the actual game
        while(True):
            # watch for keyboard and mouse events 
            # pygame.event.get() returns list of events that has taken place since function was last called
            for event in pygame.event.get():
                # if user closes out the game window a pygame.QUIT event is detected
                if event.type == pygame.QUIT:
                    # call sys.exit() to exit the game
                    sys.exit()

                # Redraw the screen during each pass through the loop
                # Fills screen with background color
                self.screen.fill(self.settings.bg_color)

                # Make the most recently drawn screen visible
                # pygame.display.flip() continually updates display to show the new positions of game elements and hides the old ones
                # creating the illusion of smooth movements 
                pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game() 