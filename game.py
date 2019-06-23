""" Magikarp Jump """

import arcade
import random

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.12
SPRITE_SCALE_PLATFORM = 0.035
SCREEN_WIDTH = 375
SCREEN_HEIGHT = 667
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 13

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.d
TOP_VIEWPORT_MARGIN = 100


# creating Player class
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


# creating Platform class
class Platform(arcade.Sprite):

    def update(self):
        self.center_y -= 1


# creating a class for MyGame
class MyGame(arcade.Window):
    """ Custom window class """

    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Doodle Jump")

        # sprite lists that will hold sprites
        self.player_list = None
        self.platform_list = None

        # Setting up player info
        self.player_sprite = None

        # physics
        self.physics_engine = None

        # scrolling
        self.view_bottom = 0
        self.view_left = 0

        arcade.set_background_color(arcade.color.BABY_BLUE)

    def setup(self):
        """ Set up the game and initialize the variables """

        self.view_bottom = 0
        self.view_left = 0

        # Sprite Lists
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()

        # Setting up the player
        self.player_sprite = Player("images/magikarp.gif", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)

        # Platform image from graphicdesign.stackexchange.com
        platform = Platform("images/ledge.png", SPRITE_SCALE_PLATFORM)
        platform.center_x = 50
        platform.center_y = 110
        self.platform_list.append(platform)

        y = 200

        for i in range(100):
            # Platform image from graphicdesign.stackexchange.com
            platform = Platform("images/ledge.png", SPRITE_SCALE_PLATFORM)

            platform.center_x = random.randrange(SCREEN_WIDTH)
            platform.center_y += y
            self.platform_list.append(platform)

            y += 130

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.platform_list)

    def on_draw(self):

        # render drawings
        arcade.start_render()

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.platform_list,
                                                             gravity_constant=GRAVITY)

        # Background image from freepik.com
        bg = arcade.load_texture("images/bg.jpg")
        scale = 2
        arcade.draw_texture_rectangle(150, SCREEN_HEIGHT/3 + self.view_bottom, scale * bg.width,
                                      scale * bg.height, bg, 0)

        # draws all features
        self.platform_list.draw()
        self.player_list.draw()

        # check if player reaches bottom (y = 0)
        if self.player_sprite.top < self.view_bottom:
            self.player_sprite.kill()
            arcade.draw_text("YOU DIED", SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2 + self.view_bottom, arcade.color.BLACK,
                             40)

    def on_key_press(self, key, modifiers):
        """ Called whenever a user presses a key """

        # move player left & right with A & D
        if key == arcade.key.A:
            self.player_sprite.dx = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.dx = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """

        # stop player if nothing is pressed / key is released
        if key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.dx = 0

    def update(self, delta_time):

        # create list of platforms that touch the player
        platform_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                 self.platform_list)

        # if player touches platform, jump
        for platform in platform_hit_list:
            self.player_sprite.dy = PLAYER_JUMP_SPEED

        # delete platforms that reach the bottom
        for platform in self.platform_list:
            if platform.top < self.view_bottom:
                platform.kill()

        # update sprite lists
        self.player_list.update()
        self.platform_list.update()

        # update physics
        self.physics_engine.update()

        # --- Scrolling ---

        changed = False

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        if changed:
            # Only scroll to integers
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