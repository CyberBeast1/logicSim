import pygame
from typing import List 

from components.Connections import Connection
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, Theme 
from components.Node import GateNode, InputNode, Node, OutputNode

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.selected_node = None
        self._gates_set = ('AND', 'OR', 'XOR', 'NOT', 'NAND')
        self.current_gate_cycle = 0 # stores which gate to add ehen clicked, this gets updated when z is pressed
        pygame.display.set_caption("LogicSim")

        # Game Vars
        self._nodes = []
        self._connections: List[Connection] = []

    def run(self):
        while self.running:
            self._event_handles()
            self._update()
            self._render()
            self.clock.tick(FPS)

    def _event_handles(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_i:
                    x, y = pygame.mouse.get_pos()
                    self._nodes.append(InputNode(x,y))
                if event.key == pygame.K_o:
                    x, y = pygame.mouse.get_pos()
                    self._nodes.append(OutputNode(x,y))
                if event.key == pygame.K_z:
                    self.current_gate_cycle = (self.current_gate_cycle + 1)%len(self._gates_set)
                    print(f"Currently Selecte Gate: {self._gates_set[self.current_gate_cycle]}")

                if event.key == pygame.K_d and isinstance(self.selected_node, GateNode):
                    print(self.selected_node.gate_type,"\n\tINputs: ",self.selected_node.inputs, "\n\tOutputs: ",self.selected_node.output)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # 1 for left click
                    x, y = event.pos
                    self.selected_node = self.get_node_at_position(x, y)
                    if not self.selected_node:
                        gate = self._gates_set[self.current_gate_cycle]
                        self._nodes.append(GateNode(x,y,gate_type=gate))
                    elif isinstance(self.selected_node, InputNode):
                        self.selected_node.toggle_state()
                        self.selected_node.draggable = True
                    elif isinstance(self.selected_node, OutputNode) or isinstance(self.selected_node, GateNode):
                        self.selected_node.draggable = True
                if event.button == 2:
                    x, y = event.pos
                    clicked_node = self.get_node_at_position(x, y)
                    if clicked_node:
                        if not self.selected_node:
                            self.selected_node = clicked_node
                        else:
                            if self.selected_node != clicked_node:
                                connection = Connection(self.selected_node, clicked_node, Theme.SUCCESS, 6)
                                # if connection not in self._connections and tuple(reversed(connection)) not in self._connections:
                                if connection not in self._connections:
                                    self._connections.append(connection)
                                
                                if isinstance(self.selected_node, GateNode):
                                    if isinstance(clicked_node, InputNode):
                                        self.selected_node.inputs.append(clicked_node)

                                    if isinstance(clicked_node, OutputNode):
                                        self.selected_node.output.append(clicked_node)
                                # if isinstance(self.selected_node, OutputNode) and isinstance(clicked_node, GateNode):
                                    # self.selected_node, clicked_node = clicked_node, self.selected_node
                                    # self.selected_node.output = clicked_node

                                    if isinstance(clicked_node, GateNode):
                                        # Connect the selected gate to the clicked gate as an output
                                        # selected_port_type = clicked_node.get_clicked_port_type(x)
                                        # print(f"{self.selected_node.text} - {selected_port_type}")
                                        # if selected_port_type == "output":
                                        if clicked_node not in self.selected_node.output:
                                            self.selected_node.output.append(clicked_node)
                                        if self.selected_node not in clicked_node.inputs:
                                            clicked_node.inputs.append(self.selected_node)
                                        # else:
                                            # if self.selected_node not in clicked_node.output:
                                                # clicked_node.output.append(self.selected_node)
                                            # if clicked_node not in self.selected_node.inputs:
                                                # self.selected_node.inputs.append(clicked_node)
                                    # if clicked_node is not self.selected_node.output:
                                        # self.selected_node.output.append(clicked_node)
                                    # if self.selected_node not in clicked_node.inputs:
                                        # clicked_node.inputs.append(self.selected_node)
                            self.selected_node = None

            if event.type == pygame.MOUSEBUTTONUP: 
                if event.button == 1:
                    if self.selected_node:
                        self.selected_node.draggable = False
                if event.button == 3: # 3 for right click
                    x, y = event.pos
                    node = self.get_node_at_position(x, y)
                    if node:
                        self._nodes.remove(node)
                        self._connections = [conn for conn in self._connections if node not in (conn.start_node, conn.end_node)]
                    for other_nodes in self._nodes:
                        if isinstance(other_nodes, GateNode):
                            for in_node, out_nodes in zip(other_nodes.inputs, other_nodes.output):
                                if node == in_node:
                                    other_nodes.inputs.remove(node)
                                if node == out_nodes:
                                    other_nodes.output.remove(node)

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
        for node in self._nodes:
            if isinstance(node, GateNode):
                node.evaluate()

        for connection in self._connections:
            if isinstance(connection.start_node, (InputNode, OutputNode, GateNode)):
                connection.color = Theme.SUCCESS if connection.start_node.state else Theme.ERROR
            elif isinstance(connection.end_node, (InputNode, OutputNode)):
                connection.color = Theme.SUCCESS if connection.end_node.state else Theme.ERROR

                

    def _render(self):
        self.screen.fill(Theme.BACKGROUND)
        for connection in self._connections:
            connection.draw(self.screen)

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
    
