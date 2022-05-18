'''
Yuanzhe Li
CS 5001, Fall 2021

The work for designing functions of the game.
'''

# pseudocode
# 1.Draw the board
# 2.Design the class of game board and let functions of
# a piece be included in this class
# 3.Redraw the entire board after each move
# 4.Let a piece become a king when it reaches the end of the board
# 5. Design the functions of a king
# 5. Design the computer player
# 6. The game ends when a player has no pieces left or cannot move

import random
import turtle
from drawBoard import (BOARD_SIZE, CORNER, SQUARE_COLORS, CIRCLE_COLORS,
                       SQUARE, NUM_SQUARES, draw_circle, draw_square,
                       click_handler, draw_king, position_calc,
                       draw_square_border)

rows = [0, 1, 2, 3, 4, 5, 6, 7]
cols = [0, 1, 2, 3, 4, 5, 6, 7]


class GameState:
    '''
        Class - GameState:
            Represent the status of the game board
        Attributes:
            BLACK: Represent black common piece
            RED: Represent red common piece
            BLACK_KING: Represent black king piece
            RED_KING: Represent red king
            PlayerB: Represent player who controls black piece
            PlayerR: Represent player who controls red piece
            supplement_coordinate: It's used to calculate the row and
                            col
            red_remain: the current number of red pieces
            black_remain: the current number of black pieces
            game_over: It's a variable used to decide whether the game is over
                        current_player: current player
            penPiece: The pen used to draw the piece
            prev = []: A list which is used to store the row and col of the
                        first clicked piece
            move_status: current status of a piece
            capture_move: The current piece can make a capture move
            not_capture_move: The current piece can only make a
                                non-capture move
            can_capture_list_black: A list containing all black pieces
                                    which can make a capture move
            can_capture_list_red: A list containing all red pieces
                                which can make a capture move
            cannot_capture_list_black: A list containing all black pieces
                                        which can make a non-capture move
            cannot_capture_list_red: A list containing all red pieces
                                    which can make a non-capture move
        Methods:
            __init__: initialize the game board
            invalid_click: decide whether the click is valid or not
            invalid_position: decide whether the clicked position is valid
            invalid_non_capture: decide whether the non-capture move is valid
            invalid_capture: decide whether the capture move is valid or not
            invalid_player: decide whether the current player is correct or not
            reset_board: redraw the board based on the self.squares
            is_capture: check whether the selected piece can make a capture
            select_not_capture_move: draw the select box for a piece which is
                                    going to make a non-capture move
            select_capture_move: draw the select box for a piece which is
                                    going to make a capture move
            indicate_winner: show the winner of the game
            first_click: select the piece which is going to move
            second_click: select a empty position for a moving piece
            computer_operation: controls the opeation of computer
            human_operation: controls the operation of human
            get_capture_piece: get all peices which can make a capture move
                                for computer
            get_non_capture_piece: get all pieces which can make a non-capture
                                    move for computer
            empty_position: get all empty positions for a piece which is
                                going to make a non-capture move
            empty_position_capture: get all empty positions for a piece which
                                    is going to make a capture move
            winGame: decide whether the game is over
            can_piece_move: decide whether a piece can make a move
            can_non_capture_move: decide whether a piece can make a non-capture
                                    move
            can_capture_move: decide whether a piece can make a capture move
            is_black: decide whether the piece is black
            is_red: decide whether the piece is red
            check_capture: Collect all pieces which can make a caoture move
    '''
    BLACK = 'black'
    RED = 'red'
    EMPTY = 'empty'
    PlayerB = 'black'
    PlayerR = 'red'
    BLACK_KING = 'black_king'
    RED_KING = 'red_king'
    supplement_coordinate = 4
    red_remain = 12
    black_remain = 12
    game_over = False
    # Black first
    current_player = BLACK
    penPiece = turtle.Turtle
    prev = []
    move_status = None
    capture_move = 'capture'
    not_capture_move = 'not capture'
    can_capture_list_black = []
    can_capture_list_red = []
    cannot_capture_list_black = []
    cannot_capture_list_red = []

    def __init__(self):
        # 初始化棋盘状态
        self.squares = []

        for row in range(NUM_SQUARES + 1):
            if row == rows[0] or row == rows[2]:
                rowState = [self.EMPTY, self.BLACK, self.EMPTY, self.BLACK,
                            self.EMPTY, self.BLACK, self.EMPTY, self.BLACK]
            elif row == rows[1]:
                rowState = [self.BLACK, self.EMPTY, self.BLACK, self.EMPTY,
                            self.BLACK, self.EMPTY, self.BLACK, self.EMPTY]
            elif row == rows[5] or row == rows[7]:
                rowState = [self.RED, self.EMPTY, self.RED, self.EMPTY,
                            self.RED, self.EMPTY, self.RED, self.EMPTY]
            elif row == rows[6]:
                rowState = [self.EMPTY, self.RED, self.EMPTY, self.RED,
                            self.EMPTY, self.RED, self.EMPTY, self.RED]
            else:
                rowState = [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY,
                            self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY]
            self.squares.append(rowState)

    def invalid_click(self, x, y):
        '''
        Function - invalid_click
            Check if selected position is outside the boundary
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        Return:
            True if the click is invalid and False if otherwise
        '''
        if abs(x) > BOARD_SIZE or abs(y) > BOARD_SIZE:
            return True
        return False

    def invalid_position(self, x, y):
        '''
        Function - invalid_position
            Check if  position selected in the second click allows the move
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        Return:
            True if the click is invalid and False if otherwise
        '''
        row = (int)(y // SQUARE + self.supplement_coordinate)
        col = (int)(x // SQUARE + self.supplement_coordinate)
        if row == self.prev[0] and col == self.prev[1]:
            return False

        if self.invalid_click(x, y):
            return True
        if self.squares[row][col] != self.EMPTY:
            # 非空状态下如果是自己方棋子才无效
            if self.current_player == self.PlayerB:
                if self.is_black(row, col):
                    return True
            elif self.current_player == self.PlayerR:
                if self.is_red(row, col):
                    return True
        return False

    def invalid_non_capture(self, x, y):
        '''
        Function - invalid_position
            Check if  position selected in the second click allows the move
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        Return:
            True if the click is invalid and False if otherwise
        '''
        row = (int)(y // SQUARE + self.supplement_coordinate)
        col = (int)(x // SQUARE + self.supplement_coordinate)
        if row == self.prev[0] and col == self.prev[1]:
            return False

        if self.invalid_click(x, y):
            return True
        if self.squares[row][col] != self.EMPTY:
            return True

        # non-capture状态下只能移动到左右一格
        preRow = self.prev[0]
        preCol = self.prev[1]
        if (self.squares[preRow][preCol] != self.BLACK_KING and
           self.squares[preRow][preCol] != self.RED_KING):
            if self.current_player == self.PlayerB:
                if (row != preRow + 1 or (col != preCol + 1 and
                   col != preCol - 1)):
                    return True
            elif self.current_player == self.PlayerR:
                if(row != preRow - 1 or (col != preCol + 1 and
                   col != preCol - 1)):
                    return True
        else:
            if((row != preRow + 1 and row != preRow - 1) or
               (col != preCol + 1 and col != preCol - 1)):
                return True

        return False

    def invalid_capture(self, x, y):
        '''
        Function - invalid_capture
            Check if selected piece could be captured
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        Return:
            True if the capture is invalid
        '''
        row = (int)(y // SQUARE + self.supplement_coordinate)
        col = (int)(x // SQUARE + self.supplement_coordinate)
        if row == self.prev[0] and col == self.prev[1]:
            return False
        if self.invalid_click(x, y) or (self.squares[row][col] != self.EMPTY):
            return True
        # The move is valid in the following cases
        prevRow = self.prev[0]
        prevCol = self.prev[1]
        # valid capture for common piece
        if (self.squares[prevRow][prevCol] != self.BLACK_KING and
           self.squares[prevRow][prevCol] != self.RED_KING):
            if self.current_player == self.PlayerB:
                if ((col == prevCol - 2 and row == prevRow + 2) and
                   (self.is_red(row - 1, col + 1))):
                    return False
                elif ((col == prevCol + 2 and row == prevRow + 2) and
                      (self.is_red(row - 1, col - 1))):
                    return False
            elif self.current_player == self.PlayerR:
                if ((col == prevCol - 2 and row == prevRow - 2) and
                   (self.is_black(row + 1, col + 1))):
                    return False
                elif ((col == prevCol + 2 and row == prevRow - 2) and
                      (self.is_black(row + 1, col - 1))):
                    return False
        else:
            # valid capture for King piece
            if self.current_player == self.PlayerB:
                if ((col == prevCol - 2 and row == prevRow + 2) and
                   (self.is_red(row - 1, col + 1))):
                    return False
                elif ((col == prevCol + 2 and row == prevRow + 2) and
                      (self.is_red(row - 1, col - 1))):
                    return False
                elif ((col == prevCol - 2 and row == prevRow - 2) and
                      (self.is_red(row + 1, col + 1))):
                    return False
                elif ((col == prevCol + 2 and row == prevRow - 2) and
                      (self.is_red(row + 1, col - 1))):
                    return False
            elif self.current_player == self.PlayerR:
                if ((col == prevCol - 2 and row == prevRow + 2) and
                   (self.is_black(row - 1, col + 1))):
                    return False

                elif ((col == prevCol + 2 and row == prevRow + 2) and
                      (self.is_black(row - 1, col - 1))):
                    return False
                elif ((col == prevCol - 2 and row == prevRow - 2) and
                      (self.is_black(row + 1, col - 1))):
                    return False
                elif ((col == prevCol + 2 and row == prevRow - 2) and
                      (self.is_black(row + 1, col - 1))):
                    return False

        return True

    def invalid_player(self, x, y):
        '''
        Function - invalid_player
            Check if current player is the correct player
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        Return:
            True if the player is incorrect
        '''
        # Validate whether it's the right turn
        if self.invalid_click(x, y):
            return True
        row = (int)(y // SQUARE + self.supplement_coordinate)
        col = (int)(x // SQUARE + self.supplement_coordinate)
        if self.current_player == self.PlayerB:
            if not self.is_black(row, col):
                return True
        elif self.current_player == self.PlayerR:
            if not self.is_red(row, col):
                return True
        return False

    def reset_board(self):
        '''
        Function - reset_board
            Redraw the board based on the board status
        '''
        squares = self.squares
        turtle.tracer(0, 0)
        turtle.penup()
        # draw squares on the board
        for col in range(NUM_SQUARES):
            for row in range(NUM_SQUARES):
                if col % 2 != row % 2:
                    turtle.setposition(CORNER + SQUARE * col,
                                       CORNER + SQUARE * row)
                    turtle.color("black", SQUARE_COLORS[0])
                    turtle.begin_fill()
                    draw_square(turtle, SQUARE)
                    turtle.end_fill()
        radius = SQUARE / 2
        # draw pieces based on the state of the squares
        for col in range(NUM_SQUARES):
            for row in range(NUM_SQUARES):
                if squares[row][col] == self.BLACK_KING:
                    turtle.setposition(CORNER + SQUARE / 2 + SQUARE * col,
                                       CORNER + SQUARE * row)
                    turtle.color(CIRCLE_COLORS[0], CIRCLE_COLORS[0])
                    draw_circle(turtle, radius)
                    turtle.color('white')
                    turtle.setposition(CORNER + SQUARE / 2 + SQUARE * col,
                                       CORNER + SQUARE * row + SQUARE / 4)
                    draw_king(turtle, radius / 2)

                if squares[row][col] == self.BLACK:
                    turtle.setposition(CORNER + SQUARE / 2 + SQUARE * col,
                                       CORNER + SQUARE * row)
                    turtle.color(CIRCLE_COLORS[0], CIRCLE_COLORS[0])
                    draw_circle(turtle, radius)

                if squares[row][col] == self.RED_KING:
                    turtle.setposition(CORNER + SQUARE / 2 + SQUARE * col,
                                       CORNER + SQUARE * row)
                    turtle.color(CIRCLE_COLORS[1], CIRCLE_COLORS[1])
                    draw_circle(turtle, radius)
                    turtle.color('white')
                    turtle.setposition(CORNER + SQUARE / 2 + SQUARE * col,
                                       CORNER + SQUARE * row + SQUARE / 4)
                    draw_king(turtle, radius / 2)

                if squares[row][col] == self.RED:
                    turtle.setposition(CORNER + SQUARE / 2 + SQUARE * col,
                                       CORNER + SQUARE * row)
                    turtle.color(CIRCLE_COLORS[1], CIRCLE_COLORS[1])
                    draw_circle(turtle, radius)

    def is_capture(self, x, y):
        '''
        Function - is_capture
            Check if selected piece could capture any piece
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        Return:
            True if there is a piece could be captured by the current piece
        '''
        row = (int)(y // SQUARE + self.supplement_coordinate)
        col = (int)(x // SQUARE + self.supplement_coordinate)
        if self.current_player == self.PlayerB:
            if self.squares[row][col] != self.BLACK_KING:
                if (row <= rows[5] and col >= cols[2] and
                   (self.is_red(row + 1, col - 1)) and
                   self.squares[row + 2][col - 2] == self.EMPTY):
                    return True
                elif (row <= rows[5] and col <= cols[5] and
                      (self.is_red(row + 1, col + 1)) and
                      self.squares[row + 2][col + 2] == self.EMPTY):
                    return True
            else:
                if (row <= rows[5] and col >= cols[2] and
                   (self.is_red(row + 1, col - 1)) and
                   self.squares[row + 2][col - 2] == self.EMPTY):
                    return True
                elif (row <= rows[5] and col <= cols[2] and
                      (self.is_red(row + 1, col + 1)) and
                      self.squares[row + 2][col + 2] == self.EMPTY):
                    return True
                elif (row >= rows[2] and col <= cols[5] and
                      (self.is_red(row - 1, col + 1)) and
                      self.squares[row - 2][col + 2] == self.EMPTY):
                    return True
                elif (row >= rows[2] and col >= cols[2] and
                      (self.is_red(row - 1, col - 1)) and
                      self.squares[row - 2][col - 2] == self.EMPTY):
                    return True

        elif self.current_player == self.PlayerR:
            if self.squares[row][col] != self.RED_KING:
                if (row >= rows[2] and col >= cols[2] and
                   (self.is_black(row - 1, col - 1)) and
                   self.squares[row - 2][col - 2] == self.EMPTY):
                    return True
                elif ((row >= rows[2] and col <= cols[5]) and
                      (self.is_black(row - 1, col + 1)) and
                      self.squares[row - 2][col + 2] == self.EMPTY):
                    return True
            else:
                if (row <= rows[5] and col >= cols[2] and
                   (self.is_black(row + 1, col - 1)) and
                   self.squares[row + 2][col - 2] == self.EMPTY):
                    return True
                elif (row <= rows[5] and col <= cols[5] and
                      (self.is_black(row + 1, col + 1)) and
                      self.squares[row + 2][col + 2] == self.EMPTY):
                    return True
                elif (row >= rows[2] and col <= cols[5] and
                      (self.is_black(row - 1, col + 1)) and
                      self.squares[row - 2][col + 2] == self.EMPTY):
                    return True
                elif (row >= rows[2] and col >= cols[2] and
                      (self.is_black(row - 1, col - 1)) and
                      self.squares[row - 2][col - 2] == self.EMPTY):
                    return True
        return False

    def select_not_capture_move(self, x, y):
        '''
        Function - select_not_capture_move
            draw the red and blue borders for a piece which is making a
            non-capture move
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        '''
        row = (int)(y // SQUARE + self.supplement_coordinate)
        col = (int)(x // SQUARE + self.supplement_coordinate)
        turtle.penup()
        turtle.setposition(position_calc(col), position_calc(row))
        turtle.pendown()
        turtle.color("green")
        draw_square_border(turtle, SQUARE)
        turtle.color("red")
        if self.squares[row][col] == self.BLACK:
            if col <= cols[6]:
                turtle.setposition(position_calc(col + 1),
                                   position_calc(row + 1))
                draw_square_border(turtle, SQUARE)
            if col >= cols[1]:
                turtle.setposition(position_calc(col - 1),
                                   position_calc(row + 1))
                draw_square_border(turtle, SQUARE)
            turtle.penup()
        elif self.squares[row][col] == self.BLACK_KING:
            if col <= cols[6] and row <= rows[6]:
                turtle.setposition(position_calc(col + 1),
                                   position_calc(row + 1))
                draw_square_border(turtle, SQUARE)
            if col >= cols[1] and row <= rows[6]:
                turtle.setposition(position_calc(col - 1),
                                   position_calc(row + 1))
                draw_square_border(turtle, SQUARE)
            if col <= cols[6] and row >= rows[1]:
                turtle.setposition(position_calc(col + 1),
                                   position_calc(row - 1))
                draw_square_border(turtle, SQUARE)
            if col >= cols[1] and row >= rows[1]:
                turtle.setposition(position_calc(col - 1),
                                   position_calc(row - 1))
                draw_square_border(turtle, SQUARE)
            turtle.penup()
        elif self.squares[row][col] == self.RED:
            if col <= cols[6]:
                turtle.setposition(position_calc(col + 1),
                                   position_calc(row - 1))
                draw_square_border(turtle, SQUARE)
            if col >= cols[1]:
                turtle.setposition(position_calc(col - 1),
                                   position_calc(row - 1))
                draw_square_border(turtle, SQUARE)
            turtle.penup()
        elif self.squares[row][col] == self.RED_KING:
            if col <= cols[6] and row <= rows[6]:
                turtle.setposition(position_calc(col + 1),
                                   position_calc(row + 1))
                draw_square_border(turtle, SQUARE)
            if col >= cols[1] and row <= rows[6]:
                turtle.setposition(position_calc(col - 1),
                                   position_calc(row + 1))
                draw_square_border(turtle, SQUARE)
            if col <= cols[6] and row >= rows[1]:
                turtle.setposition(position_calc(col + 1),
                                   position_calc(row - 1))
                draw_square_border(turtle, SQUARE)
            if col >= cols[1] and row >= rows[1]:
                turtle.setposition(position_calc(col - 1),
                                   position_calc(row - 1))
                draw_square_border(turtle, SQUARE)

    def indicate_winner(self, player):
        '''
        Function - indicate_winner
            show the result of this game
        Parameters:
            player: the winner
        '''
        turtle.penup()
        turtle.setposition(0, -50)
        turtle.pendown()
        turtle.color("dark green")
        if player == self.PlayerB:
            turtle.write("Black Win", align="center",
                         font=("Verdana", 40, "normal"))
        elif player == self.PlayerR:
            turtle.write("Red Win", align="center",
                         font=("Verdana", 40, "normal"))
        turtle.penup()

    def select_capture_move(self, x, y):
        '''
        Function - select_capture_move
            draw the red and blue borders for a piece which is making a
            capture move
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        '''
        row = (int)(y // SQUARE + self.supplement_coordinate)
        col = (int)(x // SQUARE + self.supplement_coordinate)
        turtle.penup()
        turtle.setposition(position_calc(col), position_calc(row))
        turtle.pendown()
        turtle.color("green")
        draw_square_border(turtle, SQUARE)
        turtle.color("red")
        if self.is_black(row, col):
            if self.squares[row][col] == self.BLACK:
                if ((row <= rows[5] and col >= cols[2]) and
                    (self.is_red(row + 1, col - 1)) and
                   (self.squares[row + 2][col - 2] == self.EMPTY)):
                    turtle.setposition(position_calc(col - 2),
                                       position_calc(row + 2))
                    draw_square_border(turtle, SQUARE)
                elif (row <= rows[5] and col <= cols[5] and
                      (self.is_red(row + 1, col + 1)) and
                      self.squares[row + 2][col + 2] == self.EMPTY):
                    turtle.setposition(position_calc(col + 2),
                                       position_calc(row + 2))
                    draw_square_border(turtle, SQUARE)
            else:
                if (row <= rows[5] and col >= cols[2] and
                   (self.is_red(row + 1, col - 1)) and
                   self.squares[row + 2][col - 2] == self.EMPTY):
                    turtle.setposition(position_calc(col - 2),
                                       position_calc(row + 2))
                    draw_square_border(turtle, SQUARE)
                elif (row <= rows[5] and col <= cols[5] and
                      (self.is_red(row + 1, col + 1)) and
                      self.squares[row + 2][col + 2] == self.EMPTY):
                    turtle.setposition(position_calc(col + 2),
                                       position_calc(row + 2))
                    draw_square_border(turtle, SQUARE)
                elif (row >= rows[2] and col <= cols[5] and
                      (self.is_red(row - 1, col + 1)) and
                      self.squares[row - 2][col + 2] == self.EMPTY):
                    turtle.setposition(position_calc(col + 2),
                                       position_calc(row - 2))
                    draw_square_border(turtle, SQUARE)
                elif (row >= rows[2] and col >= cols[2] and
                      (self.is_red(row - 1, col - 1)) and
                      self.squares[row - 2][col - 2] == self.EMPTY):
                    turtle.setposition(position_calc(col - 2),
                                       position_calc(row - 2))
                    draw_square_border(turtle, SQUARE)
        elif self.is_red(row, col):
            if self.squares[row][col] == self.RED:
                if (row >= rows[2] and col >= cols[2] and
                    (self.is_black(row - 1, col - 1)) and
                   self.squares[row - 2][col - 2] == self.EMPTY):
                    turtle.setposition(position_calc(col - 2),
                                       position_calc(row - 2))
                    draw_square_border(turtle, SQUARE)
                elif ((row >= rows[2] and col <= cols[5]) and
                      (self.is_black(row - 1, col + 1)) and
                      self.squares[row - 2][col + 2] == self.EMPTY):
                    turtle.setposition(position_calc(col + 2),
                                       position_calc(row - 2))
                    draw_square_border(turtle, SQUARE)
            else:
                if (row <= rows[5] and col >= cols[2] and
                    (self.is_black(row + 1, col - 1)) and
                   self.squares[row + 2][col - 2] == self.EMPTY):
                    turtle.setposition(position_calc(col - 2),
                                       position_calc(row + 2))
                    draw_square_border(turtle, SQUARE)
                elif (row <= rows[5] and col <= cols[5] and
                      (self.is_black(row + 1, col + 1)) and
                      self.squares[row + 2][col + 2] == self.EMPTY):
                    turtle.setposition(position_calc(col + 2),
                                       position_calc(row + 2))
                    draw_square_border(turtle, SQUARE)
                elif (row >= rows[2] and col <= cols[5] and
                      (self.is_black(row - 1, col + 1)) and
                      self.squares[row - 2][col + 2] == self.EMPTY):
                    turtle.setposition(position_calc(col + 2),
                                       position_calc(row - 2))
                    draw_square_border(turtle, SQUARE)
                elif (row >= rows[2] and col >= cols[2] and
                      (self.is_black(row - 1, col - 1)) and
                      self.squares[row - 2][col - 2] == self.EMPTY):
                    turtle.setposition(position_calc(col - 2),
                                       position_calc(row - 2))
                    draw_square_border(turtle, SQUARE)

    def first_click(self, x, y):
        '''
        Function - first_click
            It's used to select a moveable piece
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        '''
        if self.game_over:
            return
        if self.current_player == self.PlayerB:
            capture_piece_list = self.check_capture(self.PlayerB)
        elif self.current_player == self.PlayerR:
            capture_piece_list = self.check_capture(self.PlayerR)
        row = (int)(y // SQUARE + self.supplement_coordinate)
        col = (int)(x // SQUARE + self.supplement_coordinate)
        cur = (str(row) + "," + str(col))
        if len(capture_piece_list) > 0 and cur not in capture_piece_list:
            return

        if len(self.prev) == 0 and not self.invalid_player(x, y):
            # draw the border of the selected piece
            if not self.is_capture(x, y):
                self.move_status = self.not_capture_move
                if self.current_player == self.PlayerB:
                    self.select_not_capture_move(x, y)
                elif self.current_player == self.PlayerR:
                    self.select_not_capture_move(x, y)
            elif self.is_capture(x, y):
                self.move_status = self.capture_move
                self.select_capture_move(x, y)
            self.prev.append(row)
            self.prev.append(col)
            print("The piece you selected is in ({},{})".format(row, col))
            Turn = self.current_player
            print("It's the turn of {}".format(Turn))

    def second_click(self, x, y):
        '''
        Function - second_click
            It's used to select a suitable position for the move
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        '''
        if self.game_over:
            return
        row = (int)(y // SQUARE + self.supplement_coordinate)
        col = (int)(x // SQUARE + self.supplement_coordinate)
        # The following state means that it is the second click
        if len(self.prev) > 0:
            # Validate the second postion clicked
            if self.invalid_position(x, y):
                print("Invalid Selection")
            # cancel the selection
            elif row == self.prev[0] and col == self.prev[1]:
                self.prev.pop()
                self.prev.pop()
                self.reset_board()
            # make capture or not_capture move
            else:
                if self.move_status == self.not_capture_move:
                    if self.invalid_non_capture(x, y):
                        print("You can not move to this position,"
                              "invalid non_capture move")
                    else:
                        # Reset the board, not capture
                        preRow = self.prev[0]
                        preCol = self.prev[1]
                        if self.current_player == self.PlayerB:
                            # Change the player after moving
                            self.current_player = self.PlayerR
                            if(self.squares[preRow][preCol] == self.BLACK_KING
                               or row == 7):
                                self.squares[row][col] = self.BLACK_KING
                            else:
                                self.squares[row][col] = self.BLACK 
                        elif self.current_player == self.PlayerR:
                            # Change the player after moving
                            self.current_player = self.PlayerB
                            if (self.squares[preRow][preCol] == self.RED_KING
                               or row == 0):
                                self.squares[row][col] = self.RED_KING
                            else:
                                self.squares[row][col] = self.RED   
                        self.squares[self.prev[0]][self.prev[1]] = self.EMPTY
                        self.prev[0] = row
                        self.prev[1] = col
                        self.reset_board()
                        self.prev.pop()
                        self.prev.pop()
                elif self.move_status == self.capture_move:
                    if self.invalid_capture(x, y):
                        print("You can not move to this position,"
                              "invalid capture move")
                    else:
                        preRow = self.prev[0]
                        preCol = self.prev[1]
                        if self.current_player == self.PlayerB:
                            if (self.squares[preRow][preCol] == self.BLACK_KING
                               or row == 7):
                                self.squares[row][col] = self.BLACK_KING
                            else:
                                self.squares[row][col] = self.BLACK
                            # If is_capture is still true after capturing a
                            # piece, then keep capturing until the status
                            # changed
                            if not self.is_capture(x, y):
                                self.current_player = self.PlayerR
                                self.prev.pop()
                                self.prev.pop()
                            else:
                                self.prev[0] = row
                                self.prev[1] = col
                            # red_remain - 1 after a capture by black
                            self.red_remain -= 1
                        elif self.current_player == self.PlayerR:
                            if(self.squares[preRow][preCol] == self.RED_KING
                               or row == 0):
                                self.squares[row][col] = self.RED_KING
                            else:
                                self.squares[row][col] = self.RED

                            if not self.is_capture(x, y):
                                self.current_player = self.PlayerB
                                self.prev.pop()
                                self.prev.pop()
                            else:
                                self.prev[0] = row
                                self.prev[1] = col
                            self.black_remain -= 1
                        self.squares[preRow][preCol] = self.EMPTY
                        enemyRow = (int)((row + preRow) / 2)
                        enemyCol = (int)((col + preCol) / 2)
                        self.squares[enemyRow][enemyCol] = self.EMPTY
                        self.reset_board()
                if self.winGame():
                    self.game_over = True

    def computer_operation(self, x, y):
        '''
        Function - computer_operation
            It's a function to control computer's operation
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        '''
        if len(self.prev) == 0:
            red_piece_can_capture_move = self.get_capture_piece()
            red_piece_non_capture_move = self.get_non_capture_piece()
            if len(red_piece_can_capture_move) > 0:
                piece = random.choice(red_piece_can_capture_move)
            elif len(red_piece_non_capture_move) > 0:
                piece = random.choice(red_piece_non_capture_move)
            newRow = piece[0]
            newCol = piece[1]
            newX = CORNER + newCol * SQUARE + SQUARE / 2
            newY = CORNER + newRow * SQUARE + SQUARE / 2
            self.first_click(newX, newY)

        if len(self.prev) > 0:
            prevRow = self.prev[0]
            prevCol = self.prev[1]

            if self.can_capture_move(prevRow, prevCol):
                positions = self.empty_position_capture(prevRow, prevCol)
            elif self.can_non_capture_move(prevRow, prevCol):
                positions = self.empty_position(prevRow, prevCol)
            position = positions[0]
            newRow = position[0]
            newCol = position[1]
            newX = CORNER + newCol * SQUARE + SQUARE / 2
            newY = CORNER + newRow * SQUARE + SQUARE / 2
            self.second_click(newX, newY)

    def human_operation(self, x, y):
        '''
        Function - human_operation
            It's a function to control human's operation
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        '''
        click_handler(x, y)
        if len(self.prev) == 0 and not self.invalid_player(x, y):
            self.first_click(x, y)
        elif len(self.prev) > 0:
            self.second_click(x, y)
            if self.current_player == self.PlayerR:
                self.computer_operation(x, y)

    def get_capture_piece(self):
        '''
        Function - get_capture_piece
            It's a function to get all pieces which can make a capture move
        '''
        list = []
        for row in range(len(rows)):
            for col in range(len(cols)):
                x = CORNER + SQUARE * col + SQUARE / 2
                y = CORNER + SQUARE * row + SQUARE / 2
                if ((self.squares[row][col] == self.RED or
                    self.squares[row][col] == self.RED_KING) and
                   self.is_capture(x, y)):
                    list.append([row, col])
        return list

    def get_non_capture_piece(self):
        '''
        Function - get_non_capture_piece
            It's a function to get all pieces which can non-capture move
        '''
        list = []
        for row in range(len(rows)):
            for col in range(len(cols)):
                x = CORNER + SQUARE * col + SQUARE / 2
                y = CORNER + SQUARE * row + SQUARE / 2
                if ((self.squares[row][col] == self.RED or
                    self.squares[row][col] == self.RED_KING) and
                   not self.is_capture(x, y) and
                   self.can_non_capture_move(row, col)):
                    list.append([row, col])
        return list

    def empty_position(self, row, col):
        '''
        Function - empty_position
            It's a function to get all empty positions for a piece which can
            make a non-capture move
        Parameters:
            row -- The row of the selected piece which is going to move
            col -- The col of the selected piece which is going to move
        '''
        list = []
        if self.squares[row][col] == self.RED:
            if (row >= rows[1] and col >= cols[1] and
               self.squares[row - 1][col - 1] == self.EMPTY):
                list.append([row - 1, col - 1])
            if (row >= rows[1] and col <= cols[6] and
               self.squares[row - 1][col + 1] == self.EMPTY):
                list.append([row - 1, col + 1])
        elif self.squares[row][col] == self.RED_KING:
            if (row >= rows[1] and col >= cols[1] and
               self.squares[row - 1][col - 1] == self.EMPTY):
                list.append([row - 1, col - 1])
            if (row >= rows[1] and col <= cols[6] and
               self.squares[row - 1][col + 1] == self.EMPTY):
                list.append([row - 1, col + 1])
            if (row <= rows[6] and col >= cols[1] and
               self.squares[row + 1][col - 1] == self.EMPTY):
                list.append([row + 1, col - 1])
            if (row <= rows[6] and col <= cols[6] and
               self.squares[row + 1][col + 1] == self.EMPTY):
                list.append([row + 1, col + 1])
        return list

    def empty_position_capture(self, row, col):
        '''
        Function - empty_position_capture
            It's a function to get all empty positions for a piece which can
            make a capture move
        Parameters:
            row -- The row of the selected piece which is going to move
            col -- The col of the selected piece which is going to move
        '''
        list = []
        if self.squares[row][col] == self.RED:
            if (row >= rows[2] and col >= cols[2] and
                (self.is_black(row - 1, col - 1)) and
               self.squares[row - 2][col - 2] == self.EMPTY):
                list.append([row - 2, col - 2])
            if (row >= rows[2] and col <= cols[5] and
                (self.is_black(row - 1, col + 1)) and
               self.squares[row - 2][col + 2] == self.EMPTY):
                list.append([row - 2, col + 2])
        elif self.squares[row][col] == self.RED_KING:
            if (row <= rows[5] and col >= cols[2] and
                (self.is_black(row + 1, col - 1)) and
               self.squares[row + 2][col - 2] == self.EMPTY):
                list.append([row + 2, col - 2])
            if (row <= rows[5] and col <= cols[5] and
                (self.is_black(row - 1, col + 1)) and
               self.squares[row + 2][col + 2] == self.EMPTY):
                list.append([row + 2, col + 2])
            if (row >= rows[2] and col <= cols[5] and
                (self.is_black(row - 1, col + 1)) and
               self.squares[row - 2][col + 2] == self.EMPTY):
                list.append([row - 2, col + 2])
            if (row >= rows[2] and col >= cols[2] and
                (self.is_black(row - 1, col + 1)) and
               self.squares[row - 2][col - 2] == self.EMPTY):
                list.append([row - 2, col - 2])
        return list

    def winGame(self):
        '''
        Function - winGame
            It's a function to indicate whether this game is over or not
        '''
        self.can_black_move = False
        self.can_red_move = False
        for row in range(len(rows)):
            for col in range(len(cols)):
                if (self.is_black(row, col) and self.can_piece_move(row, col)):
                    self.can_black_move = True
                if (self.is_red(row, col) and self.can_piece_move(row, col)):
                    self.can_red_move = True
        if self.black_remain == 0 or not self.can_black_move:
            self.indicate_winner(self.PlayerR)
            return True
        elif self.red_remain == 0 or not self.can_red_move:
            self.indicate_winner(self.PlayerB)
            return True
        return False

    def can_piece_move(self, row, col):
        '''
        Function - can_piece_move
            It's a function to decide whether a piece can make a move
        Parameters:
            row -- The row of the selected piece which is going to move
            col -- The col of the selected piece which is going to move
        Return:
            True if it can make a move
        '''
        if (self.can_non_capture_move(row, col) or
           self.can_capture_move(row, col)):
            return True
        return False

    def can_non_capture_move(self, row, col):
        '''
        Function - can_non_capture_move
            It's a function to decide whether a piece can make a non-capture
            move
        Parameters:
            row -- The row of the selected piece which is going to move
            col -- The col of the selected piece which is going to move
        Return:
            True if it can make a non-capture move
        '''
        if self.squares[row][col] == self.BLACK:
            if ((row <= rows[6] and col >= cols[1] and
                self.squares[row + 1][col - 1] == self.EMPTY) or
               (row <= rows[6] and col <= cols[6] and
               self.squares[row + 1][col + 1] == self.EMPTY)):
                return True
        elif self.squares[row][col] == self.BLACK_KING:
            if ((row <= rows[6] and col >= cols[1] and
                self.squares[row + 1][col - 1] == self.EMPTY) or
                (row <= rows[6] and col <= cols[6] and
                self.squares[row + 1][col + 1] == self.EMPTY) or
                (row >= rows[1] and col <= cols[6] and
                self.squares[row - 1][col + 1] == self.EMPTY) or
                (row >= rows[1] and col >= cols[1] and
                 self.squares[row - 1][col - 1] == self.EMPTY)):
                return True
        elif self.squares[row][col] == self.RED:
            if ((row >= rows[1] and col >= cols[1] and
                self.squares[row - 1][col - 1] == self.EMPTY) or
               (row >= rows[1] and col <= cols[6] and
               self.squares[row - 1][col + 1] == self.EMPTY)):
                return True
        elif self.squares[row][col] == self.RED_KING:
            if ((row <= rows[6] and col >= cols[1] and
                self.squares[row + 1][col - 1] == self.EMPTY) or
                (row <= rows[6] and col <= cols[6] and
                self.squares[row + 1][col + 1] == self.EMPTY) or
                (row >= rows[1] and col <= cols[6] and
                self.squares[row - 1][col + 1] == self.EMPTY) or
                (row >= rows[1] and col >= cols[1] and
                 self.squares[row - 1][col - 1] == self.EMPTY)):
                return True
        return False

    def can_capture_move(self, row, col):
        '''
        Function - can_capture_move
            It's a function to decide whether a piece can make a capture
            move
        Parameters:
            row -- The row of the selected piece which is going to move
            col -- The col of the selected piece which is going to move
        Return:
            True if it can make a capture move
        '''
        if self.squares[row][col] == self.BLACK:
            if (
                ((row <= rows[5] and col >= cols[2]) and
                 (self.is_red(row + 1, col - 1)) and
                 self.squares[row + 2][col - 2] == self.EMPTY) or
                ((row <= rows[5] and col <= 5) and
                 (self.is_red(row + 1, col + 1)) and
                 self.squares[row + 2][col + 2] == self.EMPTY)):
                return True
        elif self.squares[row][col] == self.BLACK_KING:
            if (((row <= rows[5] and col >= cols[2]) and
                 (self.is_red(row + 1, col - 1)) and
                 self.squares[row + 2][col - 2] == self.EMPTY) or

               ((row <= rows[5] and col <= cols[5]) and
                (self.is_red(row + 1, col + 1)) and
                self.squares[row + 2][col + 2] == self.EMPTY) or

               ((row >= rows[2] and col >= cols[2]) and
               (self.is_red(row - 1, col - 1)) and
               self.squares[row - 2][col - 2] == self.EMPTY) or

               ((row >= rows[2] and col <= cols[5]) and
               (self.is_red(row - 1, col + 1)) and
               self.squares[row - 2][col + 2] == self.EMPTY)):
                return True

        elif self.squares[row][col] == self.RED:
            if (
                ((row >= rows[2] and col >= cols[2]) and
                 (self.is_black(row - 1, col - 1)) and
                 self.squares[row - 2][col - 2] == self.EMPTY) or
                ((row >= rows[2] and col <= cols[5]) and
                 (self.is_black(row - 1, col + 1)) and
                 self.squares[row - 2][col + 2] == self.EMPTY)):
                return True

        elif self.squares[row][col] == self.RED_KING:
            if (((row <= rows[5] and col >= cols[2]) and
                 (self.is_black(row + 1, col - 1)) and
                 self.squares[row + 2][col - 2] == self.EMPTY) or

               ((row <= rows[5] and col <= cols[5]) and
                (self.is_black(row + 1, col + 1)) and
                self.squares[row + 2][col + 2] == self.EMPTY) or

               ((row >= rows[2] and col >= cols[2]) and
                (self.is_black(row - 1, col - 1)) and
                self.squares[row - 2][col - 2] == self.EMPTY) or

               ((row >= rows[2] and col <= cols[5]) and
                (self.is_black(row - 1, col + 1)) and
               self.squares[row - 2][col + 2] == self.EMPTY)):
                return True
        return False

    def is_black(self, row, col):
        '''
        Function - is_black
            It's a function to decide whether a piece is black or not
        Parameters:
            row -- The row of the selected piece
            col -- The col of the selected piece
        Return:
            True if it is a black piece
        '''
        if (self.squares[row][col] == self.BLACK or
           self.squares[row][col] == self.BLACK_KING):
            return True
        return False

    def is_red(self, row, col):
        '''
        Function - is_red
            It's a function to decide whether a piece is red or not
        Parameters:
            row -- The row of the selected piece
            col -- The col of the selected piece
        Return:
            True if it is a red piece
        '''
        if (self.squares[row][col] == self.RED or
           self.squares[row][col] == self.RED_KING):
            return True
        return False

    def check_capture(self, player):
        '''
        Function - check_capture
            It's a function to collect all pieces which can make a capture move
        Parameters:
            player: The current player
        Return:
            True if it is a red piece
        '''
        list = []
        if player == self.PlayerB:
            for row in range(len(rows)):
                for col in range(len(cols)):
                    if ((self.is_black(row, col)) and
                       self.can_capture_move(row, col)):
                        cur = str(row) + "," + str(col)
                        list.append(cur)
        elif player == self.PlayerR:
            for row in range(len(rows)):
                for col in range(len(cols)):
                    if ((self.is_red(row, col)) and
                       self.can_capture_move(row, col)):
                        cur = str(row) + "," + str(col)
                        list.append(cur)
        return list
