import TicTacToeAI as AI

class TicTacToe:
    def __init__(self):
    # "board" is a list of 10 strings representing the board (ignore index 0)
        self.board = [" "]*10
        self.board[0]="#"
        self.turn = "x"
        

    def drawBoard(self):
    # This method prints out the board with current plays adjacent to a board with index.
        print('')
        print(' {} | {} | {} \t 1 | 2 | 3 '.format(
        self.board[1], self.board[2], self.board[3]))        
        print('-'*11 + '\t' + '-'*11)
        print(' {} | {} | {} \t 4 | 5 | 6 '.format(
        self.board[4], self.board[5], self.board[6]))
        print('-'*11 + '\t' + '-'*11)
        print(' {} | {} | {} \t 7 | 8 | 9 '.format(
        self.board[7], self.board[8], self.board[9]))
        print('')


    def boardFull(self):
    # This method checks if the board is already full and returns True. 
    # Returns false otherwise
        return ' ' not in self.board
    

    def cellIsEmpty(self, cell):
        if cell in range(1,10):
            return self.board[cell] == ' '
        else:
            return False


    def assignMove(self, cell):
    # assigns the cell of the board to the character ch
        self.board[cell] = self.turn
        self.changeTurn()
        

    def whoWon(self):
    # returns the symbol of the player who won if there is a winner,
    # otherwise it returns an empty string. 
        if self.isWinner("x"):
            return "x"
        elif self.isWinner("o"):
            return "o"
        else:
            return ""


    def isWinner(self, ch):
    # Given a player's letter, this method returns True if that player has won.
        lines = ['123', '456', '789', '147', '258', '369', '159', '357']
        for line in lines:
            did_win = True
            for cell in line:
                if self.board[int(cell)] != ch:
                    did_win = False
            if did_win:
                return True
        return False


    def changeTurn(self):
        if self.turn == "x":
            self.turn = "o"
        else:
            self.turn = "x"


    
def main():
    game = TicTacToe()
    game.drawBoard()
    game_over = False
    
    while not game_over:
        try:
            user_input = int(input(
            'It is the turn for {}. What is your move? '.format(game.turn)))
        except:
            continue
        if user_input == 41 :
            AI.playTurn(game)
        elif user_input == 90 :
            game_over = True
            continue 
        elif user_input in range(1,10):
            if not game.cellIsEmpty(user_input):
                continue
            game.assignMove(user_input)
        else:
            continue
        
        game.drawBoard()
        
        whoWon = game.whoWon()
        if whoWon:
            game_over = True
            print('{} wins. Congrats!'.format(whoWon))
        else:
            if game.boardFull():
                game_over = True
                print("It's a tie.")


main()
