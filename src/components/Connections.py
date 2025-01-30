import pygame
from settings import Theme
class Connection:
    def __init__(self, start_node, end_node, color=Theme.WARNING, thickness=9):
       self.start_node = start_node
       self.end_node = end_node
       self.color = color
       self.thickness=thickness


    def draw(self, screen):
            if self.start_node and self.end_node:
                start_pos = self.start_node.rect.center
                end_pos = self.end_node.rect.center
                pygame.draw.line(screen, self.color, start_pos, end_pos, self.thickness)

