import random
import pickle
from collections import defaultdict, Counter
from isolation import Isolation
from isolation import DebugState


def build_book(book, num_rounds = 100):
       
    for num in range(num_rounds):
        state = Isolation()
        states = []
        
        while state.ply_count <= 3:
            action = random.choice(state.actions())
            player = state.player()
            states.append((state, player, action))
            state = state.result(action)            
            
        while not state.terminal_test():
            action = alpha_beta(state, state.player())
            player = state.player()
            state = state.result(action)
                    
        win_0 = state.utility(0) > 0
        win_1 = state.utility(1) > 0
        assert win_0 != win_1
        
        for s in states:
            state  = s[0]
            player = s[1]
            action = s[2]
            
            if win_0:
                if player == 0:
                    book[state][action] +=  1
                else:
                    book[state][action] += -1
            else:
                if player == 0:
                    book[state][action] += -1
                else:
                    book[state][action] +=  1
                    
    return book
    
    
def alpha_beta(state, player_id, depth = 4):
    
    def min_value(state, player_id, alpha, beta, depth):
        if state.terminal_test():
            return state.utility(player_id)   
        if depth <= 0: 
                return score(state, player_id)
        
        value = float("inf")
        
        for action in state.actions():
            value = min(value, max_value(state.result(action), player_id, alpha, beta, depth - 1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        
        return value

    def max_value(state, player_id, alpha, beta, depth):
        if state.terminal_test():
            return state.utility(player_id)
        if depth <= 0: 
                return score(state, player_id)
        
        value = float("-inf")
        
        for action in state.actions():
            value = max(value, min_value(state.result(action), player_id, alpha, beta, depth - 1))
            if value > beta:
                return value
            alpha = max(alpha, value)
            
        return value

    alpha = float("-inf")
    beta = float("inf")
    best_score = float("-inf")
    best_move = None
    
    for action in state.actions():
        value = min_value(state.result(action), state.player(), alpha, beta, depth - 1)
        alpha = max(alpha, value)
        
        if value >= best_score:
            best_score = value
            best_move = action
            
    return best_move


def score(state, player_id):
    if state.utility(player_id) > 0:
        return float('inf')
    if state.utility(player_id) < 0:
        return float('-inf')
    
    own_loc = state.locs[player_id]
    opp_loc = state.locs[1 - player_id]
    
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)
    
    return (dist_to_center[opp_loc] + 1) * len(own_liberties) - \
           (dist_to_center[own_loc] + 1) * len(opp_liberties)
           
           
dist_to_center = \
    {0: 6.4031242374328485, 1: 5.656854249492381, 2: 5.0, 3: 4.47213595499958, 
     4: 4.123105625617661, 5: 4.0, 6: 4.123105625617661, 7: 4.47213595499958, 
     8: 5.0, 9: 5.656854249492381, 10: 6.4031242374328485, 13: 5.830951894845301, 
     14: 5.0, 15: 4.242640687119285, 16: 3.605551275463989, 17: 3.1622776601683795, 
     18: 3.0, 19: 3.1622776601683795, 20: 3.605551275463989, 21: 4.242640687119285, 
     22: 5.0, 23: 5.830951894845301, 26: 5.385164807134504, 27: 4.47213595499958,
     28: 3.605551275463989, 29: 2.8284271247461903, 30: 2.23606797749979, 31: 2.0, 
     32: 2.23606797749979, 33: 2.8284271247461903, 34: 3.605551275463989, 
     35: 4.47213595499958, 36: 5.385164807134504, 39: 5.0990195135927845, 
     40: 4.123105625617661, 41: 3.1622776601683795, 42: 2.23606797749979, 
     43: 1.4142135623730951, 44: 1.0, 45: 1.4142135623730951, 46: 2.23606797749979, 
     47: 3.1622776601683795, 48: 4.123105625617661, 49: 5.0990195135927845, 52: 5.0, 
     53: 4.0, 54: 3.0, 55: 2.0, 56: 1.0, 57: 0.0, 58: 1.0, 59: 2.0, 60: 3.0, 61: 4.0, 
     62: 5.0, 65: 5.0990195135927845, 66: 4.123105625617661, 67: 3.1622776601683795, 
     68: 2.23606797749979, 69: 1.4142135623730951, 70: 1.0, 71: 1.4142135623730951, 
     72: 2.23606797749979, 73: 3.1622776601683795, 74: 4.123105625617661, 
     75: 5.0990195135927845, 78: 5.385164807134504, 79: 4.47213595499958, 
     80: 3.605551275463989, 81: 2.8284271247461903, 82: 2.23606797749979, 83: 2.0, 
     84: 2.23606797749979, 85: 2.8284271247461903, 86: 3.605551275463989, 
     87: 4.47213595499958, 88: 5.385164807134504, 91: 5.830951894845301, 92: 5.0, 
     93: 4.242640687119285, 94: 3.605551275463989, 95: 3.1622776601683795, 96: 3.0, 
     97: 3.1622776601683795, 98: 3.605551275463989, 99: 4.242640687119285, 100: 5.0, 
     101: 5.830951894845301, 104: 6.4031242374328485, 105: 5.656854249492381, 106: 5.0, 
     107: 4.47213595499958, 108: 4.123105625617661, 109: 4.0, 110: 4.123105625617661, 
     111: 4.47213595499958, 112: 5.0, 113: 5.656854249492381, 114: 6.4031242374328485}

    
if __name__ == '__main__':
    import time
    start = time.time()
    
    try:
        book = pickle.load(open("data.pickle", "rb"))
    except:   
        book = defaultdict(Counter)
    
    for i in range(1350):
        book = build_book(book) 
        if i % 100 == 0:
            print('Iteration Number mod 100: ', i)        
            pickle.dump(book, open("data.pickle", "wb"))
        
    stop = time.time()
    print(stop - start, 'seconds')
        