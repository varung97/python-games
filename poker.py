#starting bet is 20

import simplegui
import random
import math

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (37, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

CANVAS_SIZE = (1000, 600)

CARD_OFFSET = 50

TEXT_SIZE = 40

# initialize some useful global variables
player_action = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}

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

    def draw(self, canvas, pos, angle, is_open):
        if angle == 0:
            card_pos = [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]]
        elif angle == math.radians(90):
            card_pos = [pos[0] + CARD_CENTER[1], pos[1] + CARD_CENTER[0]]
        
        if is_open:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, card_pos, CARD_SIZE, angle)
        else:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, card_pos, CARD_SIZE, angle)

class Hand:
    def __init__(self):
        self.cards = []
    
    def __str__(self):
        cards_str = ""
        
        for card in self.cards:
            cards_str += " " + str(card)
            
        return "Hand contains the cards" + cards_str
    
    def add_card(self, card):
        self.cards.append(card)

    def draw(self, canvas, pos, angle, is_open):
        n = 0
        
        for card in self.cards:
            x_pos = pos[0] + math.cos(angle) * n * 100
            y_pos = pos[1] + math.sin(angle) * n * 100
            card.draw(canvas, [x_pos, y_pos], angle, is_open)
            
            n += 1
    
    def reset(self):
        self.cards = []

class Deck:
    def __init__(self):
        # create a Deck object
        self.all_cards = []
        
        for suit in SUITS:
            for rank in RANKS:
                self.all_cards.append(Card(suit, rank))
        
        self.cards = list(self.all_cards)
    
    def __str__(self):
        # return a string representing the deck
        
        cards_str = ""
        
        for card in self.cards:
            cards_str += " " + str(card)
            
        return "Deck contains the cards" + cards_str

    def shuffle(self):
        # shuffle the deck 
        
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        
        card_dealt = random.choice(self.cards)
        self.cards.remove(card_dealt)
        
        return card_dealt
    
    def reset(self):
        self.cards = list(self.all_cards)
        self.shuffle()

class Player:
    def __init__(self, player_number):
        self.money = 1000
        self.hand = Hand()
        self.hand_ranking = None
        self.check = None
        self.folded = False
        self.played = False
        self.number = player_number
        if self.number == 1:
            self.pos = [CANVAS_SIZE[0] / 2 - 86,
                        CARD_OFFSET]
            self.angle = 0
            self.money_pos = [CANVAS_SIZE[0] / 2 + 120,
                              CARD_OFFSET + 65]
        elif self.number == 2:
            self.pos = [CARD_OFFSET,
                        CANVAS_SIZE[1] / 2 - 86]
            self.angle = math.radians(90)
            self.money_pos = [CARD_OFFSET + 10,
                              CANVAS_SIZE[1] / 2 + 150]
        elif self.number == 3:
            self.pos = [CANVAS_SIZE[0] / 2 - 86,
                        CARD_OFFSET + CANVAS_SIZE[1] - CARD_OFFSET * 2 - CARD_SIZE[1]]
            self.angle = 0
            self.money_pos = [CANVAS_SIZE[0] / 2 + 120,
                              CANVAS_SIZE[1] - CARD_OFFSET - 31]
        elif self.number == 4:
            self.pos = [CARD_OFFSET + CANVAS_SIZE[0] - CARD_OFFSET * 2 - CARD_SIZE[1],
                        CANVAS_SIZE[1] / 2 - 86]
            self.angle = math.radians(90)
            self.money_pos = [CANVAS_SIZE[0] - CARD_OFFSET - 86,
                              CANVAS_SIZE[1] / 2 + 150]
        self.showdown = False
    
    def bet(self, amount):
        global bet_turn
        
        if self.money >= amount:
            self.money -= amount
            pot.bet(amount)
    
    def reset(self):
        self.hand.reset()
        self.hand_ranking = None
        self.check = None
        self.folded = False
        self.played = False
        self.showdown = False
    
    def has_played(self):
        self.played = True
    
    def folds(self):
        self.folded = True
    
    def new_round(self):
        if not self.folded:
            self.played = False
    
    def draw(self, canvas):
        if self.number == bet_turn + 1 or self.showdown:
            self.hand.draw(canvas, self.pos, self.angle, True)
        else:
            self.hand.draw(canvas, self.pos, self.angle, False)
        canvas.draw_text("$" + str(self.money), self.money_pos, TEXT_SIZE, "Yellow")
    
