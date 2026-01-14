from circleshape import CircleShape
import pygame
from constants import PLAYER_LIVES

class PowerUp(CircleShape):
    def __init__(self, x, y, kind):
        radius = 15
        super().__init__(x, y, radius)
        self.kind = kind
        self.lifetime = 5.0

    def draw(self, screen):
        color = "white"
        letter = "?"
        if self.kind == "speed":
            color = "yellow"
            letter = "S"
        elif self.kind == "shield":
            color = "cyan"
            letter = "I"
        elif self.kind == "bomb":
            color = "orange"
            letter = "B"
        elif self.kind == "life":
            color = "green"
            letter = "L"
            
        pygame.draw.circle(screen, color, self.position, self.radius)
        
        font = pygame.font.Font(None, 24)
        text = font.render(letter, True, "black")
        text_rect = text.get_rect(center=self.position)
        screen.blit(text, text_rect)

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
