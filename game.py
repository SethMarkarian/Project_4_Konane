class Game:
    def __init__(self, board, player, last_move_made):
        self.board = board
        self.current_player = 0
        self.last_move_made = ((),())
        self.player_piece = ('X', 'O')
        self.end_game = 0