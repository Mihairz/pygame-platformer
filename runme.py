import pygame
from PIL import Image
import ctypes  # For Windows icon manipulation

from ground import Ground
from coin import display_score
from level import Level


# Initialize Pygame
pygame.init()

background_music = pygame.mixer.Sound("assets/bg-song.mp3")
background_music.play(-1)

icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)

# Set the taskbar icon (Windows only)
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
    "GISS Final Project")
# Set the caption to make sure Windows recognizes the icon change
pygame.display.set_caption("GISS Final Project")


# Screen dimensions
SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Physics constants
WALK_SPD = 5
RUN_SPD = 7
JUMP_STRENGTH = -12
GRAVITY = 0.5

score = 0


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


# Loading assets
player_frames_standing = load_gif("assets/stand-gif.gif")
player_frames_walkRight = load_gif("assets/walk-right-gif.gif")
player_frames_walkLeft = load_gif("assets/walk-left-gif.gif")
player_frames_runRight = load_gif("assets/run-right-gif.gif")
player_frames_runLeft = load_gif("assets/run-left-gif.gif")

ground_image = pygame.image.load("assets/ground.png")
ground_image = pygame.transform.scale(ground_image, (SCREEN_WIDTH, 100))

coin_image = load_gif("assets/coin-gif.gif")
coin_sound = pygame.mixer.Sound("assets/coin-wav.wav")
coin_sound.set_volume(0.2)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.standing_frames = player_frames_standing
        self.walk_right_frames = player_frames_walkRight
        self.walk_left_frames = player_frames_walkLeft
        self.run_right_frames = player_frames_runRight
        self.run_left_frames = player_frames_runLeft

        self.frames = self.standing_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.animation_speed = 100  # Speed in ms
        self.last_update = pygame.time.get_ticks()
        self.rect = self.image.get_rect()

        # Starting position
        self.rect.center = (100, 890)
        self.on_ground = True

        self.speed_x = 0
        self.speed_y = 0
        
        self.current_platform = None

    def update(self):

        # Apply gravity
        if not self.on_ground:
            self.speed_y += GRAVITY

        # Update gif based on speed
        if self.speed_x > WALK_SPD:
            if self.frames != self.run_right_frames:
                self.frames = self.run_right_frames
                self.current_frame = 0
        elif self.speed_x > 0:
            if self.frames != self.walk_right_frames:
                self.frames = self.walk_right_frames
                self.current_frame = 0
        elif self.speed_x < -WALK_SPD:
            if self.frames != self.run_left_frames:
                self.frames = self.run_left_frames
                self.current_frame = 0
        elif self.speed_x < 0:
            if self.frames != self.walk_left_frames:
                self.frames = self.walk_left_frames
                self.current_freame = 0
        else:
            if self.frames != self.standing_frames:
                self.frames = self.standing_frames
                self.current_frame = 0

        # Update position based on speed
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Update the current frame for animation
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:  # Change frame every 100 ms
            # Loop through frames
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]  # Update image
            self.last_update = now

        # Check if the player is on the ground or platforms
        self.on_ground = False
        
        if self.rect.colliderect(ground.ground_rect) and self.speed_y > 0:
            self.rect.bottom = ground.ground_rect.top
            self.speed_y = 0
            self.on_ground = True
        else:
            for platform in current_level.platforms:
                if self.rect.colliderect(platform.ground_rect) and self.speed_y > 0:
                    self.rect.bottom = platform.ground_rect.top
                    self.speed_y = 0
                    self.on_ground = True
                     # If the platform is moving, adjust the player's position
                    if platform.move_type == "horizontal":
                         self.rect.x += platform.move_speed * platform.direction
                    elif platform.move_type == "vertical":
                        self.rect.y += platform.move_speed * platform.direction

                    break  # Stop checking once we've landed
                
# Handle input
def handle_input(player):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        if keys[pygame.K_z]:
            player.speed_x = -RUN_SPD
        else:
            player.speed_x = -WALK_SPD
    elif keys[pygame.K_RIGHT]:
        if keys[pygame.K_z]:
            player.speed_x = RUN_SPD
        else:
            player.speed_x = WALK_SPD
    else:
        player.speed_x = 0

    if keys[pygame.K_SPACE] and player.on_ground:
        player.speed_y = JUMP_STRENGTH
        player.on_ground = False


def display_commands(screen):
    font = pygame.font.Font(None, 36)
    text = 'Move with arrow keys, jump with space, run with z + arrow key. Collect all the coins and move to the right edge.'
    
    main_text = font.render(text, True, (255, 255, 255))
    
    stroke_color = (0, 0, 0)
    offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for offset in offsets:
        stroke_text = font.render(text, True, stroke_color)
        screen.blit(stroke_text, (50 + offset[0], 10 + offset[1]))
    
    screen.blit(main_text, (50, 10))



# Main loop
player = Player()
ground = Ground(0, 800, SCREEN_WIDTH, 100, ground_image, 28)

current_level_number = 1
current_level = Level(current_level_number, SCREEN_WIDTH, SCREEN_HEIGHT)

player_sprites = pygame.sprite.Group()
player_sprites.add(player)

gameIsRunning = True
clock = pygame.time.Clock()

while gameIsRunning:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameIsRunning = False

    # Updates
    handle_input(player)
    player_sprites.update()
    current_level.update()
    current_level.coins.update()

    # Gathering coins
    for coin in pygame.sprite.spritecollide(player, current_level.coins, False):
        coin_sound.play()

    collected_coins = pygame.sprite.spritecollide(player, current_level.coins, True)
    score += len(collected_coins)

   # Check if all coins are collected
    if len(current_level.coins) == 0:
        # Player must move to the right edge to proceed to the next level
        if player.rect.right >= SCREEN_WIDTH and current_level.level_number < 4:
            current_level_number += 1
            current_level = Level(current_level_number,
                                  SCREEN_WIDTH, SCREEN_HEIGHT)
            current_level.reset_player_position(player)

    # Reset level 4        
    if pygame.sprite.spritecollideany(player, current_level.enemy_group):
        current_level = Level(4, SCREEN_WIDTH, SCREEN_HEIGHT)
        player.rect.center = (100, SCREEN_HEIGHT - 150)  # Reset player position
        score = 15  # Subtract collected coins from score


    # Drawing
    current_level.draw(screen)
    screen.blit(player.image, player.rect)
    current_level.coins.draw(screen)
    current_level.platforms.draw(screen)
    display_score(screen, SCREEN_WIDTH, score)
    display_commands(screen)
    
    if current_level.winner and current_level.level_number == 4:
        font = pygame.font.Font(None, 72)
        winner_text = font.render("You Win!", True, (255, 255, 0))
        text_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(winner_text, text_rect)

    # Refresh screen
    pygame.display.flip()

    # Frame rate
    clock.tick(120)

pygame.mixer.music.stop()
pygame.quit()
