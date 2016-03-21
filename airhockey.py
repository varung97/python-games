import simplegui
import math

#declaring global variables
WIDTH = 900
HEIGHT = 450

striker1_pos = [70, HEIGHT / 2]
striker2_pos = [830, HEIGHT / 2]
striker1_vel = [0, 0]
striker2_vel = [0, 0]
striker_speed = 5
striker_rad = 23

puck_pos = [(WIDTH * 1) / 4, HEIGHT / 2]
puck_vel = [0, 0]
puck_rad = 15
cap = 12

w_pressed = False
s_pressed = False
a_pressed = False
d_pressed = False
up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False

right = True #Boolean telling code which side puck should be placed on

score1 = 0
score2 = 0
win_score = 7

is_not_colliding = True

#helper functions
def new_game():
    global striker1_pos, striker2_pos, striker1_vel, striker2_vel, \
           puck_pos, puck_vel, w_pressed, s_pressed, a_pressed, \
           d_pressed, up_pressed, down_pressed, left_pressed, \
           right_pressed, score1, score2, is_not_colliding, \
           striker_speed
    
    striker1_pos = [70, HEIGHT / 2]
    striker2_pos = [830, HEIGHT / 2]
    striker1_vel = [0, 0]
    striker2_vel = [0, 0]
    striker_speed = 5
    
    if right:
        puck_pos = [(WIDTH * 3) / 4, HEIGHT / 2]
    else:
        puck_pos = [(WIDTH * 1) / 4, HEIGHT / 2]
    
    puck_vel = [0, 0]
    puck_rad = 15
    
    w_pressed = False
    s_pressed = False
    a_pressed = False
    d_pressed = False
    up_pressed = False
    down_pressed = False
    left_pressed = False
    right_pressed = False
    
    score1 = 0
    score2 = 0
    
    is_not_colliding = True    

def new_point():
    global striker1_pos, striker2_pos, striker1_vel, striker2_vel, \
           puck_pos, puck_vel, w_pressed, s_pressed, a_pressed, \
           d_pressed, up_pressed, down_pressed, left_pressed, \
           right_pressed, is_not_colliding
    
    striker1_pos = [70, HEIGHT / 2]
    striker2_pos = [830, HEIGHT / 2]
    striker1_vel = [0, 0]
    striker2_vel = [0, 0]
    
    if right:
        puck_pos = [(WIDTH * 3) / 4, HEIGHT / 2]
    else:
        puck_pos = [(WIDTH * 1) / 4, HEIGHT / 2]
    
    puck_vel = [0, 0]
    puck_rad = 15
    
    w_pressed = False
    s_pressed = False
    a_pressed = False
    d_pressed = False
    up_pressed = False
    down_pressed = False
    left_pressed = False
    right_pressed = False
    
    is_not_colliding = True

def dist(p, q):
    distance = math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)
    
    return distance

def get_mag(vec):
    mag = math.sqrt(vec[0]**2 + vec[1]**2)
    
    return mag

def solve_quad(x2coeff, xcoeff, constant): #solves quad eq
    
    det = (xcoeff**2) - (4 * x2coeff * constant)
    
    sol1 = (-xcoeff - math.sqrt(det))/(2 * x2coeff)
    sol2 = (-xcoeff + math.sqrt(det))/(2 * x2coeff)
    
    return sol1, sol2

