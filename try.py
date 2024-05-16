import numpy as np


X = 'X'
EMPTY = '0'
R = 'R'
Y = 'Y'

board = np.array([
        [R, X, R, X, R],
        [X, R, R, R, X],
        [0, 0, X, 0, 0],
        [X, 0, 0, 0, X],
        [0, X, 0, X, 0]
    ])

def score_position(board, player):
    score = 0

    pos1 = [(0,0), (1,1)]

    # for horizontal
    for r in range(5):
        window = [(i) for i in list(board[r,:])]
        if r != 2:
            if window.count(player) == 3:
                score += 100
            elif window.count(player) == 2 and window.count(EMPTY) == 1:
                score += 10
        
    return score

# count = np.count_nonzero(board == EMPTY)
# print(count)
# x = [0, 1]

# game_over = x

# if len(x) == 2:
#     print("2 siya")

print(np.where(board == R))