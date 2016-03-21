"""
Implementation of 2048
"""

import user39_gJ6fzqUS7K_3 as merge
import random
import simplegui

SIDE_LEN = 5
BASE_NUM = 10

class Gameboard:
    def __init__(self):
        self._board = [[0 for dummy_num1 in range(SIDE_LEN)] for dummy_num in range(SIDE_LEN)]
        
    def merge_row(self, row_num, direction):
        """
        Merges a given row.
        If direction = False, then merged to left, otherwise merged to right.
        """

        if direction == True:
            return merge.merge(self._board[row_num][::-1])[::-1]
        elif direction == False:
            return merge.merge(self._board[row_num])
        else:
            print("Please enter True or False for direction")

    def merge_column(self, column_num, direction):
        """
        Merges a given column.
        If direction = False, then merged downwards, otherwise merged upwards.
        """
        column = []
        for row_num in range(len(self._board)):
            column.append(self._board[row_num][column_num])
        if direction == True:
            column = merge.merge(column)
        elif direction == False:
            column = merge.merge(column[::-1])[::-1]
        else:
            print("Please enter True or False for direction")
        for row_num in range(len(self._board)):
            return column
    
    def merge_right(self):
        """
        Merges all rows to the right
        """
        temp_board = []
        # Creation of temp_board is necessary, since if result of
        # move is the same as before the move, then the move doesn't 
        # count
        for row_num in range(len(self._board)):
            temp_board.append(self.merge_row(row_num, True))
        if temp_board != self._board:
            self._board = temp_board
            self.random_2()
    
    def merge_left(self):
        """
        Merges all rows to the left
        """
        temp_board = []
        for row_num in range(len(self._board)):
            temp_board.append(self.merge_row(row_num, False))
        if temp_board != self._board:
            self._board = temp_board
            self.random_2()
    
    def merge_up(self):
        """
        Merges all columns upwards
        """
        temp_board = [[] for dummy_num in range(len(self._board))]
        for column_num in range(len(self._board[0])):
            new_column = self.merge_column(column_num, True)
            for row_num in range(len(self._board)):
                temp_board[row_num].append(new_column[row_num])
        if temp_board != self._board:
            self._board = temp_board
            self.random_2()
    
    def merge_down(self):
        """
        Merges all columns downwards
        """
        temp_board = [[] for dummy_num in range(len(self._board))]
        for column_num in range(len(self._board[0])):
            new_column = self.merge_column(column_num, False)
            for row_num in range(len(self._board)):
                temp_board[row_num].append(new_column[row_num])
        if temp_board != self._board:
            self._board = temp_board
            self.random_2()
    
    def random_2(self):
        """
        Generates a '2' in a random position
        """

        # The first value in position is the x-pos and second is y-pos
        position = [random.randint(0, SIDE_LEN - 1), random.randint(0, SIDE_LEN - 1)]
        while self._board[position[1]][position[0]] != 0:
            position = [random.randint(0, SIDE_LEN - 1), random.randint(0, SIDE_LEN - 1)]
        self._board[position[1]][position[0]] = random.choice([BASE_NUM, BASE_NUM * 2])

    def __str__(self):
        """
        Pretty-prints the gameboard
        """
        string_repr = ""
        # All the complicated looking stuff just adds the row one by 
        # one to the string representation of the gameboard, with 
        # new-lines between rows. The end of the rows have been handled
        # separately to avoid putting the extra space
        for row in self._board:
            for number in row[:-1]:
                string_repr += str(number) + ' '
            string_repr += str(row[-1]) + '\n'
        return string_repr
    
    def draw_board(self, canvas):
        """
        Draws board on the canvas
        """
        for line_num in range(0, SIDE_LEN):
            canvas.draw_line((line_num * 100, 0), (line_num * 100, SIDE_LEN * 100), 5, '#FFFFFF')
            canvas.draw_line((0, line_num * 100), (SIDE_LEN * 100, line_num * 100), 5, '#FFFFFF')
        
        for row_num, row in enumerate(self._board):
            for column_num, number in enumerate(row):
                extra_box_width = 0
                extra_box_height = 0
                if column_num == SIDE_LEN - 1:
                    extra_box_width = 4
                if row_num == SIDE_LEN - 1:
                    extra_box_height = 4
                
                box_colour = '#E0FFD2'
                if number == BASE_NUM:
                    box_colour = '#90FB90'
                elif number == BASE_NUM * 2:
                    box_colour = '#00FF7F'
                elif number == BASE_NUM * 2 ** 2:
                    box_colour = '#00FA9A'
                elif number == BASE_NUM * 2 ** 3:
                    box_colour = '#00FFFF'
                elif number == BASE_NUM * 2 ** 4:
                    box_colour = '#40E0D0'
                elif number == BASE_NUM * 2 ** 5:
                    box_colour = '#00BFFF'
                elif number == BASE_NUM * 2 ** 6:
                    box_colour = '#1E90FF'
                elif number == BASE_NUM * 2 ** 7:
                    box_colour = '#7B68EE'
                elif number == BASE_NUM * 2 ** 8:
                    box_colour = '#9400D3'
                elif number == BASE_NUM * 2 ** 9:
                    box_colour = '#8B008B'
                elif number == 2048:
                    box_colour = '#4B0082'
                
                canvas.draw_polygon([(0 + column_num * 100, 0 + row_num * 100), 
                                     (97 + column_num * 100 + extra_box_width, 0 + row_num * 100), 
                                     (97 + column_num * 100 + extra_box_width, 97 + row_num * 100 + extra_box_height), 
                                     (0 + column_num * 100, 97 + row_num * 100 + extra_box_height)], 
                                    1, '#FFFFFF', box_colour)
                
                text_x_pos = 50 - frame.get_canvas_textwidth(str(number), 40) / 2
                canvas.draw_text(str(number), (text_x_pos + column_num * 100, 65 + row_num * 100), 40, 'Black')

def keydown_handler(key):
    if key == simplegui.KEY_MAP['right']: # merge to right
        gameboard.merge_right()
    elif key == simplegui.KEY_MAP['left']: # merge to left
        gameboard.merge_left()
    elif key == simplegui.KEY_MAP['up']: # merge upwards
        gameboard.merge_up()
    elif key == simplegui.KEY_MAP['down']: # merge downwards
        gameboard.merge_down()

def draw(canvas): 
    gameboard.draw_board(canvas)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", SIDE_LEN * 100, SIDE_LEN * 100)
frame.set_draw_handler(draw)
frame.set_canvas_background('White')
frame.set_keydown_handler(keydown_handler)

frame.start()
    
gameboard = Gameboard()
gameboard.random_2()
