import pygame
import sys
import random

pygame.init()


def update_screen():
    pygame.display.flip()
    pygame.time.Clock().tick(60)


def draw_screen():
    # draw bg and artificial wall
    screen.fill(white)
    pygame.draw.rect(screen, black, (WALL_WIDTH, TOPPER, WIDTH - (2 * WALL_WIDTH), HEIGHT))
    # draw objects
    pygame.draw.rect(screen, blue, paddle)
    pygame.draw.rect(screen, white, ball)
    # draw HUD
    screen.blit(game_font.render(f"{score_m1}", True, white), score_text_r1)
    screen.blit(game_font.render(f"{score_m2}", True, white), score_text_r2)
    screen.blit(game_font.render(f"{deaths}", True, white), deaths_text)
    screen.blit(game_font.render(f"{players}", True, white), players_text)
    # draw bricks
    for row in bricks:
        for brick, color in row:
            pygame.draw.rect(screen, color, brick)


def create_bricks():
    for i in range(BRICK_ROWS):
        row_bricks = []
        for j in range(BRICK_COLS):
            color = yellow
            if i == 0 or i == 1:
                color = red
            elif i == 2 or i == 3:
                color = orange
            elif i == 4 or i == 5:
                color = green
            brick = pygame.Rect(j * (BRICK_WIDTH + 5) + 16, i * (BRICK_HEIGHT + 5) + HUD, BRICK_WIDTH, BRICK_HEIGHT)
            row_bricks.append((brick, color))
        bricks.append(row_bricks)


def spawn_bricks():
    if all(not row for row in bricks):
        if score_m1 > 0 or score_m2 > 0:
            scoring_sound_effect.play()
        create_bricks()


def ball_movement():
    global ball_speed, ball_speed_x, ball_speed_y, score_m1, ball_direction, num_of_collisions
    ball.x += ball_speed_x * ball_direction
    ball.y += ball_speed_y
    # collision with walls
    if ball.left <= WALL_WIDTH + BALL_SIZE or ball.right >= WIDTH - (WALL_WIDTH + BALL_SIZE):
        bounce_sound_effect.play()
        ball_speed_x *= -1
    if ball.top <= TOPPER:
        bounce_sound_effect.play()
        ball_speed_y *= -1
    # collision with paddle
    if ball.colliderect(paddle):
        bounce_sound_effect.play()
        ball_speed_y *= -1
        if not ended_game:
            ball_direction = (paddle.centerx - ball.centerx) / (BRICK_WIDTH / 2)
            num_of_collisions += 1
            if num_of_collisions == 4 or num_of_collisions == 12:
                ball_speed += 2
                ball_speed_x = ball_speed
                ball_speed_y = -ball_speed


def ball_punches_brick(match_value):
    global ball_speed, ball_speed_x, ball_speed_y, score_m1, score_m2, hit_orange, hit_red, ball
    for row in bricks:
        for brick, color in row:
            if ball.colliderect(brick):
                bounce_sound_effect.play()
                ball_speed_y *= -1
                if not ended_game:
                    row.remove((brick, color))
                    if match_value == 1:
                        if color == green:
                            score_m1 += 3
                        elif color == orange:
                            score_m1 += 5
                            if not hit_orange:
                                hit_orange = True
                                ball_speed += 2
                                ball_speed_x = ball_speed
                                ball_speed_y = -ball_speed
                        elif color == red:
                            score_m1 += 7
                            if not hit_red:
                                hit_red = True
                                ball_speed += 2
                                ball_speed_x = ball_speed
                                ball_speed_y = -ball_speed
                        else:
                            score_m1 += 1
                    else:
                        if color == green:
                            score_m2 += 3
                        elif color == orange:
                            score_m2 += 5
                        elif color == red:
                            score_m2 += 7
                        else:
                            score_m2 += 1


def restore_ball():
    global deaths, ball_speed, ball_speed_x, ball_speed_y, ball_direction, num_of_collisions, hit_red, hit_orange
    if ball.top >= HEIGHT:
        deaths += 1
        ball.x = WIDTH // 2 - BALL_SIZE
        ball.y = HEIGHT // 2 - BALL_SIZE
        ball_speed = 4
        ball_speed_x = ball_speed
        ball_speed_y = -ball_speed
        ball_direction = round(random.uniform(-1.5, 1.5), 3)
        num_of_collisions = 0
        hit_orange = False
        hit_red = False


def scoring_matches():
    global score_m1, score_m2, match
    if score_m1 >= max_score_per_matches:
        score_m2 += int(score_m1 - max_score_per_matches)
        score_m1 = 0
        match = 2
    if score_m2 >= max_score_per_matches:
        score_m2 = score_m1 = 0
        match = 1


def end_screen():
    global ended_game
    if deaths > 3 or score_m2 >= max_score_per_matches:
        paddle.width = WIDTH
        paddle.x = 0
        ended_game = True


# colors
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
orange = (255, 165, 0)
red = (255, 0, 0)
blue = (10, 133, 194)

# screen settings
WIDTH = 600
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")
HUD = 150

# wall size
WALL_WIDTH = 10
TOPPER = 20

# SFX effects and fonts
bounce_sound_effect = pygame.mixer.Sound('assets/bounce.wav')
scoring_sound_effect = pygame.mixer.Sound('assets/258020__kodack__arcade-bleep-sound.wav')
game_font = pygame.font.Font("assets/PressStart2P.ttf", 40)
game_text = game_font.render('000', True, white)
score_text_r1 = game_text.get_rect(center=(WIDTH - (WALL_WIDTH * 12), TOPPER * 6))
deaths_text = game_text.get_rect(center=(WIDTH - (WALL_WIDTH * 12), TOPPER * 3))
players_text = game_text.get_rect(center=(WALL_WIDTH * 12, TOPPER * 3))
score_text_r2 = game_text.get_rect(center=(WALL_WIDTH * 12, TOPPER * 6))

# Paddle
BRICK_WIDTH = 36
BRICK_HEIGHT = 10
paddle_speed = 15
paddle = pygame.Rect((WIDTH - BRICK_WIDTH) // 2, HEIGHT - BRICK_HEIGHT - HUD // 2, BRICK_WIDTH, BRICK_HEIGHT)

# Ball
BALL_SIZE = 5
ball_speed = 4
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE, HEIGHT // 2 - BALL_SIZE, BALL_SIZE * 2, BALL_SIZE * 2)
ball_speed_x = ball_speed
ball_speed_y = -ball_speed
ball_direction = round(random.uniform(-1.5, 1.5), 3)
num_of_collisions = 0
hit_orange = False
hit_red = False

# Bricks
BRICK_ROWS = 8
BRICK_COLS = 14
bricks = []

# game control
running = True
ended_game = False

# scores and matches
max_score = 896
max_score_per_matches = max_score / 2
score_m1 = 0
score_m2 = 0
match = 1
deaths = 0
players = 1

# main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > (WALL_WIDTH * 2):
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH - (WALL_WIDTH * 2):
        paddle.x += paddle_speed

    # ball movement and collision
    ball_movement()
    # scoring system
    ball_punches_brick(match)
    scoring_matches()
    # create bricks
    spawn_bricks()
    # Check if the ball missed the paddle
    restore_ball()

    # Draw everything
    draw_screen()
    # update screen
    update_screen()

    # show end screen
    end_screen()

# End of game
pygame.display.flip()
pygame.time.delay(3000)

pygame.quit()
sys.exit()
