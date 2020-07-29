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

    def _image(self, path, size):
        temp = pygame.image.load(path).convert()
        return pygame.transform.scale(temp, size)

    def commit(self, screen):
        for piece in self.pieces:
            if piece.tile == "xx": continue
            pos = ChessHandler.get_position(piece.tile)
            screen.blit(piece.sprite, pos)

    def get_piece(self, tile):
        for piece in self.pieces:
            if piece.tile == tile:
                return piece
        return None
