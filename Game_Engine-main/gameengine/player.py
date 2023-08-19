import game_rules, random
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):
    def __init__(self, symbol, depth):
        super(MinimaxPlayer, self).__init__(symbol)
        self.depth=depth

    # Leave these two functions alone.
    def selectInitialX(self, board):
        return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]
    
    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or game_rules.isGameOver(board):
            return self.evaluate(board)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in game_rules.getLegalMoves(board, self.symbol):
                new_board = game_rules.makeMove(board, self.symbol, move)
                eval = self.minimax(new_board, depth - 1, False)
                if eval >= max_eval:  # Use >= for consistency
                    max_eval = eval
                    best_move = move
            return best_move  # Return only the best_move
        else:
            min_eval = float('inf')
            best_move = None  # Initialize best_move here
            for move in game_rules.getLegalMoves(board, game_rules.getOpponentSymbol(self.symbol)):
                new_board = game_rules.makeMove(board, game_rules.getOpponentSymbol(self.symbol), move)
                eval = self.minimax(new_board, depth - 1, True)
                if eval <= min_eval:  # Use <= for consistency
                    min_eval = eval
                    best_move = move
            return best_move  # Return only the best_move

    # Edit this one here. :)
    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0:
            best_move = self.minimax(board, self.depth, True)
            return best_move
        else:
            return None



# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth): super(AlphaBetaPlayer, self).__init__(symbol)

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedError('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedError('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedError('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedError('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)
