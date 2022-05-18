'''
Yuanzhe Li
CS 5001, Fall 2021

The main function for final project.
'''

import turtle
from drawBoard import (draw_circle, draw_square, NUM_SQUARES,
                       SQUARE, SQUARE_COLORS, CIRCLE_COLORS,
                       CORNER)
from boardDesign import GameState


def main():
    checkBoard = GameState()
    CIRCLE = 25

    board_size = NUM_SQUARES * SQUARE
    # Create the UI window. This should be the width of the board plus a
    # little margin
    window_size = board_size + SQUARE  # The extra + SQUARE is the margin
    turtle.setup(window_size, window_size)

    # Set the drawing canvas size. The should be actual board size
    turtle.screensize(board_size, board_size)
    turtle.bgcolor("white")  # The window's background color
    turtle.tracer(0, 0)  # makes the drawing appear immediately

    pen = turtle.Turtle()  # This variable does the drawing.
    pen.penup()  # This allows the pen to be moved.
    pen.hideturtle()  # This gets rid of the triangle cursor.

    # The first parameter is the outline color, the second is the filler
    pen.color("black", "white")

    # Step 1 - the board outline

    pen.setposition(CORNER, CORNER)
    draw_square(pen, board_size)

    # Step 2 & 3 - the checkerboard squares
    pen.color("black", SQUARE_COLORS[0])
    for col in range(NUM_SQUARES):
        for row in range(NUM_SQUARES):
            pen.setposition(CORNER + SQUARE * col, CORNER + SQUARE * row)
            if col % 2 != row % 2:
                draw_square(pen, SQUARE)

    # draw those circles
    pen.color("black", CIRCLE_COLORS[0])
    for col in range(NUM_SQUARES):
        for row in range(NUM_SQUARES):
            pen.setposition(CORNER + SQUARE * col + CIRCLE,
                            CORNER + SQUARE * row)
            if col % 2 != row % 2:
                if row == 3 or row == 4:
                    continue
                else:
                    if row < 3:
                        pen.color("black", CIRCLE_COLORS[0])
                    elif row > 4:
                        pen.color("red", CIRCLE_COLORS[1])
                    draw_circle(pen, CIRCLE)
    # Click handling
    screen = turtle.Screen()

    # This will call the click_handler function when a click occurs
    # screen.onclick(checkBoard.click_operation)
    screen.onclick(checkBoard.human_operation)
    turtle.done()  # Stops the window from closing.


if __name__ == "__main__":
    main()