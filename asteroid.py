from circleshape import CircleShape
import pygame
from constants import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.angle = 0
        self.spin_speed = random.uniform(-50, 50)
        
        self.points = []
        point_count = random.randint(8, 12)
        for i in range(point_count):
            angle = (360 / point_count) * i
            dist = random.uniform(radius * 0.8, radius * 1.2)
            vector = pygame.Vector2(0, 1).rotate(angle) * dist
            self.points.append(vector)

    def draw(self, screen):
        rotated_points = []
        for point in self.points:
            rotated_point = point.rotate(self.angle) + self.position
            rotated_points.append(rotated_point)
        pygame.draw.polygon(screen, "white", rotated_points, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        self.angle += self.spin_speed * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        random_angle = random.uniform(20, 50)
        
        vector1 = self.velocity.rotate(random_angle)
        vector2 = self.velocity.rotate(-random_angle)
        
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = vector1 * 1.2
        
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = vector2 * 1.2