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
# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):
    def __init__(self, symbol, depth): super(MinimaxPlayer, self).__init__(symbol)

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
def getMove(self, board):
    move, val = self.minmax(board, self.symbol, self.depth)
    return move

def minmax(self, board, turn, depth):
    legalMoves = game_rules.getLegalMoves(board, turn)
    if depth <= 0 or len(legalMoves) < 1:
        return None, self.h1(board, turn)

    best_move = None
    if turn == self.symbol:
        best_val = NEG_INF
    else:
        best_val = POS_INF

    for move in legalMoves:
        next_board = game_rules.makeMove(board, move)
        m, next_val = self.minmax(next_board, 'o' if turn == 'x' else 'x', depth-1)
        if turn == self.symbol and next_val > best_val:
            best_val = next_val
            best_move = move
        elif turn != self.symbol and next_val < best_val:
            best_val = next_val
            best_move = move

    return best_move, best_val



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
    move, val = self.ab_max(board, self.symbol, NEG_INF, POS_INF, self.depth)
    return move

def ab_max(self, board, turn, alpha, beta, depth):
    legal_moves = game_rules.getLegalMoves(board, turn)
    if depth <= 0 or len(legal_moves) < 1:
        return None, self.h1(board, turn)

    best_move = None
    opt = NEG_INF
    for move in legal_moves:
        next_board = game_rules.makeMove(board, move)
        m, val = self.ab_min(next_board, 'o' if turn == 'x' else 'x', alpha, beta, depth-1)
        if val > opt:
            opt = val
            best_move = move
        alpha = max(alpha, opt)
        if beta <= alpha:
            break
    return best_move, opt

def ab_min(self, board, turn, alpha, beta, depth):
    legal_moves = game_rules.getLegalMoves(board, turn)
    if depth <= 0 or len(legal_moves) < 1:
        return None, self.h1(board, turn)

    best_move = None
    opt = POS_INF
    for move in legal_moves:
        next_board = game_rules.makeMove(board, move)
        m, val = self.ab_max(next_board, 'o' if turn == 'x' else 'x', alpha, beta, depth-1)
        if val < opt:
            opt = val
            best_move = move
        beta = min(beta,opt)
        if beta <= alpha:
            break
    return best_move,opt



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
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)