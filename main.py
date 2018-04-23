from enum import Enum

# all ship and outpost factions
class Faction(Enum):
    UNALIGNED = 1
    BLOB = 2
    TRADE_FED = 3
    MACH_CULT = 4
    STAR_EMP = 5
    ALL = 6

# all possible functions
class FuncName(Enum):
    ADD_TRADE = 1
    ADD_COMBAT = 2
    DRAW_CARDS = 3
    SCRAP_TRADE_ROW = 4
    DESTROY_BASE = 5
    ACQUIRE_FREE_SHIP = 6  # should also add to top of deck
    SHIP_TO_TOP_DECK = 7
    DRAW_CARD_BLOB = 8
    ADD_INFL = 9
    DRAW_CARDS_IF_BASE = 10
    SCRAP_HAND_DISC = 11
    COPY_SHIP = 12
    DRAW_THEN_SCRAP = 13
    SCRAP_THEN_DRAW = 14
    OPP_DISCARD = 15
    DISC_THEN_DRAW = 16
    SHIP_POWERUP = 17
    AND = 18  # two functions can be applied
    OR = 19  # one of two functions can be applied
    NONE = 20

class Function:
    def __init__(self, func_name, effect = 0, func1 = None, func2 = None, func3 = None):
        self.function_name = func_name # should be from the FuncName enum
        self.effect = effect # int to be used when a function needs to be described by a number
        self.func1 = func1  # two-three functions are stored here for AND and OR
        self.func2 = func2
        self.func3 = func3


class Ship: #initialize card parameters for ship type cards
    #possibly can unify card_trade, card_combat into the play_function
    def __init__(self, play_function, discard_function = Function(FuncName.NONE), faction_function = Function(FuncName.NONE), card_cost = 0, card_name = "default card name", card_faction = Faction.UNALIGNED, card_description = "default description"):
        #The default init will make a card with the functions as given
        #play_function: takes a current player_state as input, outputs a player_state
        self.discard_function = discard_function #discard function to be implemented when card is dusted
        self.play_function = play_function #function to be applied when card is played
        self.faction_function = faction_function #function to be applied for faction bonus
        self.card_cost = card_cost #amount of trade needed to acquire card
        self.card_name = card_name
        self.card_faction = card_faction
        self.card_description = card_description
        #self.card_combat = card_combat #amount of combat card yields when played
        #self.card_trade = card_trade #amount of trade card yields when played

class Base: #initialize card parameters for a base
    def __init__(self, turn_function, discard_function = Function(FuncName.NONE), faction_function = Function(FuncName.NONE), card_cost = 0, card_name = "default name", card_faction = Faction.UNALIGNED, card_description = "default_description", card_shield = 0):
        self.play_function = turn_function #turn function is the effect that you get when played, and the function that is applied each turn
        self.discard_function = discard_function #card function called when card is discarded from the board
        self.faction_function = faction_function #function to be applied (per turn) for faction bonus
        self.card_name = card_name
        self.card_cost = card_cost
        self.card_faction = card_faction
        self.card_description = card_description
        self.card_shields = card_shield #default to zero for passable shields

class Landscape: #initialize card_parameters for landscape cards
    def __init__(self, act_function, discard_function = Function(FuncName.NONE), faction_function = Function(FuncName.NONE), card_cost = 0, card_name = "default name", card_faction = Faction.UNALIGNED, card_description = "default description", card_shield = 0):
        self.play_function = act_function #function that is called as the turn activation for landscapes
        self.discard_function = discard_function #function called when card is discarded
        self.faction_function = faction_function #function to be applied (per turn) for faction bonus
        self.card_cost = card_cost
        self.card_name = card_name
        self.card_faction = card_faction
        self.card_description = card_description
        self.card_shield = card_shield
    
# defining all cards
scout = Ship(Function(FuncName.ADD_TRADE, effect=1), card_name = 'Scout', card_faction = Faction.UNALIGNED)
viper = Ship(Function(FuncName.ADD_COMBAT, effect=1), card_name = 'Viper', card_faction = Faction.UNALIGNED)
explorer = Ship(Function(FuncName.ADD_TRADE, effect=2), discard_function = Function(FuncName.ADD_COMBAT, 2), card_cost = 2, card_name = 'Explorer', card_faction = Faction.UNALIGNED)

