class Settings:
    """A class to store all settings for Alien Invasion """

    def __init__(self):
        """Initialize the game's settings """

        #screen settings
        # makes the screen(called a "surface" in pygame) of the game 1200px wide by 800px high
        self.screen_width = 1200
        self.screen_height = 800
        # set background color
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5

        # Bullet setting
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        