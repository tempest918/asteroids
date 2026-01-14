from circleshape import CircleShape
import pygame
import random

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.particles = []
        for _ in range(20):
            velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            velocity.scale_to_length(random.uniform(50, 200))
            self.particles.append({
                "pos": pygame.Vector2(x, y),
                "vel": velocity,
                "life": random.uniform(0.3, 0.8),
                "color": random.choice(["white", "orange", "yellow"])
            })

    def update(self, dt):
        alive_particles = []
        for p in self.particles:
            p["life"] -= dt
            if p["life"] > 0:
                p["pos"] += p["vel"] * dt
                alive_particles.append(p)
        self.particles = alive_particles
        if not self.particles:
            self.kill()

    def draw(self, screen):
        for p in self.particles:
            pygame.draw.circle(screen, p["color"], p["pos"], 2)