def puckstrikercollision(puck_pos1, puck_vel1, striker_pos, striker_vel):
    
    new_vel = [0, 0]
    
    if puck_vel1[0] != 0 or puck_vel1[1] != 0:
        
        vec_to_reflect_around = [-(puck_pos1[1] - striker_pos[1]), puck_pos1[0] - striker_pos[0]]
        
        a = vec_to_reflect_around[0]
        b = vec_to_reflect_around[1]
        c = puck_vel1[0]
        d = puck_vel1[1]
        e = c**2 + d**2
        f = a * c + b * d
        
        x2coeff = a**2 + b**2
        xcoeff = -2 * a * f
        constant = f**2 - e * b**2
        
        sol1, sol2 = solve_quad(x2coeff, xcoeff, constant)
        
        if not(sol1 < puck_vel1[0] + 0.0000000001 and sol1 > puck_vel1[0] - 0.0000000001):
            xcomp = sol1
        else:
            xcomp = sol2
        
        ycomp = (f - a * xcomp) / b
                  
        new_vel = [xcomp + striker_vel[0], ycomp + striker_vel[1]]
    
    else:
        vec_rebounds_along = [puck_pos1[0] - striker_pos[0], puck_pos1[1] - striker_pos[1]]
        magnitude_of_prev = get_mag(vec_rebounds_along)
        unit_vec = [vec_rebounds_along[0] / magnitude_of_prev, vec_rebounds_along[1] / magnitude_of_prev]
                
        new_vel[0] += unit_vec[0] * striker_speed * 1.3
        new_vel[1] += unit_vec[1] * striker_speed * 1.3
    
    if get_mag(new_vel) > cap:
        mag = get_mag(new_vel)
        
        new_vel[0] *= cap / mag
        new_vel[1] *= cap / mag
    
    return new_vel

# Handlers for keys
def keydown(key):
    global w_pressed, s_pressed, a_pressed, d_pressed, up_pressed, down_pressed, left_pressed, right_pressed
    
    if key == simplegui.KEY_MAP['w']:
        striker1_vel[1] = -striker_speed
        w_pressed = True
    elif key == simplegui.KEY_MAP['s']:
        striker1_vel[1] = striker_speed
        s_pressed = True
    elif key == simplegui.KEY_MAP['a']:
        striker1_vel[0] = -striker_speed
        a_pressed = True
    elif key == simplegui.KEY_MAP['d']:
        striker1_vel[0] = striker_speed
        d_pressed = True
    elif key == simplegui.KEY_MAP['up']:
        striker2_vel[1] = -striker_speed
        up_pressed = True
    elif key == simplegui.KEY_MAP['down']:
        striker2_vel[1] = striker_speed
        down_pressed = True
    elif key == simplegui.KEY_MAP['left']:
        striker2_vel[0] = -striker_speed
        left_pressed = True
    elif key == simplegui.KEY_MAP['right']:
        striker2_vel[0] = striker_speed
        right_pressed = True

def keyup(key):
    global w_pressed, s_pressed, a_pressed, d_pressed, up_pressed, down_pressed, left_pressed, right_pressed
    
    if key == simplegui.KEY_MAP['w']:
        if not s_pressed:
            striker1_vel[1] = 0
        w_pressed = False
    elif key == simplegui.KEY_MAP['s']:
        if not w_pressed:
            striker1_vel[1] = 0
        s_pressed = False
    elif key == simplegui.KEY_MAP['a']:
        if not d_pressed:
            striker1_vel[0] = 0
        a_pressed = False
    elif key == simplegui.KEY_MAP['d']:
        if not a_pressed:
            striker1_vel[0] = 0
        d_pressed = False
    elif key == simplegui.KEY_MAP['up']:
        if not down_pressed:
            striker2_vel[1] = 0
        up_pressed = False
    elif key == simplegui.KEY_MAP['down']:
        if not up_pressed:
            striker2_vel[1] = 0
        down_pressed = False
    elif key == simplegui.KEY_MAP['left']:
        if not right_pressed:
            striker2_vel[0] = 0
        left_pressed = False
    elif key == simplegui.KEY_MAP['right']:
        if not left_pressed:
            striker2_vel[0] = 0
        right_pressed = False

def timer_handler():
    new_game()
    timer.stop()
        
