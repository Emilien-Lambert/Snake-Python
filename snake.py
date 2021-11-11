import pygame
import sys
import random

from pygame import surface


class Snake(object):
    def __init__(self):
        self.length = 1
        self.position = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (158, 145, 93)
        self.score = 0

    def get_head_position(self):
        return self.position[0]

    def turn(self, direction):
        if direction == LEFT:
            if self.direction != RIGHT:
                self.direction = LEFT
        elif direction == RIGHT:
            if self.direction != LEFT:
                self.direction = RIGHT
        elif direction == UP:
            if self.direction != DOWN:
                self.direction = UP
        elif direction == DOWN:
            if self.direction != UP:
                self.direction = DOWN

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRIDSIZE)) % SCREEN_WIDTH),
               (cur[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.position) > 2 and new in self.position[2:]:
            self.reset()
        else:
            self.position.insert(0, new)
            if len(self.position) > self.length:
                self.position.pop()

    def reset(self):
        self.length = 1
        self.position = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        for p in self.position:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (0, 0, 0), r, 3)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)


class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 0, 0)
        self.random_spawn()

    def random_spawn(self):
        self.position = (random.randint(0, (SCREEN_HEIGHT // GRIDSIZE) - 1) *
                         GRIDSIZE, random.randint(0, (SCREEN_HEIGHT // GRIDSIZE) - 1) * GRIDSIZE)

    def draw(self, surface):
        r = pygame.Rect(
            (self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (0, 0, 0), r, 3)


def draw_grid(surface):
    for y in range(0, GRID_HEIGHT):
        for x in range(0, GRID_WIDTH):
            if (x + y % 2) % 2 == 0:
                r = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE),
                                (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                rr = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE),
                                 (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (84, 194, 205), rr)


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRIDSIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRIDSIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)

    snake = Snake()
    food = Food()
    highestScore = 0

    while (True):
        clock.tick(10)
        snake.handle_keys()
        draw_grid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            food.random_spawn()
            snake.score += 1
        if snake.score > highestScore:
            highestScore = snake.score
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        textScore = ("Score: " + str(snake.score))
        textHighestScore = ("Highest Score: " + str(highestScore))
        randerScore = pygame.font.SysFont("monospace", 15).render(
            textScore, True, (0, 0, 0))
        randerHighestScore = pygame.font.SysFont(
            "monospace", 15).render(textHighestScore, True, (0, 0, 0))
        screen.blit(randerScore, (0, 0))
        screen.blit(randerHighestScore, (0, 20))
        pygame.display.update()


main()
