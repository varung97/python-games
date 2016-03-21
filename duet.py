import simplegui
import math
import random

ball_1_pos = [225, 500]
ball_1_vel = [0, 0] #vector representing ball's velocity

ball_2_pos = [75, 500]
ball_2_vel = [0, 0] #vector representing ball's velocity

ball_speed = 3.5 #shows that balls travels 3.5 pixels each time draw_handler is called
ball_is_moving = False
is_clock = True

obslist = []

obs_vel = 2.0 #number of pixels moved downwards every time draw handler is called

score = 0

gameon = True

class Obstacle:
    def __init__ (self):
        pass
    
    height = 20
    width = 100
    has_to_spawn = True #stores whether this obstacle has to spawned another obstacle yet or not
        
    def disappear(self):
        obslist.pop(0)
    def move(self):
        self.tlcor_pos[1] += obs_vel

class Obs1(Obstacle):
    def __init__ (self):
        self.tlcor_pos = [30, 30] #co-ords of top left corner
        
class Obs2(Obstacle):
    def __init__ (self):
        self.tlcor_pos = [100, 30] #co-ords of top left corner

class Obs3(Obstacle):
    def __init__ (self):
        self.tlcor_pos = [170, 30] #co-ords of top left corner

def conv_to_unit(vec): #returns unit vector and mag of original vector
    mag = math.sqrt(vec[0]**2 + vec[1]**2)
    
    if gameon and mag != 0:
        unit_vec = [vec[0]/mag, vec[1]/mag]
    else:
        unit_vec = [0, 0]
    return unit_vec, mag

def solve_quad (a, b, c): #solves quad eq when a, b and c are provided
    
    d = (b**2) - (4*a*c)
    
    sol1 = (-b - math.sqrt(d))/(2*a)
    sol2 = (-b + math.sqrt(d))/(2*a)
    
    return sol1, sol2

def get_new_vec(vec, clock): #returns vector of same mag. Parameter clock expects a boolean which decides whether vector should be rotated clokwise or anticlockwise
    #Calculates new vector using simultaneuous equations derived from the dot product formula
    
    new_vec = [0, 0]
    
    unit_vector, orig_mag = conv_to_unit(vec)
    
    cos1 = math.cos(math.radians(2.7))
    
    m = unit_vector[0] #orig x-val
    n = unit_vector[1] #orig y-val
    
    if n > 0.00000001 or n < -0.0000001: #To catch case where n is really tiny but not exactly 0
        a = 1 + (m**2/n**2)
        b = - (2 * m * cos1) / n**2
        c = (cos1**2/n**2) - 1
        
        if clock:
            if n < 0:
                discard, new_vec[0] = solve_quad (a, b, c)  #above x-axis, takes vector with larger x-val
            elif n > 0:
                new_vec[0], discard = solve_quad (a, b, c)  #below x-axis, takes vector with larger x-val
            elif n == 0:
                if m < 0:
                    discard, new_vec[0] = solve_quad (a, b, c)  #vector lies along negative x-axis, takes vector with larger x-val
                elif m > 0:
                    new_vec[0], discard = solve_quad (a, b, c)  #vector lies along positive x-axis, takes vector with smaller x-val
        else:
            if n < 0:
                new_vec[0], discard = solve_quad (a, b, c)  #above x-axis, takes vector with larger x-val
            elif n > 0:
                discard, new_vec[0] = solve_quad (a, b, c)  #below x-axis, takes vector with larger x-val
            elif n == 0:
                if m < 0:
                    new_vec[0], discard = solve_quad (a, b, c)  #vector lies along negative x-axis, takes vector with larger x-val
                elif m > 0:
                    discard, new_vec[0] = solve_quad (a, b, c)  #vector lies along positive x-axis, takes vector with smaller x-val
        
        new_vec[1] = (cos1 - m * new_vec[0]) / n 
    
    else:
        if m != 0: #catch case where m = 0
            new_vec[0] = cos1/m
        
        if clock:
            if m > 0:
                y_val_pos = True
            else:
                y_val_pos = False
        else:
            if m > 0:
                y_val_pos = False
            else:
                y_val_pos = True
             
        if y_val_pos:
            new_vec[1] = math.sqrt(1 - new_vec[0]**2) #if previous formula is used to get y-val, the value becomes very large since n is very small
        else:
            new_vec[1] = - math.sqrt(1 - new_vec[0]**2)
    
    if new_vec[0] == 1 or new_vec[0] == -1: #Because math.sqrt returns NaN instead of 0 when 0 is passed into it
        new_vec[1] = 0
    
    new_vec[0] *= orig_mag #get vector with same mag as original
    new_vec[1] *= orig_mag
    
    return new_vec

def check_col (tl_cor, tr_cor, br_cor, bl_cor): #checks whether the obstacle has collided with a ball
    
    if ball_1_pos[1] >= tl_cor[1] - 10 and \
       ball_1_pos[1] <= bl_cor[1] + 10 and \
       ball_1_pos[0] >= tl_cor[0] and \
       ball_1_pos[0] <= tr_cor[0]: #the '10' accounts for radius
        
        gameover()
        
    elif ball_1_pos[0] >= tl_cor[0] - 10 and \
         ball_1_pos[0] <= tr_cor[0] + 10 and \
         ball_1_pos[1] >= tl_cor[1] and \
         ball_1_pos[1] <= bl_cor[1]:
        
        gameover()
    
    elif ball_2_pos[1] >= tl_cor[1] - 10 and \
         ball_2_pos[1] <= bl_cor[1] + 10 and \
         ball_2_pos[0] >= tl_cor[0] and \
         ball_2_pos[0] <= tr_cor[0]: #the '10' accounts for radius
        
        gameover()
        
    elif ball_2_pos[0] >= tl_cor[0] - 10 and \
         ball_2_pos[0] <= tr_cor[0] + 10 and \
         ball_2_pos[1] >= tl_cor[1] and \
         ball_2_pos[1] <= bl_cor[1]:
        
        gameover()