class Pot:
    def __init__(self):
        self.total_money = 0
        self.current_round_player_bets = [0 for a in range(len(players))]
        self.round_number = 0
        self.max_current_bet = 0
    
    def bet(self, amount):
        self.total_money += amount
        self.current_round_player_bets[bet_turn] += amount
        self.max_current_bet = max(self.current_round_player_bets)
    
    def new_round(self):
        self.current_round_player_bets = [0 for a in range(len(players))]
        self.round_number += 1
        self.max_current_bet = 0
    
    def reset(self):
        self.total_money = 0
        self.current_round_player_bets = [0 for a in range(len(players))]
        self.round_number = 0
        self.max_current_bet = 0

class Text:
    def __init__(self, text, y_pos, frame):
        self.text = text
        self.y_pos = y_pos
        self.text_pos = [0, 0]
        self.lifespan = None
        self.new_lifespan = None
        self.age = 0
        self.text_after_time_up = ''
    
    def decide_text_pos(self):
        text_length = frame.get_canvas_textwidth(self.text, TEXT_SIZE)
        self.text_pos = [CANVAS_SIZE[0] / 2 - text_length / 2, self.y_pos]
    
    def update_age(self):
        if self.lifespan:
            self.age += 1.0 / 60.0
            if self.age >= self.lifespan:
                self.replace_text(self.text_after_time_up)
    
    def replace_text(self, new_text, lifespan = None, text_after_time_up = ''):
        self.text = new_text
        self.decide_text_pos()
        self.lifespan = lifespan
        self.age = 0
        self.text_after_time_up = text_after_time_up
    
    def set_new_text(self, lifespan, new_text):
        self.lifespan = lifespan
        self.text_after_time_up = new_text
    
    def draw(self, canvas):
        canvas.draw_text(self.text, self.text_pos, TEXT_SIZE, "White")

def deal():
    global game_on
    
    for player in players:
        for a in range(2):
            player.hand.add_card(deck.deal_card())
    
    game_on = True

def deal_comm():
    if pot.round_number == 1:
        for i in range(3):
            community_cards.add_card(deck.deal_card())
    else:
        community_cards.add_card(deck.deal_card())
    
def check_pair(player_values, player_suits, player_cards):
    player_values = list(player_values) #to ensure values are not removed from the original list
    player_values.reverse() #to ensure largest pair found when checking for full house
    n = 1
    
    for value1 in player_values[:6]:
        for value2 in player_values[n:]:
            if value1 == value2:
                player_values.remove(value1)
                player_values.remove(value2) #removes these values from the list (value 1 could have been removed twice, but this makes code more readable)
                return True, [value1], player_values[:3]
        n += 1
    
    return False, None, None

def check_two_pair(player_values, player_suits, player_cards):
    player_values = list(player_values)
    player_values.reverse() #so that highest two pair is found
    n = 1
    num_pairs = 0
    pair_values = []
    
    for value1 in player_values[:6]:
        for value2 in player_values[n:]:
            if value1 == value2:
                num_pairs += 1
                pair_values.append(value1)
                if num_pairs == 2:
                    player_values.remove(pair_values[0])
                    player_values.remove(pair_values[0])
                    player_values.remove(pair_values[1])
                    player_values.remove(pair_values[1])
                    return True, pair_values, player_values[:1]
        n += 1
    
    return False, None, None

def check_three_of_a_kind(player_values, player_suits, player_cards, for_full_house=False):
    player_values = list(player_values)
    player_values.reverse() #so that highest triple is found
    n = 1
    
    for value1 in player_values[:5]:
        for value2 in player_values[n:6]:
            for value3 in player_values[n+1:7]:
                if value1 == value2 and value1 == value3:
                    player_values.remove(value1)
                    player_values.remove(value2)
                    player_values.remove(value3)
                    if for_full_house:
                        return True, [value1], player_values
                    else:
                        return True, [value1], player_values[:2]
        n += 1
    
    return False, None, None