# Handler to draw on canvas
def draw(canvas):
    global right, is_not_colliding, puck_vel, score1, score2
    
    #draw out the gameboard
    canvas.draw_line([10, 0], [10, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - 10, 0], [WIDTH - 10, HEIGHT], 1, "White")
    canvas.draw_line([10, HEIGHT / 2 - 80], [10, HEIGHT / 2 + 80], 1, "Yellow")
    canvas.draw_line([WIDTH - 10, HEIGHT / 2 - 80], [WIDTH - 10, HEIGHT / 2 + 80], 1, "Yellow")
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    
    #update puck
    puck_pos[0] += puck_vel[0]
    puck_pos[1] += puck_vel[1]
    
    #update strikers
    if striker1_pos[0] + striker1_vel[0] + striker_rad + 1 <= WIDTH / 2 and \
       striker1_pos[0] + striker1_vel[0] - striker_rad >= 10: #to limit hor pos of striker 1
            striker1_pos[0] += striker1_vel[0]
            
    if striker1_pos[1] + striker1_vel[1] + striker_rad + 1 <= HEIGHT and \
       striker1_pos[1] + striker1_vel[1] - striker_rad >= 0: #to limit ver pos of striker 1
            striker1_pos[1] += striker1_vel[1]
    
    if striker2_pos[0] + striker2_vel[0] + striker_rad + 1 <= WIDTH - 10 and \
       striker2_pos[0] + striker2_vel[0] - striker_rad - 1 >= WIDTH / 2: #to limit hor pos of striker 2
            striker2_pos[0] += striker2_vel[0]
            
    if striker2_pos[1] + striker2_vel[1] + striker_rad + 1 <= HEIGHT and \
       striker2_pos[1] + striker2_vel[1] - striker_rad >= 0: #to limit ver pos of striker 1
            striker2_pos[1] += striker2_vel[1]
    
    #reflect puck from edges of gameboard
    if puck_pos[1] + puck_rad >= HEIGHT or \
       puck_pos[1] - puck_rad <= 0:
            puck_vel[1] = -puck_vel[1]
    
    if puck_pos[0] + puck_rad + 1 >= WIDTH - 10:
        if puck_pos[1] <= HEIGHT / 2 - 80 or \
           puck_pos[1] >= HEIGHT / 2 + 80:
                puck_vel[0] = -puck_vel[0]
        
        else:
            right = True
            score1 += 1
            new_point()
                            
    elif puck_pos[0] - puck_rad <= 10:
        if puck_pos[1] <= HEIGHT / 2 - 80 or \
           puck_pos[1] >= HEIGHT / 2 + 80:
                puck_vel[0] = -puck_vel[0]
        
        else:               
            right = False
            score2 += 1
            new_point()
    
    if dist(puck_pos, striker1_pos) <= puck_rad + striker_rad + 1 and is_not_colliding:
        puck_vel = puckstrikercollision(puck_pos, puck_vel, striker1_pos, striker1_vel)
        is_not_colliding = False
    
    if dist(puck_pos, striker2_pos) <= puck_rad + striker_rad + 1 and is_not_colliding:
        puck_vel = puckstrikercollision(puck_pos, puck_vel, striker2_pos, striker2_vel)
        is_not_colliding = False
    
    if dist(puck_pos, striker1_pos) > puck_rad + striker_rad + 1 and dist(puck_pos, striker2_pos) > puck_rad + striker_rad + 1:
        is_not_colliding = True
    
    #draw puck and strikers
    canvas.draw_circle(striker1_pos, striker_rad, 1, "Red", "Red")
    canvas.draw_circle(striker2_pos, striker_rad, 1, "Blue", "Blue")
    canvas.draw_circle(puck_pos, puck_rad, 1, "White", "White")
    
    canvas.draw_text(str(score1), [WIDTH / 2 - 50, 40], 40, "Lime")
    canvas.draw_text(str(score2), [WIDTH / 2 + 30, 40], 40, "Lime")
    
    if score1 == win_score:
        canvas.draw_text("Player 1 wins!", [WIDTH / 2 - 150, 250], 60, "Lime")
        timer.start()
    elif score2 == win_score:
        canvas.draw_text("Player 2 wins!", [WIDTH / 2 - 100, 250], 60, "Lime")
        timer.start()

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Air Hockey", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(3000, timer_handler)

# Start the frame animation
frame.start()
