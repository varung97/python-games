# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
SCREEN_SIZE = [800, 600]
WIDTH = SCREEN_SIZE[0]
HEIGHT = SCREEN_SIZE[1]
score = 0
time = 0.5
num_dim = 2 #shows that action happens in 2D space
max_missile_number = 3

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 4)
missile1_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")
missile2_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, missile_image, ship_number):
        self.pos = [pos[0],pos[1]]
        self.start_pos = list(self.pos)
        self.vel = [vel[0],vel[1]]
        self.acc = [0, 0]
        self.thrusting = False
        self.angle = angle
        self.orig_angle = float(angle)
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.thrust_image_center = [self.image_center[0] + self.image_size[0], self.image_center[1]]
        self.radius = info.get_radius()
        self.invincible = True
        self.invincible_time = 0
        self.score = 0
        self.missiles = []
        self.missile_image = missile_image
        self.number = ship_number
        
    def draw(self,canvas):
        if self.thrusting:
            canvas.draw_image(self.image, self.thrust_image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
        canvas.draw_circle(self.pos, 30, 1, ship_colours[self.number])

    def update(self):
        self.angle += self.angle_vel
        self.acc = [0.1 * component for component in angle_to_vector(self.angle)]
        
        for a in range (num_dim):
            self.pos[a] += self.vel[a]
            self.pos[a] %= SCREEN_SIZE[a]
            self.vel[a] *= (1 - 0.013)
            if self.thrusting:
                self.vel[a] += self.acc[a]
        
        if self.invincible:
            self.invincible_time += 1.0/60.0
        if self.invincible_time >= 2:
            self.invincible_time = 0
            self.invincible = False
    
    def turn_right(self, is_not_turning):
        if is_not_turning:
            self.angle_vel = 0.1
        else:
            self.angle_vel = 0
    
    def turn_left(self, is_not_turning):
        if is_not_turning:
            self.angle_vel = -0.1
        else:
            self.angle_vel = 0
    
    def thrust(self, is_not_thrusting):
        if is_not_thrusting:
            self.thrusting = True
            ship_thrust_sound.play()
        else:
            self.thrusting = False
            ship_thrust_sound.rewind()
    
    def shoot(self, is_firing):
        global missiles
        
        if is_firing:
            missile_pos = [self.pos[0] + angle_to_vector(self.angle)[0] * 40, self.pos[1] + angle_to_vector(self.angle)[1] * 40]
            missile_vel = list(self.vel)
            
            for a in range(num_dim):
                missile_vel[a] += self.acc[a] * 50
            
            if len(self.missiles) < max_missile_number:
                self.missiles.append(Sprite(missile_pos, missile_vel, 0, 0, self.missile_image, missile_info, missile_sound))
    
    def reset(self):
        self.pos = list(self.start_pos)
        self.vel = [0, 0]
        self.acc = [0, 0]
        self.angle = float(self.orig_angle)
        self.angle_vel = 0
        self.invincible = True
        self.invincible_time = 0
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        
        for a in range (num_dim):
            self.pos[a] += self.vel[a]
            self.pos[a] %= SCREEN_SIZE[a]
        
        self.age += 1.0/60.0

def keydown(key):
    for key1 in key_functions:
        if key1 == key:
            key_functions[key1](True)

def keyup(key):
    for key1 in key_functions:
        if key1 == key:
            key_functions[key1](False)

def draw(canvas):
    global time, lives, my_ship, missiles, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    for ship in ships:
        ship.draw(canvas)
        for missile in ship.missiles:
            missile.draw(canvas)
    
    # update ship and sprites
    for ship in ships:
        ship.update()
    
    ship_number = -1
    for ship in ships:
        missiles_to_be_removed = []
        ship_number += 1
        for missile in ship.missiles:
            missile.update()
            if missile.age >= missile.lifespan:
                missiles_to_be_removed.append(missile)
            
            if ship_number == 0:
                other_ship_number = 1
            else:
                other_ship_number = 0
            
            if dist(missile.pos, ships[other_ship_number].pos) <= missile.radius + ships[other_ship_number].radius and \
               not ships[other_ship_number].invincible:
                    ship.score += 1
                    ships[other_ship_number].invincible = True
                    if missile not in missiles_to_be_removed:
                        missiles_to_be_removed.append(missile)
        
        for a in missiles_to_be_removed:
            ship.missiles.remove(a)
    
    for ship in ships:
        if ship.invincible:
            canvas.draw_circle(ship.pos, 60, 1, "Lime")
    
    canvas.draw_text("Score: " + str(ships[0].score), [20, 40], 30, ship_colours[0])
    canvas.draw_text("Score: " + str(ships[1].score), [680, 40], 30, ship_colours[1])
            
# timer handler that spawns a rock

def new_game():
    global missiles, score
    
    for ship in ships:
        ship.reset()
        ship.score = 0
    missiles = []

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
ships = [Ship([WIDTH * 1 / 4, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, missile2_image, 0),
         Ship([WIDTH * 3 / 4, HEIGHT / 2], [0, 0], math.pi, ship_image, ship_info, missile1_image, 1)
         ]

ship_colours = ["Aqua", "Red"]

key_functions = {68: ships[0].turn_right,		#d
                 65: ships[0].turn_left, 		#a
                 87: ships[0].thrust,    		#w
                 32: ships[0].shoot,			#space
                 39: ships[1].turn_right,		#right
                 37: ships[1].turn_left,		#left
                 38: ships[1].thrust,			#up
                 16: ships[1].shoot 			#shift
                 }

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("New Game", new_game, 150)

# get things rolling
frame.start()
