import pygame
import sys
import time


def ball_movement():
    global ballx, bally, b_score, p_score, still_playing
    ball.x += ballx * balldirect.x
    ball.y += bally * balldirect.y
    if ball.top <= 0 or ball.bottom >= height:
        bally *= -1
        bounce_sound_effect.play()
    if ball.right >= width or ball.left <= 0:
        if ball.right >= width:
            b_score += 1
            scoring_sound_effect.play()
        if ball.left <= 0:
            p_score += 1
            scoring_sound_effect.play()
        ball_reset()
        if b_score > 2 or p_score > 2:
            still_playing = False
    if ball.colliderect(player):
        balldirect.x *= -1
        balldirect.y = ((player.centery - ball.y) / (pallet_size / 2)) * -1
        bounce_sound_effect.play()
        ballx += 0.25
        bally += 0.25
    if ball.colliderect(bot):
        balldirect.x *= -1
        balldirect.y = ((bot.centery - ball.y) / (pallet_size / 2)) * -1
        bounce_sound_effect.play()
        ballx += 0.25
        bally += 0.25


def player_animation():
    player.y += p_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= height:
        player.bottom = height


def ball_reset():
    global ballx, bally
    ball.center = (width / 2, height / 2)
    ballx *= 0
    bally *= 0
    balldirect.x = 1
    balldirect.y = 0
    bot.center = (10, height / 2)
    player.center = (width - 5, height / 2)


# texts and measures
width = 1280
height = 720
pallet_size = 180
pallet_width = 10
ball_size = 30
p_score = 0
b_score = 0
pygame.init()
game_font = pygame.font.Font("assets/PressStart2P.ttf", 100)

# songs
bounce_sound_effect = pygame.mixer.Sound('assets/bounce.wav')
scoring_sound_effect = pygame.mixer.Sound('assets/258020__kodack__arcade-bleep-sound.wav')

# size screen
size = (width, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
bg = (0, 0, 0)

# draw
player = pygame.Rect(width - 20, height / 2 - 100, pallet_width, pallet_size)
bot = pygame.Rect(10, height / 2 - 100, pallet_width, pallet_size)
ball = pygame.Rect(width / 2 - 15, height / 2 - 15, ball_size, ball_size)

# ball and paddle speed
ballx = 0
bally = 0
balldirect = pygame.math.Vector2(1, 0)
p_speed = 0
b_speed = 10
a = 10
still_playing = True

while still_playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                p_speed += a
            if event.key == pygame.K_UP:
                p_speed -= a
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                p_speed -= a
            if event.key == pygame.K_UP:
                p_speed += a
        if ballx == 0 or bally == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    ballx, bally = 10, 10

    player_animation()
    ball_movement()

    if ball.x < width / 2:
        if bot.top <= ball.y:
            bot.top += b_speed
        if bot.bottom >= ball.y:
            bot.bottom -= b_speed

    if bot.top <= 0:
        bot.top = 0
    if bot.bottom >= height:
        bot.bottom = height

    # visible
    screen.fill(bg)
    pygame.draw.rect(screen, (255, 255, 255), player)
    pygame.draw.rect(screen, (255, 255, 255), bot)
    pygame.draw.rect(screen, (255, 255, 255), ball)
    pygame.draw.aaline(screen, (255, 255, 255), (width / 2, 0), (width / 2, height))
    player_text = game_font.render(f"{p_score}", False, (255, 255, 255))
    screen.blit(player_text, (width / 2 + 250, 50))
    bot_text = game_font.render(f"{b_score}", False, (255, 255, 255))
    screen.blit(bot_text, (270, 50))
    pygame.display.flip()
    clock.tick(75)

# END GAME SCREEN
screen.fill((0, 0, 0))
if p_score > b_score:
    end_text = f"Victory"
else:
    end_text = f"Defeat"
end_text_formated = game_font.render(end_text, False, (255, 255, 255))
screen.blit(end_text_formated, (350, 300))
pygame.display.update()
time.sleep(4)
