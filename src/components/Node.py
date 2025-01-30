import pygame
from settings import Theme

class Node:
    def __init__(self, x, y, text, width=100, height=50, color=Theme.SHADOW, font_color=Theme.TEXT_PRIMARY, font_size=25, border_radius=10) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font_color = font_color
        self.border_radius = border_radius
        self.draggable = False
        self.font = pygame.font.Font(None, font_size)
        self.state = False
        self.connected_nodes = []
    
    def draw(self, screen, selected=False):
        # Rectangle
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)

        # Render text
        text_surf = self.font.render(self.text, 1, self.font_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

        if selected:
            pygame.draw.rect(screen, (255,0,255), self.rect, 2, self.border_radius)


class InputNode(Node):
    def __init__(self, x, y, width=100, height=50, color=Theme.WARNING, font_color=Theme.TEXT_DARK, text="0", font_size=30, border_radius=50) -> None:
        super().__init__(x, y, text, width, height, color, font_color, font_size, border_radius)
        self.state = False
        self.font

    def toggle_state(self):
        self.state = not self.state
        self.text = "IN: "+str(int(self.state))
        self.color = Theme.SUCCESS if self.state else Theme.WARNING


class OutputNode(Node):
    def __init__(self, x, y, width=100, height=50, color=Theme.WARNING, font_color=Theme.TEXT_DARK, text="0", font_size=30, border_radius=50) -> None:
        super().__init__(x, y, text, width, height, color, font_color, font_size, border_radius)

    def set_state(self, state):
        self.state = state
        self.text = "OUT: "+str(int(self.state))
        self.color = Theme.SUCCESS if self.state else Theme.WARNING

class GateNode(Node):
    def __init__(self, x, y, gate_type, width=100, height=50, color=Theme.SHADOW,font_color=Theme.TEXT_PRIMARY,font_size=25) -> None:
        super().__init__(x, y, f"{gate_type} Gate", width, height, color, font_color, font_size)
        self.no_of_inputs = 2
        self.gate_type = gate_type.upper()
        self.inputs = []
        self.output = []

    def get_clicked_port_type(self, x):
        if x < self.rect.centerx:
            return "input"
        else:
            return "output"

    def evaluate(self, visited=None):
           # Prevent infinite recursion
        if visited is None:
            visited = set()
        
        # If this gate is already evaluated in this cycle, return
        if self in visited:
            return
        visited.add(self)
        input_states = [node.state for node in self.inputs if node is not None]
        if self.gate_type == 'NOT':
            if len(input_states) > 1:
                raise ValueError("NOT Gate should have 1 input")
            elif len(input_states) == 1:
                self.state = not input_states[0]
        elif self.gate_type in {'AND', 'OR', 'XOR', 'NAND'}:
            if len(self.inputs) > 2:
                raise ValueError(f"{self.gate_type} Gate should have exactly 2 inputs")
            elif len(input_states) == 2:
                if self.gate_type == "AND":
                    self.state = input_states[0] and input_states[1]
                if self.gate_type == "NAND":
                    self.state = not (input_states[0] and input_states[1])
                if self.gate_type == "OR":
                    self.state = input_states[0] or input_states[1]
                if self.gate_type == "XOR":
                    self.state = input_states[0] ^ input_states[1]
        else:
            raise ValueError(f"Unsupported gate_type {self.gate_type}.")
        # if isinstance(self.output, OutputNode):
            # self.output.set_state(self.state)
        # Propagate the state to connected nodes
        if len(self.output) == 1:
            if isinstance(self.output[0], GateNode):
                self.output[0].evaluate(visited)  # Pass the visited set to avoid recursion
            elif isinstance(self.output[0], OutputNode):
                self.output[0].set_state(self.state)
        elif len(self.output) > 1:
            for output in self.output:
                if isinstance(output, GateNode):
                    output.evaluate(visited)
                elif isinstance(output, OutputNode):
                    output.set_state(self.state)

