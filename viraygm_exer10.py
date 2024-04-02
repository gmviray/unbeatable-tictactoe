# VIRAY, Geraldine Marie M.
# CMSC 170 X5L
# EXER 10 MINMAX

import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# initialize board attributes
BOARD_SIZE = 3
BACKGROUND_COLOR = '#E0115F'
X_COLOR = '#FF007F'
O_COLOR = '#6600FF'

# initialize symbols, will change if player decides to be player 'O'
player_symbol = 'X'
computer_symbol = 'O'

# checks if move is initial
# initial = 1

# initialize board
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# initialize GUI
root = tk.Tk()
root.title("Unbeatable Tic Tac Toe")
root.configure(bg=BACKGROUND_COLOR)

# initialize buttons
buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# drawing the board
def draw_board():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            buttons[i][j] = tk.Button(
                root, text='', font=('normal', 20, 'bold'), width=8, height=4,
                command=lambda row=i, col=j: make_player_move(row, col),
                bg='pink', fg=X_COLOR
            )
            buttons[i][j].grid(row=i, column=j, padx=0, pady=8)


# drawing symbols inside buttons
def draw_symbols():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            symbol = board[i][j]
            if symbol == 'X':
                buttons[i][j].config(text='X', fg='white', bg=X_COLOR)
            elif symbol == 'O':
                buttons[i][j].config(text='O', fg='white', bg=O_COLOR)

# checks for draw
def is_board_full():
    for row in board:
        if ' ' in row:
            return False
    return True

# checks for winner
def is_winner(symbol):
    for row in board:
        # checks rows
        if all(cell == symbol for cell in row):
            return True

    # checks columns
    for j in range(BOARD_SIZE):
        if all(board[i][j] == symbol for i in range(BOARD_SIZE)):
            return True

    # checks diagonals
    if all(board[i][i] == symbol for i in range(BOARD_SIZE)):
        return True

    # check reverse diagonal
    if all(board[i][BOARD_SIZE - 1 - i] == symbol for i in range(BOARD_SIZE)):
        return True

    return False

# function for turns of AI
def make_computer_move():
    # global initial
    # # if the move is initial, computer plays 'X'
    # if initial == 1:
    #     # randomly chooses a tile for initial turn
    #     empty_tiles = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == ' ']
    #     i, j = random.choice(empty_tiles)
    #     board[i][j] = computer_symbol
    #     draw_symbols()

    #     initial = 0
    
    # else:
        # initializes negative infinity as best score
    best_score = float('-inf')
    best_move = None

    # iterate through all possible moves
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # check if the current tile is empty
            if board[i][j] == ' ':
                board[i][j] = computer_symbol
                # evaluate its score through minmax algorithm
                score = minmax(0, False, float('-inf'), float('inf'))

                # undo
                board[i][j] = ' '

                # update best score and move if score > best_score
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    # apply the best move
    if best_move:
        i, j = best_move
        board[i][j] = computer_symbol
        draw_symbols()

        # checks if turn is a winning move
        if is_winner(computer_symbol):
            messagebox.showinfo("Game Over", "Computer Wins!")
            root.quit()
        elif is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            root.quit()


def minmax(depth, is_maximizing_player, alpha, beta):
    # checks for board status
    score = evaluate()

    # there is already a winner
    if score == 1 or score == -1:
        return score

    # game is already draw
    if is_board_full():
        return 0

    # code block for max
    if is_maximizing_player:
        # m = neg_inf
        best_score = float('-inf')

        # iterate through all possible moves
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                # check if current tile is empty
                if board[i][j] == ' ':
                    # make hypothetical move
                    board[i][j] = computer_symbol

                    # recursively evaluate move and update the best score
                    score = minmax(depth + 1, False, alpha, beta)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)

                    if beta <= alpha:
                        break

        return best_score
    # code block for min
    else:
        # m = pos_inf
        best_score = float('inf')

        # iterate through all possible moves
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                # check if the current tile is empty
                if board[i][j] == ' ':
                    # make hypothetical move
                    board[i][j] = player_symbol
                    # recursively evaluate the move and update best score
                    score = minmax(depth + 1, True, alpha, beta)
                    board[i][j] = ' '

                    best_score = min(score, best_score)
                    beta = min(beta, best_score)

                    if beta <= alpha:
                            break

        return best_score

# function for checking if there is already a winner or draw
def evaluate():
    # player wins
    if is_winner(player_symbol):
        return -1
    # computer wins
    elif is_winner(computer_symbol):
        return 1
    # draw
    else:
        return 0

# function for player moves
def make_player_move(row, col):
    # draws player symbol to the button
    if board[row][col] == ' ':
        board[row][col] = player_symbol
        draw_symbols()

        # checks if the move is a winning turn
        if is_winner(player_symbol):
            messagebox.showinfo("Game Over", "Player Win!")
            root.quit()
        # checks if the board is already a draw
        elif is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            root.quit()

        make_computer_move()

# function for resetting the board
def reset_game():
    # global initial
    global board
    # initial = 1
    board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    draw_board()

# function for quitting
def quit_game():
    root.quit()

# initial drawing of board
draw_board()

# reset button
reset_button = tk.Button(root, text="RESET", command=reset_game, bg="red", fg="white", font=("Arial", 15, "bold"))
reset_button.grid(row=BOARD_SIZE, column=0)

# text label
tic_tac_toe_label = tk.Label(root, text="TIC-TAC-TOE", font=("Arial", 20, "bold"), fg="white", bg=BACKGROUND_COLOR)
tic_tac_toe_label.grid(row=BOARD_SIZE, column=1)

# quit button
quit_button = tk.Button(root, text="QUIT", command=quit_game, bg="red", fg="white", font=("Arial", 15, "bold"))
quit_button.grid(row=BOARD_SIZE, column=2, pady=10)

# asks if player wants to play 'X' or 'O'
player_choice = messagebox.askquestion("Choose Symbol", "Do you want to be 'X'?", icon='question')

# changes the initialized symbols if player decides to be player O
if player_choice == 'yes':
    player_symbol = 'X'
    computer_symbol = 'O'
else:
    player_symbol = 'O'
    computer_symbol = 'X'
    make_computer_move()


root.mainloop()
