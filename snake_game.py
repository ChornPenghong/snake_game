import turtle
import random

# Constants
WIDTH = 500
HEIGHT = 500
DELAY = 100
GRID_SIZE = 20
FOOD_SIZE = 20

# Directions
OFFSETS = {
    "up": (0, GRID_SIZE),
    "down": (0, -GRID_SIZE),
    "left": (-GRID_SIZE, 0),
    "right": (GRID_SIZE, 0)
}

class SnakeGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(WIDTH, HEIGHT)
        self.screen.title("Improved Snake Game")
        self.screen.bgcolor("black")
        self.screen.tracer(0)

        self.pen = turtle.Turtle("square")
        self.pen.penup()
        self.pen.color("green")

        self.food = turtle.Turtle("circle")
        self.food.shapesize(FOOD_SIZE / 20)
        self.food.color("red")
        self.food.penup()

        self.screen.listen()
        self.screen.onkey(self.go_up, "Up")
        self.screen.onkey(self.go_down, "Down")
        self.screen.onkey(self.go_left, "Left")
        self.screen.onkey(self.go_right, "Right")

        self.reset()

    def reset(self):
        self.snake = [[0, 0], [0, GRID_SIZE], [0, GRID_SIZE * 2]]
        self.snake_dir = "up"
        self.last_dir = "up"
        self.food.goto(self.random_food_position())
        self.move()

    def move(self):
        head_x, head_y = self.snake[-1]
        offset_x, offset_y = OFFSETS[self.snake_dir]
        new_head = [head_x + offset_x, head_y + offset_y]

        # Wrap around screen edges
        new_head[0] %= WIDTH
        new_head[1] %= HEIGHT
        new_head[0] -= WIDTH // 2
        new_head[1] -= HEIGHT // 2

        # Collision with self
        if new_head in self.snake:
            self.show_game_over()
            return

        self.snake.append(new_head)

        if not self.check_food_collision(new_head):
            self.snake.pop(0)

        self.draw_snake()
        self.last_dir = self.snake_dir
        self.screen.update()
        turtle.ontimer(self.move, DELAY)

    def draw_snake(self):
        self.pen.clearstamps()
        for segment in self.snake:
            self.pen.goto(segment)
            self.pen.stamp()

    def check_food_collision(self, head):
        if self.distance(head, self.food.pos()) < GRID_SIZE:
            self.food.goto(self.random_food_position())
            return True
        return False

    def random_food_position(self):
        x = random.randint(-WIDTH // 2 + GRID_SIZE, WIDTH // 2 - GRID_SIZE)
        y = random.randint(-HEIGHT // 2 + GRID_SIZE, HEIGHT // 2 - GRID_SIZE)
        # Snap to grid
        x = GRID_SIZE * round(x / GRID_SIZE)
        y = GRID_SIZE * round(y / GRID_SIZE)
        return x, y

    def distance(self, pos1, pos2):
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

    def go_up(self):
        if self.last_dir != "down":
            self.snake_dir = "up"

    def go_down(self):
        if self.last_dir != "up":
            self.snake_dir = "down"

    def go_left(self):
        if self.last_dir != "right":
            self.snake_dir = "left"

    def go_right(self):
        if self.last_dir != "left":
            self.snake_dir = "right"

    def show_game_over(self):
        self.pen.goto(0, 0)
        self.pen.color("white")
        self.pen.write("Game Over", align="center", font=("Arial", 24, "bold"))
        self.screen.update()
        self.screen.ontimer(self.reset, 2000)

# Run the game
game = SnakeGame()
turtle.done()