blob_fighter = Ship(Function(FuncName.ADD_COMBAT, effect=3), faction_function=Function(FuncName.DRAW_CARDS, effect=1), card_cost = 1, card_name = 'Blob Fighter', card_faction = Faction.BLOB)
battle_pod = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_COMBAT, effect=4), func2=Function(FuncName.SCRAP_TRADE_ROW, effect=1)), faction_function=Function(FuncName.ADD_COMBAT, effect=2), card_cost = 2, card_name = 'Battle Pod', card_faction = Faction.BLOB)
trade_pod = Ship(Function(FuncName.ADD_TRADE, effect=3), faction_function=Function(FuncName.ADD_COMBAT, effect=2), card_cost = 2, card_name = 'Trade Pod', card_faction = Faction.BLOB)
blob_wheel = Landscape(Function(FuncName.ADD_COMBAT, effect=1), discard_function=Function(FuncName.ADD_TRADE, effect=3), card_cost=3, card_name='Blob Wheel', card_faction=Faction.BLOB, card_shield=5)
ram = Ship(Function(FuncName.ADD_COMBAT, effect=5), faction_function=Function(FuncName.ADD_COMBAT, effect=2), discard_function=Function(FuncName.ADD_TRADE, effect=3), card_cost = 3, card_name = 'Ram', card_faction = Faction.BLOB)
blob_destroyer = Ship(Function(FuncName.ADD_COMBAT, effect=6), faction_function=Function(FuncName.AND, func1=Function(FuncName.DESTROY_BASE), func2=Function(FuncName.SCRAP_TRADE_ROW, effect=1)), card_cost = 4, card_name = 'Blob Destroyer', card_faction = Faction.BLOB)
the_hive = Landscape(Function(FuncName.ADD_COMBAT, effect=3), faction_function=Function(FuncName.DRAW_CARDS, effect=1), card_cost=5, card_name='The Hive', card_faction=Faction.BLOB, card_shield=5)
battle_blob = Ship(Function(FuncName.ADD_COMBAT, effect=8), faction_function=Function(FuncName.DRAW_CARDS, effect=1), discard_function=Function(FuncName.ADD_COMBAT, effect=4), card_cost = 6, card_name = 'Battle Blob', card_faction = Faction.BLOB)
blob_carrier = Ship(Function(FuncName.ADD_COMBAT, effect=7), faction_function=Function(FuncName.ACQUIRE_FREE_SHIP), card_cost = 6, card_name = 'Blob Carrier', card_faction = Faction.BLOB)
mothership = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_COMBAT, effect=5), func2=Function(FuncName.DRAW_CARDS, effect=1)), faction_function=Function(FuncName.DRAW_CARDS, effect=1), card_cost = 7, card_name = 'Mothership', card_faction = Faction.BLOB)
blob_world = Landscape(Function(FuncName.OR, func1 = Function(FuncName.ADD_COMBAT, effect=5), func2 = Function(FuncName.DRAW_CARD_BLOB)), card_cost=8, card_name='Blob World', card_faction=Faction.BLOB, card_shield=7)

