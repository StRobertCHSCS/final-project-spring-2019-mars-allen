""" Doodle Jump """

import arcade
import random

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.35

SCREEN_WIDTH = 375
SCREEN_HEIGHT = 667

"""
class Platform(arcade.Sprite):

    def update(self):
"""

class MyGame(arcade.Window):
    """ Custom window class """

    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Doodle Jump")

        # Variables that will hold sprite lists
        self.player_list = None
        self.platform_list = None
        self.enemy_list = None

        # Setting up player info
        self.player_sprite = None
        self.score = 0

        # Hide mouse cursor
        # self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def setup(self):
        """ Set up the game and initialize the variables """

        # Sprite Lists
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Setting up the player
        self.player_sprite = arcade.Sprite("images/player.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 150
        # self.player_sprite.change_x = 0
        # self.player_sprite.change_y = 0
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()

    """
    def update(self):
        self.player_sprite.center_x += self.player_sprite.change_x
        self.player_sprite.center_y += self.player_sprite.change_y
    """

    def on_key_press(self, key, modifiers):
        """ Called whenever a user presses a key """
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -5
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 5

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()