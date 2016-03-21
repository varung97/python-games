# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
width = 600
height = 400       
ball_radius = 20
pad_width = 8
pad_height = 80
half_pad_width = pad_width / 2
half_pad_height = pad_height / 2
right = True

ball_pos = [width / 2, height / 2]
ball_vel = [0, 0]

paddle1_pos = [half_pad_width, height / 2]
paddle2_pos = [width - half_pad_width - 1, height / 2]

paddle1_vel = 0
paddle2_vel = 0

score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball():
    global ball_pos, ball_vel, right # these are vectors stored as lists
    
    # Using 'right' variable to get correct direction to spawn in
    if right:
        hor_vel = random.randrange(120, 240) / 60.0
    else:
        hor_vel = - (random.randrange(120, 240) / 60.0)
    
    ver_vel = - (random.randrange(60, 180) / 60.0)
    
    ball_pos = [width / 2, height / 2]
    ball_vel = [hor_vel, ver_vel]
    
    right = True

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    score1 = 0
    score2 = 0
    
    spawn_ball()

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, right
 
        
    # draw mid line and gutters
    canvas.draw_line([width / 2, 0],[width / 2, height], 1, "White")
    canvas.draw_line([pad_width, 0],[pad_width, height], 1, "White")
    canvas.draw_line([width - pad_width, 0],[width - pad_width, height], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if (ball_pos[1] <= ball_radius) or (ball_pos[1] >= height - ball_radius - 1): # bounce ball off horizontal walls
        ball_vel[1] = - ball_vel[1]
    
    #Booleans for whether ball is touching paddles or not
    if ball_pos[1] > paddle1_pos[1] + half_pad_height or ball_pos[1] < paddle1_pos[1] - half_pad_height:
        touching_paddle1 = False
    else:
        touching_paddle1 = True
    
    if ball_pos[1] > paddle2_pos[1] + half_pad_height or ball_pos[1] < paddle2_pos[1] - half_pad_height:
        touching_paddle2 = False
    else:
        touching_paddle2 = True
    
    # Checking whether ball is touching gutter, first left, then right
    if ball_pos[0] <= pad_width + ball_radius:
        if not(touching_paddle1): # check whether ball is touching paddle1
            right = True
            score2 += 1
            spawn_ball()
        else:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
    elif ball_pos[0] >= width - pad_width - ball_radius - 1:
        if not(touching_paddle2): # check whether ball is touching paddle2
            right = False
            score1 += 1
            spawn_ball()
        else:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
            
    # draw ball
    canvas.draw_circle(ball_pos, ball_radius, 1, 'Blue', 'Blue')
    
    # update paddle's vertical position, keep paddle on the screen
    
    # stopping the paddles from going off the screen
    if not(paddle1_pos[1] + paddle1_vel + half_pad_height > 400) and not(paddle1_pos[1] + paddle1_vel - half_pad_height < 0):
        paddle1_pos[1] += paddle1_vel
    
    if not(paddle2_pos[1] + paddle2_vel + half_pad_height > 400) and not(paddle2_pos[1] + paddle2_vel - half_pad_height < 0):
        paddle2_pos[1] += paddle2_vel
    
    # getting the y values of the top and bottom of both paddles to use in drawing them
    paddle1bottom_yval = paddle1_pos[1] + half_pad_height
    paddle1top_yval = paddle1_pos[1] - half_pad_height
    
    paddle2bottom_yval = paddle2_pos[1] + half_pad_height
    paddle2top_yval = paddle2_pos[1] - half_pad_height
    
    # draw paddles
    canvas.draw_polygon([[0, paddle1bottom_yval], [7, paddle1bottom_yval], [7, paddle1top_yval], [0, paddle1top_yval]], 1, 'Red', 'Red')
    canvas.draw_polygon([[600, paddle2bottom_yval], [593, paddle2bottom_yval], [593, paddle2top_yval], [600, paddle2top_yval]], 1, 'Red', 'Red')

    # draw scores
    canvas.draw_text(str(score1), [140, 60], 40, 'Lime')
    canvas.draw_text(str(score2), [440, 60], 40, 'Lime')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    padacc = 270.0 / 60.0
    if key == simplegui.KEY_MAP['W']:
        paddle1_vel = - padacc
    elif key == simplegui.KEY_MAP['S']:
        paddle1_vel = padacc
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = - padacc
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = padacc
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['W'] or key == simplegui.KEY_MAP['S']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0

def button_handler():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", width, height)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
restart = frame.add_button('Restart', button_handler, 100)

# start frame
new_game()
frame.start()