def check_straight(player_values, player_suits, player_cards):
    player_values = list(player_values)
    player_values.reverse() #so that highest straight is found
    
    if 14 in player_values:
        player_values = [1] + player_values
    
    #strip player_values of duplicate vals
    stripped_vals = []
    
    for a in player_values:
        if a not in stripped_vals:
            stripped_vals.append(a)
    
    if len(stripped_vals) >= 5: #catching case where stripped_vals is too small
        for n in range(len(stripped_vals) - 4):
            sequence_counter = 0
            for a in range(n, n + 4):
                if stripped_vals[a] - 1 == stripped_vals[a+1]:
                    sequence_counter += 1
            if sequence_counter == 4:
                return True, [stripped_vals[a-3]], [None] #gives highest value in straight
    
    return False, None, None

def check_flush(player_values, player_suits, player_cards):
    if player_suits.count('C') >= 5:
        flush_suit = 'C'
    elif player_suits.count('D') >= 5:
        flush_suit = 'D'
    elif player_suits.count('H') >= 5:
        flush_suit = 'H'
    elif player_suits.count('S') >= 5:
        flush_suit = 'S'
    else:
        return False, None, None
    
    same_suit_values = [VALUES[card.get_rank()] for card in player_cards if card.get_suit() == flush_suit]
    same_suit_values.sort()
    same_suit_values.reverse()
    
    return True, same_suit_values[-5:], [None]

def check_full_house(player_values, player_suits, player_cards):
    player_values = list(player_values)
    
    is_triple, triple_val, remaining_cards = check_three_of_a_kind(player_values, player_suits, player_cards, True)
    
    if is_triple:
        remaining_cards.reverse()
        has_pair, pair_val, discard = check_pair(remaining_cards, player_suits, player_cards)
        if has_pair:
            return True, [triple_val], [pair_val]
    
    return False, None, None

def check_four_of_a_kind(player_values, player_suits, player_cards):
    player_values = list(player_values)
    player_values.reverse() #to ensure consistency with other functions
    n = 1
    
    for value1 in player_values[:4]:
        for value2 in player_values[n:5]:
            for value3 in player_values[n+1:6]:
                for value4 in player_values[n+2:7]:
                    if value1 == value2 and value1 == value3 and value1 == value4:
                        player_values.remove(value1)
                        player_values.remove(value2)
                        player_values.remove(value3)
                        player_values.remove(value4)
                        return True, [value1], player_values[:1]
        n += 1
    
    return False, None, None

def check_straight_flush(player_values, player_suits, player_cards):
    
    is_flush, same_suit_values = check_flush(player_values, player_suits, player_cards)
    
    if is_flush:
        is_straight, highest_val = check_straight(same_suit_values, player_suits, player_cards)
        if is_straight:
            return True, [highest_val], [None]
    
    return False, None, None

check_functions = [check_straight_flush,
                   check_four_of_a_kind,
                   check_full_house,
                   check_flush,
                   check_straight,
                   check_three_of_a_kind,
                   check_two_pair,
                   check_pair]

hand_rankings = ['Straight flush',
                 'Four of a kind',
                 'Full house',
                 'Flush',
                 'Straight',
                 'Three of a kind',
                 'Two Pair',
                 'Pair',
                 'High card']

def check_hand(hand):
    player_cards = []
    player_cards.extend([card for card in hand.cards])
    player_cards.extend([card for card in community_cards.cards])
    
    player_suits = [card.get_suit() for card in player_cards]
    player_values = [VALUES[card.get_rank()] for card in player_cards]
    
    player_values.sort()
    
    got_sequence = False
    b = -1
    
    while not got_sequence:
        b += 1
        if b <= 7:
            got_sequence, check1, check2 = check_functions[b](player_values, player_suits, player_cards)
        else:
            player_values.reverse()
            got_sequence, check1, check2 = True, player_values[:5], [None]
    
    return hand_rankings[b], check1, check2

def check_higher(players_with_highest_rank, player_list):
    if players_with_highest_rank[0].check[-1] == None:
        for player in players_with_highest_rank:
            player.check.pop()
    
    players_with_same_hand = list(players_with_highest_rank) #contains list of all players who have same hand as far as computer has checked
    winners = [players_with_highest_rank[0]] #assumption made for first comparison
    player_won = False #whether a player has won or not
    check_val_number = 0 #which check value is being compared
    
    while not player_won:
        for a in range(1, len(players_with_same_hand)):
            if winners[0].check[check_val_number] > players_with_highest_rank[a].check[check_val_number]:
                winners = [winners[0]]
            elif winners[0].check[check_val_number] < players_with_highest_rank[a].check[check_val_number]:
                winners = [players_with_highest_rank[a]]
            else:
                if players_with_highest_rank[a] not in winners:
                    winners.append(players_with_highest_rank[a])
        
        if len(winners) == 1:
            player_won = True
        
        for player in list(players_with_same_hand):
            if player not in winners:
                players_with_same_hand.remove(player)
        
        check_val_number += 1
        
        if check_val_number == len(players_with_highest_rank[0].check):
            player_won = True
        
    return winners

