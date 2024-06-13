import pygame as py
import sys
import random

py.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
SNAKE_SIZE = 20
INITIAL_SPEED = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

font = py.font.SysFont(None, 40)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = (0, 0)
        self.color = GREEN
        self.score = 0
        self.level = 1
        self.speed = INITIAL_SPEED

    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def change_direction(self, dir):
        if dir == py.K_UP and self.direction != (0, 1):
            self.direction = (0, -1)
        if dir == py.K_DOWN and self.direction != (0, -1):
            self.direction = (0, 1)
        if dir == py.K_LEFT and self.direction != (1, 0):
            self.direction = (-1, 0)
        if dir == py.K_RIGHT and self.direction != (-1, 0):
            self.direction = (1, 0)

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([py.K_UP, py.K_DOWN, py.K_LEFT, py.K_RIGHT])
        self.score = 0
        self.level = 1
        self.speed = INITIAL_SPEED

    def increase_length(self, weight):
        self.length += weight
        self.score += weight
        if self.score % 3 == 0:
            self.level += 1
            self.speed += 1

    def draw(self, surface):
        for p in self.positions:
            r = py.Rect((p[0], p[1]), (SNAKE_SIZE, SNAKE_SIZE))
            py.draw.rect(surface, self.color, r)
            py.draw.rect(surface, WHITE, r, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.colors = [RED, BLUE, GREEN]
        self.weights = [1, 2, 3]
        self.color = RED
        self.weight = 1
        self.randomize_position()

    def randomize_position(self):
        idx = random.randint(0, 2)
        self.color = self.colors[idx]
        self.weight = self.weights[idx]
        self.position = (random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                         random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)

    def draw(self, surface):
        r = py.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        py.draw.rect(surface, self.color, r)
        py.draw.rect(surface, WHITE, r, 1)

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption("Snake Game")

snake = Snake()
food = Food()

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        elif event.type == py.KEYDOWN:
            snake.change_direction(event.key)

    snake.move()

    if snake.positions[0] == food.position:
        snake.increase_length(food.weight)
        food.randomize_position()

    if snake.positions[0][0] < 0 or snake.positions[0][0] >= SCREEN_WIDTH or \
            snake.positions[0][1] < 0 or snake.positions[0][1] >= SCREEN_HEIGHT:
        snake.reset()

    screen.fill(BLACK)

    snake.draw(screen)
    food.draw(screen)

    score_text = font.render(f"Score: {snake.score}", True, WHITE)
    level_text = font.render(f"Level: {snake.level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    py.display.update()

    py.time.Clock().tick(snake.speed)
