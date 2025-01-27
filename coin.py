import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, frames, x, y):
        super().__init__()

        self.frames = [pygame.transform.scale(frame, (50, 50)) for frame in frames]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]

        self.animation_speed = 150  # Speed in ms
        self.last_update = pygame.time.get_ticks()

        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.last_update = now

def display_score(screen, SCREEN_WIDTH, score):
    font = pygame.font.Font(None, 36)
    text = f'Score: {score}'

    main_text = font.render(text, True, (255, 255, 255))
    
    stroke_color = (0, 0, 0)
    offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for offset in offsets:
        stroke_text = font.render(text, True, stroke_color)
        screen.blit(stroke_text, (SCREEN_WIDTH - 150 + offset[0], 10 + offset[1]))
    
    screen.blit(main_text, (SCREEN_WIDTH - 150, 10))

def display_winner(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    font = pygame.font.Font("assets/win-font.ttf", 72)
    text = font.render("WINNER", True, (255, 255, 255))

    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
