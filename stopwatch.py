# template for "Stopwatch: The Game"

import simplegui

# define global variables
elapsed = 0
num_stops = 0
num_wins = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format_time(t):
    deciseconds = t % 10
    seconds = (t / 10) % 60
    minutes = t / 600
    
    if minutes == 0:
        minutes_str = '0'
    else:
        minutes_str = str(minutes)
    
    if seconds == 0:
        seconds_str = '00'
    elif seconds / 10 == 0:
        seconds_str = '0' + str(seconds)
    else:
        seconds_str = str(seconds)
    
    if deciseconds == 0:
        deciseconds_str = '0'
    else:
        deciseconds_str = str(deciseconds)
    
    return minutes_str + ':' + seconds_str + '.' + deciseconds_str
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    timer.start()

def stop_handler():
    global num_stops
    global num_wins
    global elapsed
    
    timer_running = timer.is_running()
    
    timer.stop()
    if timer_running:
        num_stops += 1
    
    if timer_running and elapsed % 10 == 0:
        num_wins += 1

def reset_handler():
    global elapsed
    global num_stops
    global num_wins
    
    timer.stop()
    elapsed = 0
    num_stops = 0
    num_wins = 0
    

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global elapsed
    
    elapsed += 1

# define draw handler
def draw_handler(canvas):
    score_record = str(num_wins) + '/' + str(num_stops)
    
    canvas.draw_text(format_time(elapsed), (100, 120), 40, 'White')
    canvas.draw_text(score_record, (240, 40), 30, 'Blue')
    
# create frame
f = simplegui.create_frame("Stopwatch", 300, 200)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)

start_but = f.add_button('Start', start_handler, 100)
stop_but = f.add_button('Stop', stop_handler, 100)
reset_but = f.add_button('Reset', reset_handler, 100)

f.set_draw_handler(draw_handler)


# start frame
f.start()

# Please remember to review the grading rubric
