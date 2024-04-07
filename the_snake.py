from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Основной класс игровых объектов."""

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self) -> None:
        """Объявление метода draw для родительского класса."""
        pass


class Snake(GameObject):
    """Класс для объектов змейка."""

    length = 1
    direction = RIGHT
    next_direction = None

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [self.position]
        self.body_color = (0, 255, 0)
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple_position):
        """Метод, отвечающий за изменение положения змейки на игровом поле."""
        head_position = self.get_head_position()

        new_position = self.get_new_position(head_position)

        if new_position in self.positions:
            self.reset()
        else:
            if self.length == 1:
                self.last = head_position
                if new_position == apple_position:
                    self.positions.insert(0, new_position)
                    self.length += 1
                else:
                    self.positions.insert(0, new_position)
                    self.last = self.positions.pop()
            if new_position == apple_position:
                self.positions.insert(0, new_position)
                self.length += 1
            else:
                self.positions.insert(0, new_position)
                self.positions.pop()

    def get_new_position(self, head_position):
        """Функция для получения новой позиции головы змейки."""
        if self.direction == UP:
            new_position = (head_position[0], head_position[1] - GRID_SIZE)
        elif self.direction == DOWN:
            new_position = (head_position[0], head_position[1] + GRID_SIZE)
        elif self.direction == RIGHT:
            new_position = (head_position[0] + GRID_SIZE, head_position[1])
        else:
            new_position = (head_position[0] - GRID_SIZE, head_position[1])

        if new_position[0] < 0:
            new_position = (620, new_position[1])
        elif new_position[0] > 639:
            new_position = (0, new_position[1])
        elif new_position[1] < 0:
            new_position = (new_position[0], 460)
        elif new_position[1] > 479:
            new_position = (new_position[0], 0)

        return new_position

    def draw(self):
        """Метод draw класса Snake."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Функция для получения положения головы змейки."""
        return self.positions[0]

    def reset(self):
        """Функция для выполнения перезапуска игры."""
        self.positions = [self.position]
        self.length = 1
        self.direction = choice([UP, DOWN, RIGHT, LEFT])


class Apple(GameObject):
    """Класс для объектов яблоко."""

    def __init__(self):
        self.body_color = (255, 0, 0)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Функция для получения случайной координаты на игровом поле."""
        width = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        height = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (width, height)

    def draw(self):
        """Метод draw класса Apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция запускающая игру и определяющая ее логику."""
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple.position)

        if apple.position == snake.positions[0]:
            apple.position = apple.randomize_position()

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
