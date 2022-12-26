import pygame.font

class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the intial score image
        self.prep_score()
        # Prepare the high score image
        self.prep_high_score()

    
    def prep_score(self):
        """Turn score into a rendered image"""
        # round() normally rounds a decimal number to a set number of decimal places given as the second argument if you pass a negative
            # number it will round to the neares 10,100,1000 and so on here it rounds to the nearest 10 and stores it in rounded_score
        rounded_score = round(self.stats.score, -1)
        # Tells python to insert commas into numbers when converting numerical val into a string
        score_str = "{:,}".format(rounded_score)
        # Then pass this string to render() which turns it into an image; passing screens background color and text color to render()
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Create a rect called score_rect which stores the score so we can position it
        self.score_rect = self.score_image.get_rect()
        # Set its right edge 20px from the right edge of the screen 
        self.score_rect.right = self.screen_rect.right - 20
        # Place top edge 20px down from top of the screen
        self.score_rect.top = 20

    def show_score(self):
        """Draw score to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def prep_high_score(self):
        """Turn the high score into a rendered image"""
        # Round the highest score to the nearest 10
        high_score = round(self.stats.high_score, -1)
        # Add commads to the high score
        high_score_str = "{:,}".format(high_score)
        # Create an image of the high score
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        # Set its top attribute to match the top of the score image
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check to see if there's a new high score"""
        # if the current score is greater than the high score
        if self.stats.score > self.stats.high_score:
            # The current score becomes the new high score
            self.stats.high_score = self.stats.score
            # Call prep_high_score to update the image on the screen with new high score
            self.prep_high_score()