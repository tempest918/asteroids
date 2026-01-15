from circleshape import CircleShape
from constants import *
from shot import Shot
from particle import Particle
import pygame
import random

class Player(CircleShape):
    def __init__(self, x, y, sound_manager=None):
        super().__init__(x, y, PLAYER_RADIUS)
        self.sound_manager = sound_manager
        self.rotation = 0
        self.shoot_cooldown = 0
        self.speed_boost_timer = 0
        self.invulnerable_timer = 0
        self.weapon_type = "normal"
        self.num_bombs = PLAYER_BOMBS
        self.locked_keys = [k for k, v in enumerate(pygame.key.get_pressed()) if v]
    
    def power_up(self, power_type):
        if power_type == "speed":
            self.speed_boost_timer = 5.0
        elif power_type == "shield":
            self.invulnerable_timer = 5.0
        elif power_type == "weapon":
            self.weapon_type = "spread"
            
    def respawn(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.speed_boost_timer = 0
        self.invulnerable_timer = PLAYER_RESPAWN_INVULNERABILITY_SECONDS
        self.weapon_type = "normal"
        self.num_bombs = PLAYER_BOMBS
        self.locked_keys = [k for k, v in enumerate(pygame.key.get_pressed()) if v]
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def collides_with(self, other):
        vertices = self.triangle()
        
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)
        
        d1 = sign(other.position, vertices[0], vertices[1])
        d2 = sign(other.position, vertices[1], vertices[2])
        d3 = sign(other.position, vertices[2], vertices[0])
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        if not (has_neg and has_pos):
            return True
            
        for i in range(3):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % 3]
            
            l2 = p1.distance_squared_to(p2)
            if l2 == 0:
                dist_sq = other.position.distance_squared_to(p1)
            else:
                t = ((other.position.x - p1.x) * (p2.x - p1.x) + (other.position.y - p1.y) * (p2.y - p1.y)) / l2
                t = max(0, min(1, t))
                projection = p1 + (p2 - p1) * t
                dist_sq = other.position.distance_squared_to(projection)
            
            if dist_sq <= other.radius * other.radius:
                return True
                
        return False
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
        if self.invulnerable_timer > 0:
            pygame.draw.circle(screen, "cyan", self.position, self.radius + 5, 2)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        accel = PLAYER_ACCELERATION
        if self.speed_boost_timer > 0:
            accel *= 2.0
        self.velocity += forward * accel * dt
        
        # Spawn particles
        particle_pos = self.position - forward * self.radius
        particle_vel = -forward * 100 + pygame.Vector2(random.uniform(-20, 20), random.uniform(-20, 20))
        Particle(particle_pos.x, particle_pos.y, particle_vel)

    def shoot(self):
        if self.weapon_type == "normal":
            self._spawn_shot(0)
            if self.sound_manager:
                self.sound_manager.play_shoot()
        elif self.weapon_type == "spread":
            self._spawn_shot(0)
            self._spawn_shot(15)
            self._spawn_shot(-15)
            if self.sound_manager:
                self.sound_manager.play_spread_shoot()

    def _spawn_shot(self, angle_offset):
        forward = pygame.Vector2(0, 1).rotate(self.rotation + angle_offset)
        position = self.position + forward * self.radius
        velocity = forward * PLAYER_SHOT_SPEED
        shot = Shot(position.x, position.y)
        shot.velocity = velocity

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shoot_cooldown -= dt
        self.speed_boost_timer -= dt
        self.invulnerable_timer -= dt
        
        for k in list(self.locked_keys):
            if not keys[k]:
                self.locked_keys.remove(k)

        def is_active(key):
            return keys[key] and key not in self.locked_keys

        if is_active(pygame.K_a):
            self.rotate(-dt)
        if is_active(pygame.K_d):
            self.rotate(dt)
        if is_active(pygame.K_w):
            self.move(dt)
        if is_active(pygame.K_s):
            self.move(-dt)
        if is_active(pygame.K_SPACE):
            if self.shoot_cooldown <= 0:
                self.shoot()
                self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        
        self.velocity *= PLAYER_FRICTION
        self.position += self.velocity * dt

