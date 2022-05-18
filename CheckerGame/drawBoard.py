'''
Sample Code
CS 5001, Fall 2021
This code will get you started with the final project.
'''
import turtle
CIRCLE = 25
NUM_SQUARES = 8  # The number of squares on each row.
SQUARE = 50  # The size of each square in the checkerboard.
BOARD_SIZE = NUM_SQUARES * SQUARE
CORNER = -BOARD_SIZE / 2
SQUARE_COLORS = ("light gray", "white")
CIRCLE_COLORS = ("black", "dark red")


def draw_square(a_turtle, size):
    '''
        Function -- draw_square
            Draw a square of a given size.
        Parameters:
            a_turtle -- an instance of Turtle
            size -- the length of each side of the square
        Returns:
            Nothing. Draws a square in the graphics window.
    '''
    RIGHT_ANGLE = 90
    a_turtle.begin_fill()
    a_turtle.pendown()
    for i in range(4):
        a_turtle.forward(size)
        a_turtle.left(RIGHT_ANGLE)
    a_turtle.end_fill()
    a_turtle.penup()


def draw_square_border(a_turtle, size):
    '''
        Function -- draw_square_border
            Draw a square of a given size.
        Parameters:
            a_turtle -- an instance of Turtle
            size -- the length of each side of the square
        Returns:
            Nothing. Draws a square in the graphics window.
    '''
    RIGHT_ANGLE = 90
    a_turtle.pendown()
    for i in range(4):
        a_turtle.forward(size)
        a_turtle.left(RIGHT_ANGLE)
    a_turtle.penup()


def draw_circle(a_turtle, size):
    '''
        Function -- draw_circle
            Draw a circle with a given radius.
        Parameters:
            a_turtle -- an instance of Turtle
            size -- the radius of the circle
        Returns:
            Nothing. Draws a circle in the graphics windo.
    '''
    a_turtle.begin_fill()
    a_turtle.pendown()
    a_turtle.circle(size)
    a_turtle.end_fill()
    a_turtle.penup()


def click_handler(x, y):
    '''
        Function -- click_handler
            Called when a click occurs.
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        Returns:
            Does not and should not return. Click handlers are a special type
            of function automatically called by Turtle. You will not have
            access to anything returned by this function.
    '''
    print("Clicked at ", x, y)
    borderline = []
    base = -200
    for i in range(9):
        borderline.append(base)
        base += 50

    if (x in borderline or y in borderline or x < borderline[0] or
       x > borderline[-1] or y < borderline[0] or y > borderline[-1]):
        print("This is not a valid click")
    else:
        print("This is a valid click")


def position_calc(position):
    '''
        Function -- position_calc
            calculate the index of a piece.
        Parameters:
            position: The row or col of a piece
        Returns:
            The x or y of a piece.
    '''
    return CORNER + SQUARE * position


def draw_king(a_turtle, size):
    '''
        Function -- draw_king
            Draw a white circle inside a piece.
        Parameters:
            a_turtle -- an instance of Turtle
            size -- the radius of the circle
        Returns:
            Nothing. Draws a circle in the graphics windo.
    '''
    a_turtle.pendown()
    a_turtle.circle(size)
    a_turtle.penup()