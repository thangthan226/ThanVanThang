# THAY TOÀN BỘ FILE `main.py` BẰNG CODE NÀY


import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

WIDTH = 500
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Meme Edition")

clock = pygame.time.Clock()
FPS = 60

# =========================
# LOAD IMAGES
# =========================

bird_img = pygame.image.load("bird.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (60, 60))

pipe_top_img = pygame.image.load("pipe_top.png").convert_alpha()
pipe_bottom_img = pygame.image.load("pipe_bottom.png").convert_alpha()

pipe_top_img = pygame.transform.scale(pipe_top_img, (90, 400))
pipe_bottom_img = pygame.transform.scale(pipe_bottom_img, (90, 400))

background_img = pygame.image.load("background.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

ground_img = pygame.image.load("ground.png").convert()
ground_img = pygame.transform.scale(ground_img, (WIDTH, 100))

# =========================
# LOAD SOUND
# =========================

jump_sound = pygame.mixer.Sound("jump.wav")
score_sound = pygame.mixer.Sound("score.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

# =========================
# FONT
# =========================

big_font = pygame.font.SysFont("Arial", 55, bold=True)
medium_font = pygame.font.SysFont("Arial", 35, bold=True)
small_font = pygame.font.SysFont("Arial", 25)

# =========================
# GAME SETTINGS
# =========================

bird_x = 120
pipe_gap = 180
pipe_speed = 4
ground_height = 100
gravity = 0.5
jump_force = -9

# =========================
# RESET GAME
# =========================


def reset_game():

    bird_y = 300
    bird_velocity = 0
    ground_x = 0
    score = 0

    pipes = []

    for i in range(3):

        pipes.append({
            "x": 600 + i * 220,
            "height": random.randint(150, 350),
            "passed": False
        })

    return bird_y, bird_velocity, ground_x, score, pipes


# =========================
# MENU
# =========================


def draw_menu():

    while True:

        screen.blit(background_img, (0, 0))

        title = big_font.render("FLAPPY BIRD", True, (255, 255, 255))
        text = medium_font.render("PRESS SPACE", True, (255, 255, 255))
        info = small_font.render("ESC TO QUIT", True, (255, 255, 255))

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 300))
        screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 360))

        screen.blit(bird_img, (220, 430))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    return

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# =========================
# GAME OVER SCREEN
# =========================


def game_over_screen(score):

    while True:

        screen.blit(background_img, (0, 0))

        over_text = big_font.render("GAME OVER", True, (255, 50, 50))
        score_text = medium_font.render(f"SCORE: {score}", True, (255, 255, 255))

        retry_text = small_font.render("PRESS R TO RETRY", True, (255, 255, 255))
        menu_text = small_font.render("PRESS M FOR MENU", True, (255, 255, 255))

        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, 180))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 300))
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, 390))
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, 440))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    return "retry"

                if event.key == pygame.K_m:
                    return "menu"


# =========================
# MAIN LOOP
# =========================

while True:

    draw_menu()

    bird_y, bird_velocity, ground_x, score, pipes = reset_game()

    running = True

    while running:

        clock.tick(FPS)

        # EVENTS
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_force
                    jump_sound.play()

        # PHYSICS
        bird_velocity += gravity
        bird_y += bird_velocity

        # MOVE GROUND
        ground_x -= pipe_speed

        if ground_x <= -WIDTH:
            ground_x = 0

        # MOVE PIPES
        for pipe in pipes:
            pipe["x"] -= pipe_speed

        # REMOVE OLD PIPE
        if pipes[0]["x"] < -100:

            pipes.pop(0)

            pipes.append({
                "x": pipes[-1]["x"] + 220,
                "height": random.randint(150, 350),
                "passed": False
            })

        # SCORE
        for pipe in pipes:

            if not pipe["passed"] and pipe["x"] < bird_x:
                pipe["passed"] = True
                score += 1
                score_sound.play()

        # COLLISION
        for pipe in pipes:

            if bird_x + 40 > pipe["x"] and bird_x < pipe["x"] + 90:

                if bird_y < pipe["height"]:
                    hit_sound.play()
                    running = False

                if bird_y + 50 > pipe["height"] + pipe_gap:
                    hit_sound.play()
                    running = False

        # HIT GROUND
        if bird_y < 0 or bird_y + 60 > HEIGHT - ground_height:
            hit_sound.play()
            running = False

        # DRAW BACKGROUND
        screen.blit(background_img, (0, 0))

        # DRAW PIPES
        for pipe in pipes:

            screen.blit(pipe_top_img, (pipe["x"], pipe["height"] - 400))

            screen.blit(pipe_bottom_img, (pipe["x"], pipe["height"] + pipe_gap))

        # DRAW GROUND
        screen.blit(ground_img, (ground_x, HEIGHT - ground_height))
        screen.blit(ground_img, (ground_x + WIDTH, HEIGHT - ground_height))

        # DRAW BIRD
        screen.blit(bird_img, (bird_x, bird_y))

        # DRAW SCORE
        score_text = big_font.render(str(score), True, (255, 255, 255))
        screen.blit(score_text, (WIDTH // 2 - 15, 40))

        pygame.display.update()

    result = game_over_screen(score)

    if result == "menu":
        continue

