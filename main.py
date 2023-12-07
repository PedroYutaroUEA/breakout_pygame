import pygame
import sys
import time


def update_screen():
    pygame.display.flip()
    clock.tick(60)


def ball_movement():
    # ball movement update
    ball["body"].x += ball["x"] * ball["direction"].x
    ball["body"].y += ball["y"] * ball["direction"].y
    # ball collision with top
    if ball["body"].top <= TOPPER:
        ball["y"] *= -1
        bounce_sound_effect.play()
    # ball collision with right/left
    if ball["body"].right >= WIDTH - WALL_WIDTH or ball["body"].left <= WALL_WIDTH:
        ball["x"] *= -1
        bounce_sound_effect.play()

    # ball collision with player
    if ball["body"].colliderect(player["body"]):
        ball["direction"].x *= -1
        ball["direction"].y = ((player["body"].centery - ball["body"].y) / (BRICK_HEIGHT / 2)) * -1
        bounce_sound_effect.play()
        ball["x"] += 0.25
        ball["y"] += 0.25


def player_movement():
    player["body"].x += player["speed"]
    if player["body"].left <= 0:
        player["body"].left = 0
    if player["body"].right <= WIDTH - BRICK_WIDTH:
        print("test")
        player["body"].bottom = WIDTH


def ball_reset():
    ball["body"].center = (WIDTH / 2, HEIGHT / 2)
    ball["x"] *= 0
    ball["y"] *= 0
    ball["direction"].x = 1
    ball["direction"].y = 0
    player["body"].center = (WIDTH / 2, HEIGHT - (HEIGHT / 10))


def draw_screen():
    # show objects on screen
    screen.fill(white)
    pygame.draw.rect(screen, bg, (WALL_WIDTH, TOPPER, WIDTH - (2 * WALL_WIDTH), HEIGHT))
    pygame.draw.rect(screen, (10, 133, 194), player["body"])
    pygame.draw.rect(screen, (255, 255, 255), ball["body"])
    # draw bricks
    pygame.draw.rect(screen, (196, 196, 41), yellow_brick["body"])
    pygame.draw.rect(screen, (10, 135, 51), green_brick["body"])
    pygame.draw.rect(screen, (198, 136, 10), orange_brick["body"])
    pygame.draw.rect(screen, (166, 31, 10), red_brick["body"])


# game setup
pygame.init()
clock = pygame.time.Clock()
running = True

# consts
WIDTH = 700
HEIGHT = 800
BRICK_WIDTH = 50
BRICK_HEIGHT = 20
WALL_WIDTH = 10
TOPPER = 20
BALL_SIZE = 10

# screen setup
screen_size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(screen_size)
bg = (0, 0, 0)
white = (255, 255, 255)

# SFX effects and fonts
bounce_sound_effect = pygame.mixer.Sound('assets/bounce.wav')
scoring_sound_effect = pygame.mixer.Sound('assets/258020__kodack__arcade-bleep-sound.wav')
game_font = pygame.font.Font("assets/PressStart2P.ttf", 80)

# ball
ball = {
    "body": pygame.Rect(WIDTH / 2 - 15, HEIGHT / 2 - 15, BALL_SIZE, BALL_SIZE),
    "x": 0,
    "y": 0,
    "speed": 10,
    "direction": pygame.math.Vector2(1, 0)
}

# bricks
brick_shape = pygame.Rect((WIDTH / 2) - (BRICK_WIDTH / 2), HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
yellow_brick = {"body": brick_shape, "value": 1, "punched": False}
green_brick = {"body": brick_shape, "value": 3, "punched": False}
orange_brick = {"body": brick_shape, "value": 5, "punched": False}
red_brick = {"body": brick_shape, "value": 7, "punched": False}

# player
player = {"body": brick_shape, "speed": 0}
A_FACTOR = 10
players = 1

# scores and rounds
round = 1
max_score = 896
max_score_per_round = max_score / 2
score_r1 = 0
score_r2 = 0
b_score = 0
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player["speed"] += A_FACTOR
            if event.key == pygame.K_LEFT:
                player["speed"] -= A_FACTOR
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player["speed"] -= A_FACTOR
            if event.key == pygame.K_LEFT:
                player["speed"] += A_FACTOR
        if ball["x"] == 0 or ball["y"] == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    ball["x"], ball["y"] = 10, 10

    player_movement()
    ball_movement()

    # display screen
    draw_screen()

    player_text = game_font.render(f"{score}", False, white)
    screen.blit(player_text, (WIDTH / 2 + 250, 50))
    update_screen()

# CHANGING ROUNDS
if score_r1 > max_score_per_round:
    round = 2
    score_r2 += score_r1 - max_score_per_round
    score_r1 = 0
    scoring_sound_effect.play()
elif score_r2 > max_score_per_round:
    round = 1
    score_r2 = 0
    scoring_sound_effect.play()
end_text = f"You win!"
end_text_formatted = game_font.render(end_text, False, (255, 255, 255))
screen.blit(end_text_formatted, (350, 300))
pygame.display.update()
time.sleep(4)
