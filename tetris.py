"""
Implementation of Tetris
"""

import simplegui
import random

# width and height in number of blocks
WIDTH = 10
HEIGHT = 20
BOX_SIZE = 30
ROTATE = ['Right', 'Down', 'Left', 'Up']
TIMER_CREATE = simplegui.create_timer

BLOCK_COLOURS = {'I': 'Aqua',
                 'J': 'Blue',
                 'L': 'Orange',
                 'O': 'Yellow',
                 'S': 'Green',
                 'Z': 'Red',
                 'T': 'Purple',
                 0: 'White'
                }

class Board:
    def __init__(self):
        self._fixed_layout = [[0 for column in range(WIDTH)] for row in range(HEIGHT)]
        self._layout = [lst[:] for lst in self._fixed_layout]
        self._temp_layout = [lst[:] for lst in self._fixed_layout]
        self._block = None
        self._tot_num_blocks = 0
        self._timer_interval = 750
        self._timers = []
        self._rows_deleted = 0
        
        self.add_block(random.choice(BLOCK_LIST)())
    
    def add_block(self, block):
        if self._tot_num_blocks % 20 == 0:
            for timer in self._timers:
                timer.stop()
            if self._timer_interval >= 400:
                self._timer_interval -= 50
            self._timers = [TIMER_CREATE(self._timer_interval, norm_timer_handler), TIMER_CREATE(self._timer_interval / 3, softdrop_timer_handler)]
            for timer in self._timers:
                timer.start()
        
        self._block = block
        self.populate_layout()
        self._tot_num_blocks += 1
    
    def populate_layout(self):
        """
        Adds blocks in self._blocks to the layout
        """      
        # A temporary layout variable is used since if the blocks overlap, then
        # the layout will not be updated
        
        # This method first builds layout and temp_layout to be equivalent to
        # the fixed layout, then adds the moving block to it
        
        self._layout = [lst[:] for lst in self._fixed_layout]
        self._temp_layout = [lst[:] for lst in self._fixed_layout]
        
        # This is for the moving block
        if self._block.populate_matrix(self._temp_layout):
            # Only if the moving block does not overlap is the board
            # populated with this
            self._layout = [lst[:] for lst in self._temp_layout]
            return True
        else:
            return False
              
    def get_current_block(self):
        """
        Returns currently moving block
        """
        return self._block
    
    def get_fixed_layout(self):
        """
        Returns the fixed layout
        """
        return self._fixed_layout
    
    def check_row_delete(self):
        num_rows_deleted = 0
        for row_num, row in enumerate([lst[:] for lst in self._fixed_layout][::-1]):
            if 0 not in row:
                self._fixed_layout.pop(HEIGHT - row_num - 1)
                num_rows_deleted += 1
                self._rows_deleted += 1
                label.set_text(str(self._rows_deleted))
        for dummy_var in range(num_rows_deleted):
            self._fixed_layout.insert(0, [0 for dummy_var in range(WIDTH)])
    
    def draw_board(self, canvas):
        """
        Draws board on the canvas
        """
        #for column_num in range(0, WIDTH):
        #    canvas.draw_line((column_num * BOX_SIZE, 0), (column_num * BOX_SIZE, HEIGHT * BOX_SIZE), 0.2, '#000000')
        #for row_num in range(0, HEIGHT):
        #    canvas.draw_line((0, row_num * BOX_SIZE), (WIDTH * BOX_SIZE, row_num * BOX_SIZE), 0.2, '#000000')
        
        for row_num, row in enumerate(self._layout):
            for column_num, block_name in enumerate(row):
                if block_name != 0:
                    square_colour = BLOCK_COLOURS[block_name]
                
                    canvas.draw_polygon([(0 + column_num * BOX_SIZE, 0 + row_num * BOX_SIZE),
                                        (BOX_SIZE + column_num * BOX_SIZE, 0 + row_num * BOX_SIZE), 
                                        (BOX_SIZE + column_num * BOX_SIZE, BOX_SIZE + row_num * BOX_SIZE), 
                                        (0 + column_num * BOX_SIZE, BOX_SIZE + row_num * BOX_SIZE)], 
                                        0.0001, '#FFFFFF', square_colour)

