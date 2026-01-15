import pygame
from circleshape import CircleShape
import random

class Particle(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, 2)
        self.velocity = velocity
        self.timer = 0
        self.lifetime = random.uniform(0.1, 0.3)
        self.color = "white"
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
        
    def update(self, dt):
        self.position += self.velocity * dt
        self.timer += dt
        if self.timer > self.lifetime:
            self.kill()
