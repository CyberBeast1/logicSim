import pygame
from settings import Theme

class Node:
    def __init__(self, x, y, width=100, height=50, color=Theme.ACCENT, text="Hello", font_size=25) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.draggable = False
        self.font = pygame.font.Font(None, font_size)
        self.state = False
        self.connected_nodes = []
    
    def draw(self, screen, selected=False):
        # Rectangle
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)

        # Render text
        text_surf = self.font.render(self.text, 1, Theme.TEXT_PRIMARY)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

        if selected:
            pygame.draw.rect(screen, (255,0,255), self.rect, 4, 10)


class InputNode(Node):
    def __init__(self, x, y, width=100, height=50, color=Theme.ACCENT, text="0", font_size=25) -> None:
        super().__init__(x, y, width, height, color, text, font_size)
        self.state = False

    def toggle_state(self):
        self.state = not self.state
        self.text = str(self.state)
        self.color = Theme.SUCCESS if self.state else Theme.WARNING


class OutputNode(Node):
    def __init__(self, x, y, width=100, height=50, color=Theme.WARNING, text="0", font_size=25) -> None:
        super().__init__(x, y, width, height, color, text, font_size)

    def set_state(self, state):
        self.state = state
        self.text = str(self.state)
        self.color = Theme.SUCCESS if self.state else Theme.WARNING

class GateNode(Node):
    def __init__(self, x, y, width=100, height=50, color=Theme.ACCENT, text="Hello", font_size=25) -> None:
        super().__init__(x, y, width, height, color, text, font_size)

        self.inputs = []
        self.output = None

    def evaluate(self):
        if len(self.inputs) == 2:
            self.state = all(node.state for node in self.inputs)
            if self.output:
                self.output.toggle_state()