class Block:
    def __init__(self, block_pos):
        self._pos = block_pos
        self._orientation = 'Right'
        self._moving = True
        self._temp_pos = list(self._pos)
        self._temp_layout = []
        self._is_soft_dropping = False
    
    def rotate_clock(self):
        """
        Rotates block clockwise by 90 degrees
        """
        if self._moving:
            new_idx = ROTATE.index(self._orientation) + 1 if ROTATE.index(self._orientation) + 1 < len(ROTATE) else 0

            # Since the block may not be able to rotate, the orientation is stored in a temporary variable until
            # it is checked whether the block can rotate or not
            temp_orientation = ROTATE[new_idx]

            # The following method updates the blocks temp layout
            self.new_layout(temp_orientation)

            if gameboard.populate_layout():
                # IF the block can be rotated, then actual orientation and layout are updated
                self._orientation = temp_orientation
                self._layout = [lst[:] for lst in self._temp_layout]
    
    def rotate_anticlock(self):
        """
        Rotates block anticlockwise by 90 degrees
        """
        # See above method for explanation
        if self._moving:
            new_idx = ROTATE.index(self._orientation) - 1 # no need for boundary condition since index can be -1
            temp_orientation = ROTATE[new_idx]
            self.new_layout(temp_orientation)
            if gameboard.populate_layout():
                self._orientation = temp_orientation
                self._layout = [lst[:] for lst in self._temp_layout]
    
    def populate_matrix(self, matrix, is_fixed_layout = False):
        """
        Populates given matrix with constituent squares in temp_layout
        """
        # The is fixed layout variable controls whether the actual 
        # layout of the block is added to the matrix or the temp
        # layout. This is because if it is being added to the board's
        # fixed layout, then the actual block should be added
        if is_fixed_layout:
            layout_to_be_added = [lst[:] for lst in self._layout]
        else:
            layout_to_be_added = [lst[:] for lst in self._temp_layout]
        
        for square in layout_to_be_added:
            if square[1] < len(matrix):
                if square[0] < len(matrix[square[1]]):
                    if matrix[square[1]][square[0]] != 0:
                        # Catches case where blocks overlap
                        return False
                    else:
                        matrix[square[1]][square[0]] = self._name
                else:
                    return False
            else:
                return False
        return True # Returns True if block does not overlap
    
    def move_right(self):
        """
        Move block one square to the right
        """
        if self._layout[3][0] + 1 < WIDTH and self._moving:
            self._temp_pos[0] = self._pos[0] + 1
            self.new_layout(self._orientation)
            if gameboard.populate_layout():
                #Checks if any square is overlapping
                self._pos = list(self._temp_pos)
                self._layout = [lst[:] for lst in self._temp_layout]
    
    def move_left(self):
        """
        Move block one square to the left
        """
        if self._layout[0][0] - 1 > -1 and self._moving:
            self._temp_pos[0] = self._pos[0] - 1
            self.new_layout(self._orientation)
            if gameboard.populate_layout():
                #Checks if any square is overlapping
                self._pos = list(self._temp_pos)
                self._layout = [lst[:] for lst in self._temp_layout]
    
    def move_down(self):
        """
        Move block one square downwards
        """
        if (self._layout[0][1] + 1 < HEIGHT and 
            self._layout[1][1] + 1 < HEIGHT and
            self._layout[2][1] + 1 < HEIGHT and
            self._layout[3][1] + 1 < HEIGHT and
            self._moving
           ):
                self._temp_pos[1] = self._pos[1] + 1
                self.new_layout(self._orientation)
                if gameboard.populate_layout():
                    #Checks if any square is overlapping
                    self._pos = list(self._temp_pos)
                    self._layout = [lst[:] for lst in self._temp_layout]
                else:
                    self._moving = False
                    self._is_soft_dropping = False
                    self.populate_matrix(gameboard.get_fixed_layout(), True)
                    gameboard.check_row_delete()
                    gameboard.add_block(random.choice(BLOCK_LIST)())
        else:
            self._moving = False
            self._is_soft_dropping = False
            self.populate_matrix(gameboard.get_fixed_layout(), True)
            gameboard.check_row_delete()
            gameboard.add_block(random.choice(BLOCK_LIST)())
    
    def is_moving(self):
        """
        Returns whether block is moving or not
        """
        return self._moving
    
    def soft_drop(self, is_soft_dropping):
        self._is_soft_dropping = is_soft_dropping
    
    def is_soft_dropping(self):
        return self._is_soft_dropping

class I(Block):
    def __init__(self):
        Block.__init__(self, [4, 0])
        self.new_layout(self._orientation)
        self._layout = [lst[:] for lst in self._temp_layout]
        self._name = 'I'
    
    def new_layout(self, orientation):
        """
        Updates block's temp layout - used after moving and rotation
        """
        if orientation == 'Right' or orientation == 'Left' :
            self._temp_layout = [[self._temp_pos[0] + dummy_x, self._temp_pos[1]] for dummy_x in range(4)]
        elif orientation == 'Down' or orientation == 'Up' :
            self._temp_layout = [[self._temp_pos[0], self._temp_pos[1] + dummy_x] for dummy_x in range(4)]

