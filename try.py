positions = set()
X = 'X'
EMPTY = 0
# Example usage:
board = [
    [0, X, 0, X, 0],
    [X, 1, 1, 1, X],
    [0, 1, X, 1, 0],
    [X, 1, 1, 1, X],
    [0, X, 0, X, 0]
]


# def left_empty()

# Check if adjacent empty slot exists for each position containing a piece
if board[0][0] == board[0][2] == board[0][4]:
    if board[0][0] != EMPTY:
        for i in range(0,5,2):
            positions.add((0,i))

if board[0][0] == board[2][0] == board[4][0]:
    if board[0][0] != EMPTY:
        for i in range(0,5,2):
            positions.add((i,0))

if board[0][4] == board[2][4] == board[4][4]:
    if board[0][4] != EMPTY: 
        for i in range(0,5,2):
            positions.add((i,4))

if board[4][0] == board[4][2] == board[4][4]:
    if board[4][0] != EMPTY: 
        for i in range(0,5,2):
            positions.add((4,i))

if board[1][1] == board[1][2] == board[1][3]:
    if board[1][1] != EMPTY:
        for i in range(1,4):
            positions.add((1,i))

if board[1][1] == board[2][1] == board[3][1]:
    if board[1][1] != EMPTY:
        for i in range(1,4):
            positions.add((i,1))

if board[1][3] == board[2][3] == board[3][3]:
    if board[1][3] != EMPTY:
        for i in range(1,4):
            positions.add((i,3))

if board[3][1] == board[3][2] == board[3][3]:
    if board[3][1] != EMPTY:
        for i in range(1,4):
            positions.add((3,i))


# print(array)
print(positions)
