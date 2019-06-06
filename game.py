""" Doodle Jump """

import arcade
import random

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.35

SCREEN_WIDTH = 375
SCREEN_HEIGHT = 667

PLAYER_MOVEMENT_SPEED = 5


class Player(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)

        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.velocity = 10
        self.gravity = 5

    def update(self):



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
        self.player_sprite = Player("images/player.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.x = 50
        self.player_sprite.y = 150
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
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
        if key == arcade.key.A:
            self.player_sprite.change = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

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