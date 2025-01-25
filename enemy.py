import pygame
from PIL import Image

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

enemy_frames = load_gif("assets/enemy-gif.gif")

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        
        self.standing_frames = enemy_frames
        self.frames = self.standing_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.animation_speed = 100  # Speed in ms
        self.last_update = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:  # Change frame every 100 ms
            # Loop through frames
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]  # Update image
            self.last_update = now

        # Remove enemy if it goes off-screen
        if self.rect.x < -self.rect.width:
            self.kill()
