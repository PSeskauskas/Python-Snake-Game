from tkinter import *
import random

FRAME_WIDTH = 1200
FRAME_HEIGHT = 600
GAME_SPEED = 100
SNAKE_SIZE = 25
SNAKE_PARTS = 3
FOOD_SIZE = 50
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self):
        self.body_size = SNAKE_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, SNAKE_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (FRAME_WIDTH / SNAKE_SIZE) - 1) * SNAKE_SIZE
        y = random.randint(0, (FRAME_HEIGHT / SNAKE_SIZE) - 1) * SNAKE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SNAKE_SIZE
    elif direction == "down":
        y += SNAKE_SIZE
    elif direction == "right":
        x += SNAKE_SIZE
    elif direction == "left":
        x -= SNAKE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=SNAKE_COLOR, tag="snake")

    snake.squares.insert(0, square)

    if check_collisions(snake):
        game_over()

    elif x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]


    window.after(GAME_SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= FRAME_WIDTH:
        return True
    elif y < 0 or y >= FRAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('Arial', 100), text="GAME OVER", fill="red", tag="GAME OVER")


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('Arial', 50))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=FRAME_HEIGHT, width=FRAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
