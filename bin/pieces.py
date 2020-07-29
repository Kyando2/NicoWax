
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
    @staticmethod
    def parse(input):
        try:
            original = str(list(input)[0])+str(list(input)[1])
            destination = str(list(input)[2])+str(list(input)[3])
        except IndexError as e:
            raise ChessHandler.WrongMove(str(e))
            return None
        return original, destination

    @staticmethod
    def tile_to_coordinate(tile):
        num = int(list(tile)[1])
        let = ChessHandler.letter_to_number(list(tile)[0])
        return (let, num)

    @staticmethod
    def get_offset(origin, destination):
        # --
        if origin[0] - destination[0] > 0: x_offset = -1
        else: x_offset = 1
        if origin[1] - destination[1] > 0: y_offset = -1
        else: y_offset = 1
        offset = (x_offset, y_offset)
        return offset

    @staticmethod
    def get_direct_offset(oldc, newc):
        # --
        if newc[0] - oldc[0] > 0: offset = (1, 0)
        if newc[0] - oldc[0] < 0: offset = (-1, 0)
        if newc[1] - oldc[1] > 0: offset = (0, 1)
        if newc[1] - oldc[1] < 0: offset = (0, -1)
        return offset

    @staticmethod
    def get_tile_from_coordinate(coordinate):
        letter = str.upper(chr(coordinate[0]+96))
        tile = str(letter) + str(coordinate[1])
        return tile

    @staticmethod
    def letter_to_number(letter):
        return ord(str.lower(letter)) - 96

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

        def _move(self, tile):
            self.tile = tile
            if not self.has_moved: self.has_moved = True

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

        def _isdirectdiagonal(self, tile, board):
            oldc = ChessHandler.tile_to_coordinate(self.tile)
            newc = ChessHandler.tile_to_coordinate(tile)
            if abs(oldc[0]-newc[0]) == abs(oldc[1]-newc[1]):
                offset = ChessHandler.get_offset(oldc, newc)
                loop_load = list(oldc)
                payload = None
                count = 0
                while True:
                    loop_load[0]+=offset[0]
                    loop_load[1]+=offset[1]
                    cache_tile = ChessHandler.get_tile_from_coordinate(loop_load)
                    # print(offset)
                    # print('{0}\n{1}'.format(tile, cache_tile))
                    if cache_tile == tile:
                        return True
                    if board.get_piece(cache_tile) != None:
                        return False
                    if count>10:
                        raise ChessHandler.WrongMove("Outside the board")
                        break
                    count+=1
            return False

        def _isdirectlign(self, tile, board):
            oldc = ChessHandler.tile_to_coordinate(self.tile)
            newc = ChessHandler.tile_to_coordinate(tile)
            if oldc[0] == newc[0] or oldc[1] == newc[1]:
                loop_load = list(oldc)
                # --
                offset = ChessHandler.get_direct_offset(oldc, newc)
                # --
                count = 0
                while True:
                    loop_load[0]+=offset[0]
                    loop_load[1]+=offset[1]
                    print(loop_load)
                    cache_tile = ChessHandler.get_tile_from_coordinate(loop_load)
                    # print(offset)
                    # print('{0}\n{1}'.format(tile, cache_tile))
                    if cache_tile == tile:
                        return True
                    if board.get_piece(cache_tile) != None:
                        return False
                    if count>10:
                        raise ChessHandler.WrongMove("Outside the board")
                        break
                    count+=1
            return False

        def _iscapture(self, tile, board):
            if board.get_piece(tile) != None:
                return True
            else:
                return False



    class Pawn(Piece):

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
