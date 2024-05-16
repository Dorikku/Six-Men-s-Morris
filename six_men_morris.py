"""
Six Men Morris Player
"""

import copy
import random
import math
import numpy as np


# Initialization
X = 'X'
EMPTY = '0'
p1 = 'R'
p2 = 'Y'

p1_piece_count = 6
p2_piece_count = 6

p1_piece_left = 6
p2_piece_left = 6

user_mills = set()
ai_mills = set()


def create_board():
    board = np.array([
        [0, X, 0, X, 0],
        [X, 0, 0, 0, X],
        [0, 0, X, 0, 0],
        [X, 0, 0, 0, X],
        [0, X, 0, X, 0]
    ])
    return board


def change_player(p):
    """
    returns whos player turn
    """
    if p == p1:
        return p2
    elif p == p2:
        return p1


def piece_count_board(p):
    """
    Returns the count of pieces left of a player 
    for board UI
    """
    if p == p1:
        return p1_piece_count
    elif p == p2:
        return p2_piece_count
    

def piece_count(p):
    """
    Returns the count of pieces left of a player
    for actual game
    """
    if p == p1:
        return p1_piece_left
    elif p == p2:
        return p2_piece_left


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # create a set called slots
    slots = set()

    # iterate all over slots on the board and store all that free slot
    for i in range(5):
        for j in range(5):
            if board[i][j] == EMPTY:
                slots.add((i, j))
    return slots


def moves(board, pos, player):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    slots = set()
    count = np.count_nonzero(board == player)


    if count > 3:
        # Check if adjacent empty slot exists for each position containing a piece
        for i in range(5):
            for j in range(5):
                if (i,j) == pos:
                    # for top left corner
                    if i == 0 and j == 0:
                        if board[i][j+2] == EMPTY:
                            slots.add((i, j+2))
                        if board[i+2][j] == EMPTY:
                            slots.add((i+2, j))
                    # for top right corner
                    elif i == 0 and j == 4:
                        if board[i][j-2] == EMPTY:
                            slots.add((i, j-2))
                        if board[i+2][j] == EMPTY:
                            slots.add((i+2, j))
                    # for bottom left corner
                    elif i == 4 and j == 0:
                        if board[i][j+2] == EMPTY:
                            slots.add((i, j+2))
                        if board[i-2][j] == EMPTY:
                            slots.add((i-2, j))
                    # for bottom right corner
                    elif i == 4 and j == 4:
                        if board[i][j-2] == EMPTY:
                            slots.add((i, j-2))
                        if board[i-2][j] == EMPTY:
                            slots.add((i-2, j))
                    # for left edge
                    elif i == 2 and j == 0:
                        if board[i-2][j] == EMPTY:
                            slots.add((i-2, j))
                        if board[i+2][j] == EMPTY:
                            slots.add((i+2, j))
                        if board[i][j+1] == EMPTY:
                            slots.add((i, j+1))
                    # for right edge
                    elif i == 2 and j == 4:
                        if board[i-2][j] == EMPTY:
                            slots.add((i-2, j))
                        if board[i+2][j] == EMPTY:
                            slots.add((i+2, j))
                        if board[i][j-1] == EMPTY:
                            slots.add((i, j-1))
                    # for top edge
                    elif i == 0 and j == 2:
                        if board[i][j-2] == EMPTY:
                            slots.add((i, j-2))
                        if board[i][j+2] == EMPTY:
                            slots.add((i, j+2))
                        if board[i+1][j] == EMPTY:
                            slots.add((i+1, j))
                    # for bottom edge
                    elif i == 4 and j == 2:
                        if board[i][j-2] == EMPTY:
                            slots.add((i, j-2))
                        if board[i][j+2] == EMPTY:
                            slots.add((i, j+2))
                        if board[i-1][j] == EMPTY:
                            slots.add((i-1, j))
                    else:
                        if board[i][j+1] == EMPTY:
                            slots.add((i, j+1))
                        if board[i][j-1] == EMPTY:
                            slots.add((i, j-1))
                        if board[i-1][j] == EMPTY:
                            slots.add((i-1, j))
                        if board[i+1][j] == EMPTY:
                            slots.add((i+1, j))
    if count == 3:
        for i in range(5):
            for j in range(5):
                if board[i][j] == EMPTY:
                    slots.add((i,j))

    return slots
        

