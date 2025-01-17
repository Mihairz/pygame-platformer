import pygame

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, ground_height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Create a separate smaller rect to represent the actual ground (ignoring grass)
        self.ground_rect = pygame.Rect(
            x, y + height - ground_height, width, ground_height)

