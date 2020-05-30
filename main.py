import pygame
import time
import random
from constants import *

pygame.init()
clock = pygame.time.Clock()

# setup window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Stupid Snake')
screen.fill(BACKGROUND_COLOR)

# setup scoreboard
pygame.font.init()
my_font = pygame.font.SysFont(pygame.font.get_default_font(), FONT_SIZE)
text_surface = my_font.render('Score: 0', True, TEXT_COLOR)
screen.blit(text_surface, (0, 0))

pygame.display.flip()

position_x, position_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
velocity_x, velocity_y = 0, 0
food_x, food_y = -1, -1
score = 0
snake_length = 1

# init snake
snake_cells = [(position_x, position_y)]

game_over = False


def check_position(x, y):
    return x >= 0 and y >= 0 and x < WINDOW_WIDTH and y < WINDOW_HEIGHT

def gen_food():
    food_x = random.randrange(0, WINDOW_WIDTH // PIXEL) * PIXEL
    food_y = random.randrange(0, WINDOW_HEIGHT // PIXEL) * PIXEL
    return (food_x, food_y)

def update_position():
    snake_cells.append((position_x, position_y))
    while (len(snake_cells) > snake_length):
        snake_cells.pop(0)

def check_bite():
    (x, y) = snake_cells[-1]
    for i in range(len(snake_cells) - 1):
        u, v = snake_cells[i]
        if x == u and y == v:
            return True
    return False


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if (velocity_x, velocity_y) != RIGHT:
                    velocity_x, velocity_y = LEFT
            elif event.key == pygame.K_RIGHT:
                if (velocity_x, velocity_y) != LEFT:
                    velocity_x, velocity_y = RIGHT
            elif event.key == pygame.K_UP:
                if (velocity_x, velocity_y) != DOWN:
                    velocity_x, velocity_y = UP
            elif event.key == pygame.K_DOWN:
                if (velocity_x, velocity_y) != UP:
                    velocity_x, velocity_y = DOWN

    # gen food
    if food_x == -1:
        food_x, food_y = gen_food()

    # eat food
    if position_x == food_x and position_y == food_y:
        snake_length += 1
        score += 1
        food_x, food_y = -1, -1

    # update position
    if velocity_x != 0 or velocity_y != 0:
        position_x += velocity_x
        position_y += velocity_y

        update_position()

        if not check_position(position_x, position_y):
            game_over = True
            hit_wall = my_font.render("Your stupid snake hits the wall!", True, END_GAME_COLOR)
            screen.blit(hit_wall, (WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3))
            pygame.display.update()
            time.sleep(2.0)
            continue

        if check_bite():
            game_over = True
            self_bite = my_font.render("Your stupid snake bites itself!", True, END_GAME_COLOR)
            screen.blit(self_bite, (WINDOW_WIDTH // 3.5, WINDOW_HEIGHT // 3))
            pygame.display.update()
            time.sleep(2.0)
            continue

    # refill screen
    screen.fill(BACKGROUND_COLOR)
    
    # score
    text_surface = my_font.render('Score: ' + str(score), True, TEXT_COLOR)
    screen.blit(text_surface, (0, 0))

    # draw food
    if food_x != -1 and food_y != -1:
        pygame.draw.rect(screen, FOOD_COLOR, (food_x, food_y, PIXEL, PIXEL))

    # draw the snake
    for (x, y) in snake_cells:
        pygame.draw.rect(screen, SNAKE_COLOR if (x, y) != (position_x, position_y) else SNAKE_HEAD_COLOR, (x, y, PIXEL, PIXEL))

    pygame.display.update()
    clock.tick(20)

pygame.quit()
