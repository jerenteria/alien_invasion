import pygame.font # Allows pygame to add text to screen

class Button:
    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        # Set font for game; None tells pygame to use default font; 48 is the size of text
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Call _prep_msg() to render the message as an image
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn into a rendered image and center text on the button"""
        # Turns the text stored and turns it into an image and store it as msg_image
        # font.render() takes a boolean value to turn antialiasing on or off (makes edges of text look smoother(less blocky))
        # Here we set antialiasing to True and set background color to the same color as the button
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        # Center the text image on the button by creating a rect from the image and setting its center attribute to match that of 
            # the button
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message
        # Call screen.fill() tp draw rectangular portion of the button
        self.screen.fill(self.button_color, self.rect)
        # Call screen.blit() to draw the text image to the screen
        self.screen.blit(self.msg_image, self.msg_image_rect)