import pygame
import random
from PIL import Image

from ground import Ground
from coin import Coin


class Level:
    def __init__(self, level_number, screen_width, screen_height):
        self.level_number = level_number

        self.ground_image = pygame.image.load("assets/ground.png")
        self.ground_image = pygame.transform.scale(
            self.ground_image, (screen_width, 100))
        self.ground = Ground(0, screen_height - 100,
                             screen_width, 100, self.ground_image, 28)
        
        self.platform_image = pygame.Surface((200, 20))
        self.platform_image.fill((200, 100, 50))  # Brown color for platforms

        self.platforms = pygame.sprite.Group()
        if level_number == 2:
            platform1 = Ground(400, screen_height - 100, 200, 20, self.platform_image, 20)
            platform2 = Ground(1200, screen_height - 200, 200, 20, self.platform_image, 20)
            self.platforms.add(platform1, platform2)
        if level_number == 3:
            moving_platform_h = Ground(200, screen_height - 300, 250, 20, self.platform_image, 20,
                                       move_type="horizontal", move_range=150, move_speed=2)
            moving_platform_v = Ground(600, screen_height - 500, 200, 20, self.platform_image, 20,
                                       move_type="vertical", move_range=150, move_speed=2)

            self.platforms.add(moving_platform_h, moving_platform_v)

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
        for i in range(5):
            if level_number == 1:
                # Coins in a straight line for level 1
                x = 100 + i * 300
                y = screen_height - 150
            elif level_number == 2:
                # Two coins higher, three near ground
                if i < 2:
                    x = 450 + i * 400
                    y = screen_height - 450  # Higher coins
                else:
                    x = 100 + (i - 2) * 300
                    y = screen_height - 150  # Near ground coins
            elif level_number == 3:
                if i == 0:
                    x = 650  # Above the moving vertical platform
                    y = screen_height - 650
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
        self.platforms.draw(screen)
        self.coins.draw(screen)
        
    def update(self):
        self.platforms.update()  # Update platform movements

    def reset_player_position(self, player):
        player.rect.center = (100, 890)