def line_forms(board, player):
    """
    returns set of positions that formed a line
    """

    positions = set()

    if board[0][0] == board[0][2] == board[0][4]:
        if board[0][0] == player:
            for i in range(0,5,2):
                positions.add((0,i))
    if board[0][0] == board[2][0] == board[4][0]:
        if board[0][0] == player:
            for i in range(0,5,2):
                positions.add((i,0))
    if board[0][4] == board[2][4] == board[4][4]:
        if board[0][4] == player: 
            for i in range(0,5,2):
                positions.add((i,4))
    if board[4][0] == board[4][2] == board[4][4]:
        if board[4][0] == player: 
            for i in range(0,5,2):
                positions.add((4,i))
    if board[1][1] == board[1][2] == board[1][3]:
        if board[1][1] == player:
            for i in range(1,4):
                positions.add((1,i))
    if board[1][1] == board[2][1] == board[3][1]:
        if board[1][1] == player:
            for i in range(1,4):
                positions.add((i,1))
    if board[1][3] == board[2][3] == board[3][3]:
        if board[1][3] == player:
            for i in range(1,4):
                positions.add((i,3))
    if board[3][1] == board[3][2] == board[3][3]:
        if board[3][1] == player:
            for i in range(1,4):
                positions.add((3,i))
    
    return positions


def pieces_can_remove(board, player, line):
    positions = set()

    if player == p1:
        for i in range(5):
            for j in range(5):
                if board[i][j] == p2:
                    # if (i,j) not in line:
                        positions.add((i,j))
    elif player == p2:
        for i in range(5):
            for j in range(5):
                if board[i][j] == p1:
                    if (i,j) not in line:
                        positions.add((i,j))
    
    return positions


def remove_piece(board, pos):
    """
    Removes piece from the board
    """
    # result = copy.deepcopy(board)

    board[pos[0]][pos[1]] = EMPTY
    # return result


def result(board, action, p):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # create a deep copy of the board 
    result = copy.deepcopy(board)
    
    if action[1] == None and action[2] == None:    
        result[action[0][0]][action[0][1]] = p
    elif action[1] != None:
        result[action[1][0]][action[1][1]] = EMPTY
    elif action[2] != None:
        result[action[0]][action[0][1]] = p
        result[action[2][0]][action[2][1]] = EMPTY

    return result
        



# def result(*args):
#     """
#     Returns the board that results from making move (i, j) on the board.
#     """
#     # create a deep copy of the board 
#     result = copy.deepcopy(args[0])

#     if len(args) == 3:
#         result[args[1][0]][args[1][1]] = args[2]
#         subtract_piece(args[2])
#     elif len(args) == 4:
#         result[args[1][0]][args[1][1]] = args[2]
#         result[args[3][0]][args[3][1]] = EMPTY

#     return result



def score_position(board, player):
    score = 0
    opp_player = p1
    if player == p1:
        opp_player = p2

    # for horizontal
    for r in range(5):
        window = [(i) for i in list(board[r,:])]
        if r != 2:
            if window.count(player) == 3:
                score += 100000000
            elif window.count(player) == 2 and window.count(EMPTY) == 1:
                score += 2

            if window.count(opp_player) == 2 and window.count(EMPTY) == 1:
                score -= 1
        
    # for horizontal
    for r in range(5):
        window = [(i) for i in list(board[:,r])]
        if r != 2:
            if window.count(player) == 3:
                score += 100000000
            elif window.count(player) == 2 and window.count(EMPTY) == 1:
                score += 2

            if window.count(opp_player) == 2 and window.count(EMPTY) == 1:
                score -= 1

    return score


def score_position_p2(board, player, mill):
    score = 0
    opp_player = p1
    if player == p1:
        opp_player = p2

    # for horizontal
    for r in range(5):
        window = [(i) for i in list(board[r,:])]
        if r != 2:
            if window.count(player) == 3 and (((r,0) not in mill) or ((r,1) not in mill)):
                score += 100
            elif window.count(player) == 2 and window.count(EMPTY) == 1:
                score += 10

            if window.count(opp_player) == 2 and window.count(EMPTY) == 1:
                score -= 50
        
    # for horizontal
    for r in range(5):
        window = [(i) for i in list(board[:,r])]
        if r != 2:
            if window.count(player) == 3 and (((0,r) not in mill) or ((1,r) not in mill)):
                score += 100
            elif window.count(player) == 2 and window.count(EMPTY) == 1:
                score += 10

            if window.count(opp_player) == 2 and window.count(EMPTY) == 1:
                score -= 50

    return score



