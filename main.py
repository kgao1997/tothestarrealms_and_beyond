class Ship: #initialize card parameters for ship type cards
    #possibly can unify card_trade, card_combat into the play_function
    def __init__(self, play_function, discard_function, card_cost = 0, card_name = "default card name", card_faction = "unaligned", card_description = "default description"):
        #The default init will make a card with the functions as given
        #play_function: takes a current player_state as input, outputs a player_state
        self.discard_function = discard_function #discard function to be implemented when card is dusted
        self.play_function = play_function #function to be applied when card is played
        self.card_cost = card_cost #amount of trade needed to acquire card
        self.card_name = card_name
        self.card_faction = card_faction
        self.card_description = card_description
        #self.card_combat = card_combat #amount of combat card yields when played
        #self.card_trade = card_trade #amount of trade card yields when played

class Base: #initialize card parameters for a base
    def __init__(self, turn_function, discard_function, card_cost = 0, card_name = "default name", card_faction = "unaligned", card_description = "default_description", card_shields = 0):
        self.turn_function = turn_function #turn function is the effect that you get when played, and the function that is applied each turn
        self.discard_function = discard_function #card function called when card is discarded from the board
        self.card_cost = card_cost
        self.card_faction = card_faction
        self.card_description = card_description
        self.card_shields = card_shields #default to zero for passable shields

class Landscape: #initialize card_parameters for landscape cards
    def __init__(self, act_function, discard_function, card_cost = 0, card_name = "default name", card_faction = "unaligned", card_description = "default description", card_shield = 0):
        self.act_function = act_function #function that is called as the turn activation for landscapes
        self.discard_function = discard_function #function called when card is discarded
        self.card_cost = card_cost
        self.card_name = card_name
        self.card_faction = card_faction
        self.card_description = card_description
        self.card_shield = card_shield
    

class Player:
    def __init__(self):
        self.authority = 50
        self.deck = []
        self.in_play = []
        self.combat = 0
        self.trade = 0
        self.discard = []

class Game: 
    def __init__(self):
        self.current_player = 1
        self.trade_row = []
        self.deck = [] #deck of all cards to be drawn from
        #For this game we will implement the digital version with infinite explorer cards