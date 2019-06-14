""" Doodle Jump """

import arcade
import random

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.18

SCREEN_WIDTH = 375
SCREEN_HEIGHT = 667

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 10


class Player(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)

        self.center_x = 0
        self.center_y = 0
        self.dx = 10
        self.dy = 10
        self.gravity = 10

    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy

        if self.GAME_STARTED:
            self.center_y -= self.gravity

        if self.center_x > SCREEN_WIDTH + 50:
            self.center_x = -50
        elif self.center_x < -50:
            self.center_x = SCREEN_WIDTH + 50


class MyGame(arcade.Window):
    """ Custom window class """

    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Doodle Jump")

        self.GAME_STARTED = None

        # Variables that will hold sprite lists
        self.player_list = None

        # Setting up player info
        self.player_sprite = None
        self.score = 0

        # physics
        self.physics_engine = None

        # Hide mouse cursor
        # self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def setup(self):
        """ Set up the game and initialize the variables """

        # Sprite Lists
        self.player_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Setting up the player
        self.player_sprite = Player("images/magikarp.gif", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 150
        self.player_sprite.dx = 0
        self.player_sprite.dy = 0
        self.player_sprite.GAME_STARTED = False
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()

        # output = f"Score: {self.score}"
        # arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

    def on_key_press(self, key, modifiers):
        """ Called whenever a user presses a key """

        if key == arcade.key.SPACE:
            self.player_sprite.GAME_STARTED = True

        if key == arcade.key.A:
            self.player_sprite.dx = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.dx = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """

        if key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.dx = 0

    def update(self, delta_time):

        self.player_list.update()


def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()