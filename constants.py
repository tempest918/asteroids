import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Game constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
LINE_WIDTH = 2

# Player constants
PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
PLAYER_ACCELERATION = 600
PLAYER_FRICTION = 0.98
PLAYER_SHOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3
PLAYER_LIVES = 3
PLAYER_BOMBS = 3
BOMB_RADIUS = 300

# Asteroid constants
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

# Shot constants
SHOT_RADIUS = 5
SHOT_LIFETIME_SECONDS = 1