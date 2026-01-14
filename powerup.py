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
        color = "yellow"
        if self.kind == "shield":
            color = "cyan"
        pygame.draw.circle(screen, color, self.position, self.radius, 2)

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
