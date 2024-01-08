import pygame
import sys
import random

# Pygame initialization
pygame.init()

# Screen configuration
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spiderman Dodge")

# Background
background = pygame.image.load('back.jpg')  # Game background image
background = pygame.transform.scale(background, (width, height))

# Player
player_img = pygame.image.load('spiderman.png')  # Player (Spiderman) image
player_img = pygame.transform.scale(player_img, (40, 40))
player_rect = player_img.get_rect()
player_rect.topleft = (width // 2 - player_rect.width // 2, height - 2 * player_rect.height)
player_speed = 8
invulnerability_time = 780
is_invulnerable = False
invulnerability_timer = 0

# Enemies
enemy_img = pygame.image.load('ene.png')  # Enemy image
enemy_img = pygame.transform.scale(enemy_img, (40, 40))
enemies = []

# Extra lives (hearts)
heart_img = pygame.image.load('corazon.png')  # Heart image
heart_img = pygame.transform.scale(heart_img, (40, 40))
hearts = []

# Enemy spawn time (adjusted to 0.5 seconds)
spawn_time = 500

# Heart spawn time (adjusted to 0.70 seconds)
heart_spawn_time = 700

# Enemy falling speeds
enemy_fall_speed_low = 4
enemy_fall_speed_medium = 5
enemy_fall_speed_high = 6

# Speed change points
speed_change_score_medium = 50
speed_change_score_high = 100

# Score
score = 0
win_score = 150  # New winning score

# Lives and extra lives
current_lives = 2
max_lives = 4

# Clock to manage time
clock = pygame.time.Clock()

# Font for text
font = pygame.font.SysFont(None, 30)

# Music player
pygame.mixer.music.load('spidy.mp3')  # Game music file
pygame.mixer.music.set_volume(0.2)  # Adjust music volume
pygame.mixer.music.play(-1)  # Loop playback

# Flag for the first enemy
first_enemy_spawned = False

# Initialize time since the last heart
time_since_last_heart = 0

def display_score(score, lives):
    # Display score and lives on the screen
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (width - 10 - lives_text.get_width(), 10))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < width:
        player_rect.x += player_speed

    # Update player invulnerability
    if is_invulnerable:
        current_time = pygame.time.get_ticks()
        if current_time - invulnerability_timer >= invulnerability_time:
            is_invulnerable = False

    # Generate the first enemy at the beginning of the game
    if not first_enemy_spawned:
        enemies.append([random.randint(0, width - 40), 0])
        first_enemy_spawned = True

    # Generate enemies automatically after all enemies have passed underneath
    if all(enemy[1] > player_rect.y for enemy in enemies) and not is_invulnerable:
        for _ in range(random.randint(1, 6)):
            enemies.append([random.randint(0, width - 40), 0])

    # Generate extra lives more frequently
    time_since_last_heart += clock.get_rawtime()
    if time_since_last_heart >= heart_spawn_time:
        hearts.append([random.randint(0, width - 40), 0])
        time_since_last_heart = 0

    # Move and remove enemies
    for enemy in enemies:
        if score <= speed_change_score_medium:
            enemy[1] += enemy_fall_speed_low
        elif speed_change_score_medium < score <= speed_change_score_high:
            enemy[1] += enemy_fall_speed_medium
        elif speed_change_score_high < score <= win_score:
            enemy[1] += enemy_fall_speed_high
        else:
            enemy[1] += 0  # Stop falling after reaching the victory score

        if player_rect.colliderect(pygame.Rect(enemy[0], enemy[1], 40, 40)) and not is_invulnerable:
            current_lives -= 1
            is_invulnerable = True
            invulnerability_timer = pygame.time.get_ticks()
            enemies.remove(enemy)
        elif enemy[1] > height:
            enemies.remove(enemy)
            score += 1

    # Move and remove extra lives
    for heart in hearts:
        heart[1] += 4
        if player_rect.colliderect(pygame.Rect(heart[0], heart[1], 40, 40)):
            if current_lives < max_lives:
                current_lives += 1
            hearts.remove(heart)
        elif heart[1] > height:
            hearts.remove(heart)

    # Draw elements on the screen
    screen.blit(background, (0, 0))  # Draw background
    screen.blit(player_img, (player_rect.x, player_rect.y))
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))
    for heart in hearts:
        screen.blit(heart_img, (heart[0], heart[1]))

    display_score(score, current_lives)

    if score >= win_score:
        font_win = pygame.font.SysFont(None, 80)
        win_text = font_win.render("You Win!", True, (255, 255, 255))
        screen.blit(win_text, (width // 2 - win_text.get_width() // 2, height // 2 - win_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before exiting
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(60)









































