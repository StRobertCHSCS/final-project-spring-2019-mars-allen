""" Doodle Jump """

import arcade
import random

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.15

SCREEN_WIDTH = 375
SCREEN_HEIGHT = 667
SCREEN_TITLE = "Doodle Jump"

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
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
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.GAME_STARTED = None

        # Variables that will hold sprite lists
        self.player_list = None
        self.platform_list = None

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
        self.platform_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Setting up the player
        self.player_sprite = Player("images/magikarp.gif", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 150
        self.player_sprite.dx = 0
        self.player_sprite.dy = 0
        self.player_sprite.GAME_STARTED = False
        self.player_sprite.GAME_OVER = False
        self.player_list.append(self.player_sprite)

        y = 20

        for i in range(100):

            # Platform image from graphicdesign.stackexchange.com
            platform = arcade.Sprite("images/platform.png", 0.05)

            platform.center_x = random.randrange(SCREEN_WIDTH)
            platform.center_y += y
            self.platform_list.append(platform)

            y += 90

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.platform_list)

    def on_draw(self):
        arcade.start_render()
        self.platform_list.draw()
        self.player_list.draw()


        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.platform_list,
                                                             gravity_constant=GRAVITY)

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
        self.platform_list.update()

        platform_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                 self.platform_list)

        for platform in platform_hit_list:
            self.player_sprite.dy = PLAYER_JUMP_SPEED
            self.score += 1

        self.physics_engine.update()


def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()