import pygame
from block import Block
from ball import Ball
import constants

# setup screen
pygame.init()
screen_size = [750, 750]
screen = pygame.display.set_mode(screen_size)
line_pos = [(screen_size[0]/2, 0), (screen_size[0]/2, screen_size[1])]

# setup blocks
block_width = 15
block_height = screen_size[0] / 5
block_speed = 10
h_gap = 35
left_rect_init = [h_gap, screen_size[1] / 2 - block_height / 2, block_width, block_height]
right_rect_init = [screen_size[0]-block_width-h_gap, screen_size[1] / 2 - block_height / 2, block_width, block_height]
left_block = Block(screen_size, left_rect_init, block_speed)
right_block = Block(screen_size, right_rect_init, block_speed)

# setup pong ball
ball_pos_init = [screen_size[0] / 2, screen_size[0] / 2]
# diameter should be able to fit inside the h_gap
ball_radius = 10
ball_speed_bounds = (10, 15)
ball = Ball(screen_size, ball_radius, speed_bounds=ball_speed_bounds)

# scoreboard
left_score = 0
right_score = 0
end_score = 20

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        right_block.move(upwards=True)
    if keys[pygame.K_DOWN]:
        right_block.move(upwards=False)
    if keys[pygame.K_w]:
        left_block.move(upwards=True)
    if keys[pygame.K_s]:
        left_block.move(upwards=False)

    delta_score = ball.move()
    ball.check_collide(left_block)
    ball.check_collide(right_block)
    if delta_score < 0:
        left_score += 1
    elif delta_score > 0:
        right_score += 1
    if left_score == end_score or right_score == end_score:
        running = False

    screen.fill(constants.BLACK)
    pygame.draw.line(screen, constants.WHITE, *line_pos)
    pygame.draw.rect(screen, constants.WHITE, left_block.rect)
    pygame.draw.rect(screen, constants.WHITE, right_block.rect)
    ball.draw(screen)
    pygame.display.update()
    clock.tick(50)

print(f"Score: {left_score} - {right_score}")
pygame.quit()
