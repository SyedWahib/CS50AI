"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX = 0
    countO = 0

    for row in board:
        for col in row:
            if col == X:
                countX += 1
            elif col == O:
                countO += 1
    
    if countX == countO or countX == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action in actions(board):
        new_board = [row[:] for row in board]
        new_board[action[0]][action[1]] = player(board)
    else:
        raise Exception("Invalid action")

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        # Horizontal check
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    
        # Vertical check
        elif board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
    
        # Diagonal check
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return {'O': -1, 'X': 1}.get(winner(board), 0)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Returns None if the game is over
    if terminal(board):
        return None

    current_player = player(board)

    # If player is maximizing
    if current_player == X:
        # Keeping track of best value, initialising to negative infinity
        max_val = float('-inf')
        # Keeping track of best action
        best_action = None

        for action in actions(board):
            # setting new value if older one is greater
            value = min_value(result(board, action))

            if value > max_val:
                max_val = value
                best_action = action

        return best_action
    
    # If player is minimizing    
    if current_player == O:
        min_val = float('inf')
        best_action = None

        for action in actions(board):
            # Setting new value if older one is smaller
            value = max_value(result(board, action))

            if value < min_val:
                min_val = value
                best_action = action

        return best_action


def max_value(board):
    """
    Returns the highest value for minimizer
    """
    if terminal(board):
        return utility(board)
    
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    """
    Returns the lowest value for maximizer
    """
    if terminal(board):
        return utility(board)
    
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v