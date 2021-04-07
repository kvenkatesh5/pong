import pygame
import constants


class Block(pygame.sprite.Sprite):
    def __init__(self, screen_size, init_pos, speed):
        super().__init__()
        self.screen_size = screen_size
        self.init_pos = init_pos
        self.width = self.init_pos[2]
        self.height = self.init_pos[3]
        self.speed = speed

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.BLACK)
        pygame.draw.rect(self.image, constants.WHITE, [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect[0] = self.init_pos[0]
        self.rect[1] = self.init_pos[1]
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, upwards: bool):
        if upwards:
            self.rect[1] -= self.speed
        else:
            self.rect[1] += self.speed
        self.check_edge()

    def check_edge(self):
        if self.rect[1] < 0:
            self.rect[1] = 0
        if self.rect[1] > self.screen_size[1] - self.height:
            self.rect[1] = self.screen_size[1] - self.height

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.image, self.rect)