federation_shuttle = Ship(Function(FuncName.ADD_TRADE, effect=2), faction_function=Function(FuncName.ADD_INFL, effect=4), card_cost = 1, card_name = 'Federation Shuttle', card_faction = Faction.TRADE_FED)
cutter = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_TRADE, effect=2), func2=Function(FuncName.ADD_INFL, effect=4)), faction_function=Function(FuncName.ADD_COMBAT, effect=4), card_cost = 2, card_name = 'Cutter', card_faction = Faction.TRADE_FED)
embassy_yacht = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_INFL, effect=3), func2=Function(FuncName.ADD_TRADE, effect=2), func3=Function(FuncName.DRAW_CARDS_IF_BASE)), card_cost = 3, card_name = 'Embassy Yacht', card_faction = Faction.TRADE_FED)
trading_post = Base(Function(FuncName.OR, func1 = Function(FuncName.ADD_INFL, effect=1), func2 = Function(FuncName.ADD_TRADE, effect=1)), discard_function=Function(FuncName.ADD_COMBAT, effect=3), card_cost=3, card_name = 'Trading Post', card_faction=Faction.TRADE_FED, card_shield=4)
barter_world = Landscape(Function(FuncName.OR, func1 = Function(FuncName.ADD_INFL, effect=2), func2 = Function(FuncName.ADD_TRADE, effect=2)), discard_function=Function(FuncName.ADD_COMBAT, effect=5), card_cost=4, card_name = 'Barter World', card_faction=Faction.TRADE_FED, card_shield=4)
freighter = Ship(Function(FuncName.ADD_TRADE, effect=4), faction_function=Function(FuncName.SHIP_TO_TOP_DECK), card_cost = 4, card_name = 'Freighter', card_faction = Faction.TRADE_FED)
defense_center = Base(Function(FuncName.OR, func1 = Function(FuncName.ADD_INFL, effect=3), func2 = Function(FuncName.ADD_COMBAT, effect=2)), faction_function=Function(FuncName.ADD_COMBAT, effect=2), card_cost=5, card_name = 'Defense Center', card_faction=Faction.TRADE_FED, card_shield=5)
trade_escort = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_COMBAT, effect=4), func2=Function(FuncName.ADD_INFL, effect=4)), faction_function=Function(FuncName.DRAW_CARDS, effect=1), card_cost = 5, card_name = 'Trade Escort', card_faction = Faction.TRADE_FED)
flagship = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_COMBAT, effect=5), func2=Function(FuncName.DRAW_CARDS, effect=1)), faction_function=Function(FuncName.ADD_INFL, effect=5), card_cost = 6, card_name = 'Flagship', card_faction = Faction.TRADE_FED)
port_of_call = Base(Function(FuncName.ADD_TRADE, effect=1), discard_function=Function(FuncName.AND, func1=Function(FuncName.DRAW_CARDS, effect=1), func2=Function(FuncName.DESTROY_BASE)), card_cost=6, card_name = 'Port of Call', card_faction=Faction.TRADE_FED, card_shield=6)
central_office = Landscape(Function(FuncName.AND, func1 = Function(FuncName.ADD_TRADE, effect=2), func2 = Function(FuncName.SHIP_TO_TOP_DECK)), faction_function=Function(FuncName.DRAW_CARDS, effect=1), card_cost=7, card_name = 'Central Office', card_faction=Faction.TRADE_FED, card_shield=6)
command_ship = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_INFL, effect=4), func2=Function(FuncName.ADD_COMBAT, effect=5), func3=Function(FuncName.DESTROY_BASE)), card_cost = 8, card_name = 'Command Ship', card_faction = Faction.TRADE_FED)

trade_bot = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_TRADE, effect=1), func2=Function(FuncName.SCRAP_HAND_DISC, effect=1)), faction_function=Function(FuncName.ADD_COMBAT, effect=2), card_cost = 1, card_name = 'Trade Bot', card_faction = Faction.MACH_CULT)
missile_bot = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_COMBAT, effect=2), func2=Function(FuncName.SCRAP_HAND_DISC, effect=1)), faction_function=Function(FuncName.ADD_COMBAT, effect=2), card_cost = 2, card_name = 'Missile Bot', card_faction = Faction.MACH_CULT)
battle_station = Base(Function(FuncName.NONE), discard_function=Function(FuncName.ADD_COMBAT, effect=5), card_cost=3, card_name='Battle Station', card_faction = Faction.MACH_CULT, card_shield=5)
supply_bot = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_TRADE, effect=2), func2=Function(FuncName.SCRAP_HAND_DISC, effect=1)), faction_function=Function(FuncName.ADD_COMBAT, effect=2), card_cost = 3, card_name = 'Supply Bot', card_faction = Faction.MACH_CULT)
patrol_mech = Ship(Function(FuncName.OR, func1=Function(FuncName.ADD_TRADE, effect=3), func2=Function(FuncName.ADD_COMBAT, effect=5)), faction_function=Function(FuncName.SCRAP_HAND_DISC, effect=1), card_cost = 4, card_name = 'Patrol Mech', card_faction = Faction.MACH_CULT)
stealth_needle = Ship(Function(FuncName.COPY_SHIP), card_cost=4, card_name='Stealth Needle', card_faction=Faction.MACH_CULT)
battle_mech = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_COMBAT, effect=4), func2=Function(FuncName.SCRAP_HAND_DISC, effect=1)), faction_function=Function(FuncName.DRAW_CARDS, effect=1), card_cost = 5, card_name = 'Battle Mech', card_faction = Faction.MACH_CULT)
missile_mech = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_COMBAT, effect=6), func2=Function(FuncName.DESTROY_BASE)), faction_function=Function(FuncName.DRAW_CARDS, effect=1), card_cost = 6, card_name = 'Missile Mech', card_faction = Faction.MACH_CULT)
mech_world = Base(Function(FuncName.NONE), card_cost=5, card_name='Mech World', card_faction = Faction.ALL, card_shield=6)
junkyard = Base(Function(FuncName.SCRAP_HAND_DISC, effect=1), card_cost=6, card_name='Junkyard', card_faction = Faction.MACH_CULT, card_shield=5)
machine_base = Base(Function(FuncName.DRAW_THEN_SCRAP, effect=1), card_cost=7, card_name='Machine Base', card_faction = Faction.MACH_CULT, card_shield=6)
brain_world = Base(Function(FuncName.SCRAP_THEN_DRAW, effect=2), card_cost=8, card_name='Brain World', card_faction = Faction.MACH_CULT, card_shield=6)

