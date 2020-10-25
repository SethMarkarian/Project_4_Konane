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
        #self.total_ai_nodes = 0
        #self.total_ai_time = 0
        self.total_cutoffs = 0
        self.total_branches = 0
        #self.total_parents = 0
        self.total_static_eval = 0
    
    @staticmethod
    def NORTH(position):
        return (position, (position[0] - 2, position[1]))
    
    @staticmethod
    def SOUTH(position):
        return (position, (position[0] + 2, position[1]))
    
    @staticmethod
    def EAST(position):
        return (position, (position[0], position[1] + 2))
    
    @staticmethod
    def WEST(position):
        return (position, (position[0], position[1] - 2))

    def find_moves(self, current_player):
        moves = [] #array with all possible moves for current player
        for i in range(8): #loop through rows
            for j in range(8): #loop through columns
                if self.board.rowIndex[i][j] == self.player_piece[current_player]: #if the selected piece belongs to current player
                    current_position = (i, j) #current position tuple
                    directions = [self.NORTH, self.SOUTH, self.EAST, self.WEST] #ways player can move
                    for dir in directions: #check all direction possibilities
                        possible_move = dir(current_position)
                        if self.is_legal_move(current_player, possible_move):
                            moves.append(possible_move)
                            
                            #Check for multiple jumps
                            next_start = possible_move[0]
                            next_end = possible_move[1]
                            copy_board = copy.deepcopy(self.board) #Make copy so we don't ruin current state of board
                            copy_board.updateBoard(next_start, next_end) #"Simulate" a move
                            same_direction_move = dir(next_end) # Move in the same direction again
                            new_state = Game(copy_board, current_player, same_direction_move) #make a new game state and see if same move is legal
                            while(new_state.is_legal_move(current_player, same_direction_move)):
                                current_start = next_end #Reassigns the start
                                next_end = same_direction_move[1] # Reassigns the end
                                moves.append((next_start, next_end)) #adds move to possible moves
                                copy_board = copy.deepcopy(copy_board) #Make new board
                                copy_board.updateBoard(current_start, next_end) #Update move
                                same_direction_move = dir(next_end) #Move piece
                                new_state = Game(copy_board, current_player, same_direction_move) #Create new state
        return moves

    def is_legal_move(self, player, move):
        start = move[0] #before moving
        end = move[1] #after moving
        
        if end[0] not in range(8) or end[1] not in range(8):	# Discard any generated moves that fall off of the board
			return False 
        if self.board.rowIndex[end[0]][end[1]] != ".": # Checks if end spot is empty
            return False
        return True

    def ai_playing(self):
        start = time.time()
        moves = self.find_moves(self.current_player)
        if(len(moves) == 0):
            print("Player won the game")
            #print("Total ai time: ", total_ai_time)
            #print("Total ai nodes: ", total_ai_nodes)
            self.end_the_game = 1
        else:
            if(self.ai_type == "random"):
                move = random.choice(moves) # choose random move
                move = ((move[0][0] - 1, move[0][1] - 1), (move[1][0] - 1, move[1][1] - 1)) # adjust to be zero index
                self.board.updateBoard(move[0], move[1])
                print(self.board.str_board()) # print board
                self.current_player = (1 + self.current_player) % 2 # swap player
                return
            elif(self.ai_type == "minimax"):
                depth_input = 4
                computer_move = minimax(self, float("-inf"), float("inf"), depth_input)
                computer_move = computer_move[1]
                if computer_move is not None:
                    self.board.updateBoard(computer_move[0], computer_move[1])
                    print("Made move: ", ((computer_move[0][0]+1, computer_move[0][1]+1), (computer_move[1][0]+1, computer_move[1][1]+1)))
                    self.last_move_made = computer_move
                    self.current_player = 1 - self.current_player
                    return
                    print("minimax not done")
            elif(self.ai_type == "ab_pruning"):
                print ("ab pruning not done")
        end = time.time()
        #total_ai_time = total_ai_time + end - start


    def player_playing(self):
        try:
            moves = self.find_moves(self.current_player) # find moves
            print("Possible Moves:")
            print(moves)
            if(len(moves) == 0): # if no more moves left, end the game
                print("Player lost the game")
                #print("Total ai time: ", total_ai_time)
                #print("Total ai nodes: ", total_ai_nodes)
                self.end_the_game = 1
            else:
                is_valid = False
                while is_valid == False: # get valid input from player
                    move_coord = (input("Coordinate of piece: "), input("Coordinate to move piece: "))
                    move_coord = ((move_coord[0][0] - 1, move_coord[0][1] - 1), (move_coord[1][0] - 1, move_coord[1][1] - 1)) # adjust to be zero index
                    is_valid_input = move_coord in moves
                self.board.updateBoard(move_coord[0], move_coord[1])
                print(self.board.str_board()) # print board
                self.current_player = (1 + self.current_player) % 2 # swap player
        except KeyboardInterrupt:
            raise
        except:
            print("Please provide valid input") # if invalid input
            self.player_playing()

    def first_moves(self):
        try:
            decision = raw_input("Start or Divert to ai: ")
            if(decision == "Start"):
                print("Start")
                remove = int(input("Choose 1, 4, 5, 8: "))
                if(remove == 1 or remove == 4 or remove == 5 or remove == 8):
                    remove = remove - 1 # adjust to zero index
                    remove_coord = (remove, remove)
                else:
                    "Please provide valid input"
                    self.first_moves()
                self.board.removePiece(remove_coord)
                print(self.board.str_board())
                if(remove_coord[0] == 0):
                    adjacent_coords = ((0, 1), (1, 0))
                elif(remove_coord[0] == 7):
                    adajcent_coords = ((7, 6), (6, 7))
                else:
                    adjacent_coords = ((remove, remove - 1), (remove - 1, remove), (remove, remove + 1), (remove + 1, remove))
                # adjacent_coords = ((remove, remove - 1), (remove - 1, remove), (remove, remove + 1), (remove + 1, remove))
                adjacent = random.choice(adjacent_coords)
                self.board.removePiece(adjacent)
                print(self.board.str_board())
                # then would start with player playing
            elif(decision == "Divert"):
                print("Divert")
                starts = ((0, 0), (3, 3), (4, 4), (7, 7))
                start_removal = random.choice(starts)
                self.board.removePiece(start_removal)
                print(self.board.str_board())
                if(start_removal[0] == 0):
                    adjacent_coords_output = ((1, 2), (2, 1))
                elif(start_removal[0] == 7):
                    adajcent_coords_output = ((8, 7), (7, 8))
                else:
                    adjacent_coords_output = ((start_removal + 1, start_removal), (start_removal, start_removal + 1), (start_removal + 1, start_removal + 2), (start_removal + 2, start_removal + 1))
                print("Legal inputs", adjacent_coords_output)
                input_coord = (-1, -1)
                while not(input_coord in adjacent_coords_output):
                    input_coord = (input("Please choose input coordinate: "))
                self.board.removePiece((input_coord[0] - 1, input_coord[1] - 1)) # make zero index and remove
                print(self.board.str_board())
                # then would start with ai playing
            else:
                print("Invalid input")
                self.first_moves()

        except Exception,e:
            print(str(e))
            print("Please provide valid input")
            self.first_moves()

    def get_successors(self):
        successors = []
        for move in self.find_moves(self.current_player):
            copy = copy.deepcopy(self.board) #Copy so we don't edit the board
            copy.updateBoard(move[0], move[1]) #Makes a predicted move
            successors.append(Game(copy, 1 - self.current_player, move)) #adds move to successor moves
        return successors


