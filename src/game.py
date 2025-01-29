from os import confstr_names
import pygame
from typing import List, Tuple

from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, Theme 
from components.Node import Node


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.selected_node = None
        pygame.display.set_caption("LogicSim")

        # Game Vars
        self._nodes: List[Node] = []
        self._connections: List[Tuple[Node, Node]] = []

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
                self.selected_node = self.get_node_at_position(x, y)
                if not self.selected_node:
                    self.add_node(x, y)
                else:
                    self.selected_node.draggable = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.selected_node:
                    self.selected_node.draggable = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                x, y = event.pos
                clicked_node = self.get_node_at_position(x, y)
                if clicked_node:
                    if not self.selected_node:
                        self.selected_node = clicked_node
                    else:
                        if self.selected_node != clicked_node:
                            connection = (self.selected_node, clicked_node)
                            if connection not in self._connections and tuple(reversed(connection)) not in self._connections:
                                self._connections.append((self.selected_node, clicked_node))
                        self.selected_node = None
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3: # 3 for right click
                x, y = event.pos
                node = self.get_node_at_position(x, y)
                if node:
                    self._nodes.remove(node)
                    self._connections = [conn for conn in self._connections if node not in conn]

            if event.type == pygame.MOUSEMOTION and self.selected_node:
                # if self.is_position_valid(self.selected_node, event.pos) and self.selected_node.draggable:
                if self.selected_node.draggable:
                    x, y = event.pos
                    self.selected_node.rect.centerx = max(0, min(x, WINDOW_WIDTH))
                    self.selected_node.rect.centery = max(0, min(y, WINDOW_HEIGHT))
                # self.selected_node.text = f"{event.pos}"

    def _update(self):
        '''
        Game Logic is handled here
        '''
        # print(f"selected_node: {self.selected_node}")

    def _render(self):
        self.screen.fill(Theme.BACKGROUND)
        for node1, node2 in self._connections:
            pygame.draw.line(self.screen, Theme.WARNING, node1.rect.center, node2.rect.center, 2)

        for node in self._nodes:
            node.draw(self.screen, selected=(node == self.selected_node))

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

    def is_position_valid(self, node: Node, newPos):
        newX, newY = newPos
        nodeWidth, nodeHeight = node.rect.width, node.rect.height
        if (newX - nodeWidth//2) > 0 and (newY - nodeHeight//2) > 0 and (newX + nodeWidth//2) < WINDOW_WIDTH and (newY + nodeHeight//2) < WINDOW_HEIGHT:
            return True
        return False
    
