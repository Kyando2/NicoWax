import pygame
from bin.pieces import ChessHandler
import bin.settings as settings

class Board:

    def __init__(self):
        self.pieces = []
        self.turn = 'w'
        # -- Pawns
        pawn_positions = ["A2","B2","C2","D2","E2","F2","G2","H2"]
        black_positions = ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"]
        for i in pawn_positions:
            img = self._image(settings.WHITE_PAWN, settings.DEFAULT_SIZE)
            self.pieces.append(ChessHandler.Pawn(tile=i, colour="w", image=img))
        for i in black_positions:
            img = self._image(settings.BLACK_PAWN, settings.DEFAULT_SIZE)
            self.pieces.append(ChessHandler.Pawn(tile=i, colour="b", image=img))
        # --
        img = self._image(settings.WHITE_QUEEN, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.Queen(tile="D1", colour="w", image=img))
        img = self._image(settings.BLACK_QUEEN, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.Queen(tile="D8", colour="b", image=img))
        # --
        img = self._image(settings.BLACK_ROOK, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.Rook(tile="H8", colour="b", image=img))
        img = self._image(settings.BLACK_ROOK, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.Rook(tile="A8", colour="b", image=img))
        img = self._image(settings.WHITE_ROOK, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.Rook(tile="H1", colour="w", image=img))
        img = self._image(settings.WHITE_ROOK, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.Rook(tile="A1", colour="w", image=img))
        # --
        img = self._image(settings.WHITE_BISHOP, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.Bishop(tile="C1", colour="w", image=img))
        img = self._image(settings.BLACK_BISHOP, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.Bishop(tile="C8", colour="b", image=img))
        img = self._image(settings.WHITE_BISHOP, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.Bishop(tile="F1", colour="w", image=img))
        img = self._image(settings.BLACK_BISHOP, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.Bishop(tile="F8", colour="b", image=img))
        # --
        img = self._image(settings.WHITE_KNIGHT, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.Knight(tile="B1", colour="w", image=img))
        img = self._image(settings.BLACK_KNIGHT, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.Knight(tile="B8", colour="b", image=img))
        img = self._image(settings.WHITE_KNIGHT, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.Knight(tile="G1", colour="w", image=img))
        img = self._image(settings.BLACK_KNIGHT, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.Knight(tile="G8", colour="b", image=img))
        # --
        img = self._image(settings.WHITE_KING, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.King(tile="E1", colour="w", image=img))
        img = self._image(settings.BLACK_KING, settings.DEFAULT_SIZE)
        self.pieces.append(ChessHandler.King(tile="E8", colour="b", image=img))

    def _switch(self):
        switched = False
        if self.turn == 'b':
            self.turn = 'w'
            switched = True
        if self.turn == 'w' and switched == False:
            self.turn = 'b'
        # --

    def _image(self, path, size):
        temp = pygame.image.load(path).convert()
        return pygame.transform.scale(temp, size)

    def commit(self, screen):
        for piece in self.pieces:
            if piece.tile == "xx": continue
            pos = ChessHandler.get_position(piece.tile)
            screen.blit(piece.sprite, pos)

    def small_castle(self, colour):
        if colour == "w":
            if self.get_piece("H1") != None:
                rook = self.get_piece("H1")
                if self.get_piece("E1") != None:
                    king = self.get_piece("E1")
                if rook.has_moved == False and king.has_moved == False:
                    if self.get_piece("F1") == None and self.get_piece("G1") == None:
                        rook.tile = 'F1'
                        king.tile = 'G1'
                        return
        # --
        if colour == "b":
            if self.get_piece("H8") != None:
                rook = self.get_piece("H8")
                if self.get_piece("E8") != None:
                    king = self.get_piece("E8")
                if rook.has_moved == False and king.has_moved == False:
                    if self.get_piece("F8") == None and self.get_piece("G8") == None:
                        rook.tile = 'F8'
                        king.tile = 'G8'
                        return
        raise ChessHandler.WrongMove("Cannot castle")

    def large_castle(self, colour):
        if colour == "w":
            if self.get_piece("A1") != None:
                rook = self.get_piece("A1")
                if self.get_piece("E1") != None:
                    king = self.get_piece("E1")
                if rook.has_moved == False and king.has_moved == False:
                    if self.get_piece("B1") == None and self.get_piece("C1") == None  and self.get_piece("D1") == None:
                        rook.tile = 'D1'
                        king.tile = 'C1'
                        return
        # --
        if colour == "b":
            if self.get_piece("A8") != None:
                rook = self.get_piece("A8")
                if self.get_piece("E8") != None:
                    king = self.get_piece("E8")
                if rook.has_moved == False and king.has_moved == False:
                    if self.get_piece("B8") == None and self.get_piece("C8") == None  and self.get_piece("D8") == None:
                        rook.tile = 'D8'
                        king.tile = 'C8'
                        return
        raise ChessHandler.WrongMove("Cannot castle")

    def get_piece(self, tile):
        for piece in self.pieces:
            if piece.tile == tile:
                return piece
        return None
