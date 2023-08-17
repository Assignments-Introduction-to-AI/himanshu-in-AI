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
        self.depth = depth

    # Leave these two functions alone.
    def selectInitialX(self, board): 
        return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: 
            return legalMoves[0]
        else: 
            return self.get_max_move_value(board, self.depth, self.symbol)[1]

    def get_max_move_value(self, board, depth, symbol):
        """
        Function to get the max move value.\n
        Args:\n
            board = State of board when the function is called.\n
            depth = depth on which we want the max value.\n
            symbol = checker key on which the player is playing.\n
        Returns:\n
            max value
        """

        legal_moves = game_rules.getLegalMoves(board, symbol)
        # Condition to check whether we have reached the root node of the min max tree
        if depth == 0 or len(legal_moves) == 0: # This also checks whether we have any more legal moves or not
            return (self.h1(board, symbol), None)
        best = (NEG_INF, None)

        for move in legal_moves:
            board_state = game_rules.makeMove(board, move) # new board state after the move is made
            if symbol == 'x':
                value = self.get_min_move_value(board_state, depth-1, symbol= 'o')[0]
            else:
                value = self.get_min_move_value(board_state, depth-1, symbol='x')[0]
            
            if value > best[0]: # Storing the max value from all the min values
                best = (value, move)
        return best

    def get_min_move_value(self,board, depth, symbol):
        """
        Function to get the min move value.\n
        Args:\n
            board = State of board when the function is called.\n
            depth = depth on which we want to the max value.\n
            symbol = checker key on which the player is playing.\n
        Returns:\n
            min value\n
        """
        legal_moves = game_rules.getLegalMoves(board, symbol)
        # Condition to check whether we have reached the root node of the min max tree
        if depth == 0 or len(legal_moves) == 0: # This also checks whether we have any more legal moves or not
            return (self.h1(board, symbol), None)
        best = (POS_INF, None)       

        for move in legal_moves:
            board_state = game_rules.makeMove(board,move)
            if symbol == 'x':
                value = self.get_max_move_value(board_state, depth-1, symbol= 'o')[0]
            else:
                value = self.get_max_move_value(board_state, depth-1, symbol='x')[0]

        if best[0] > value: # Stroing the min value from all the max values
            best = (value,move) 
            
        return best
    
# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth): 
        super(AlphaBetaPlayer, self).__init__(symbol)

    # Leave these two functions alone.
    def selectInitialX(self, board): 
        return (0,0)
    
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None

    def get_max_move_value(self, board, depth, lower_bound, upper_bound, symbol):
        """
        Function to implement the max move with alpha prunning.\n
        Args:\n
            board = State of board when the function is called.\n
            depth = depth on which we want the max value.\n
            symobl = checker key on which the player is playing.\n
        Returns:\n
            max value
        """

        legal_moves = game_rules.getLegalMoves(board, symbol)
        # Condition to check whether we have reached the root node of the min max tree
        if depth == 0 or len(legal_moves) == 0:
            return (self.h1(board, symbol), None)
        
        best = (NEG_INF, None)

        for move in legal_moves:
            board_state = game_rules.makeMove(board, move)
            if symbol == 'x':
                value = self.get_min_move_value(board_state, depth -1, 
                                                lower_bound, upper_bound, symbol='o')[0]
            else:
                value = self.get_min_move_value(board_state, depth-1, lower_bound, 
                                                upper_bound, symbol='x')[0]
                
            if best[0] < value:
                best = (value, move) # as we are finding maximum
            
            if best[0] >= upper_bound:
                return best # Beta prunning
            
            if best[0] < lower_bound:
                lower_bound = best[0] # This will change the lower bound to new value

        return best

    def get_min_move_value(self, board, depth, lower_bound, upper_bound, symbol):
        """
        Function to implement the max move with beta prunning.\n
        Args:\n
            board = State of board when the function is called.\n
            depth = depth on which we want the min value.\n
            symobl = checker key on which the player is playing.\n
        Returns:\n
            min value
        """

        legal_moves = game_rules.getLegalMoves(board, symbol)
        # Condition to check whether we have reached the root node of the min max tree
        if depth == 0 or len(legal_moves) == 0:
            return (self.h1(board, symbol), None)
        
        best = (POS_INF, None)

        for move in legal_moves:
            board_state = game_rules.makeMove(board,move)
            if symbol == 'x':
                value = self.get_max_move_value(board_state, depth-1, lower_bound, upper_bound, symbol='o')[0]

            else:
                value = self.get_max_move_value(board_state, depth-1, lower_bound, upper_bound, symbol='x')[0]

            if best[0] > value:
                best = (value, move)

            if best[0] >= upper_bound:
                upper_bound = best[0]

            if best[0] < lower_bound:
                return best
            
        return best

            





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
        else:

            return None


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