def compare_hands(player_list):
    players_playing_list = [player for player in player_list if not player.folded]
    
    for player in players_playing_list:
        player.hand_ranking, check_1, check_2 = check_hand(player.hand)
        player.check = check_1 + check_2
    
    players_with_highest_rank = [players_playing_list[0]] #for now, this player is assumed to have best hand
    
    for a in range(1, len(players_playing_list)):
        if hand_rankings.index(players_with_highest_rank[0].hand_ranking) < hand_rankings.index(players_playing_list[a].hand_ranking): #since hand_rankings are in reverse order
            pass
        elif hand_rankings.index(players_with_highest_rank[0].hand_ranking) > hand_rankings.index(players_playing_list[a].hand_ranking):
            players_with_highest_rank = [players_playing_list[a]]
        else:
            players_with_highest_rank.append(players_playing_list[a])
    
    if len(players_with_highest_rank) == 1:
        return players_with_highest_rank
    else:
        return check_higher(players_with_highest_rank, player_list)

def new_hand():
    global bet_turn
    
    deck.reset()
    community_cards.reset()
    for player in players:
        player.reset()
    pot.reset()
    text_set[0].replace_text("Player 1 Turn")
    text_set[1].replace_text("")
    
    bet_turn = 0
    
    deal()

def increment_bet_turn():
    global bet_turn
    
    bet_turn += 1
    
    circle_back_to_first_player()
    
    while players[bet_turn].folded:
        bet_turn += 1
        circle_back_to_first_player()
    
    text_set[0].replace_text("Player " + str(bet_turn + 1) + " Turn")

def circle_back_to_first_player():
    global bet_turn
    
    if bet_turn == len(players):
        bet_turn = 0

def is_round_over():
    over = True
    
    for player in players:
        if not player.played:
            over = False
        elif pot.current_round_player_bets[player.number - 1] < pot.max_current_bet and \
             not player.folded:
                over = False
    
    if over:
        if pot.round_number < 3:
            text_set[0].replace_text("",
                                     0.5,
                                     "This round of betting is over")
            text_set[1].set_new_text(1.0,
                                     "Starting new round...")
            new_round_timer.start()
        else:
            text_set[0].replace_text("",
                                     0.5,
                                     "This hand is over")
            text_set[1].set_new_text(1.0,
                                     "It is now time for the showdown!")
            for player in players:
                player.showdown = True
            showdown_timer.start()

def new_round():
    global bet_turn
    
    new_round_timer.stop()
    
    pot.new_round()
    for player in players:
        player.new_round()
    
    bet_turn = -1 #so that it becomes 0 in increment_bet_turn
    increment_bet_turn()
    
    text_set[1].replace_text("")
    
    deal_comm()

