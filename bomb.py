from circleshape import CircleShape
import pygame
from constants import *

class Bomb(CircleShape):
    def __init__(self, x, y):
        radius = 10
        super().__init__(x, y, radius)
        self.fuse_timer = 2.0
        self.exploding = False
        self.explosion_timer = 0.5
        self.damage_done = False

    def draw(self, screen):
        if self.exploding:
            radius = BOMB_RADIUS * (1 - self.explosion_timer / 0.5)
            pygame.draw.circle(screen, "orange", self.position, int(radius), 2)
        else:
            color = "red"
            pygame.draw.circle(screen, color, self.position, self.radius, 2)
            pygame.draw.circle(screen, "orange", self.position, int(self.radius * (self.fuse_timer/2.0)))

    def update(self, dt):
        if self.exploding:
            self.explosion_timer -= dt
            if self.explosion_timer <= 0:
                self.kill()
        else:
            self.fuse_timer -= dt
            if self.fuse_timer <= 0:
                self.exploding = True
