class Game:
    def __init__(self, board, player, last_move_made):
        self.board = board
        self.current_player = 0
        self.last_move_made = ((),())
        self.player_piece = ('X', 'O')
        self.end_game = 0
    
    @staticmethod
    def NORTH(position):
        return (position, (pos[0] - 2, pos[1]))
    
    @staticmethod
    def SOUTH(position):
        return (position, (pos[0] + 2, pos[1]))
    
    @staticmethod
    def EAST(position):
        return (position, (pos[0], pos[1] + 2))
    
    @staticmethod
    def WEST(position):
        return (position, (pos[0], pos[1] - 2))

    def get_legal_moves(self, current_player)
        legal_moves = [] #array with all possible moves for current player
        for i in range(8): #loop through rows
            for j in range(8): #loop through columns
                if self.board.rowIndex[i][j] == self.player_piece[current_player]: #if the selected piece belongs to current player
                    current_position = (i, j) #current position tuple
                    directions = [self.NORTH, self.SOUTH, self.EAST, self.WEST] #ways player can move
                    for dir in directions: #check all direction possibilities
                        possible_move = dir(current_position)
                        #NEED TO CHECK IF MOVE IS LEGAL????


