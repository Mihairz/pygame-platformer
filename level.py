import pygame
import random
from PIL import Image

from ground import Ground
from coin import Coin


class Level:
    def __init__(self, level_number, screen_width, screen_height):
        self.level_number = level_number

        # Generate ground
        self.ground_image = pygame.image.load("assets/ground.png")
        self.ground_image = pygame.transform.scale(
            self.ground_image, (screen_width, 100))
        self.ground = Ground(0, screen_height - 100,
                             screen_width, 100, self.ground_image, 28)

        # Function to load GIF and extract frames
        def load_gif(filename):
            gif = Image.open(filename)
            frames = []
            try:
                while True:
                    frames.append(pygame.image.fromstring(
                        gif.tobytes(), gif.size, gif.mode))
                    gif.seek(gif.tell() + 1)
            except EOFError:
                frames.remove(frames[0])
                pass  # End of frames
            return frames

        coin_image = load_gif("assets/coin-gif.gif")

        # Generate coins
        self.coins = pygame.sprite.Group()
        for _ in range(level_number * 5):  # Increase coin count with level
            x = random.randint(30, screen_width - 30)
            y = screen_height - 200
            coin = Coin(coin_image, x, y)
            self.coins.add(coin)

        # Load level-specific background (optional)
        self.background_image = pygame.image.load(
            "assets/background.jpg")
        self.background_image = pygame.transform.scale(
            self.background_image, (screen_width, screen_height))

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.ground.image, self.ground.rect)
        self.coins.draw(screen)

    def reset_player_position(self, player):
        player.rect.center = (100, 890)
