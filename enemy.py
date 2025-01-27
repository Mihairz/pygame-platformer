import pygame
from PIL import Image

# Function to load GIF and extract frames
def load_gif(filename, scale_size=None):
    gif = Image.open(filename)
    frames = []
    try:
        while True:
            frame_surface = pygame.image.fromstring(
                gif.tobytes(), gif.size, gif.mode
            )
            if scale_size:
                frame_surface = pygame.transform.scale(frame_surface, scale_size)
            frames.append(frame_surface)
            gif.seek(gif.tell() + 1)
    except EOFError:
        if frames:  # Ensure at least one frame was loaded
            frames.remove(frames[0])
        pass  # End of frames
    return frames

enemy_frames = load_gif("assets/enemy-gif2.gif", scale_size=(200, 200))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        
        self.enemy_frames = enemy_frames
        self.frames = self.enemy_frames
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
        if now - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update = now

        # Remove enemy if it goes off-screen
        if self.rect.x < -self.rect.width:
            self.kill()
