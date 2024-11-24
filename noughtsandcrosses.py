'''Modules importing random, os.path and json(from top to bottom)'''
import random
import os.path
import json

random.seed()

def draw_board(board):
    '''
    Draws the Nougths and crosses board to play.

    Args:
    - board (list): The 3x3 Nougths and crosses board.
    '''
    for row in board:
        print(' | '.join(row))
        print('-' * 9)

def welcome(board):
    '''
    Print a welcome message and draw the initial Nougths and crosses board.

    Args:
    - board (list): The 3x3 Nougths and crosses board.
    '''

    print("Welcome to Noughts and Crosses!")
    draw_board(board)

def initialise_board(board):
    '''
    Initialise the Nougths and crosses board with empty spaces.

    Args:
    - board (list): The 3x3 Nougths and crosses board.

    Returns:
    - list: The initialised Nougths and crosses board.
    '''
    for i in range(3):
        for j in range(3):
            board[i][j] = ' '
    return board

def get_player_move(board):
    '''
    Get the player's move and convert it to row and column.

    Args:
    - board (list): The 3x3 Nougths and crosses board.

    Returns:
    - tuple: The row and column of the player's move.
    '''
    while True:
        move = input("Enter your move (1-9): ")
        row = (int(move) - 1) // 3
        col = (int(move) - 1) % 3
        if board[row][col] == ' ':
            return row, col

def choose_computer_move(board):
    '''
    Choose the computer's move based on the current state of the board.

    Args:
    - board (list): The 3x3 Nougths and crosses board.

    Returns:
    - tuple: The row and column of the computer's move.
    '''
    # Check if the computer or player can win on the next move
    for symbol in ['O', 'X']:
        for i in range(1, 10):
            row, col = (i - 1) // 3, (i - 1) % 3
            if board[row][col] == ' ':
                board[row][col] = symbol
                if check_for_win(board, symbol):
                    board[row][col] = 'O'  # Undo the move for the computer
                    return row, col
                board[row][col] = ' '  # Undo the move

    # Take the center if it's available
    if board[1][1] == ' ':
        return 1, 1

    # Take a corner if it's available
    for row, col in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[row][col] == ' ':
            return row, col

    # Take any other cell
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                return row, col


def check_for_win(board, mark):
    '''
    Check if player or compurt has won the game.

    Args:
    - board (list): The 3x3 Nougths and crosses board.
    - mark (str): The player's mark ('X' or 'O').

    Returns:
    - bool: True if the player has won, False otherwise.
    '''
    # check horizontal spaces
    for row in board:
        if row.count(mark) == 3:
            return True

    # check vertical spaces
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == mark:
            return True

    # check diagonals
    if board[0][0] == board[1][1] == board[2][2] == mark or \
       board[0][2] == board[1][1] == board[2][0] == mark:
        return True

    return False


def check_for_draw(board):
    '''
    Check if the game has ended in a draw.

    Args:
    - board (list): The 3x3 Nougths and crosses board.

    Returns:
    - bool: True if the game is a draw, False otherwise.
    '''
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game(board):
    '''
    Play a game of Tic-Tac-Toe.

    Args:
    - board (list): The 3x3 Nougths and crosses board.

    Returns:
    - int: 1 if player X wins, -1 if computer wins, 0 if it's a draw.
    '''
    board = initialise_board(board)
    draw_board(board)
    while True:
        row, col = get_player_move(board)
        board[row][col] = 'X'
        draw_board(board)
        if check_for_win(board, 'X'):
            print("Player X wins!")
            return 1
        if check_for_draw(board):
            print("It's a draw!")
            return 0
        row, col = choose_computer_move(board)
        board[row][col] = 'O'
        draw_board(board)
        if check_for_win(board, 'O'):
            print("Computer wins!")
            return -1
        if check_for_draw(board):
            print("It's a draw!")
            return 0



def menu():
    '''
    Display the menu options and get the user's choice.

    Returns:
    - str: The user's choice.
    '''
    print("1 - Play the game")
    print("2 - Save score in file 'leaderboard.txt'")
    print("3 - Load and display the scores from the 'leaderboard.txt'")
    print("q - End the program")
    choice = input("Enter your choice: ")
    return choice

def load_scores():
    '''
    Load scores from the 'leaderboard.txt' file.

    Returns:
    - dict: A dictionary containing player names and scores.
    '''
    if os.path.exists('leaderboard.txt'):
        with open('leaderboard.txt', 'r', encoding="utf-8") as f:
            try:
                leaders = json.load(f)
            except json.decoder.JSONDecodeError:
                leaders = {}
    else:
        leaders = {}
    return leaders



def save_score(score):
    '''
    Save a player's score in the 'leaderboard.txt' file.

    Args:
    - score (int): The player's score.
    '''
    name = input("Enter your name: ")
    leaders = load_scores()
    leaders[name] = score
    with open('leaderboard.txt', 'w', encoding="utf-8") as f:
        json.dump(leaders, f)

def display_leaderboard(leaders):
    '''
    Display the leaderboard with player names and scores.

    Args:
    - leaders (dict): A dictionary containing player names and scores.
    '''
    for name, score in leaders.items():
        print(f"{name}: {score}")
