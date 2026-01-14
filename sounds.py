import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.init_sounds()

    def init_sounds(self):
        sound_files = {
            "shoot": "bullet-laser.wav",
            "shoot_spread": "bullet-plasma.wav",
            "explosion": "explosion.wav",
            "small_explosion": "explosion-small.wav",
            "powerup": "powerup.wav",
            "hit": "collision.wav",
            "warp": "warp-drive.wav",
            "bomb": "explosion.wav", 
        }

        for name, filename in sound_files.items():
            path = os.path.join("sounds", filename)
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                except Exception as e:
                    print(f"Warning: Could not load sound {filename}: {e}")
            else:
                print(f"Warning: Sound file not found: {path}")

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
    
    def play_shoot(self):
        self.play("shoot")
        
    def play_spread_shoot(self):
        if "shoot_spread" in self.sounds:
            self.play("shoot_spread")
        else:
            self.play("shoot")

    def play_explosion(self):
        self.play("explosion")
        
    def play_small_explosion(self):
        self.play("small_explosion")
        
    def play_powerup(self):
        self.play("powerup")
        
    def play_hit(self):
        self.play("hit")
        
    def play_warp(self):
        self.play("warp")