def showdown():
    global game_on
    
    showdown_timer.stop()
    
    winners = compare_hands(players)
    if len(winners) == 1:
        text_set[0].replace_text("Winner is Player " + str(winners[0].number))
        text_set[1].replace_text("He wins $" + str(pot.total_money))
    else:
        text_set[0].replace_text("It's a draw!",
                                 0.8,
                                 "Winners are Players " + " and ".join([player.number for player in winners]))
        text_set[0].replace_text("",
                                 0.8,
                                 "They win $" + str(pot.total_money // len(winners)) + " each")
    
    for player in players:
        if player in winners:
            player.money += pot.total_money // len(winners)
    
    pot.total_money = 0
    
    game_on = False

def check_handler():
    global bet_turn
    
    if game_on:
        if pot.max_current_bet == 0:
            text_set[1].replace_text("Player " + str(players[bet_turn].number) + " checks")
            players[bet_turn].has_played()
            increment_bet_turn()
        else:
            text_set[1].replace_text("Cannot Check!")
        
        is_round_over()

def bet_handler():
    global amount, bet_turn
    
    if game_on:
        if pot.max_current_bet == 0 and amount > 0:
            text_set[1].replace_text("Player " + str(players[bet_turn].number) + " bets $" + str(amount))
            players[bet_turn].bet(amount)
            players[bet_turn].has_played()
            increment_bet_turn()
        elif pot.max_current_bet != 0:
            text_set[1].replace_text("You have to either Call, Raise or Fold!")
        else:
            text_set[1].replace_text("You must enter an amount to Bet")
        
        amount = 0
        
        is_round_over()

def call_handler():
    global bet_turn
    
    if game_on:
        if pot.max_current_bet > 0:
            text_set[1].replace_text("Player " + str(players[bet_turn].number) + " calls $" + str(pot.max_current_bet))
            players[bet_turn].bet(pot.max_current_bet - pot.current_round_player_bets[bet_turn])
            players[bet_turn].has_played()
            increment_bet_turn()
        else:
            text_set[1].replace_text("You have to either Check, Bet or Fold!")
        
        is_round_over()

def raise_handler():
    global amount, bet_turn
    
    if game_on:
        if pot.max_current_bet > 0 and amount > 0:
            text_set[1].replace_text("Player " + str(players[bet_turn].number) + " calls $" + str(pot.max_current_bet) \
                                     + " and raises $" + str(amount))
            players[bet_turn].bet(pot.max_current_bet + amount - pot.current_round_player_bets[bet_turn])
            players[bet_turn].has_played()
            increment_bet_turn()
        elif amount <= 0:
            text_set[1].replace_text("You must enter an amount to Raise")
        else:
            text_set[1].replace_text("You have to either Check, Bet or Fold!")
        
        amount = 0
        
        is_round_over()

def fold_handler():
    global bet_turn, game_on
    
    if game_on:
        text_set[1].replace_text("Player " + str(players[bet_turn].number) + " folds")
        players[bet_turn].folds()
        players[bet_turn].has_played()
        
        number_of_players_folded = 0
        for player in players:
            if player.folded:
                number_of_players_folded += 1
        
        if number_of_players_folded == len(players) - 1:
            player_not_folded = None
            for player in players:
                if not player.folded:
                    player_not_folded = player
            
            text_set[0].replace_text("Player " + str(player_not_folded.number) + " is the only one left!",
                                     1,
                                     "This player automatically wins this round!")
            text_set[1].replace_text("Player " + str(players[bet_turn].number) + " folds",
                                     1.2,
                                     "Player " + str(player_not_folded.number) + " wins $" + str(pot.total_money))
            
            player_not_folded.money += pot.total_money
            pot.total_money = 0
            
            game_on = False
        else:
            increment_bet_turn()
            is_round_over()

def input_handler(text):
    global amount
    
    if int(text) % 20 == 0:
        amount = int(text)
    else:
        text_set[1].replace_text("You must bet in multiples of 20")

def draw(canvas):
    for player in players:
        player.draw(canvas)
    
    community_cards.draw(canvas, [CANVAS_SIZE[0] / 2 - 200 - CARD_SIZE[0] / 2, CANVAS_SIZE[1] / 2 - CARD_SIZE[1] / 2], 0, True)
    
    for text in set(text_set):
        text.update_age()
        text.draw(canvas)
    
    canvas.draw_text("Pot: $" + str(pot.total_money), [50, 100], 50, "Yellow")

# initialization frame
frame = simplegui.create_frame("Poker", CANVAS_SIZE[0], CANVAS_SIZE[1])
frame.set_canvas_background("#9932CC")
frame.add_button("New Hand", new_hand, 100)
frame.add_label('')
frame.add_button("Check", check_handler, 100)
frame.add_label('')
frame.add_button("Bet", bet_handler, 100)
frame.add_label('')
frame.add_button("Call", call_handler, 100)
frame.add_label('')
frame.add_button("Raise", raise_handler, 100)
frame.add_label('')
frame.add_button("Fold", fold_handler, 100)
frame.add_label('')
frame.add_input("Bet money", input_handler, 50)

#create buttons and canvas callback
frame.set_draw_handler(draw)
new_round_timer = simplegui.create_timer(2000, new_round)
showdown_timer = simplegui.create_timer(4000, showdown)

# get things rolling
deck = Deck()
community_cards = Hand()
players = [Player(1), Player(2)]
pot = Pot()
amount = 0
bet_turn = 0
text_set = [Text("", 210, frame), Text("", 425, frame)]
text_set[0].replace_text("Player 1 Turn")
game_on = False

deal()

frame.start()
