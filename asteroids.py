# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
SCREEN_SIZE = [800, 600]
WIDTH = SCREEN_SIZE[0]
HEIGHT = SCREEN_SIZE[1]
score = 0
lives = 3
time = 0.5
started = False
num_dim = 2 #shows that action happens in 2D space

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
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")
explosion_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue.png")

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
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.acc = [0, 0]
        self.thrusting = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.thrust_image_center = [self.image_center[0] + self.image_size[0], self.image_center[1]]
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrusting:
            canvas.draw_image(self.image, self.thrust_image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel
        self.acc = [0.1 * component for component in angle_to_vector(self.angle)]
        
        for a in range (num_dim):
            self.pos[a] += self.vel[a]
            self.pos[a] %= SCREEN_SIZE[a]
            self.vel[a] *= (1 - 0.013)
            if self.thrusting:
                self.vel[a] += self.acc[a]
    
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
            
            missiles.add(Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound))
    
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
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
        if self.animated:
            image_center = [self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]]
            canvas.draw_image(self.image, image_center, self.image_size, self.pos, self.image_size)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        
        for a in range (num_dim):
            self.pos[a] += self.vel[a]
            self.pos[a] %= SCREEN_SIZE[a]
        
        self.age += 1
        
        if self.age >= self.lifespan:
            return True
        else:
            return False
    
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
    def collide(self, other_object):
        if dist(self.pos, other_object.get_position()) <= self.radius + other_object.get_radius():
            return True
        else:
            return False

def process_sprite_group(canvas, sprite_group):
    for sprite in set(sprite_group):
        sprite_to_be_removed = sprite.update()
        
        if sprite_to_be_removed:
            sprite_group.remove(sprite)
        else:
            sprite.draw(canvas)

def group_collide(group, other_object):
    for sprite in set(group):
        if sprite.collide(other_object):
            if other_object == my_ship:
                explosion_group.add(Sprite(other_object.pos, [0, 0], 0, 0, explosion_image2, explosion_info, explosion_sound))
            else:
                explosion_group.add(Sprite(sprite.pos, [0, 0], 0, 0, explosion_image1, explosion_info, explosion_sound))
            group.remove(sprite)
            return True

def group_group_collide(group1, group2):
    num_collisions = 0
    
    for sprite in set(group1):
        if group_collide(group2, sprite):
            num_collisions += 1
            group1.remove(sprite)
    
    return num_collisions

def reset():
    global rocks, missiles, started
    rocks = set([])
    missiles = set([])
    started = False
    timer.stop()
    soundtrack.rewind()

def keydown(key):
    for key1 in key_functions:
        if simplegui.KEY_MAP[key1] == key:
            key_functions[key1](True)

def keyup(key):
    for key1 in key_functions:
        if simplegui.KEY_MAP[key1] == key:
            key_functions[key1](False)

def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        timer.start()
        soundtrack.play()
        lives = 3
        score = 0

def draw(canvas):
    global time, lives, score
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    
    process_sprite_group(canvas, rocks)
    process_sprite_group(canvas, missiles)
    process_sprite_group(canvas, explosion_group)
    
    if group_collide(rocks, my_ship):
        lives -= 1
    
    if lives == 0:
        reset()
    
    score += group_group_collide(missiles, rocks)
    
    canvas.draw_text("Lives: " + str(lives), [20, 40], 30, "Lime")
    canvas.draw_text("Score: " + str(score), [680, 40], 30, "Lime")
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
            
# timer handler that spawns a rock    
def rock_spawner():
    global rocks
    
    pos_rock = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    
    while dist(pos_rock, my_ship.pos) <= 200:
        pos_rock = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    
    vel_rock = [random.random() + 0.5, random.random() + 0.5]
    ang_vel_rock = (random.random() / 20) + 0.05
    
    if random.randrange(0, 2) == 0:
        vel_rock[0] *= -1
    
    if random.randrange(0, 2) == 0:
        vel_rock[1] *= -1
    
    if random.randrange(0, 2) == 0:
        ang_vel_rock *= -1
    
    if len(rocks) < 12:
        rocks.add(Sprite(pos_rock, vel_rock, 0, ang_vel_rock, asteroid_image, asteroid_info))
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rocks = set([])
missiles = set([])
explosion_group = set([])

key_functions = {'right': my_ship.turn_right,
                 'left': my_ship.turn_left,
                 'up': my_ship.thrust,
                 'space': my_ship.shoot
                 }

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
frame.start()
