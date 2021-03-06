class Player(object):
    def __init__(self, colour, name, all_pieces):
        self.colour = colour
        self.name = name
        # Starts off at 0. When a player moves a piece, it goes up by one.
        # When it goes up to 3, their turn automatically ends.
        self.turnstaken = 0
        # When it is their turn, it is changed to 1. It is decreased when a
        # Piece moves but it is incremented if you kill a piece/roll a 6.
        self.turn_token = False
        self.rollstaken = 0
        self.diceroll_token = True  # Allows player to roll dice once a roll(Mini-Turn)
        self.specialmove = False  # Allows player to roll dice after landing piece on opposing players piece.
        self.ALL_PIECES = all_pieces
        self.movable_pieces_array = []
        if self.colour == "red":
            self.start = 0
            self.end = 51
            self.low_range = 0 #Is used for move_piece function
        elif self.colour == "green":
            self.start = 13
            self.end = 11
            self.low_range = 4#Is used for move_piece function
        elif self.colour == "yellow":
            self.start = 26
            self.end = 24
            self.low_range = 8#Is used for move_piece function
        elif self.colour == "blue":
            self.start = 39
            self.end = 37
            self.low_range = 12#Is used for move_piece function
        self.my_pieces = []
        for piece in self.ALL_PIECES:
            if self.colour == piece.colour:
                self.my_pieces += [piece]
                piece.set_my_player(self)
        self.roll = 0
