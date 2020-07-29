import bin.settings as settings
# Adds default checks for the move function
def move(move_func):

    def wrapper(instance, tile, board):
        if board.get_piece(tile) != None:
            if board.get_piece(tile).colour == instance.colour:
                raise ChessHandler.WrongMove("Can't capture an ally")
        if (board.turn == instance.colour) == False:
            raise ChessHandler.WrongMove("Not your turn")
            return
        move_func(instance, tile, board)


    return wrapper


class ChessHandler:
    # Returns the origin and destination from a user's move
    @staticmethod
    def parse(input):
        try:
            original = str(list(input)[0])+str(list(input)[1])
            destination = str(list(input)[2])+str(list(input)[3])
        except IndexError as e:
            raise ChessHandler.WrongMove(str(e))
            return None
        return original, destination
    # Convert tile format (A1) to coordinate (1, 1)
    @staticmethod
    def tile_to_coordinate(tile):
        num = int(list(tile)[1])
        let = ChessHandler.letter_to_number(list(tile)[0])
        return (let, num)
    # Find the x and y offset for a two diagonal points
    @staticmethod
    def get_offset(origin, destination):
        # --
        if origin[0] - destination[0] > 0: x_offset = -1
        else: x_offset = 1
        if origin[1] - destination[1] > 0: y_offset = -1
        else: y_offset = 1
        offset = (x_offset, y_offset)
        return offset
    # Find the x and y offset for two aligned points
    @staticmethod
    def get_direct_offset(oldc, newc):
        # --
        if newc[0] - oldc[0] > 0: offset = (1, 0)
        if newc[0] - oldc[0] < 0: offset = (-1, 0)
        if newc[1] - oldc[1] > 0: offset = (0, 1)
        if newc[1] - oldc[1] < 0: offset = (0, -1)
        return offset
    # Converts coordinate format (1, 1) to tile format (A1)
    @staticmethod
    def get_tile_from_coordinate(coordinate):
        letter = str.upper(chr(coordinate[0]+96))
        tile = str(letter) + str(coordinate[1])
        return tile
    # Converts a letter to a number
    @staticmethod
    def letter_to_number(letter):
        return ord(str.lower(letter)) - 96
    # Converts tile format (A1) to PyGame positions (40, 510)
    @staticmethod
    def get_position(tile):
        tile = list(tile)
        list_pos = []
        dict_letter = {
        "A": 40,
        "B": 110,
        "C": 175,
        "D": 243,
        "E": 308,
        "F": 376,
        "G": 442,
        "H": 510
        }
        dict_number = {
        "1": 510,
        "2": 442,
        "3": 376,
        "4": 308,
        "5": 243,
        "6": 175,
        "7": 110,
        "8": 40
        }
        if tile[0] in dict_letter:
            list_pos.append(dict_letter[tile[0]])
        if tile[1] in dict_number:
            list_pos.append(dict_number[tile[1]])
        if len(list_pos)>1: return list_pos
        else: return None

    class Piece:

        def __init__(self, **kwargs):
            self.tile = kwargs.pop('tile', True)
            self.colour = kwargs.pop('colour', True)
            self.sprite = kwargs.pop('image', True)
            self.has_moved = False
        # Default move implementation
        def _move(self, tile):
            self.tile = tile
            if not self.has_moved: self.has_moved = True
        # Check if a certain tile is in front
        def _isinfront(self, tile):
            if list(self.tile)[0] == list(tile)[0]:
                og_num = int(list(self.tile)[1])
                new_num = int(list(tile)[1])
                if self.colour == 'w':
                    if new_num - og_num == 1: return True
                    else: return False
                elif self.colour == 'b':
                    if og_num - new_num == 1: return True
                    else: return False
            else:
                return False
        # Check if the tile is in a diagonal and is blocked by no pieces
        def _isdirectdiagonal(self, tile, board):
            # Obtain coordinate tuple
            oldc = ChessHandler.tile_to_coordinate(self.tile)
            newc = ChessHandler.tile_to_coordinate(tile)
            # Check if the tile is diagonal
            if abs(oldc[0]-newc[0]) == abs(oldc[1]-newc[1]):
                # Obtain the offset to loop with
                offset = ChessHandler.get_offset(oldc, newc)
                # Get a muteable list to loop over
                loop_load = list(oldc)
                count = 0
                # looping until we arrive at the right tile
                while True:
                    # Incrementing
                    loop_load[0]+=offset[0]
                    loop_load[1]+=offset[1]
                    # Finding the tile from the coords
                    cache_tile = ChessHandler.get_tile_from_coordinate(loop_load)
                    # Checking if we've finished
                    if cache_tile == tile:
                        return True
                    # Checking if there is a piece there
                    if board.get_piece(cache_tile) != None:
                        return False
                    # Checking if we've gone out of bounds
                    if count>10:
                        raise ChessHandler.WrongMove("Outside the board")
                        break
                    count+=1
            return False
        # Check if the tile is in a straight line and is blocked by no pieces
        def _isdirectlign(self, tile, board):
            # Obtain the coordinates
            oldc = ChessHandler.tile_to_coordinate(self.tile)
            newc = ChessHandler.tile_to_coordinate(tile)
            # Check if it's in a straight line
            if oldc[0] == newc[0] or oldc[1] == newc[1]:
                # List to loop over
                loop_load = list(oldc)
                # Offset to loop with
                offset = ChessHandler.get_direct_offset(oldc, newc)
                # Defining count before referencing it
                count = 0
                while True:
                    # Incrementing
                    loop_load[0]+=offset[0]
                    loop_load[1]+=offset[1]
                    # Obtaining the tile
                    cache_tile = ChessHandler.get_tile_from_coordinate(loop_load)
                    # Checking if we're finished
                    if cache_tile == tile:
                        return True
                    # Checking if there's a piece there
                    if board.get_piece(cache_tile) != None:
                        return False
                    # Checking if we've gone out of bounds
                    if count>10:
                        raise ChessHandler.WrongMove("Outside the board")
                        break
                    count+=1
            return False

        def _iscapture(self, tile, board):
            # Sugar code for "if board.get_piece != None:" replaced by if self._iscapture(tile, board)
            if board.get_piece(tile) != None:
                return True
            else:
                return False



    class Pawn(Piece):
        # Check if this is a pawn double move
        def _isdoublemove(self, tile):
            if self.has_moved == False:
                if list(self.tile)[0] == list(tile)[0]:
                    og_num = int(list(self.tile)[1])
                    new_num = int(list(tile)[1])
                    if self.colour == 'w':
                        if new_num - og_num == 2: return True
                        else: return False
                    elif self.colour == 'b':
                        if og_num - new_num == 2: return True
                        else: return False
                else:
                    return False
            else:
                return False
            pass
        # Check if this is a pawn capture
        def _iscapture(self, tile, board):
            og_num = int(list(self.tile)[1])
            new_num = int(list(tile)[1])
            og_numlet = ChessHandler.letter_to_number(list(self.tile)[0])
            new_numlet = ChessHandler.letter_to_number(list(tile)[0])
            if board.get_piece(tile) != None:
                if self.colour == 'w':
                    if new_num - og_num == 1:
                        if og_numlet == (new_numlet+1) or og_numlet == (new_numlet-1):
                            return True
                elif self.colour == 'b':
                    if og_num - new_num == 1:
                        if og_numlet == (new_numlet+1) or og_numlet == (new_numlet-1):
                            return True
            return False

        @move
        def _move(self, tile, board):
            if self._isinfront(tile) == True or self._isdoublemove(tile) == True or self._iscapture(tile, board) == True:
                # print (self._iscapture(tile, board))
                if self._iscapture(tile, board) == True:
                    piece = board.get_piece(tile)
                    # print(piece)
                    piece.tile = 'xx'
                self.tile = tile
                coords = ChessHandler.tile_to_coordinate(self.tile)
                if self.colour == 'w':
                    if coords[1] == 8:
                        img = board._image(settings.WHITE_QUEEN, settings.DEFAULT_SIZE)
                        queen = ChessHandler.Queen(tile=self.tile, colour="w", image=img)
                        self.tile = 'xx'
                        board.pieces.append(queen)
                if self.colour == 'b':
                    if coords[1] == 1:
                        img = board._image(settings.BLACK_QUEEN, settings.DEFAULT_SIZE)
                        queen = ChessHandler.Queen(tile=self.tile, colour="b", image=img)
                        self.tile = 'xx'
                        board.pieces.append(queen)
                board._switch()
            else:
                raise ChessHandler.WrongMove("Illegal move")
            if self.has_moved == False:
                self.has_moved = True

    class Queen(Piece):
        @move
        def _move(self, tile, board):
            if self._isdirectdiagonal(tile, board) or self._isdirectlign(tile, board):
                if self._iscapture(tile, board) == True:
                    piece = board.get_piece(tile)
                    piece.tile = 'xx'
                self.tile = tile
                board._switch()
                if self.has_moved == False:
                    self.has_moved = True
            else:
                raise ChessHandler.WrongMove("Illegal Move")

        def can_attack(self, tile, board):
            if self.isdirectdiagonal(tile, board) or self._isdirectlign(tile, board): return True
            return False

    class Bishop(Piece):
        @move
        def _move(self, tile, board):
            if self._isdirectdiagonal(tile, board):
                if self._iscapture(tile, board) == True:
                    piece = board.get_piece(tile)
                    piece.tile = 'xx'
                self.tile = tile
                board._switch()
                if self.has_moved == False:
                    self.has_moved = True
            else:
                raise ChessHandler.WrongMove("Illegal Move")

        def can_attack(self, tile, board):
            if self.isdirectdiagonal(tile, board): return True
            return False

    class Rook(Piece):
        @move
        def _move(self, tile, board):
            if self._isdirectlign(tile, board):
                if self._iscapture(tile, board) == True:
                    piece = board.get_piece(tile)
                    piece.tile = 'xx'
                self.tile = tile
                board._switch()
                if self.has_moved == False:
                    self.has_moved = True
            else:
                raise ChessHandler.WrongMove("Illegal Move")

        def can_attack(self, tile, board):
            if self._isdirectlign(tile, board): return True
            return False

    class King(Piece):
        @move
        def _move(self, tile, board):
            if self._legalkingmove(tile, board):
                if self._iscapture(tile, board) == True:
                    piece = board.get_piece(tile)
                    piece.tile = 'xx'
                self.tile = tile
                board._switch()
                if self.has_moved == False:
                    self.has_moved = True
            else:
                raise ChessHandler.WrongMove("Illegal Move")

        def _legalkingmove(self, tile, board):
            oldc = ChessHandler.tile_to_coordinate(self.tile)
            newc = ChessHandler.tile_to_coordinate(tile)
            if abs(oldc[0] - newc[0]) < 2 and abs(oldc[1] - newc[1]) < 2:
                return True
            return False

    class Knight(Piece):
        @move
        def _move(self, tile, board):
            if self._legalknightmove(tile, board):
                if self._iscapture(tile, board) == True:
                    piece = board.get_piece(tile)
                    piece.tile = 'xx'
                self.tile = tile
                board._switch()
                if self.has_moved == False:
                    self.has_moved = True
            else:
                raise ChessHandler.WrongMove("Illegal Move")


        def _legalknightmove(self, tile, board):
            oldc = ChessHandler.tile_to_coordinate(self.tile)
            newc = ChessHandler.tile_to_coordinate(tile)
            if abs(oldc[0] - newc[0]) == 2 and abs(oldc[1] - newc[1]) == 1:
                return True
            if abs(oldc[0] - newc[0]) == 1 and abs(oldc[1] - newc[1]) == 2:
                return True
            return False


    class ChessError(Exception):
        pass

    class WrongMove(ChessError):
        def __init__(self, text):
            self.text =text
        def __str__(self):
            return "ChessHandler.WrongMove was raised for the following reason:\n{}".format(self.text)
