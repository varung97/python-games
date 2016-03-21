# implementation of card game - Memory

import simplegui
import random

state = 0
cards = 2 * [n for n in range(0, 8)]
exposed = 16 * [False]
curr_exp = []
num_turns = 0

height = 100

# helper function to initialize globals
def new_game():
    global num_turns, exposed, state, curr_exp
    
    random.shuffle(cards)
    exposed = 16 * [False]
    curr_exp = []
    num_turns = 0
    state = 0
    
    label.set_text("Turns = " + str(num_turns))
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, curr_exp, num_turns
    
    card_idx = pos[0] / 50
    
    if not(exposed[card_idx]) and pos[0] % 50 < 48:
        
        exposed[card_idx] = True
        
        if state == 0:
            state = 1
            curr_exp.append(card_idx)
            
        elif state == 1:
            state = 2
            curr_exp.append(card_idx)
            
            num_turns += 1
            label.set_text("Turns = " + str(num_turns))
            
        else:
            state = 1
            if not(cards[curr_exp[0]] == cards[curr_exp[1]]):
                exposed[curr_exp[0]] = False
                exposed[curr_exp[1]] = False
            
            curr_exp = [card_idx]
            
            
# cards are logically 50x100 pixels in size    
def draw(canvas):
    n = 0
    for card in cards:
        if exposed[n]:
            canvas.draw_text(str(card), [n * 50 + 15, 60], 40, "White")
        else:
            canvas.draw_polygon([[n * 50, 0], [n * 50 + 47, 0], [n * 50 + 47, height], [n * 50, height]], 1, "Blue", "Blue")
        n += 1


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 799, 100)
frame.add_button("Reset", new_game)

blank_line = frame.add_label("")

label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric
