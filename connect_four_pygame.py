# Import
import math
import numpy as np
import pygame
from pygame.locals import *
import pygame.freetype
import pygame.gfxdraw

# init pygame
pygame.init()

# screen
WIDTH = 700
HEIGHT = 750
ROWS = 6
COLUMNS = 7
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("connect four game")

# colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 139)
GRAY = (128, 128, 128)
GRAY_ALPHA = (128, 128, 128, 150)
DARKRED = (139, 0, 0)
WHITE = (255, 255, 255)
DARKORANGE = (255, 140, 0)

# font
font = pygame.freetype.Font(None, 16)


class Player:
    """Klasse für Spieler Objekte"""

    def __init__(self, name, color, symbol):
        """Konstruktor"""
        self.name = name
        self.color = color
        self.symbol = symbol

    def drop(self, board, position):
        """Spielstein aufs Board bringen. Gibt True zurück, wenn drop erfolgreich"""
        try:
            row_position = np.where(board.board[:, position] == "-")[0][-1]
            board.board[row_position, position] = f"{self.symbol}"
            return True
        except IndexError:
            print("Disc kann hier nicht platziert werden")
            return False


class Gameboard:
    """Klasse für das Spielfeld"""

    def __init__(self):
        """Konstruktor"""
        # Vier Gewinnt Spielbrett hat 7 Spalten und 6 Zeilen
        self.board = np.array([["-", "-", "-", "-", "-", "-", "-"]] * 6)
        self.rows = np.size(self.board, axis=0)
        self.columns = np.size(self.board, axis=1)

    def clear_board(self):
        """Spielfeld zurücksetzen"""
        self.board = np.array([["-", "-", "-", "-", "-", "-", "-"]] * 6)

    def check_if_won(self):
        """Check, ob ein Spieler gewonnen hat (4 in einer Reihe, Spalte oder Diagonale)"""
        # Waagerecht
        for x in range(self.rows):
            for y in range(self.columns - 3):
                if self.board[x, y] != "-" \
                        and self.board[x, y] == self.board[x, y + 1] == self.board[x, y + 2] == self.board[x, y + 3]:
                    return True
        # Senkrecht
        for y in range(self.columns):
            for x in range(self.rows - 3):
                if self.board[x, y] != "-" \
                        and self.board[x, y] == self.board[x + 1, y] == self.board[x + 2, y] == self.board[x + 3, y]:
                    return True
        # Diagonal (links nach rechts)
        for x in range(self.rows - 3):
            for y in range(self.columns - 3):
                if self.board[x, y] != "-" \
                        and self.board[x, y] == self.board[x + 1, y + 1] == self.board[x + 2, y + 2] == \
                        self.board[x + 3, y + 3]:
                    return True
        # Diagonal (rechts nach links)
        for x in range(self.rows - 3):
            for y in range(3, self.columns):
                if self.board[x, y] != "-" \
                        and self.board[x, y] == self.board[x + 1, y - 1] == self.board[x + 2, y - 2] == \
                        self.board[x + 3, y - 3]:
                    return True
        # Default return
        return False

    def check_if_draw(self):
        """Check, ob unentschieden (Alle Felder belegt und kein Gewinner)"""
        if len(np.where(self.board == "-")[0]) == 0:
            return True
        return False


def switch_player(player1, player2):
    """Utility Funktion zum Wechseln zwischen den Spieler Objekten"""
    while True:
        yield player1
        yield player2


def reset_disc_and_switch_player(disc_info, playerswitch):
    """Spielsteinposition zurücksetzen und Spieler wechseln"""
    # Spielsteinposition zurücksetzen
    disc_info[0] = [WIDTH / 2, 80]
    disc_info[1] = DARKORANGE if disc_info[1] == DARKRED else DARKRED
    # Aktiver Spieler wechselt
    return next(playerswitch)


