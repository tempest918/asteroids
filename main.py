import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_LIVES
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    score = 0
    lives = PLAYER_LIVES
    font = pygame.font.Font(None, 36)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load("space.png")

    clock = pygame.time.Clock()
    dt = 0
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = updatable, drawable
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()


    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.blit(background_image, (0, 0))

        updatable.update(dt)
        
        for obj in updatable:
            if hasattr(obj, "wrap_screen"):
                obj.wrap_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    score += 100

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                lives -= 1
                if lives > 0:
                    player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                else:
                    print("Game over!")
                    sys.exit()
        
        for obj in drawable:
            obj.draw(screen)
        
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        for i in range(lives):
            x = SCREEN_WIDTH - 30 - (i * 30)
            y = 30
            points = [
                (x, y - 10),
                (x - 8, y + 10),
                (x + 8, y + 10)
            ]
            pygame.draw.polygon(screen, "white", points, 2)

        pygame.display.flip()   
        dt = (clock.tick(60)) / 1000

if __name__ == "__main__":
    main()
