# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (37, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
player_action = ""
wins = 0
losses = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.rank + self.suit

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], [73, 96])
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        
        self.cards = []
    
    def __str__(self):
        # return a string representation of a hand
        
        cards_str = ""
        
        for card in self.cards:
            cards_str += " " + str(card)
            
        return "Hand contains the cards" + cards_str
    
    def add_card(self, card):
        # add a card object to a hand
        
        self.cards.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        
        hand_val = 0
        num_aces = 0
        
        for card in self.cards:
            rank = card.get_rank()
            
            hand_val += VALUES[rank]
            if rank == "A":
                num_aces += 1
        
        if num_aces == 0:
            return hand_val
        else:
            if hand_val + 10 > 21:
                return hand_val
            else:
                return hand_val + 10
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        
        n = 0
        
        for card in self.cards:
            x_pos = pos[0] + n * 100
            y_pos = pos[1]
            card.draw(canvas, [x_pos, y_pos])
            
            n += 1

# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        
        self.cards = []
        
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
    
    def __str__(self):
        # return a string representing the deck
        
        cards_str = ""
        
        for card in self.cards:
            cards_str += " " + str(card)
            
        return "Deck contains the cards" + cards_str

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        
        card_dealt = random.choice(self.cards)
        self.cards.remove(card_dealt)
        
        return card_dealt

deck = Deck()
player_hand = None
dealer_hand = None

#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, deck, player_action, losses
    
    deck = Deck()    
    deck.shuffle()
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    if in_play:
        outcome = "You lose!"
        losses += 1
    else:
        outcome = ""
    
    player_action = "Hit or stand?"
    
    in_play = True

def hit():
    global in_play, outcome, player_action, losses
    
    # if thehand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
    
        if player_hand.get_value() > 21:
            outcome = "Busted! You lose!"
            in_play = False
            player_action = "New deal?"
            losses += 1
        else:
            outcome = ""
            
    elif player_hand.get_value() > 21:
        outcome = "You're already bust, buster"
        
    elif dealer_hand.get_value() >= player_hand.get_value():
        outcome = "You already lost, buster"
    
    else:
        outcome = "You've already won!"
       
def stand():
    global in_play, outcome, player_action, wins, losses
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        
        if dealer_hand.get_value() > 21:
            outcome = "The Dealer has bust! You win!"
            wins += 1
        else:
            if dealer_hand.get_value() >= player_hand.get_value():
                outcome = "Dealer wins!"
                losses += 1
            else:
                outcome = "You win!"
                wins += 1
                
    elif player_hand.get_value() > 21:
        outcome = "You're already bust, buster"
        
    elif dealer_hand.get_value() >= player_hand.get_value():
        outcome = "You already lost, buster"
    
    else:
        outcome = "You've already won"
    
    player_action = "New deal?"
    
    in_play = False

# draw handler    
def draw(canvas):
    
    canvas.draw_text("Blackjack", [60, 110], 40, "Yellow")
    canvas.draw_text("Dealer", [60, 200], 30, "Black")
    canvas.draw_text("Player", [60, 400], 30, "Black")
    canvas.draw_text(outcome, [210, 200], 30, "Black")
    canvas.draw_text(player_action, [210, 400], 30, "Black")
    canvas.draw_text("Wins: " + str(wins), [450, 90], 30, "Black")
    canvas.draw_text("Losses: " + str(losses), [432, 130], 30, "Black")
    
    dealer_hand.draw(canvas, [60, 240])
    player_hand.draw(canvas, [60, 440])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [60 + CARD_CENTER[0], 240 + CARD_CENTER[1]], [73, 96])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