imperial_fighter = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_COMBAT, effect=2), func2=Function(FuncName.OPP_DISCARD, effect=1)), faction_function=Function(FuncName.ADD_COMBAT, effect=2), card_cost = 1, card_name = 'Imperial Fighter', card_faction = Faction.STAR_EMP)
corvette = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_COMBAT, effect=1), func2=Function(FuncName.DRAW_CARDS, effect=1)), faction_function=Function(FuncName.ADD_COMBAT, effect=2), card_cost = 2, card_name = 'Corvette', card_faction = Faction.STAR_EMP)
imperial_frigate = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_COMBAT, effect=4), func2=Function(FuncName.OPP_DISCARD, effect=1)), faction_function=Function(FuncName.ADD_COMBAT, effect=2), discard_function=Function(FuncName.DRAW_CARDS, effect=1), card_cost = 3, card_name = 'Imperial Frigate', card_faction = Faction.STAR_EMP)
survey_ship = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_TRADE, effect=1), func2=Function(FuncName.DRAW_CARDS, effect=1)), discard_function=Function(FuncName.OPP_DISCARD, effect=1), card_cost = 3, card_name = 'Survey Ship', card_faction = Faction.STAR_EMP)
battlecruiser = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_COMBAT, effect=5), func2=Function(FuncName.DRAW_CARDS, effect=1)), faction_function=Function(FuncName.OPP_DISCARD, effect=1), discard_function=Function(FuncName.AND, func1=Function(FuncName.DRAW_CARDS, effect=1), func2=Function(FuncName.DESTROY_BASE)), card_cost = 6, card_name = 'Battlecruiser', card_faction = Faction.STAR_EMP)
dreadnaught = Ship(Function(FuncName.AND, func1=Function(FuncName.ADD_COMBAT, effect=7), func2=Function(FuncName.DRAW_CARDS, effect=1)), faction_function=Function(FuncName.ADD_COMBAT, effect=5), card_cost = 7, card_name = 'Dreadnaught', card_faction = Faction.STAR_EMP)
recycling_station = Base(Function(FuncName.OR, func1=Function(FuncName.ADD_TRADE, effect=1), func2=Function(FuncName.DISC_THEN_DRAW, effect=2)), card_cost=4, card_name='Recycling Station', card_faction=Faction.STAR_EMP, card_shield=4)
space_station = Base(Function(FuncName.ADD_COMBAT, effect=2), faction_function=Function(FuncName.ADD_COMBAT, effect=2), discard_function=Function(FuncName.ADD_TRADE, effect=4), card_cost=4, card_name='Space Station', card_faction=Faction.STAR_EMP, card_shield=4)
war_world = Base(Function(FuncName.ADD_COMBAT, effect=3), faction_function=Function(FuncName.ADD_COMBAT, effect=4), card_cost=5, card_name='War World', card_faction=Faction.STAR_EMP, card_shield=4)
royal_redoubt = Base(Function(FuncName.ADD_COMBAT, effect=3), faction_function=Function(FuncName.OPP_DISCARD, effect=1), card_cost=6, card_name='Royal Redoubt', card_faction=Faction.STAR_EMP, card_shield=6)
fleet_hq = Landscape(Function(FuncName.SHIP_POWERUP, effect=1), card_cost=8, card_name='Fleet HQ', card_faction=Faction.STAR_EMP, card_shield=9)


