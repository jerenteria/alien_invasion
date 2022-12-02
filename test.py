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

                # The surface(part of the screen where a game element can be displayed)
                    # Each element in the game(ship/alien) is its own surface
                    # Screen itself is a surface
                # Redraw the screen during each pass through the loop
                # Fills screen with background color
                self.screen.fill(self.settings.bg_color)
                # Call ship.blitme() after filling the screen so the ship appears on top of the background
                self.ship.blitme()
                
                # Make the most recently drawn screen visible
                # pygame.display.flip() continually updates display to show the new positions of game elements and hides the old ones
                # creating the illusion of smooth movements 
                pygame.display.flip()
