import math

class TicTacToeAI:
    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent

    def get_empty_cells(self, board):
        """Returns a list of empty cells (row, col) on the board."""
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    empty_cells.append((i, j))
        return empty_cells

    def check_winner(self, board, player):
        """Checks if the given player has won the game."""
        # Check rows
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return True

        # Check columns
        for j in range(3):
            if all(board[i][j] == player for i in range(3)):
                return True

        # Check diagonals
        if all(board[i][i] == player for i in range(3)):
            return True
        if all(board[i][2 - i] == player for i in range(3)):
            return True

        return False

    def is_board_full(self, board):
        """Checks if the board is full."""
        for row in board:
            if ' ' in row:
                return False
        return True

    def minimax(self, board, depth, is_maximizing):
        """Minimax algorithm to find the best move."""
        if self.check_winner(board, self.player):
            return 1
        if self.check_winner(board, self.opponent):
            return -1
        if self.is_board_full(board):
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i, j in self.get_empty_cells(board):
                board[i][j] = self.player
                score = self.minimax(board, depth + 1, False)
                board[i][j] = ' '  # Undo the move
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = math.inf
            for i, j in self.get_empty_cells(board):
                board[i][j] = self.opponent
                score = self.minimax(board, depth + 1, True)
                board[i][j] = ' '  # Undo the move
                best_score = min(best_score, score)
            return best_score

    def get_best_move(self, board):
        """Returns the best move for the AI."""
        best_score = -math.inf
        best_move = None

        for i, j in self.get_empty_cells(board):
            board[i][j] = self.player
            score = self.minimax(board, 0, False)
            board[i][j] = ' '  # Undo the move

            if score > best_score:
                best_score = score
                best_move = (i, j)

        return best_move

def print_board(board):
    """Prints the Tic Tac Toe board."""
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def play_game():
    """Plays a game of Tic Tac Toe with the AI."""
    board = [[' ' for _ in range(3)] for _ in range(3)]
    player_symbol = 'X'
    ai_symbol = 'O'
    ai = TicTacToeAI(ai_symbol, player_symbol)

    current_player = player_symbol

    while True:
        print_board(board)

        if current_player == player_symbol:
            while True:
                try:
                    row = int(input("Enter row (0, 1, 2): "))
                    col = int(input("Enter column (0, 1, 2): "))
                    if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == ' ':
                        board[row][col] = player_symbol
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter numbers.")

        else:
            print("AI's turn...")
            row, col = ai.get_best_move(board)
            board[row][col] = ai_symbol

        if ai.check_winner(board, player_symbol):
            print_board(board)
            print("You win!")
            break
        elif ai.check_winner(board, ai_symbol):
            print_board(board)
            print("AI wins!")
            break
        elif ai.is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break

        current_player = ai_symbol if current_player == player_symbol else player_symbol

if __name__ == "__main__":
    play_game()