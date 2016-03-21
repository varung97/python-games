# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor runs in Chrome 18+, Firefox 11+, and Safari 6+.
# Some features may work in other browsers, but do not expect
# full functionality.  It does NOT run in Internet Explorer.

import simplegui, random

WIDTH = 600
HEIGHT = 400
score = 0
time = 0
draw_reps = 0
started = True
PILLAR_PER = 4
PILLAR_VEL = 80.0/60
PILLAR_WIDTH = 30
GAP = 70
GRAV = 7.0/60
UP_VEL = -200.0/60

class Bird:
    def __init__(self):
        self._x = WIDTH / 2
        self._y = HEIGHT / 2
        self._y_vel = 0
        self._grav = GRAV
        self._up_vel = UP_VEL
        self._radius = 10
    
    def draw(self, canvas):
        canvas.draw_circle([self._x, self._y], self._radius, 1, 'Blue', 'Blue')
    
    def update(self):
        self._y_vel += self._grav
        self._y += self._y_vel
    
    def up(self):
        self._y_vel = self._up_vel
    
    def get_vars(self):
        return ((self._x, self._y), self._radius)

class Pillar:
    def __init__(self, gap, gap_pos):
        self._x = WIDTH
        self._gap = gap
        self._gap_pos = gap_pos
        self._width = PILLAR_WIDTH
        self._passed = False
    
    def draw(self, canvas):
        canvas.draw_polygon([(self._x, 0),
                             (self._x + self._width, 0),
                             (self._x + self._width, self._gap_pos),
                             (self._x, self._gap_pos)
                            ],
                            2, 'Red'
                           )
        canvas.draw_polygon([(self._x, self._gap_pos + self._gap),
                             (self._x + self._width, self._gap_pos + self._gap),
                             (self._x + self._width, HEIGHT),
                             (self._x, HEIGHT)
                            ],
                            2, 'Red'
                           )
    
    def update(self):
        self._x -= PILLAR_VEL
        if abs(self._x + PILLAR_WIDTH) < 0.00001:
            return False
        else:
            return True
    
    def get_vars(self):
        return self._gap_pos, self._gap, self._x, self._width

    
    def just_passed(self, bird):
        bird_pos, bird_rad = bird.get_vars()
        
        if (self._x + self._width <= bird_pos[0] - bird_rad and 
            not self._passed):

            self._passed = True
            return True

        return False    	


bird = Bird()
pillars = [Pillar(GAP, 100)]

def bird_pil_col(bird, pillar):
    bird_pos, bird_rad = bird.get_vars()
    pil_gap_pos, pil_gap, pil_x, pil_width = pillar.get_vars()
    if (bird_pos[1] >= pil_gap_pos + pil_gap or 
        bird_pos[1] <= pil_gap_pos):

        return (bird_pos[0] >= pil_x - bird_rad and
                bird_pos[0] <= pil_x + pil_width + bird_rad)

    elif (bird_pos[0] >= pil_x and
          bird_pos[0] <= pil_x + pil_width):

        return (bird_pos[1] <= pil_gap_pos + bird_rad or
                bird_pos[1] >= pil_gap_pos + pil_gap - bird_rad)

    else:
        return (dist_sq(bird_pos, (pil_x, pil_gap_pos)) <= bird_rad ** 2 or
                dist_sq(bird_pos, (pil_x + pil_width, pil_gap_pos)) <= bird_rad ** 2 or
                dist_sq(bird_pos, (pil_x + pil_width, pil_gap_pos + pil_gap)) <= bird_rad ** 2 or
                dist_sq(bird_pos, (pil_x, pil_gap_pos + pil_gap)) <= bird_rad ** 2 
               )

def bird_wall_col(bird):
    bird_pos, bird_rad = bird.get_vars()
    
    return bird_pos[1] <= bird_rad or bird_pos[1] >= HEIGHT - bird_rad

def dist_sq(pt1, pt2):
    return (pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2

def restart():
    global started, time, draw_reps, bird, pillars, score
    
    bird = Bird()
    pillars = [Pillar(GAP, 100)]
    score = 0
    time = 0
    draw_rep = 0
    started = True

def key_up(key):
    global started
    
    if key == simplegui.KEY_MAP['space']:
        if started:
            bird.up()
        else:
            restart()

# Handler to draw on canvas
def draw(canvas):
    global draw_reps, time, started, score
    
    if started:
        draw_reps = (draw_reps + 1) % 60
        if draw_reps == 0:
            time += 1

            if time % PILLAR_PER == 0:
                pillars.append(Pillar(GAP, random.randint(0, HEIGHT - GAP)))

        bird.update()
        if bird_wall_col(bird):
            started = False

        to_remove = False
        for pillar in pillars:
            if not pillar.update():
                to_remove = True
            else:
                if bird_pil_col(bird, pillar):
                    started = False
                elif pillar.just_passed(bird):
                    score += 1
        if to_remove:
            pillars.pop(0)
    
    canvas.draw_text(str(score), (20, 50), 40, 'White')
    bird.draw(canvas)
    for pillar in pillars:
        pillar.draw(canvas)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keyup_handler(key_up)

# Start the frame animation
frame.start()
