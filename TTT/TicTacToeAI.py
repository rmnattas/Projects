# Oct 2018
import random

def playTurn(game):
    orig = game.board[:]
    AIPlayer = game.turn
    move = findBestMove(game, AIPlayer)
    game.board = orig[:]      
    game.turn = AIPlayer
    game.assignMove(move)


def findBestMove(game, AIPlayer):
    orig = game.board[:]
    orig_turn = game.turn
    play_tree = {}
    empty_cells = spaces_in_board(game.board)

    # win move
    if len(empty_cells) != 9:
        move = winMove(game, AIPlayer)
        if move:
            print("Win Move!!!")
            return move

    # block opponent
    if len(empty_cells) != 9:
        move = blockOpponent(game, AIPlayer)
        if move:
            print("Block Opponent!!!")
            return move
    
    # best move by stat
    for empty_cell in empty_cells:
        game.assignMove(empty_cell)
        play_tree[empty_cell] = findMoveStat(game, AIPlayer)
        game.board = orig[:]
        game.turn = orig_turn
    print_tree(play_tree)
    move = selectBestMove(play_tree)
    return move


def findMoveStat(game, AIPlayer):
    orig = game.board[:]
    orig_turn = game.turn
    move_status = [0,0,0]

    # Base case
    whoWon = game.whoWon()
    if whoWon:
        if whoWon == AIPlayer:
            move_status[0] += 1
            return move_status
        else:
            move_status[2] += 1
            return move_status
    elif game.boardFull():
        move_status[1] += 1
        return move_status

    empty_cells = spaces_in_board(game.board)
    for empty_cell in empty_cells:
        game.assignMove(empty_cell)
        status = findMoveStat(game, AIPlayer)
        move_status = array_add(move_status, status)
        game.board = orig[:]
        game.turn = orig_turn

    return move_status


def winMove(game, AIPlayer):
    orig = game.board[:]
    orig_turn = game.turn
    play_percent = {}

#   check returning orig turn

    # get moves stat
    empty_cells = spaces_in_board(game.board)
    for empty_cell in empty_cells:
        game.assignMove(empty_cell)
        percent = calc_percentage(findMoveStat(game, AIPlayer))
        play_percent[empty_cell] = percent
        game.board = orig[:]
        game.turn = orig_turn

    # if move win stat is 100%
    for cell, percent in play_percent.items():
        if percent == 100.0:
            return cell

    return False


def blockOpponent(game, AIPlayer):
    orig = game.board[:]
    orig_turn = game.turn
    play_percent = {}

    # set opponent
    if AIPlayer == "x":
        opponent = "o"
    else:
        opponent = "x"

    # get opponent moves stat
    empty_cells = spaces_in_board(game.board)
    for empty_cell in empty_cells:
        game.turn = opponent
        game.assignMove(empty_cell)
        percent = calc_percentage(findMoveStat(game, opponent))
        play_percent[empty_cell] = percent
        game.board = orig[:]
    game.turn = orig_turn

    # if opponent win move stat is 100%
    for cell, percent in play_percent.items():
        if percent == 100.0:
            return cell

    return False



def selectBestMove(play_tree):
    maxWinMove = 0
    maxWinPrecentage = 0
    
    for play_key in play_tree.keys():
        percentage = calc_percentage(play_tree[play_key])
        if percentage > maxWinPrecentage:
            maxWinPrecentage = percentage
            maxWinMove = play_key

    if maxWinMove == 0:
        maxWinMove = random.choice(list(play_tree.keys()))

    return maxWinMove




def spaces_in_board(board):
    empty_cells = []
    for i in range(1, len(board)):
        if board[i] == " ":
            empty_cells.append(i)
    return empty_cells


def array_add(A, B):
    C = []
    for i in range(len(A)):
        C.append(A[i] + B[i])
    return C


def calc_percentage(stat):
    total = (stat[0] + stat[1] + stat[2])
    percentage = (stat[0]/total)*100
    return percentage



def print_tree(tree):
    print("cell\twin\ttie\tlose\twin %")
    for key in tree.keys():
        print("{}\t{}\t{}\t{}\t{:.2f}".format(
        key, tree[key][0],
        tree[key][2], tree[key][2],
        float(calc_percentage(tree[key]))))



