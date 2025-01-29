import pygame
from typing import List
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, Theme 
from components.Node import Node


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        pygame.display.set_caption("LogicSim")

        # Game Vars
        self._nodes: List[Node] = []

    def run(self):
        while self.running:
            self._event_handles()
            self._update()
            self._render()
            self.clock.tick(FPS)

    def _event_handles(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or ( event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # 1 for left click
                x, y = event.pos
                self.add_node(x, y)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3: # 3 for right click
                x, y = event.pos
                node = self.get_node_at_position(x, y)
                if node:
                    self._nodes.remove(node)

    def _update(self):
        '''
        Game Logic is handled here
        '''
        pass

    def _render(self):
        self.screen.fill(Theme.BACKGROUND)
        for node in self._nodes:
            node.draw(self.screen)
        pygame.display.update()

    def add_node(self, x, y):
        '''
        Create new Node and at given position
        '''
        node = Node(x - 50,y - 25, text=f"({x - 50}, {y - 25})", color=Theme.SURFACE)
        self._nodes.append(node)

    def get_node_at_position(self, x, y):
        for node in self._nodes:
            if node.rect.collidepoint(x, y):
                return node
        return None

    
