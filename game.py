import pygame
from pygame import locals
import random


class Game:
    def __init__(self, height, width, board_height, board_width, square_size=10):
        self.width = width
        self.height = height
        self.board_height = board_height
        self.board_width = board_width
        self.square_size = square_size
        self.board = Board(board_height, board_width)
        self.board.randomize()
        self.clock = pygame.time.Clock()
        self.surface = None

    def run(self):
        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption("Game Of Life")
        while True:
            self.draw()
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    return True

    def draw(self):
        for column in range(self.board_height):
            for row in range(self.board_width):
                position = (column * self.square_size, row * self.square_size)
                size = (self.square_size, self.square_size)
                border = 1
                if self.board.board[column][row].alive:
                    color = (255, 0, 255)
                    pygame.draw.rect(self.surface, color, (position, size), border)
                else:
                    black = (0, 0, 0)
                    pygame.draw.rect(self.surface, black, (position, size), border)
        self.board.refresh()
        pygame.display.update()


class Cell:
    def __init__(self):
        self.alive = False

    def kill(self):
        self.alive = False

    def revive(self):
        self.alive = True


class Board:
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.board = [[Cell() for i in range(width)] for j in range(height)]
        self.next_generation = []

    def count_alive_neighbours(self, column, row):
        counter = 0
        neighbors = [[i, j] for i in range(-1, 2) for j in range(-1, 2) if i or j]
        for neighbor in neighbors:
            try:
                if self.board[column + neighbor[0]][row + neighbor[1]].alive:
                    counter += 1
            except IndexError:
                pass
        return counter

    def refresh(self):  # TODO kolumne z rzedem pozmieniaj
        self.next_generation = [[Cell() for i in range(self.width)] for j in range(self.height)]
        for column in range(self.height):
            for row in range(self.width):
                alive_neighbours = self.count_alive_neighbours(column, row)
                if self.board[column][row].alive:
                    if alive_neighbours in {2, 3}:
                        self.next_generation[column][row].revive()
                    else:
                        self.next_generation[column][row].kill()
                else:
                    if alive_neighbours == 3:
                        self.next_generation[column][row].revive()
                    else:
                        self.next_generation[column][row].kill()
        self.board = self.next_generation

    def print(self):
        for column in range(self.height):
            for row in range(self.width):
                cell = self.board[column][row].alive
                if cell:
                    print("o", end="")
                else:
                    print(".", end="")
            print("\n")

    def randomize(self):
        for column in range(self.height):
            for row in range(self.width):
                n = random.random()
                if n > 0.5:
                    self.board[column][row].revive()
                else:
                    self.board[column][row].kill()


game = Game(400, 400, 40, 40)
game.run()