def render_game(board, player1, player2):
    """Spielfeld auf den Bildschirm zeichnen"""
    # Spielfeld zeichnen
    screen.fill(GRAY)
    pygame.draw.rect(screen, BLUE, Rect(0, 150, WIDTH, HEIGHT - 150))
    for i in range(len(board.board)):
        for j in range(len(board.board[i])):
            if board.board[i][j] == "-":
                pygame.draw.circle(screen, GRAY, (j * 100 + 50, 150 + (i * 100 + 50)), 45)
            elif board.board[i][j] == player1.symbol:
                pygame.draw.circle(screen, player1.color, (j * 100 + 50, 150 + (i * 100 + 50)), 45)
            elif board.board[i][j] == player2.symbol:
                pygame.draw.circle(screen, player2.color, (j * 100 + 50, 150 + (i * 100 + 50)), 45)


def play_game():
    """Hauptfunktion zum Spielen"""
    # Gameboard erstellen
    board = Gameboard()

    # Spieler Objekte erzeugen
    player1 = Player("Player 1", DARKRED, "1")
    player2 = Player("Player 2", DARKORANGE, "2")
    playerswitch = switch_player(player1, player2)
    active_player = next(playerswitch)

    # Position der Disc
    disc_info = [[WIDTH // 2, 80], DARKRED]

    # Wir spielen
    play = True
    gaming = True

    # Spielschleife
    while play:

        if gaming:
            # Spielfeld zeichnen
            render_game(board, player1, player2)

            # Spielstein zeichen
            pygame.draw.circle(screen, disc_info[1], disc_info[0], 45)

            # Text (Welcher Spieler ist am Zug?)
            font.render_to(screen, (5, 5), f"{active_player.name} plays", BLACK)

            # Update der Anzeige
            pygame.display.update()

        # Pygame Events abfragen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            # Pfeiltasten
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if disc_info[0][0] > 50:
                        disc_info[0][0] = disc_info[0][0] - 100
                if event.key == pygame.K_RIGHT:
                    if disc_info[0][0] < WIDTH - 50:
                        disc_info[0][0] = disc_info[0][0] + 100
                if event.key == pygame.K_RETURN:
                    # Spielstein fallen lassen
                    has_dropped = active_player.drop(board, math.ceil(disc_info[0][0] / 100) - 1)
                    if not has_dropped:
                        break
                    if not board.check_if_won() and not board.check_if_draw():
                        active_player = reset_disc_and_switch_player(disc_info, playerswitch)
                if pygame.key.name(event.key) == "y" and not gaming:
                    # Board zurücksetzen
                    board.clear_board()
                    active_player = reset_disc_and_switch_player(disc_info, playerswitch)
                    gaming = True
                if pygame.key.name(event.key) == "n" and not gaming:
                    play = False

        # Gibt es einen Gewinner?
        if board.check_if_won():
            gaming = False
            # Spielfeld zeichnen
            render_game(board, player1, player2)
            # Infotext
            pygame.gfxdraw.box(screen, pygame.Rect(0, 0, WIDTH, HEIGHT), GRAY_ALPHA)
            font.render_to(screen, (20, 20), f"{active_player.name} hat gewonnen",
                           fgcolor=BLACK, size=28)
            font.render_to(screen, (20, 20 + 50),
                           "Nochmal spielen? Drücke y für Ja oder n für Nein",
                           fgcolor=BLACK, size=16)
        # Unentschieden
        elif board.check_if_draw():
            gaming = False
            # Spielfeld zeichnen
            render_game(board, player1, player2)
            # Spielstein zeichen
            pygame.draw.circle(screen, disc_info[1], disc_info[0], 45)
            # Infotext
            pygame.gfxdraw.box(screen, pygame.Rect(0, 0, WIDTH, HEIGHT), GRAY_ALPHA)
            font.render_to(screen, (20, 20), "Unentschieden", fgcolor=BLACK, size=42)

        # Update
        pygame.display.flip()

    # Spiel verlassen
    pygame.quit()


# Programm starten
if __name__ == '__main__':
    play_game()