class O(Block):
    def __init__(self):
        Block.__init__(self, [5, 0])
        self.new_layout(self._orientation)
        self._layout = [lst[:] for lst in self._temp_layout]
        self._name = 'O'
    
    def new_layout(self, dummy_orientation):
        """
        Updates block's layout - used after moving and rotation
        """
        # Since the O block remains the same after rotation, no if statements are needed
        self._temp_layout = [[self._temp_pos[0], self._temp_pos[1]],
                             [self._temp_pos[0], self._temp_pos[1] + 1],
                             [self._temp_pos[0] + 1, self._temp_pos[1]],
                             [self._temp_pos[0] + 1, self._temp_pos[1] + 1]
                            ]

class J(Block):
    def __init__(self):
        Block.__init__(self, [5, 1])
        self.new_layout(self._orientation)
        self._layout = [lst[:] for lst in self._temp_layout]
        self._name = 'J'
    
    def new_layout(self, orientation):
        """
        Updates block's layout - used after moving and rotation
        """
        if orientation == 'Right':
            self._temp_layout = [[self._temp_pos[0] - 1, self._temp_pos[1]],
                            [self._temp_pos[0] - 1, self._temp_pos[1] - 1],
                            [self._temp_pos[0], self._temp_pos[1]],
                            [self._temp_pos[0] + 1, self._temp_pos[1]]
                            ]
        elif orientation == 'Down':
            self._temp_layout = [[self._temp_pos[0], self._temp_pos[1] - 1],
                            [self._temp_pos[0], self._temp_pos[1]],
                            [self._temp_pos[0], self._temp_pos[1] + 1],
                            [self._temp_pos[0] + 1, self._temp_pos[1] - 1]
                            ]
        elif orientation == 'Left':
            self._temp_layout = [[self._temp_pos[0] - 1, self._temp_pos[1]],
                            [self._temp_pos[0], self._temp_pos[1]],
                            [self._temp_pos[0] + 1, self._temp_pos[1]],
                            [self._temp_pos[0] + 1, self._temp_pos[1] + 1]
                            ]
        elif orientation == 'Up':
            self._temp_layout = [[self._temp_pos[0] - 1, self._temp_pos[1] + 1],
                            [self._temp_pos[0], self._temp_pos[1] - 1],
                            [self._temp_pos[0], self._temp_pos[1]],
                            [self._temp_pos[0], self._temp_pos[1] + 1]
                            ]

class L(Block):
    def __init__(self):
        Block.__init__(self, [6, 1])
        self.new_layout(self._orientation)
        self._layout = [lst[:] for lst in self._temp_layout]
        self._name = 'L'
    
    def new_layout(self, orientation):
        """
        Updates block's layout - used after moving and rotation
        """
        if orientation == 'Right':
            self._temp_layout = [[self._temp_pos[0] - 1, self._temp_pos[1]],
                                 [self._temp_pos[0], self._temp_pos[1]],
                                 [self._temp_pos[0] + 1, self._temp_pos[1]],
                                 [self._temp_pos[0] + 1, self._temp_pos[1] - 1]
                                ]
        elif orientation == 'Down':
            self._temp_layout = [[self._temp_pos[0], self._temp_pos[1] - 1],
                                 [self._temp_pos[0], self._temp_pos[1]],
                                 [self._temp_pos[0], self._temp_pos[1] + 1],
                                 [self._temp_pos[0] + 1, self._temp_pos[1] + 1]
                                ]
        elif orientation == 'Left':
            self._temp_layout = [[self._temp_pos[0] - 1, self._temp_pos[1]],
                                 [self._temp_pos[0] - 1, self._temp_pos[1] + 1],
                                 [self._temp_pos[0], self._temp_pos[1]],
                                 [self._temp_pos[0] + 1, self._temp_pos[1]]
                                ]
        elif orientation == 'Up':
            self._temp_layout = [[self._temp_pos[0] - 1, self._temp_pos[1] - 1],
                                 [self._temp_pos[0], self._temp_pos[1] - 1],
                                 [self._temp_pos[0], self._temp_pos[1]],
                                 [self._temp_pos[0], self._temp_pos[1] + 1]
                                ]

class S(Block):
    def __init__(self):
        Block.__init__(self, [5, 0])
        self.new_layout(self._orientation)
        self._layout = [lst[:] for lst in self._temp_layout]
        self._name = 'S'
    
    def new_layout(self, orientation):
        """
        Updates block's layout - used after moving and rotation
        """
        if orientation == 'Right' or self._orientation == 'Left':
            self._temp_layout = [[self._temp_pos[0] - 1, self._temp_pos[1] + 1],
                            [self._temp_pos[0], self._temp_pos[1] + 1],
                            [self._temp_pos[0], self._temp_pos[1]],
                            [self._temp_pos[0] + 1, self._temp_pos[1]]
                            ]
        elif orientation == 'Down' or self._orientation == 'Up':
            self._temp_layout = [[self._temp_pos[0], self._temp_pos[1] - 1],
                            [self._temp_pos[0], self._temp_pos[1]],
                            [self._temp_pos[0] + 1, self._temp_pos[1]],
                            [self._temp_pos[0] + 1, self._temp_pos[1] + 1]
                            ]

