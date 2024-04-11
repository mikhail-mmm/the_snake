from random import choice, randint

import pygame

pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -20)
DOWN = (0, 20)
LEFT = (-20, 0)
RIGHT = (20, 0)

USER_ACTIONS = {
    (pygame.K_UP, UP): UP,
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_UP, LEFT): UP,
    (pygame.K_DOWN, DOWN): DOWN,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_LEFT, LEFT): LEFT,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, RIGHT): RIGHT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет несъедобного объекта:
INEDIBLE_OBJECT_COLOR = (150, 75, 0)

# Цвет камня:
ROCK_COLOR = (128, 128, 128)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Стартовая позиция змейки:
SNAKE_START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


class GameObject:
    """Основной класс игровых объектов."""

    def __init__(self, body_color=None, position=SNAKE_START_POSITION):
        self.body_color = body_color
        self.position = position

    def randomize_position(self, snake_positions):
        """Функция для получения случайной координаты на игровом поле."""
        while True:
            width = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            height = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            object_position = (width, height)
            if object_position not in snake_positions:
                break
        return object_position

    def draw(self):
        """Метод draw родительского класса."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для объектов змейка."""

    def __init__(self, body_color=(0, 255, 0), position=SNAKE_START_POSITION):
        self.position = position
        self.positions = [self.position]
        self.body_color = body_color
        self.next_direction = None
        self.direction = LEFT

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """Метод, отвечающий за изменение положения змейки на игровом поле."""
        head_position = self.get_head_position()
        self.position = self.get_new_position(head_position)

    def get_new_position(self, head_position):
        """Функция для получения новой позиции головы змейки."""
        new_position = (
            head_position[0] + self.direction[0],
            head_position[1] + self.direction[1],
        )

        if new_position[0] < 0:
            new_position = (620, new_position[1])
        elif new_position[0] > 639:
            new_position = (0, new_position[1])
        elif new_position[1] < 0:
            new_position = (new_position[0], 460)
        elif new_position[1] > 479:
            new_position = (new_position[0], 0)

        return new_position

    def pain_over(self, last):
        """Затирание последнего сегмента"""
        if last:
            last_rect = pygame.Rect(last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Функция для получения положения головы змейки."""
        return self.positions[0]

    def reset(self):
        """Функция для выполнения перезапуска игры."""
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        screen.fill(BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Класс для съедобных объектов яблоко."""

    def __init__(self, position=SNAKE_START_POSITION):
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position(position)


class InedibleObject(GameObject):
    """Класс для несъедобных объектов."""

    def __init__(self, position=SNAKE_START_POSITION):
        self.body_color = INEDIBLE_OBJECT_COLOR
        self.position = self.randomize_position(position)


class Rock(GameObject):
    """Класс объекта камень."""

    def __init__(self, position=SNAKE_START_POSITION):
        self.body_color = ROCK_COLOR
        self.position = self.randomize_position(position)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            try:
                game_object.next_direction = USER_ACTIONS[
                    (event.key, game_object.direction)
                ]
            except KeyError:
                game_object.next_direction = game_object.direction


def main():
    """Функция запускающая игру и определяющая ее логику."""
    snake = Snake()
    apple = Apple()
    rock = Rock()
    inedible = InedibleObject()
    speed = SPEED

    while True:
        clock.tick(speed)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if (snake.position in snake.positions
           or rock.position == snake.position):
            snake.reset()
            speed = 10
            rock.position = rock.randomize_position(SNAKE_START_POSITION)
            apple.position = apple.randomize_position(SNAKE_START_POSITION)
            inedible.position = inedible.randomize_position(
                SNAKE_START_POSITION,
            )

        if snake.position == apple.position:
            snake.positions.insert(0, snake.position)
            apple.position = apple.randomize_position(snake.positions)
            speed += 1
        elif snake.position == inedible.position:
            inedible.position = inedible.randomize_position(snake.positions)
            if len(snake.positions) != 1:
                snake.positions.insert(0, snake.position)
                snake.pain_over(snake.positions.pop())
                snake.pain_over(snake.positions.pop())
        else:
            snake.positions.insert(0, snake.position)
            snake.pain_over(snake.positions.pop())

        snake.draw()
        apple.draw()
        rock.draw()
        inedible.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
