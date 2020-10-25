from board import Board
import copy

class Game:
    def __init__(self, board, player, last_move_made):
        self.board = board
        self.current_player = 0
        self.last_move = ((),())
        self.player_piece = ('B', 'W')
        self.end_the_game = 0
    
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
                            copy = copy.deepcopy(self.board) #Make copy so we don't ruin current state of board
                            copy.updateBoard(next_start, next_end) #"Simulate" a move
                            same_direction_move = dir(next_end) # Move in the same direction again
                            new_state = Game(copy, current_player) #make a new game state and see if same move is legal
                            while(new_state.is_legal_move(current_player, same_direction_move)):
                                current_start = next_end #Reassigns the start
                                next_end = same_direction_move[1] # Reassigns the end
                                moves.append((next_start, next_end)) #adds move to possible moves
                                copy = copy.deepcopy(copy) #Make new board
                                copy.updateBoard(current_start, next_end) #Update move
                                same_direction_move = dir(next_end) #Move piece
                                new_state = Game(copy, current_player) #Create new state
        return moves

    def is_legal_move(self, player, move):
        start = move[0] #before moving
        end = move[1] #after moving
        
        if end[0] > 8 or end[1] < 8: #Out of range
            return False
        if self.board.rowIndex[end[0]][end[1]] != ".": # Checks if end spot is empty
            return False
        return True

    def player_playing(self):
        try:
            moves = self.find_moves(self.current_player)
            print("Possible Moves:")
            print(moves)
            if(len(moves) == 0): # if no more moves left, end the game
                print("Player lost the game")
                self.end_the_game = 1
            else:
                is_valid = False
                while is_valid = False: # get valid input from player
                    move_coord = (input("Coordinate of piece: "), input("Coordinate to move piece: "))
                    move_coord = ((move_coord[0][0] - 1, move_coord[0][1] - 1), (move_coord[1][0] - 1, move_coord[1][1] - 1)) # adjust to be zero index
                    is_valid_input = move_coord in moves

        except KeyboardInterrupt:
            raise
        except:
            print("Please provide valid input") # if invalid input
            self.player_playing()



    def ai_playing(self):
        return 0 #placeholder for compilation
    
    def get_successors(self):
        successors = []
        for move in self.find_moves(self.current_player):
            copy = copy.deepcopy(self.board) #Copy so we don't edit the board
            copy.updateBoard(move[0], move[1]) #Makes a predicted move
            successors.append(Game(copy, 1 - self.current_player, move)) #adds move to successor moves
        return successors