class Z(Block):
    def __init__(self):
        Block.__init__(self, [6, 0])
        self.new_layout(self._orientation)
        self._layout = [lst[:] for lst in self._temp_layout]
        self._name = 'Z'
    
    def new_layout(self, orientation):
        """
        Updates block's layout - used after moving and rotation
        """
        if orientation == 'Right' or self._orientation == 'Left':
            self._temp_layout = [[self._temp_pos[0] - 1, self._temp_pos[1]],
                            [self._temp_pos[0], self._temp_pos[1]],
                            [self._temp_pos[0], self._temp_pos[1] + 1],
                            [self._temp_pos[0] + 1, self._temp_pos[1] + 1]
                            ]
        elif orientation == 'Down' or self._orientation == 'Up':
            self._temp_layout = [[self._temp_pos[0] - 1, self._temp_pos[1]],
                            [self._temp_pos[0] - 1, self._temp_pos[1] + 1],
                            [self._temp_pos[0], self._temp_pos[1] - 1],
                            [self._temp_pos[0], self._temp_pos[1]]
                            ]

class T(Block):
    def __init__(self):
        Block.__init__(self, [5, 1])
        self.new_layout(self._orientation)
        self._layout = [lst[:] for lst in self._temp_layout]
        self._name = 'T'
    
    def new_layout(self, orientation):
        """
        Updates block's layout - used after moving and rotation
        """
        if orientation == 'Right':
            self._temp_layout = [[self._temp_pos[0] - 1, self._temp_pos[1]],
                            [self._temp_pos[0], self._temp_pos[1]],
                            [self._temp_pos[0], self._temp_pos[1] - 1],
                            [self._temp_pos[0] + 1, self._temp_pos[1]]
                            ]
        elif orientation == 'Down':
            self._temp_layout = [[self._temp_pos[0], self._temp_pos[1] - 1],
                            [self._temp_pos[0], self._temp_pos[1]],
                            [self._temp_pos[0], self._temp_pos[1] + 1],
                            [self._temp_pos[0] + 1, self._temp_pos[1]]
                            ]
        elif orientation == 'Left':
            self._temp_layout = [[self._temp_pos[0] - 1, self._temp_pos[1]],
                            [self._temp_pos[0], self._temp_pos[1]],
                            [self._temp_pos[0], self._temp_pos[1] + 1],
                            [self._temp_pos[0] + 1, self._temp_pos[1]]
                            ]
        elif orientation == 'Up':
            self._temp_layout = [[self._temp_pos[0] - 1, self._temp_pos[1]],
                            [self._temp_pos[0], self._temp_pos[1] - 1],
                            [self._temp_pos[0], self._temp_pos[1]],
                            [self._temp_pos[0], self._temp_pos[1] + 1]
                            ]

def keydown_handler(key):
    curr_block = gameboard.get_current_block()
    
    if key == simplegui.KEY_MAP['right']: # move block to right
        curr_block.move_right()
    elif key == simplegui.KEY_MAP['left']: # move block to left
        curr_block.move_left()
    elif key == simplegui.KEY_MAP['Z']: # rotate block anticlockwise
        curr_block.rotate_anticlock()
    elif key == simplegui.KEY_MAP['X']: # rotate block clockwise
        curr_block.rotate_clock()
    elif key == simplegui.KEY_MAP['space']: # hard drops the block
        while curr_block.is_moving():
            curr_block.move_down()
    elif key == simplegui.KEY_MAP['down']:
        curr_block.soft_drop(True)

def keyup_handler(key):
    curr_block = gameboard.get_current_block()
    
    if key == simplegui.KEY_MAP['down']:
        curr_block.soft_drop(False)

def norm_timer_handler():
    curr_block = gameboard.get_current_block()
    
    if not curr_block.is_soft_dropping():
        curr_block.move_down()

def softdrop_timer_handler():
    curr_block = gameboard.get_current_block()
    
    if curr_block.is_soft_dropping():
        curr_block.move_down()

def draw(canvas): 
    gameboard.draw_board(canvas)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", WIDTH * BOX_SIZE, HEIGHT * BOX_SIZE)
frame.set_draw_handler(draw)
frame.set_canvas_background('White')
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.add_label("Number of lines destroyed")
frame.add_label("")
label = frame.add_label(str(0))

BLOCK_LIST = [I, O, J, L, S, Z, T]

gameboard = Board()

frame.start()