calls = 0
# num_branches = 0
# static_evaluation_count = 0
# total_cutoffs = 0
def minimax(state, alpha, beta, depth):
    #global total_cutoffs, num_branches, static_evaluation_count, total_cutoffs
    if depth == 4: #why 4 specifically???
        self.total_static_eval += 1
        return (state.static_evaluation(), None)
    elif state.current_player == 0:
        move = None
        calls += 1
        for successor_state in state.get_successors():
            num_branches += 1
            ab, player_move = minimax(successor_state, alpha, beta, depth + 1)
            if ab > alpha:
                alpha = ab
                move = successor_state.last_move_made
            if alpha >= beta:
                total_cutoffs += 1
                return (beta, move)
        return (alpha, move)
    else:
        move = None
        calls += 1
        for successor_state in state.get_successors():
            num_branches += 1
            ab, player_move = minimax(successor_state, alpha, beta, depth + 1)
            if be < beta:
                beta = ab
                move = successor_state.last_move_made
            if beta <= alpha:
                total_cutoffs += 1
                return (beta, move)
        return (beta, move)
    
def static_evaluation(self):
    player_moves = self.get_legal_moves(0)
    ai_moves = self.get_legal_moves(1)
    if ai_moves == 0:
        return float("inf")
    if player_moves == 0:
        return float("-inf")
    return len(player_moves) - len(ai_moves)
    
def play_game(game_state):
    print(game_state.board.str_board())
    #remove = input("B remove a piece: ")
    #game_state.board.removePiece((remove[0] - 1, remove[1] - 1))
    #print(game_state.board.str_board())
    #remove = input("W remove a piece: ")
    #game_state.board.removePiece((remove[0] - 1, remove[1] - 1))
    game_state.first_moves()
    while game_state.end_the_game != 1:
        if game_state.current_player == 0:
            game_state.ai_playing()
        else:
            game_state.player_playing()

    
    
if __name__ == '__main__':
	start = time.time()
	game = Game(Board(), None, None)
	play_game(game)
	print "Time elapsed: ", time.time() - start, " seconds"
	print "Static Evaluations: ", game.total_static_eval
	#print "Average branching factor: ", game.total_branches/(calls+0.0)
	print "Total cutoffs: ", game.total_cutoffs