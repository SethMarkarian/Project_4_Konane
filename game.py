class Game:
    def __init__(self, board, player, last_move_made):
        self.board = board
        self.current_player = 0
        self.last_move_made = ((),())
        self.player_piece = ('B', 'W')
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

    def find_moves(self, current_player):
        moves = [] #array with all possible moves for current player
        for i in range(8): #loop through rows
            for j in range(8): #loop through columns
                if self.board.rowIndex[i][j] == self.player_piece[current_player]: #if the selected piece belongs to current player
                    current_position = (i, j) #current position tuple
                    directions = [self.NORTH, self.SOUTH, self.EAST, self.WEST] #ways player can move
                    for dir in directions: #check all direction possibilities
                        possible_move = dir(current_position)
                        if self.is_legal_move(possible_move):
                            moves.append(possible_move)
                            
                            #Check for multiple jumps
                            next_start = possible_move[0]
                            next_end = possible_move[1]
                            #HOW DO I SIMULATE A MOVE???????
        return moves

    def is_legal_move(self, player, move):
        start = move[0] #before moving
        end = move[1] #after moving
        
        if end[0] > 8 or end[1] < 8: #Out of range
            return False
        if self.board.rowIndex[end[0]][end[1]] != ".": # Checks if end spot is empty
            return False
        return True

    def ai_playing(self):
        moves = self.find_moves(self.current_player)

    def player_playing(self):
        return 0 #placeholder for compilation
