import pygame
import random


class Screen:
    def __init__(self, width=1200, height=800, background_color=(0, 0, 0)):
        """Initializes the screen with given width, height, and background color.

        Args:
            width (int): The width of the screen. Default is 1200.
            height (int): The height of the screen. Default is 800.
            background_color (tuple): RGB color for the background. Default is black (0, 0, 0).
        """
        self.screen_width = width
        self.screen_height = height
        self.background_color = background_color
        self.screen = None

    def create_screen(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def fill(self):
        self.screen.fill(self.background_color)

    def update(self):
        pygame.display.flip()

    def quit(self):
        pygame.quit()


class Game:
    def __init__(self, screen, snake_color=(67, 171, 67), food_color=(171, 67, 67)):
        """Initializes the game with a screen, snake color, and food color.

        Args:
            screen (Screen): The screen object where the game is drawn.
            snake_color (tuple): RGB color for the snake. Default is green (67, 171, 67).
            food_color (tuple): RGB color for the food. Default is red (171, 67, 67).
        """
        self.screen = screen.screen
        self.screen_width = screen.screen_width
        self.screen_height = screen.screen_height

        self.snake_color = snake_color
        self.snake_body = [(self.screen_width / 2, self.screen_height / 2)]
        self.direction = pygame.K_UP
        self.speed = 25

        self.food_color = food_color
        self.food_x = None
        self.food_y = None

        self.score = 0
        self.text_font = pygame.font.Font("assets/VT323-Regular.ttf", 50)

        self.eat_sound = pygame.mixer.Sound("assets/collect-sounds.mp3")

    def draw_score(self):
        """Draws the current score on the top right of the screen."""
        score_text = self.text_font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(topright=(self.screen_width - 10, 10))
        self.screen.blit(score_text, score_rect)

    def draw_snake(self):
        """Draws the snake on the screen."""
        for segment in self.snake_body:
            pygame.draw.rect(
                self.screen,
                self.snake_color,
                pygame.Rect(segment[0], segment[1], 25, 25),
            )

    def get_snake_position(self):
        """Gets the current position of the snake's head.

        Returns:
            tuple: (x, y) coordinates of the snake's head.
        """
        return self.snake_body[0]

    def draw_food(self):
        """Draws the food on the screen at a random position if not already placed."""
        if self.food_x is None or self.food_y is None:
            self.food_x = random.randint(0, self.screen_width - 25)
            self.food_y = random.randint(0, self.screen_height - 25)
        pygame.draw.rect(
            self.screen, self.food_color, pygame.Rect(self.food_x, self.food_y, 25, 25)
        )

    def update_position(self):
        """Updates the snake's position based on the current direction."""
        head_x, head_y = self.snake_body[0]
        if self.direction == pygame.K_UP:
            head_y -= self.speed
        elif self.direction == pygame.K_DOWN:
            head_y += self.speed
        elif self.direction == pygame.K_LEFT:
            head_x -= self.speed
        elif self.direction == pygame.K_RIGHT:
            head_x += self.speed

        head_x = head_x % self.screen_width
        head_y = head_y % self.screen_height

        new_head = (head_x, head_y)
        self.snake_body.insert(0, new_head)
        if not self.check_collision_with_food():
            self.snake_body.pop()
        else:
            self.food_x = None
            self.food_y = None
            self.score += 1

            pygame.mixer.Sound.play(self.eat_sound)

    def check_collision_with_food(self):
        head_rect = pygame.Rect(self.snake_body[0][0], self.snake_body[0][1], 25, 25)
        food_rect = pygame.Rect(self.food_x, self.food_y, 25, 25)
        return head_rect.colliderect(food_rect)

    def check_collision_with_self(self):
        if self.snake_body[0] in self.snake_body[1:]:
            return True

    def start_game_screen(self):
        name_creator_text = self.text_font.render(
            "Created by: Giovani Simões", True, (255, 255, 255)
        )
        game_title_text = self.text_font.render(
            "Python the Game!", True, (255, 255, 255)
        )
        start_text = self.text_font.render(
            'Press "Space" to Start', True, (255, 255, 255)
        )
        tutorial_text = self.text_font.render(
            "Use Arrow Keys to Move", True, (255, 255, 255)
        )

        name_creator_rect = name_creator_text.get_rect(
            center=(self.screen_width / 2 + 300, self.screen_height / 2 + 350)
        )
        game_title_rect = game_title_text.get_rect(
            center=(self.screen_width / 2, self.screen_height / 2 - 200)
        )
        start_rect = start_text.get_rect(
            center=(self.screen_width / 2, self.screen_height / 2)
        )
        tutorial_rect = tutorial_text.get_rect(
            center=(self.screen_width / 2, self.screen_height / 2 + 50)
        )

        self.screen.blit(name_creator_text, name_creator_rect)
        self.screen.blit(game_title_text, game_title_rect)
        self.screen.blit(start_text, start_rect)
        self.screen.blit(tutorial_text, tutorial_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

    def game_over_screen(self):
        """Displays the game over screen with the score and options to restart or quit.

        Returns:
            bool: True if the game is restarted, False if quit.
        """
        self.screen.fill((0, 0, 0))
        game_over_text = self.text_font.render(f"Game Over", True, (255, 255, 255))
        score_text = self.text_font.render(
            f"Your Score was {self.score}!", True, (255, 255, 255)
        )
        restart_text = self.text_font.render(
            "Press R to Restart", True, (255, 255, 255)
        )
        quit_text = self.text_font.render("Press Q to Quit", True, (255, 255, 255))

        game_over_rect = game_over_text.get_rect(
            center=(self.screen_width / 2, self.screen_height / 2 - 50)
        )
        score_rect = score_text.get_rect(
            center=(self.screen_width / 2, self.screen_height / 2)
        )
        restart_rect = restart_text.get_rect(
            center=(self.screen_width / 2, self.screen_height / 2 + 50)
        )
        quit_rect = quit_text.get_rect(
            center=(self.screen_width / 2, self.screen_height / 2 + 100)
        )

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        pygame.mixer.music.stop()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        return True
                    elif event.key == pygame.K_q:
                        return False
                elif event.type == pygame.QUIT:
                    return False

    def reset_game(self):
        self.snake_body = [(self.screen_width / 2, self.screen_height / 2)]
        self.direction = pygame.K_UP
        self.food_x = None
        self.food_y = None
        self.score = 0
        pygame.mixer.music.play(-1)




def main():
    """Initializes the game and runs the main game loop."""
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    running = True

    screen = Screen()
    screen.create_screen()

    game = Game(screen)
    game.start_game_screen()

    pygame.mixer.music.load("assets/background-music-Pixel Dreams.mp3")
    pygame.mixer.music.set_volume(0.02)
    pygame.mixer.music.play(-1)

    game.eat_sound.set_volume(0.05)

    while running:
        screen.fill()

        if game.check_collision_with_self():
            if not game.game_over_screen():
                running = False
                break
            else:
                screen.fill()
                continue

        allow_any_direction = len(game.snake_body) == 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen.quit()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [
                    pygame.K_UP,
                    pygame.K_DOWN,
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                ]:
                    if allow_any_direction:
                        game.direction = event.key
                    else:
                        if event.key == pygame.K_UP and game.direction != pygame.K_DOWN:
                            game.direction = event.key
                        elif (
                                event.key == pygame.K_DOWN and game.direction != pygame.K_UP
                        ):
                            game.direction = event.key
                        elif (
                                event.key == pygame.K_LEFT
                                and game.direction != pygame.K_RIGHT
                        ):
                            game.direction = event.key
                        elif (
                                event.key == pygame.K_RIGHT
                                and game.direction != pygame.K_LEFT
                        ):
                            game.direction = event.key
                else:
                    pass

        game.draw_food()
        game.draw_snake()
        game.draw_score()

        game.update_position()
        screen.update()
        pygame.time.delay(100)

if __name__ == "__main__":
    main()
