import pygame
import random
import math
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Avoiding Rockets")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

coin_radius = 10
plane_speed = 7
initial_rocket_speed = 3
rocket_speed = initial_rocket_speed
score = 0
level = 1

font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()
last_rocket_spawn_time = time.time()
last_coin_spawn_time = time.time()
last_level_up_time = time.time()

background_image = pygame.image.load("background.png")
plane_image = pygame.image.load("plane.png")
rocket_image = pygame.image.load("rocket.png")

background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
plane_image = pygame.transform.scale(plane_image, (40, 40))
rocket_image = pygame.transform.scale(rocket_image, (30, 30))

plane_rect = plane_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

rockets = []
coins = []

def spawn_rocket():
    x = random.choice([0, WIDTH])
    y = random.randint(0, HEIGHT)
    rockets.append([x, y])

def spawn_coin():
    x = random.randint(coin_radius, WIDTH - coin_radius)
    y = random.randint(coin_radius, HEIGHT - coin_radius)
    spawn_time = time.time()
    coins.append([x, y, spawn_time])

def display_score_and_level():
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, [WIDTH - 120, 10])
    screen.blit(level_text, [WIDTH - 120, 40])

running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()

    angle = math.degrees(math.atan2(mouse_y - plane_rect.centery, mouse_x - plane_rect.centerx)) - 90
    rotated_plane = pygame.transform.rotate(plane_image, angle)
    rotated_plane_rect = rotated_plane.get_rect(center=plane_rect.center)

    small_plane_hitbox = rotated_plane_rect.inflate(-20, -20)

    direction = math.atan2(mouse_y - plane_rect.centery, mouse_x - plane_rect.centerx)
    plane_rect.x += plane_speed * math.cos(direction)
    plane_rect.y += plane_speed * math.sin(direction)

    screen.blit(rotated_plane, rotated_plane_rect)

    for i, rocket in enumerate(rockets[:]):
        rx, ry = rocket
        angle = math.atan2(plane_rect.centery - ry, plane_rect.centerx - rx)
        rocket[0] += rocket_speed * math.cos(angle)
        rocket[1] += rocket_speed * math.sin(angle)

        rocket_angle = math.degrees(angle) - 90
        rotated_rocket = pygame.transform.rotate(rocket_image, rocket_angle)
        rotated_rocket_rect = rotated_rocket.get_rect(center=(int(rocket[0]), int(rocket[1])))

        small_rocket_hitbox = rotated_rocket_rect.inflate(-10, -10)

        if small_plane_hitbox.colliderect(small_rocket_hitbox):
            running = False

        for j in range(i + 1, len(rockets)):
            other_rocket = rockets[j]
            other_rocket_rect = pygame.Rect(other_rocket[0], other_rocket[1], rotated_rocket_rect.width, rotated_rocket_rect.height)

            if small_rocket_hitbox.colliderect(other_rocket_rect):
                rockets.remove(rocket)
                rockets.remove(other_rocket)
                break  

        screen.blit(rotated_rocket, rotated_rocket_rect)

    for coin in coins[:]:
        coin_x, coin_y, spawn_time = coin

        if time.time() - spawn_time > 10:
            coins.remove(coin)
            continue

        pygame.draw.circle(screen, YELLOW, (int(coin_x), int(coin_y)), coin_radius)

        if small_plane_hitbox.collidepoint(coin_x, coin_y):
            coins.remove(coin)
            score += 1

    current_time = time.time()
    if current_time - last_rocket_spawn_time > 4:
        spawn_rocket()
        last_rocket_spawn_time = current_time

    if current_time - last_coin_spawn_time > 3:
        spawn_coin()
        last_coin_spawn_time = current_time

    if current_time - last_level_up_time > 10:
        level += 1
        rocket_speed += 0.5
        last_level_up_time = current_time

    display_score_and_level()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()