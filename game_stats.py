class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        # Start Alien Invasion in an inactive state; Dont want to start game from launch we want to wait until player presses start
        self.game_active = False
        # High score should never be reset 
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        # Start the player with a score of 0
        self.score = 0
        self.level = 1