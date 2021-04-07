import math
import random
import pygame
import constants
from block import Block
import numpy as np


def vadd(x, y):
    return [x[0] + y[0], x[1] + y[1]]


def vsub(x, y):
    return [x[0] - y[0], x[1] - y[1]]


def vdot(x, y):
    return x[0] * y[0] + x[1] * y[1]


def vscale(x, k):
    return [k * e for e in x]


def project(x, y):
    x = np.array(x)
    y = np.array(y)
    # project x onto y
    return vscale(y, vdot(x, y) / vdot(y, y))


class Ball(pygame.sprite.Sprite):
    def __init__(self, screen_size, radius, speed_bounds=(5, 10)):
        super().__init__()
        self.screen_size = screen_size
        self.radius = radius
        self.speed_bounds = speed_bounds
        self.vel = [0, 0]

        self.image = pygame.Surface([2 * self.radius, 2 * self.radius])
        self.image.fill(constants.BLACK)
        pygame.draw.circle(self.image, constants.WHITE, [self.image.get_width() / 2, self.image.get_height() / 2],
                           self.radius)
        self.rect = self.image.get_rect()
        self.reset()
        # TODO: does this need to be updated?
        self.mask = pygame.mask.from_surface(self.image)

    def reset(self):
        def reset_speed():
            return random.uniform(self.speed_bounds[0], self.speed_bounds[1])

        def reset_angle():
            if random.random() > 0.5:
                return random.uniform(-math.pi / 4, math.pi / 4)
            else:
                return random.uniform(math.pi * 3 / 4, math.pi * 5 / 4)

        self.rect[0] = self.screen_size[0] / 2
        self.rect[1] = random.uniform(self.screen_size[1] / 4, self.screen_size[1] * 3 / 4)
        speed = reset_speed()
        theta = reset_angle()
        vx = speed * math.cos(theta)
        vy = speed * math.sin(theta)
        self.vel = [vx, vy]

    def move(self):
        self.rect[0] += self.vel[0]
        self.rect[1] += self.vel[1]
        self.check_horizontal_edge()
        delta_score = self.check_vertical_edge()
        return delta_score

    def check_horizontal_edge(self):
        # check if ball hit a screen horizontal edge
        top_most = self.rect[1] - self.radius
        bottom_most = self.rect[1] + self.radius
        if top_most <= 0:
            self.vel[1] *= -1
        if bottom_most >= self.screen_size[1]:
            self.vel[1] *= -1

    def check_vertical_edge(self):
        delta_score = 0
        # check if ball hit a vertical edge, indicating score
        left_most = self.rect[0] - self.radius
        right_most = self.rect[0] + self.radius
        if left_most <= 0:
            delta_score = -1
        if right_most >= self.screen_size[0]:
            delta_score = 1
        if delta_score != 0:
            # reset the ball
            self.reset()
        return delta_score

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def check_collide(self, block: Block):
        offset = list(map(int, vsub(block.rect, self.rect)))
        overlap = self.mask.overlap_area(block.mask, offset)
        if overlap == 0:
            return
        # collision normal
        nx = (self.mask.overlap_area(block.mask, (offset[0] + 1, offset[1])) -
              self.mask.overlap_area(block.mask, (offset[0] - 1, offset[1])))
        ny = (self.mask.overlap_area(block.mask, (offset[0], offset[1] + 1)) -
              self.mask.overlap_area(block.mask, (offset[0], offset[1] - 1)))
        if nx == 0 and ny == 0:
            return
        n = [nx, ny]
        v = self.vel
        v_prime = vsub(v, vscale(project(v, n), 2))
        self.vel = v_prime
        self.move()