class Player:
    def __init__(self, authority = 50, deck = [], in_play = [], hand = [], combat = 0, trade = 0, discard = 0):
        self.authority = authority
        self.deck = deck
        self.in_play = in_play  # includes cards played this turn and all active bases
        self.hand = hand
        self.combat = combat
        self.trade = trade
        self.discard = discard


class Game: 
    def __init__(self, curr_player = 0, player_list = [], trade_row = [], deck = []):
        self.current_player = curr_player
        self.player_list = player_list
        self.trade_row = trade_row
        self.deck = deck #deck of all cards to be drawn from
        #For this game we will implement the digital version with infinite explorer cards

# all possible actions
class ActName(Enum):
    PLAY_CARD = 1
    BUY_CARD = 2
    ATTACK = 3
    SCRAP_EFFECT = 4 # scrapping a played card for the discard_effect
    SCRAP_TRADE_ROW = 5
    DESTROY_BASE = 6
    ACQUIRE_FREE_SHIP = 7
    ACTIVATE_EFFECT = 8 # for activating between a choice of effects, or activating an optional effect
    SCRAP_HAND_DISC = 9
    COPY_SHIP = 10
    SCRAP_HAND = 11
    DISCARD_HAND = 12
    END_TURN = 13

class Action:
    def __init__(self, act_name, target = None):
        self.action_name = act_name # from ActName enum
        self.target = target # for when an action requires targetting a card

# true if player has a base in play
def has_base(player):
    val = False
    for card in player.in_play:
        if isinstance(card, Base):
            val = True
    return val

# return bools (blob, trade, mach, star), each true if there is a faction bonus for the faction (i.e. >1 cards in play)
def faction_bonus(player):
    blob_num = 0
    trade_num = 0
    mach_num = 0
    star_num = 0
    for card in player.in_play:
        if card.card_faction == Faction.BLOB or card.card_faction == Faction.ALL: 
            blob_num = blob_num + 1
        if card.card_faction == Faction.TRADE_FED or card.card_faction == Faction.ALL:
            trade_num = trade_num + 1
        if card.card_faction == Faction.MACH_CULT or card.card_faction == Faction.ALL:
            mach_num = mach_num + 1
        if card.card_faction == Faction.STAR_EMP or card.card_faction == Faction.ALL:
            star_num = star_num + 1
    blob_bonus = False
    trade_bonus = False
    mach_bonus = False
    star_bonus = False
    if blob_num > 1:
        blob_bonus = True
    if trade_num > 1:
        trade_bonus = True
    if mach_num > 1:
        mach_bonus = True
    if star_num > 1:
        star_bonus = True
    return (blob_bonus, trade_bonus, mach_bonus, star_bonus)

# return a list of valid functions, given a player state (not including scrap effects)
def valid_functions(player):
    (blob_bonus, trade_bonus, mach_bonus, star_bonus) = faction_bonus(player)
    valid_functions = []
    for card in player.in_play:
        if card.play_function.function_name != FuncName.NONE:
            valid_functions.append(card.play_function)
        if card.play_function.func1 is not None:
            valid_functions.append(card.play_function.func1)
        if card.play_function.func2 is not None:
            valid_functions.append(card.play_function.func2)
        if card.play_function.func3 is not None:
            valid_functions.append(card.play_function.func3)
        if (card.card_faction == Faction.BLOB and blob_bonus) or (card.card_faction == Faction.TRADE_FED and trade_bonus) or (card.card_faction == Faction.MACH_CULT and mach_bonus) or (card.card_faction == Faction.STAR_EMP and star_bonus):
            if card.faction_function.function_name != FuncName.NONE:
                valid_functions.append(card.faction_function)
            if card.faction_function.func1 is not None:
                valid_functions.append(card.faction_function.func1)
            if card.faction_function.func2 is not None:
                valid_functions.append(card.faction_function.func2)
            if card.faction_function.func3 is not None:
                valid_functions.append(card.faction_function.func3)
    #for f in valid_functions:
    #    print (f.function_name, f.effect)
    return valid_functions

