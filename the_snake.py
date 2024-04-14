from random import choice

import pygame as pg

pg.init()

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
    (pg.K_UP, UP): UP,
    (pg.K_UP, RIGHT): UP,
    (pg.K_UP, LEFT): UP,
    (pg.K_DOWN, DOWN): DOWN,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_LEFT, LEFT): LEFT,
    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_RIGHT, RIGHT): RIGHT,
    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT,
}

# Все ячейка поля:
ALL_CELLS = set(
    (x, y)
    for x in range(0, SCREEN_WIDTH, 20)
    for y in range(0, SCREEN_HEIGHT, 20)
)

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Стартовая позиция змейки:
SNAKE_START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


class GameObject:
    """Основной класс игровых объектов."""

    def __init__(self, body_color=None, position=SNAKE_START_POSITION):
        self.body_color = body_color
        self.position = position

    def randomize_position(self, snake_positions):
        """Функция для получения случайной координаты на игровом поле."""
        random_cell = choice(tuple(ALL_CELLS - set(snake_positions)))
        return random_cell

    def draw(self):
        """Метод draw родительского класса."""
        raise NotImplementedError(
            f'Определите метод draw() в {self.__class__.__name__}',
        )

    def paint_one_cell(self):
        """Метод закрашивания одной ячейки игрового поля."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для объектов змейка."""

    def __init__(self, body_color=(0, 255, 0), position=SNAKE_START_POSITION):
        self.position = position
        self.positions = [self.position]
        self.body_color = body_color
        self.next_direction = None
        self.direction = RIGHT

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """Метод, отвечающий за изменение положения змейки на игровом поле."""
        head_position = self.get_head_position()
        self.position = (
            head_position[0] + self.direction[0],
            head_position[1] + self.direction[1],
        )

        if self.position[0] < 0:
            self.position = (620, self.position[1])
        elif self.position[0] > 639:
            self.position = (0, self.position[1])
        elif self.position[1] < 0:
            self.position = (self.position[0], 460)
        elif self.position[1] > 479:
            self.position = (self.position[0], 0)

    def draw(self):
        """Метод draw дочернего класса."""
        self.paint_one_cell()

    def pain_over(self, last):
        """Затирание последнего сегмента"""
        if last:
            last_rect = pg.Rect(last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

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

    def draw(self):
        """Метод draw дочернего класса."""
        self.paint_one_cell()


class InedibleObject(GameObject):
    """Класс для несъедобных объектов."""

    def __init__(self, position=SNAKE_START_POSITION):
        self.body_color = INEDIBLE_OBJECT_COLOR
        self.position = self.randomize_position(position)

    def draw(self):
        """Метод draw дочернего класса."""
        self.paint_one_cell()


class Rock(GameObject):
    """Класс объекта камень."""

    def __init__(self, position=SNAKE_START_POSITION):
        self.body_color = ROCK_COLOR
        self.position = self.randomize_position(position)

    def draw(self):
        """Метод draw дочернего класса."""
        self.paint_one_cell()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
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

        pg.display.update()


if __name__ == '__main__':
    main()