def pick_best_move(board, player):
    valid_locations = actions(board)
    best_score = -10000
    best_pos = next(iter(valid_locations))
    for pos in valid_locations:
        temp_board = board.copy()
        put_piece(temp_board, pos, player)
        score = score_position(temp_board, player)
        if score > best_score:
            best_score = score
            best_pos = pos

    return best_pos


def put_piece(board, pos, player):
    """
    puts piece on the board
    """
    board[pos[0]][pos[1]] = player
    return board


def move_piece(board, pos, action, player):
    """
    moves piece on the board
    """

    board[action[0]][action[1]] = player
    board[pos[0]][pos[1]] = EMPTY

    return board


# Subtract player piece by 1
def subtract_piece(p):

    global p1_piece_count
    global p2_piece_count

    if p == p1:
        p1_piece_count -= 1
    elif p == p2:
        p2_piece_count -= 1


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    p1_count = np.count_nonzero(board == p1)
    p2_count = np.count_nonzero(board == p2)

    if p1_count < 3:
        return p2
    elif p2_count < 3:
        return p1

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    pass


def utility(board, player):
    if winner(board) == player:
        return (None, 1)
    elif winner(board) != player:
        return (None, -1)
    else:
        return (None, 0)
    


def pieces_can_move(board, player):
    pieces = set()
    for i in range(5):
        for j in range(5):
            if board[i][j] == player:
                if moves(board, (i,j), player):
                    pieces.add((i,j))
    return pieces


def minimax(board, depth, alpha, beta, maximizingPlayer, ai_piece, ai_mill, player_mill):
    # valid_moves = pieces_can_move(board, maximizingPlayer)
    is_terminal = winner(board)
    

    

    if depth == 0 or is_terminal:
        if is_terminal:
            if is_terminal == ai_piece:
                return (None, 100000000000000)
            elif is_terminal != ai_piece:
                return (None, -100000000000000)
        else:
            # return (None, score_position_p2(board, ai_piece, ai_mill))
            return (None, score_position(board, ai_piece))

    
    if maximizingPlayer:
        value = -math.inf
        pieces = pieces_can_move(board, ai_piece)
        piece = random.choice(list(pieces))
        act = random.choice(list(moves(board, piece, ai_piece)))
        action = [piece, act, None]

        for p in pieces:
            valid_moves = moves(board, p, ai_piece)
            for m in valid_moves:
                b_copy = copy.deepcopy(board)

                ai_mill_copy = ai_mill.copy()
                player_mill_copy = player_mill.copy()

               
                move_piece(b_copy, p, m, ai_piece)
                mill = line_forms(b_copy, ai_piece)

                remove = None

                if not mill.issubset(ai_mill_copy):
                    for pos in mill:
                        ai_mill_copy.add(pos)  
                    
                    can_remove = pieces_can_remove(b_copy, ai_piece, player_mill_copy)
                    remove = random.choice(list(can_remove))
                    remove_piece(b_copy, remove)

                
                new_score = minimax(b_copy, depth-1, alpha, beta, False, ai_piece, ai_mill_copy, player_mill_copy)[1]
                if new_score > value:
                    value = new_score
                    action[0] = p
                    action[1] = m
                    action[2] = remove



                alpha = max(alpha, value)
                if alpha >= beta:
                    break

        return action, value
    
    else:   # Minimizing player
        value = math.inf

        player_piece = p1
        if ai_piece == p1:
            player_piece = p2

        pieces = pieces_can_move(board, player_piece)
        piece = random.choice(list(pieces))
        act = random.choice(list(moves(board, piece, player_piece)))

        action = [piece, act, None]

        for p in pieces:
            valid_moves = moves(board, p, player_piece)
            for m in valid_moves:
                b_copy = copy.deepcopy(board)

                ai_mill_copy = ai_mill.copy()
                player_mill_copy = player_mill.copy()
                move_piece(b_copy, p, m, player_piece)
                mill = line_forms(b_copy, player_piece)

                remove = None

                if not mill.issubset(player_mill_copy):
                    for pos in mill:
                        player_mill_copy.add(pos)
                    
                    can_remove = pieces_can_remove(b_copy, player_piece, ai_mill_copy)
                    remove = random.choice(list(can_remove))
                    remove_piece(b_copy, remove)
                    action[2] = remove

                
                new_score = minimax(b_copy, depth-1, alpha, beta, True, ai_piece, ai_mill_copy, player_mill_copy)[1]
                if new_score < value:
                    value = new_score
                    action[0] = p
                    action[1] = m
                    action[2] = remove

                beta = min(beta, value)
                if alpha >= beta:
                    break 
        return action, value
    
