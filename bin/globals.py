import pygame
import sys
from bin.board import ChessHandler
# --
pygame.init()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

class EventHandler:

    def __init__(self, event, board):
        if event.type == pygame.QUIT:
            self._quit()

    def _quit(self):
        sys.exit()

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.turn = 'w'

    def handle_event(self, event, board):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:

                # ----
                    if self.text != "O-O" and self.text != "O-O-O":
                        try:
                            original, destination = ChessHandler.parse(self.text)
                            piece = board.get_piece(original)
                            if piece == None:
                                raise ChessHandler.WrongMove("This piece does not exists")
                            piece._move(destination, board)
                            self.text = ''
                        except ChessHandler.WrongMove as e:
                            print(e)
                    else:
                        try:
                            if self.text == "O-O":
                                board.small_castle(board.turn)
                            elif self.text == "O-O-O":
                                board.large_castle(board.turn)
                        except ChessHandler.WrongMove as e:
                            print(e)
                # ----
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
