import pygame
from settings import Theme

class Node:
    def __init__(self, x, y, width=100, height=50, color=Theme.ACCENT, text="Hello", font_size=25) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, font_size)
    
    def draw(self, screen):
        # Rectangle
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)

        # Render text
        text_surf = self.font.render(self.text, 1, Theme.TEXT_PRIMARY)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
