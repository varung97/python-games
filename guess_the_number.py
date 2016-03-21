# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import simplegui

# defining global variables

no_of_guesses = 7 #this var holds the no of guesses used in the previous game so that the new game will have the same
no_of_guesses_left = 7
secret_number = 0
current_range = 100 #this var holds the range used in the previous game so that the new game will have the same

def new_game(range):
    """this function initializes the secret number for a new game 
    and changes number of guesses remaining to the req number"""
    
    global secret_number
    global no_of_guesses
    global no_of_guesses_left
    
    secret_number = random.randrange(0, range)
    
    no_of_guesses_left = no_of_guesses
    
    
# define event handlers for control panel

def range100():
    # button that changes the range to [0,100) and starts a new game 
    
    global no_of_guesses
    global current_range
    
    #changing range user wants to 100
    current_range = 100
    
    #changing no_of_guesses to required number
    no_of_guesses = 7
     
    print "-" * 50
    print
    print "The range has been changed to [0,100)"
    print
    print "Starting new game..."
    print
    print "-" * 50
    print
    
    # starting a new game and passing range into function
    new_game(current_range)    
    
def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global no_of_guesses
    global current_range
      
    #changing range user wants to 1000
    current_range = 1000
    
    #changing no_of_guesses to required number
    no_of_guesses = 10

    print "-" * 50
    print
    print "The range has been changed to [0,1000)"
    print
    print "Starting new game..."
    print
    print "-" * 50
    print
    
    # starting a new game and passing range into function
    new_game(current_range)
    
def input_guess(guess):
    # main game logic goes here	
    
    global no_of_guesses
    global secret_number
    global no_of_guesses_left
    
    guess_float = float(guess)
    
    print "You guessed " + guess
       
    if guess_float > secret_number:
        print "The computer's number is lower than your guess"
        no_of_guesses_left -= 1
        
    elif guess_float < secret_number:
        print "The computer's number is higher than your guess"
        no_of_guesses_left -= 1
        
    else:
        print "That is correct!"
        print
        print "Yay! You have won the game!"
        print
        print "Starting new game..."
        print
        print "-" * 50
        print
        
        # starting a new game with the current range
        new_game(current_range)
        
        
    if no_of_guesses_left == 0:
        print "Sorry, you have run out of guesses"
        print "The secret number was", secret_number
        print
        print "Starting new game..."
        print
        print "-" * 50
        print
        
        # changing no_of_guesses left back to req no
        no_of_guesses_left = no_of_guesses
        
        # starting a new game with the current range
        new_game(current_range)
        
    elif no_of_guesses_left == 1:
        # just to make output look more gramatically correct :)
        
        print "You have " + str(no_of_guesses_left) + " guess left"
        print "Please guess another number..."
        print
        
    elif not (no_of_guesses_left == no_of_guesses):
        # to catch the case where a new game was started in the previous if/else loop - in this case no message needs to be printed
        
        print "You have " + str(no_of_guesses_left) + " guesses left"
        print "Please guess another number..."
        print
              
# create frame

f = simplegui.create_frame('Guess the number', 200, 200)

# register event handlers for control elements and start frame

button_range_100 = f.add_button('Range is [0,100)', range100, 200)
button_range_1000 = f.add_button('Range is [0,1000)', range1000, 200)
user_guess_input = f.add_input('Enter a guess', input_guess, 200)

f.start()

# starting the first game with the initial range
new_game(100)
