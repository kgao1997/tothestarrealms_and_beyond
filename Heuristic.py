from main import Player 
from main import Faction
from main import Base
from main import Ship
from main import Landscape
import math


def bias_compute(b, t, e, c):
    #b = blob, t = trade_fed, e = star_emp, c = mach_cult
    total_sum = b + t + e + c
    blob_bias = b / total_sum
    tfed_bias = t / total_sum
    star_bias = e / total_sum
    mach_bias = c / total_sum #Extract bias for each faction
    return blob_bias, tfed_bias, star_bias, mach_bias #Return all faction biases 

#Helper function to determine if a card exists in a current deck. If card exists in pool then return the number of copies else return 0
def card_count(card_id, card_pool):
    card_count = 0
    for i in (0, card_deck.length - 1):
        if(card_deck[i].card_name == card_id):
            card_count = card_count + 1
    return card_count


#Return a value that estimates the quality of a given player's deck. Higher values are better
def player_heuristic_func(p):
    card_pool = p.deck + p.discard + p.in_play + p.hand #Combine player's card pool
    blob_count = 0
    trade_fed_count = 0
    empire_count = 0
    cult_count = 0
    e_yacht_count = 0
    total_deck_value = 0
    deck_dictionary = {}
    for i in range (0, card_pool.length - 1):
        if(card_pool[i].card_faction == Faction.BLOB):
            blob_count = blob_count + 1
        elif(card_pool[i].card_faction == Faction.TRADE_FED):
            trade_fed_count = trade_fed_count + 1
        elif(card_pool[i].card_faction == Faction.STAR_EMP):
            empire_count = empire_count + 1
        elif(card_pool[i].card_faction == Faction.MACH_CULT):
            cult_count = cult_count + 1
        elif(card_pool[i].card_name == "Embassy Yacht"):
            e_yacht_count = e_yacht_count + 1 
    #extract faction biases
    blob_bias, tfed_bias, star_bias, mach_bias = bias_compute (blob_count, trade_fed_count, empire_count, cult_count)
    #Special case for the Embassy Yacht deck, bias the heuristic function towards picking more bases 
    if(e_yacht_count > 0):
        for i in range (0, card_pool.length - 1):
            if(type(card_pool[i]) is Base or Landscape):
                total_deck_value = total_deck_value + 5
    #convert the deck list of cards into a dictionary for O(1) access, these for loops are going to drive me mad
    for i in range (0, card_pool.length - 1):
        if(card_pool[i].card_name in deck_dictionary):
            deck_dictionary[card_pool[i].card_name] = deck_dictionary[card_pool[i].card_name] + 1 #inc card count for multiple cards in deck
        else:
            deck_dictionary[card_pool[i].card_name] = 1 #add new card to dictionary representation of deck
    if "Explorer" in deck_dictionary:
        total_deck_value = total_deck_value + (1 * deck_dictionary["Explorer"])
        if(card_pool.length > 20):
            total_deck_value = total_deck_value - (2 * deck_dictionary["Explorer"])
        #Idea is that Explorers lose value as the game goes on, while being useful in the early game. Add 1 score for each until mid-game established when they should be dusted
    #Baseline draft value of card to value dictionary. 1 is least useful, 5 is most useful
    base_card_values = {
        #Note that vipers and scouts are awful cards and should be eviscerated out of your deck as soon as possible
        "Viper" : -2, #These are truly awful
        "Scout" : 0, #These are also awful

        #Blobs, note will have high tribal synergy
        "Battle Blob" : 3,
        "Battle Pod" : 2,
        "Blob Carrier" : 3,
        "Blob Destroyer" : 3, #Will increase in value based on number of opponent's bases
        "Blob Fighter" : 1, #Find way to scale since it's one of the best cards in the full Blob deck
        "Blob Wheel" : 1,
        "Blob World" : 4,
        "Mothership" : 4,
        "Ram" : 3,
        "The Hive" : 5, 
        "Trade Pod" : 2, #Special multiplier: Multiplies by tribal bias 
        
        #Machine Cult, generally decent early picks but I've never seen them actually succeed as a main deck
        "Battle Mech" : 2,
        "Battle Station" : 2,
        "Brain World" : 5, 
        "Junkyard" : 4,
        "Machine Base" : 5, 
        "Mech World" : 2, #Note will have an effect on the faction multiplier
        "Missle Bot" : 3, 
        "Missle Mech" : 2, #Destroys base
        "Patrol Mech" : 2, 
        "Stealth Needle" : 5, #Actually code to be the 5/n th highest score of all cards in your deck
        "Supply Bot" : 2, 
        "Trade Bot" : 3, 

        #Star Empire: Turns out multiplicatively discarding cards from your opponent is good, and cantrips are good
        "Battlecruiser": 4, 
        "Corvette" : 3, 
        "Dreadnaught" : 4, 
        "Fleet HQ" : 5, 
        "Imperial Fighter" : 1, 
        "Imperial Frigate" : 1, 
        "Recycling Station" : 5, 
        "Royal Redoubt" : 2, 
        "Space Station" : 2, 
        "Survey Ship" : 3, 
        "War World" : 2, 

        #Trade Federation: This stuff is generally awful
        "Barter World" : 3, 
        "Central Office" : 1, 
        "Command Ship" : 5, 
        "Cutter" : 2, 
        "Defense Center" : 2, 
        "Embassy Yacht" : 6, #Higher to trigger YOLO Embassy Yacht deck
        "Federation Shuttle" : 1, 
        "Flagship" : 3, 
        "Freighter" : 3, 
        "Port of Call" : 3, 
        "Trade Escort" : 2, 
        "Trading Post" : 1
    }

    deck_raw_value = 0 #Compute raw value of deck for cantrip calculations
    for i in range(0, card_pool.length - 1):
        deck_raw_value = deck_raw_value + base_card_values[card_pool[i]]

    #Compute Blob Deck value using sigmoid function to evaluate score that Blob adds to the deck score
    blob_value = 0
    for i in range(0, card_pool.length - 1):
        if(card_pool[i].card_name in base_card_values and card_pool[i].card_faction == Faction.BLOB):
            blob_value = blob_value + base_card_values[card_pool[i].card_name] #add blob value to the card pool name
    #Postcondition: Raw value of all blob cards added to deck value
    
    #We will try to bias the card value scaling of the blob faction such that a high concentration of blob cards will result 
    #in a higher deck score, since the Blob faction draws power from having a high concentration of Blobs to trigger faction 
    #abilities. Thus, we put the blob bias through a tight sigmoidal activation function 
    sigmoid_scalar = 1.0/(1.0 - (2.71 ** (2.0 * blob_bias))) #use a sharp sigmoid function to scale the blob bias
    blob_scalar = blob_value * sigmoid_scalar #Returns sigmoid pass through blob scalar
    if(card_count("Blob Fighter", card_pool) > 0):
        cantrip_value = (deck_raw_value // card_pool.length)
        expected_value = int(card_count("Blob Fighter", card_pool) * cantrip_value * blob_bias)
        total_deck_value = total_deck_value + expected_value #add the expected value of the cantrips to the blob deck
    blob_scalar = blob_scalar * blob_count
        
    total_deck_value = total_deck_value + blob_scalar #Computed blob value

    #Machine Cult: Since Machine Cult is better as a support option in the base set than as a dominant faction,
    #Machine Cult's contribution will be a linear operation directly added to the score of the current deck
    mcult_value = 0
    for i in range(0, card_pool.length - 1):
        if(card_pool[i].card_name in base_card_values and card_pool[i].card_faction == Faction.MACH_CULT):
            mcult_value = mcult_value + base_card_values[card_pool[i].card_name]
    #Postcondition: Machine Cult value is the raw summation of all Machine Cult cards

    #Star Empire relies on drawing cards and forcing the opponent to discard, as well as some faction abilities.
    #Notably, in gameplay discarding a single card tends to be low value, but forcing a discard of two or more cards in a 
    #turn can be backbreaking. Thus, we will apply a function that values having a higher percentage of Star Empire cards, 
    #and in particular their signature ability to force the opponent to discard cards, as well as the Machine Cult's cantrips

    #Discarders is a dictionary of all cards that can cause a discard, with the value 0 if the card does not require a faction ability to discard and 1 if it does
    discarders = {
        "Battlecrusier" : 1, 
        "Imperial Fighter" : 0, 
        "Imperial Frigate" : 0, 
        "Royal Redoubt" : 1
    }

    semp_value = 0
    for i in range(0, card_pool.length - 1):
        if(card_pool[i].card_name in base_card_values and card_pool[i].card_faction == Faction.STAR_EMP):
            semp_value = semp_value + base_card_values[card_pool[i].card_name]
    #Postcondition: Raw value of all star empire cards saved in semp_value 
    #Compute raw value of cantrips:
    survey_ship_count = card_count("Survey Ship", card_pool)
    corvette_count = card_count("Corvette", card_pool)
    battlecruiser_count = card_count("Battlecruiser", card_pool)
    dreadnaught_count = card_count("Dreadnaught", card_pool)
    total_cantrips = survey_ship_count + corvette_count + battlecruiser_count + dreadnaught_count
    semp_cantrip_value = int ((deck_raw_value // card_pool.length) * total_cantrips)
    total_deck_value = total_deck_value + semp_cantrip_value 
    #Cantrips computed, then compute the score of discard
    num_discard_uncondition = 0
    num_discard_condition = 0
    for i in range(0, card_pool.length - 1):
        if(card_pool[i].card_id in discarders):
            if(discarders[card_pool[i].card_id] == 0):
                num_discard_uncondition = num_discard_uncondition + 1
            else:
                num_discard_condition = num_discard_condition + 1
    #postcondition num_discard_condition and num_discard_uncondition contain the number of conditional and unconditional discard effects each
    





        
        
    return total_deck_value
