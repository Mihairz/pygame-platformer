import pygame

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, ground_height, move_type=None, move_range=0, move_speed=0):
        super().__init__()

        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ground_rect = pygame.Rect(x, y + height - ground_height, width, ground_height)

        self.move_type = move_type  # None, "horizontal", or "vertical"
        self.move_range = move_range
        self.move_speed = move_speed
        self.start_pos = (x, y)
        self.direction = 1  # 1 for forward, -1 for backward

    def update(self):
        if self.move_type == "horizontal":
            self.rect.x += self.move_speed * self.direction
        if abs(self.rect.x - self.start_pos[0]) > self.move_range:
            self.direction *= -1
        elif self.move_type == "vertical":
            self.rect.y += self.move_speed * self.direction
        if abs(self.rect.y - self.start_pos[1]) > self.move_range:
            self.direction *= -1

        self.ground_rect.x = self.rect.x
        self.ground_rect.y = self.rect.y + self.rect.height - self.ground_rect.height

