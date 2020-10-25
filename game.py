from board import Board
import copy
import random
import time

class Game:
    def __init__(self, board, player, last_move_made):
        self.board = board
        self.current_player = 0
        self.last_move = ((),())
        self.player_piece = ('B', 'W')
        self.end_the_game = 0
        self.ai_type = "random"
        self.total_ai_nodes = 0
        self.total_ai_time = 0
        self.total_cutoffs = 0
        self.total_branches = 0
        self.total_parents = 0
        self.total_static_eval = 0
    
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

    def ai_playing(self):
        start = time.time()
        moves = self.find_moves(self.current_player)
        if(len(moves) == 0):
            print("Player won the game")
            print("Total ai time: ", total_ai_time)
            print("Total ai nodes: ", total_ai_nodes)
            self.end_the_game = 1
        else:
            if(ai_type == "random"):
                move = random.choice(moves) # choose random move
                move = ((move[0][0] - 1, move[0][1] - 1), (move[1][0] - 1, move[1][1] - 1)) # adjust to be zero index
                self.board.updateBoard(move[0], move[1])
                print(self.board.str_board) # print board
                self.current_player = (1 + self.current_player) % 2 # swap player
                return
            elif(ai_type == "minimax"):
                print("minimax not done")
            elif(ai_type == "ab_pruning"):
                print ("ab pruning not done")
        end = time.time()
        total_ai_time = total_ai_time + end - start


    def player_playing(self):
        try:
            moves = self.find_moves(self.current_player) # find moves
            print("Possible Moves:")
            print(moves)
            if(len(moves) == 0): # if no more moves left, end the game
                print("Player lost the game")
                print("Total ai time: ", total_ai_time)
                print("Total ai nodes: ", total_ai_nodes)
                self.end_the_game = 1
            else:
                is_valid = False
                while is_valid == False: # get valid input from player
                    move_coord = (input("Coordinate of piece: "), input("Coordinate to move piece: "))
                    move_coord = ((move_coord[0][0] - 1, move_coord[0][1] - 1), (move_coord[1][0] - 1, move_coord[1][1] - 1)) # adjust to be zero index
                    is_valid_input = move_coord in moves
                self.board.updateBoard(move_coord[0], move_coord[1])
                print(self.board.str_board) # print board
                self.current_player = (1 + self.current_player) % 2 # swap player
        except KeyboardInterrupt:
            raise
        except:
            print("Please provide valid input") # if invalid input
            self.player_playing()

    def first_moves(self):
        try:
            decision = (input("Start or Divert to ai: "))
            if(decision == "Start"):
                remove = int(input("Choose 1, 4, 5, 8: "))
                if(remove == 1 or remove == 4 or remove == 5 or remove == 8):
                    remove = remove - 1 # adjust to zero index
                    remove_coord = (remove, remove)
                else:
                    "Please provide valid input"
                    self.first_moves()
                self.board.removePiece(self, remove_coord)
                print(self.board.str_board)
                if(remove_coord[0] == 0):
                    adjacent_coords = ((0, 1), (1, 0))
                elif(remove_coord[0] == 7):
                    adajcent_coords = ((7, 6), (6, 7))
                else:
                    adjacent_coords = ((remove, remove - 1), (remove - 1, remove), (remove, remove + 1), (remove + 1, remove))
                # adjacent_coords = ((remove, remove - 1), (remove - 1, remove), (remove, remove + 1), (remove + 1, remove))
                adjacent = random.choice(adjacent_coords)
                self.board.removePiece(self, adjacent)
                print(self.board.str_board)
                # then would start with player playing
            else:
                starts = ((0, 0), (3, 3), (4, 4), (7, 7))
                start_removal = random.choice(starts)
                self.board.removePiece(self, start_removal)
                print(self.board.str_board)
                if(start_removal[0] == 0):
                    adjacent_coords_output = ((1, 2), (2, 1))
                elif(start_removal_output[0] == 7):
                    adajcent_coords_output = ((8, 7), (7, 8))
                else:
                    adjacent_coords_output = ((remove + 1, remove), (remove, remove + 1), (remove + 1, remove + 2), (remove + 2, remove + 1))
                print("Legal inputs", adjacent_coords_output)
                input_coord = (-1, -1)
                while not(input_coord in adjacent_coords_output):
                    input_coord = (input("Please choose input coordinate: "))
                self.board.removePiece(self, (input_coord[0] - 1, input_coord[1] - 1)) # make zero index and remove
                print(self.board.str_board)
                # then would start with ai playing

        except:
            "Please provide valid input"
            self.first_moves()

    def get_successors(self):
        successors = []
        for move in self.find_moves(self.current_player):
            copy = copy.deepcopy(self.board) #Copy so we don't edit the board
            copy.updateBoard(move[0], move[1]) #Makes a predicted move
            successors.append(Game(copy, 1 - self.current_player, move)) #adds move to successor moves
        return successors


