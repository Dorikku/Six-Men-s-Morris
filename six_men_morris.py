"""
Six Men Morris Player
"""

import copy
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

    if piece_count(player) > 3:
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
    else:
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
                    if (i,j) not in line:
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
    result = copy.deepcopy(board)

    result[pos[0]][pos[1]] = EMPTY
    return result


# def result(board, action, p, init_pos):
#     """
#     Returns the board that results from making move (i, j) on the board.
#     """
#     # create a deep copy of the board 
#     result = copy.deepcopy(board)
#     all_pieces_placed = False
#     # print(p1_piece_count, " - ", p2_piece_count)
#     if all_pieces_placed:
#         print("tite")
#         result[action[0]][action[1]] = p
#         result[init_pos[0]][init_pos[1]] = EMPTY
#     else:
#         result[action[0]][action[1]] = p
#         subtract_piece(p)
        
#         print(p1_piece_count, " - ", p2_piece_count)

#         if (p1_piece_count == 0 and p2_piece_count == 0):
#             all_pieces_placed = True


def result(*args):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # create a deep copy of the board 
    result = copy.deepcopy(args[0])

    if len(args) == 3:
        result[args[1][0]][args[1][1]] = args[2]
        subtract_piece(args[2])
    elif len(args) == 4:
        result[args[1][0]][args[1][1]] = args[2]
        result[args[3][0]][args[3][1]] = EMPTY

    return result


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
    pass


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    pass


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # check who is the winner and return the corresponding integer
    if winner(board) == 1:
        return 1
    elif winner(board) == 2:
        return -1 
    else:
        return 0


def minimax(board, p):
    """
    Returns the optimal action for the current player on the board.
    """
    if p == p1:
        move = next(iter(actions(board)))
    elif p == p2:
        move = next(iter(actions(board)))

    return move