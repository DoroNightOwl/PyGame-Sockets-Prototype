import pygame
from sprites import StaticObject
class TileMap:
    def __init__(self):
        self.sprites = []
    def load(self, matrix, sprite, sprite_id, grid_size):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == sprite_id :
                    self.sprites.append(StaticObject(sprite, (grid_size*j, grid_size*i)))