def gameover():
    global ball_is_moving, obs_vel, gameon, ball_speed
    
    ball_is_moving = False
    obs_vel = 0
    ball_speed = 0
    gameon = False

def restart():
    global gameon, ball_1_pos, ball_1_vel, ball_2_pos, ball_2_vel,  ball_speed, ball_is_moving, is_clock, obslist, obs_vel, score
    
    gameon = True
    
    ball_1_pos = [225, 500]
    ball_1_vel = [0, 0] 
    
    ball_2_pos = [75, 500]
    ball_2_vel = [0, 0]
    
    ball_speed = 3.5
    
    ball_is_moving = False
    is_clock = True
    
    obslist = [Obs1()]
    
    obs_vel = 2.0
    
    score = 0

def create_obs(): #creates new random obstacles
    obstype = random.randrange(1, 4)
    
    if obstype == 1:
        obslist.append(Obs1())
    elif obstype == 2:
        obslist.append(Obs2())
    elif obstype == 3:
        obslist.append(Obs3())

def keydown_handler(key):
    #assign an initial velocity
    
    global ball_1_vel, ball_2_vel, ball_is_moving, is_clock
    
    position_1_vec = [ball_1_pos[0] - 150, ball_1_pos[1] - 500]
    position_2_vec = [ball_2_pos[0] - 150, ball_2_pos[1] - 500]
    
    if key == simplegui.KEY_MAP['right']: #turn clockwise
        ball_1_vel = [-position_1_vec[1], position_1_vec[0]] #Find perpendicular to position vector according to direction of rotation (because two perpendicular vectors exist
        ball_2_vel = [-position_2_vec[1], position_2_vec[0]]
        is_clock = True
    elif key == simplegui.KEY_MAP['left']: #turn anticlockwise
        ball_1_vel = [position_1_vec[1], -position_1_vec[0]] #Find perpendicular to position vector
        ball_2_vel = [position_2_vec[1], -position_2_vec[0]]
        is_clock = False
    
    unit_ball_1_vel, discard = conv_to_unit(ball_1_vel) #scale velocity vector up to ball speed
    ball_1_vel[0] = unit_ball_1_vel[0] * ball_speed
    ball_1_vel[1] = unit_ball_1_vel[1] * ball_speed
    
    unit_ball_2_vel, discard = conv_to_unit(ball_2_vel) #scale velocity vector up to ball speed
    ball_2_vel[0] = unit_ball_2_vel[0] * ball_speed
    ball_2_vel[1] = unit_ball_2_vel[1] * ball_speed
    
    ball_is_moving = True
    
    if key == simplegui.KEY_MAP['space'] and not(gameon): #Restart game
        restart()        

def keyup_handler(key):
    global ball_is_moving
    
    ball_is_moving = False

def draw(canvas):
    global ball_1_pos, ball_1_vel, ball_2_pos, ball_2_vel
    
    if ball_is_moving:
        ball_1_pos[0] += ball_1_vel[0]
        ball_1_pos[1] += ball_1_vel[1]
        
        ball_1_vel = get_new_vec(ball_1_vel, is_clock)
        
        ball_2_pos[0] += ball_2_vel[0]
        ball_2_pos[1] += ball_2_vel[1]
        
        ball_2_vel = get_new_vec(ball_2_vel, is_clock)
        
    canvas.draw_circle([150, 500], 75, 1, 'White')
    canvas.draw_circle(ball_1_pos, 10, 1, 'Red', 'Red')
    canvas.draw_circle(ball_2_pos, 10, 1, 'Blue', 'Blue')
    
    obsnum = 0
    
    for a in obslist: #draw obstacles
        obs_tlcor = a.tlcor_pos
        obs_height = a.height
        obs_width = a.width
           
        a.move()
        
        if obs_tlcor[1] >= 200 and a.has_to_spawn:
            create_obs()
            a.has_to_spawn = False
           
        if obs_tlcor[1] >= 600:
            global obs_vel, score
            
            score += 1
            a.disappear() #remove obstacle from list
            
            if obs_vel <= 2.45: #increase speed faster initially
                obs_vel += 0.05
                
            elif obs_vel <= 2.975: #cap speed at manageable level of 3.0
               obs_vel += 0.025 #increase speed of obstacles whenever one goes off the screen
            
        obs_trcor = [obs_tlcor[0] + obs_width, obs_tlcor[1]]
        obs_brcor = [obs_tlcor[0] + obs_width, obs_tlcor[1] + obs_height]
        obs_blcor = [obs_tlcor[0], obs_tlcor[1] + obs_height]
            
        canvas.draw_polygon([obs_tlcor, obs_trcor, obs_brcor, obs_blcor], 1, "Orange", "Orange")
        
        if (obsnum == 0 or obsnum == 1) and gameon: #so that comparison is done only with the two obstacles closest to the bottom of the screen
            check_col(obs_tlcor, obs_trcor, obs_brcor, obs_blcor)
            
        obsnum += 1
    
    canvas.draw_text(str(score), [270, 30], 30, 'White')
    
    if not(gameon):
        canvas.draw_text('GAME OVER', [30, 300], 40, 'Lime')
        canvas.draw_text('Press Space to restart', [40, 350], 25, 'Purple')

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", 300, 600)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)

# Start the frame animation
frame.start()
obslist = [Obs1()]