# given a game state, list the possible actions of the current player
def list_actions(state):
    curr_player = state.player_list[state.current_player]
    opp_player = state.player_list[state.current_player + 1 % 2]
    valid_actions = []
    for card in curr_player.hand:  # can play any card in your hand
        valid_actions.append(Action(ActName.PLAY_CARD, card))
    for card in state.trade_row:   # can buy any trade row card that you can afford
        if (curr_player.trade >= card.card_cost):   # use polymorphism for card_cost field?
            valid_actions.append(Action(ActName.BUY_CARD, card))
    if curr_player.combat > 0:   # can attack base if in play, or opponent if no base in play
        if has_base(opp_player):
            for card in opp_player.in_play:
                if isinstance(card, Base):
                    valid_actions.append(Action(ActName.ATTACK, card))
        else:
            for card in opp_player.in_play:
                if isinstance(card, Landscape):
                    valid_actions.append(Action(ActName.ATTACK, card))
            valid_actions.append(Action(ActName.ATTACK, 'Opponent'))
    for card in curr_player.in_play:   # can scrap any card with a discard effect
        if card.discard_function.function_name != FuncName.NONE:
            valid_actions.append(Action(ActName.SCRAP_EFFECT, card))
    valid_funcs = valid_functions(curr_player)
    for f in valid_funcs:   # special effects: scrap a card in the trade row, destroy target base, etc.
        if f.function_name == FuncName.SCRAP_TRADE_ROW:
            for card in state.trade_row:
                valid_actions.append(Action(ActName.SCRAP_TRADE_ROW, card))
        elif f.function_name == FuncName.DESTROY_BASE:
            for card in opp_player.in_play:
                if isinstance(card, Base) or isinstance(card, Landscape):
                    valid_actions.append(Action(ActName.DESTROY_BASE, card))
        elif f.function_name == FuncName.ACQUIRE_FREE_SHIP:
            for card in state.trade_row:
                valid_actions.append(Action(ActName.ACQUIRE_FREE_SHIP, card))
        elif f.function_name == FuncName.SCRAP_HAND_DISC:
            for card in curr_player.hand:
                valid_actions.append(Action(ActName.SCRAP_HAND_DISC, card))
            for card in curr_player.discard:
                valid_actions.append(Action(ActName.SCRAP_HAND_DISC, card))
        elif f.function_name == FuncName.COPY_SHIP:
            for card in curr_player.in_play:
                if isinstance(card, Ship) and card != stealth_needle:
                    valid_actions.append(Action(ActName.COPY_SHIP, card))
    # TODO: activate effect for a choice of effects
    # TODO: more complex functions, i.e. scrap->draw, draw->scrap, disc->draw
    valid_actions.append(Action(ActName.END_TURN))
    for action in valid_actions:   # print actions (for debugging)
        if isinstance(action.target, Ship) or isinstance(action.target, Landscape) or isinstance(action.target, Base):   # polymorphism pls
            print(action.action_name, action.target.card_name)
        else:
            print(action.action_name, action.target)

p0 = Player(authority = 50, deck = [scout, scout, scout, scout, scout, scout, viper], in_play = [scout, stealth_needle], hand = [scout, scout, viper], combat = 3, trade = 3, discard = [junkyard])
p1 = Player(authority = 50, deck = [scout, scout, scout, scout, scout, scout, scout, scout, viper, viper], in_play = [barter_world], hand = [], combat = 0, trade = 0, discard = [])
state_example = Game(curr_player=0, player_list=[p0, p1], trade_row=[patrol_mech, blob_wheel, imperial_frigate, missile_bot, embassy_yacht], deck=[])

valid_functions(p0)
list_actions(state_example)

# TODO: given a state and an action, return a new state
# def action(state, action):
