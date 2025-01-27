import pygame
import random
from PIL import Image

from enemy import Enemy
from ground import Ground
from coin import Coin

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

class Level:
    def __init__(self, level_number, screen_width, screen_height):
        self.level_number = level_number
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.winner = False

        self.ground_image = pygame.image.load("assets/ground.png")
        self.ground_image = pygame.transform.scale(
            self.ground_image, (screen_width, 100))
        self.ground = Ground(0, screen_height - 100,
                             screen_width, 100, self.ground_image, 28)
        
        self.platform_image = pygame.image.load("assets/platform.png")

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
        if self.level_number == 4:
            platform1 = Ground(200, screen_height - 400, 150, 20, self.platform_image, 20, move_type="horizontal", move_range=200, move_speed=2)
            platform2 = Ground(500, screen_height - 300, 150, 20, self.platform_image, 20, move_type="vertical", move_range=100, move_speed=2)
            platform3 = Ground(800, screen_height - 400, 150, 20, self.platform_image, 20, move_type="horizontal", move_range=200, move_speed=2)
            self.platforms.add(platform1, platform2, platform3)

        coin_image = load_gif("assets/coin-gif.gif")
        # Generate coins
        self.coins = pygame.sprite.Group()
        for i in range(5):
            if level_number == 1:
                # Coins in a straight line
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
                else:
                    x = 300 + i * 200  # Above the moving vertical platform
                    y = screen_height - 650
            elif level_number == 4:
                for i in range(5):
                    if i == 0:
                        x = 220
                        y = screen_height - 450  # On the first horizontal platform
                    elif i == 1:
                        x = 550
                        y = screen_height - 350  # On the vertical platform
                    elif i == 2:
                        x = 820
                        y = screen_height - 450  # On the last horizontal platform
                    elif i == 3:
                        x = 550
                        y = screen_height - 500  # Highest
                    elif i == 4:
                        x = random.randint(200, screen_width - 200)  # Near enemies
                        y = screen_height - 150
                        
            coin = Coin(coin_image, x, y)
            self.coins.add(coin)

        # Level-specific background
        match (level_number):
            case 1:
                self.background_image = pygame.image.load("assets/background.jpg")
            case 2:
                self.background_image = pygame.image.load("assets/background2.jpg")
            case 3:
                self.background_image = pygame.image.load("assets/background3.jpg")
            case 4:
                self.background_image = pygame.image.load("assets/background4.jpg")
            case _:
                self.background_image = pygame.image.load("assets/background.jpg")


        self.background_image = pygame.transform.scale(
            self.background_image, (screen_width, screen_height))
        
        self.enemy_group = pygame.sprite.Group()
        self.enemy_spawn_timer = 0
        
        # Load arrow image
        self.arrow_image = pygame.image.load("assets/right-arrow.png")
        self.arrow_image = pygame.transform.scale(self.arrow_image, (150, 150))
        self.arrow_rect = self.arrow_image.get_rect()
        self.arrow_rect.right = screen_width - 20
        self.arrow_rect.centery = screen_height // 2


    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.ground.image, self.ground.rect)
        self.platforms.draw(screen)
        self.coins.draw(screen)
        self.enemy_group.draw(screen)
        
        if len(self.coins) == 0 and self.level_number != 4:
            screen.blit(self.arrow_image, self.arrow_rect)
        
    def update(self):
        self.platforms.update()
        
        if not self.winner and self.level_number == 4:
            self.enemy_spawn_timer += 1
            
            if self.enemy_spawn_timer >= 100:  # ms
                enemy = Enemy(self.screen_width, self.screen_height - 150, speed=3)
                self.enemy_group.add(enemy)
                self.enemy_spawn_timer = 0
        self.enemy_group.update()
        
        for coin in self.coins:
            coin.update()
        if len(self.coins) == 0:
            self.winner = True
            self.enemy_group.empty()

    def reset_player_position(self, player):
        player.rect.center = (100, 890)
