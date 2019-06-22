""" Doodle Jump """

import arcade
import random

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.12

SCREEN_WIDTH = 375
SCREEN_HEIGHT = 667

PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 15

TITLE_SCREEN = 1
GAME_START = 2

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


class Player(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)

        self.center_x = 0
        self.center_y = 0
        self.dx = 0
        self.dy = 0

    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy

        if self.center_x > SCREEN_WIDTH + 50:
            self.center_x = -50
        elif self.center_x < -50:
            self.center_x = SCREEN_WIDTH + 50

        if self.center_y < 0:
            self.kill()


class Platform(arcade.Sprite):

    def update(self):
        self.center_y -= 1


class MyGame(arcade.Window):
    """ Custom window class """

    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Doodle Jump")

        # Variables that will hold sprite lists
        self.player_list = None
        self.platform_list = None

        # Setting up player info
        self.player_sprite = None
        self.score = 0

        # physics
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Hide mouse cursor
        # self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def setup(self):
        """ Set up the game and initialize the variables """

        self.view_bottom = 0
        self.view_left = 0

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

        # Platform image from graphicdesign.stackexchange.com
        platform = Platform("images/platform.png", 0.05)

        platform.center_x = 50
        platform.center_y = 110
        self.platform_list.append(platform)

        y = 200

        for i in range(100):
            # Platform image from graphicdesign.stackexchange.com
            platform = Platform("images/platform.png", 0.05)

            platform.center_x = random.randrange(SCREEN_WIDTH)
            platform.center_y += y
            self.platform_list.append(platform)

            y += 90

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.platform_list)

    def on_draw(self):

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.platform_list,
                                                             gravity_constant=GRAVITY)

        arcade.start_render()
        self.platform_list.draw()
        self.player_list.draw()

        # draw score on screen
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10 + self.view_bottom, arcade.color.BLACK, 18)

    def on_key_press(self, key, modifiers):
        """ Called whenever a user presses a key """

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
        self.physics_engine.update()

        platform_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                 self.platform_list)

        for platform in platform_hit_list:
            self.player_sprite.dy = PLAYER_JUMP_SPEED
            self.score += 1


        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left = 0
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left = 0
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom = 0

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)



def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()