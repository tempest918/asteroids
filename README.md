# Asteroids

A classic Asteroids game implementation in Python using Pygame.

## Features

- **Classic Gameplay**: Fly a spaceship, shoot asteroids, and avoid collisions.
- **Physics**: acceleration, friction, and screen wrapping.
- **Scoring**: Earn points by destroying asteroids.
- **Lives**: You have 3 lives. Respawn at the center when hit.

## Controls

- `W`: Accelerate forward
- `A`: Turn left
- `D`: Turn right
- `S`: Reverse (move backward)
- `SPACE`: Shoot

## Setup

1. Install dependencies:
   ```bash
   pip install pygame
   # or with uv
   uv sync
   ```

2. Run the game:
   ```bash
   python3 main.py
   # or
   uv run main.py
   ```

## Development

- `main.py`: Entry point and game loop.
- `player.py`: Player class and movement logic.
- `asteroid.py`: Asteroid behavior and splitting logic.
- `shot.py`: Projectile logic.
- `constants.py`: Game settings and physics constants.
