import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from powerup import PowerUp
from bomb import Bomb
from explosion import Explosion
from sounds import SoundManager
import random

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load(resource_path("space.png"))
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 96)
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    Player.containers = updatable, drawable
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    Bomb.containers = (bombs, updatable, drawable)
    Explosion.containers = (explosions, updatable, drawable)

    state = "MENU"
    score = 0
    lives = PLAYER_LIVES
    player = None
    asteroid_field = None
    sound_manager = SoundManager()
    dt = 0

    def start_game():
        nonlocal player, asteroid_field, score, lives
        updatable.empty()
        drawable.empty()
        asteroids.empty()
        shots.empty()
        powerups.empty()
        bombs.empty()
        explosions.empty()
        
        score = 0
        lives = PLAYER_LIVES
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, sound_manager)
        asteroid_field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        start_game()
                        state = "PLAYING"
            
            elif state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        if player.num_bombs > 0:
                             Bomb(player.position.x, player.position.y)
                             player.num_bombs -= 1
                    if event.key == pygame.K_TAB:
                        pass

            elif state == "GAME_OVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        start_game()
                        state = "PLAYING"
                    if event.key == pygame.K_q:
                        return

        screen.blit(background_image, (0, 0))

        if state == "MENU":
            title_text = title_font.render("ASTEROIDS", True, "white")
            start_text = font.render("Press Enter to start", True, "white")
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
            screen.blit(title_text, title_rect)
            screen.blit(start_text, start_rect)

        elif state == "PLAYING":
            if random.randint(0, 900) == 0:
                x = random.randint(50, SCREEN_WIDTH - 50)
                y = random.randint(50, SCREEN_HEIGHT - 50)
                if len(asteroids) > 35:
                    kind = "weapon"
                else:
                    kind = random.choices(
                        ["speed", "shield", "bomb", "life", "weapon"],
                        weights=[30, 30, 20, 5, 15],
                        k=1
                    )[0]
                PowerUp(x, y, kind)

            updatable.update(dt)
            
            for obj in updatable:
                if hasattr(obj, "wrap_screen"):
                    obj.wrap_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        asteroid.split()
                        Explosion(asteroid.position.x, asteroid.position.y)
                        sound_manager.play_small_explosion()
                        shot.kill()
                        score += 100

            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    if player.invulnerable_timer > 0:
                         continue
                    sound_manager.play_hit()
                    lives -= 1
                    if lives > 0:
                        player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    else:
                        state = "GAME_OVER"

            for powerup in powerups:
                if player.collides_with(powerup):
                    sound_manager.play_powerup()
                    if powerup.kind == "bomb":
                        player.num_bombs += 1
                    elif powerup.kind == "life":
                        lives += 1
                    else:
                        player.power_up(powerup.kind)
                    powerup.kill()
            
            for bomb in bombs:
                if bomb.exploding and not bomb.damage_done:
                    sound_manager.play_explosion()
                    for asteroid in asteroids:
                        if bomb.position.distance_to(asteroid.position) <= BOMB_RADIUS:
                            asteroid.kill()
                            Explosion(asteroid.position.x, asteroid.position.y)
                            score += 50
                    bomb.damage_done = True
            
            for obj in drawable:
                obj.draw(screen)
            
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            
            bomb_text = font.render(f"Bombs: {player.num_bombs}", True, (255, 255, 255))
            screen.blit(bomb_text, (10, 40))

            for i in range(lives - 1):
                x = SCREEN_WIDTH - 30 - (i * 30)
                y = 30
                points = [
                    (x, y - 10),
                    (x - 8, y + 10),
                    (x + 8, y + 10)
                ]
                pygame.draw.polygon(screen, "white", points, 2)

        elif state == "GAME_OVER":
            over_text = title_font.render("GAME OVER", True, "white")
            score_text = font.render(f"Final Score: {score}", True, "white")
            restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, "white")
            
            over_rect = over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 60))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 10))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60))
            
            screen.blit(over_text, over_rect)
            screen.blit(score_text, score_rect)
            screen.blit(restart_text, restart_rect)

        pygame.display.flip()   
        dt = (clock.tick(60)) / 1000

if __name__ == "__main__":
    main()
