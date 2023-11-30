import pygame
import random

pygame.init()

# consts
COLOR_BLACK, COLOR_WHITE = (0, 0, 0), (255, 255, 255)
VW, VH = 1280, 720
MAX_SCORE = 5
PADDLE_HEIGHT = 150

# game settings
size = (VW, VH)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MyPong - PyGame Edition - 2022-12-12")
game_clock = pygame.time.Clock()

# score text
score_font = pygame.font.Font('assets/PressStart2P.ttf', 44)
score_text = score_font.render('00 x 00', True, COLOR_WHITE, COLOR_BLACK)
score_text_rect = score_text.get_rect(center=(680, 50))

# victory text
victory_font = pygame.font.Font('assets/PressStart2P.ttf', 50)
victory_text_rect = score_text.get_rect(center=(400, 350))

# sound effects
bounce_sound_effect = pygame.mixer.Sound('assets/bounce.wav')
scoring_sound_effect = pygame.mixer.Sound('assets/258020__kodack__arcade-bleep-sound.wav')

# players
player_1 = {"image": pygame.image.load("assets/player.png"), "y": 300, "move_up": False, "move_down": False}
player_2 = {"image": pygame.image.load("assets/player.png"), "y": 300}

# ball
ball = {
    "image": pygame.image.load("assets/ball.png"),
    "x": VW / 2,
    "y": VH / 2,
    "d_x": random.choice([6, -6]),
    "d_y": random.choice([6, -6])
}


# functions
def update_screen():
    pygame.display.flip()
    game_clock.tick(60)


def draw_objects():
    screen.blit(ball["image"], (ball["x"], ball["y"]))
    screen.blit(player_1["image"], (50, player_1["y"]))
    screen.blit(player_2["image"], (1180, player_2["y"]))
    screen.blit(score_font.render(
        f"{score_1} x {score_2}", True, COLOR_WHITE, COLOR_BLACK),
        score_text_rect
    )


def reset_ball():
    ball["x"] = VW / 2
    ball["y"] = random.uniform(50, VH - 50)
    ball["d_x"] = random.choice([6, -6])
    ball["d_y"] = random.choice([6, -6])


def scoring_points():
    if ball["x"] < -50:
        scoring_sound_effect.play()
        reset_ball()
        return 2
    elif ball["x"] > VW + 50:
        scoring_sound_effect.play()
        reset_ball()
        return 1
    return 0


def ball_collision_with_wall():
    if ball["y"] > 700 or ball["y"] <= 0:
        ball["d_y"] *= -1
        bounce_sound_effect.play()
        return True
    return False


def check_wall_collision(player):
    if player["y"] <= 0:
        player["y"] = 0
    elif player["y"] >= VH - PADDLE_HEIGHT:
        player["y"] = VH - PADDLE_HEIGHT


def ball_collision_with_paddle(player, acc_x):
    if player["y"] < ball["y"] + 25:
        if player["y"] + PADDLE_HEIGHT > ball["y"]:
            bounce_sound_effect.play()
            ball["d_y"] = random.choice([6, 7, 8, 9, -6, -7, -8, -9])
            if not acc_x:
                ball["d_x"] *= -1.05
            else:
                ball["d_x"] *= -1


def ball_collision_with_paddle_corner(player):
    if player["y"] < ball["y"] + 25:
        if player["y"] + PADDLE_HEIGHT > ball["y"]:
            ball["d_y"] *= -1
            bounce_sound_effect.play()
            return True
    return False


# ball conditionals
punched_corner = False
accelerated_x = False

# game loop
score_1, score_2 = 0, 0
game_loop = True

while game_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

        #  keystroke events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_1["move_up"] = True
            if event.key == pygame.K_DOWN:
                player_1["move_down"] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_1["move_up"] = False
            if event.key == pygame.K_DOWN:
                player_1["move_down"] = False

    # objects drawing render
    screen.fill(COLOR_BLACK)
    draw_objects()

    # checking the victory condition
    if score_1 < MAX_SCORE and score_2 < MAX_SCORE:
        # refresh screen render
        update_screen()

        # player 1 movement
        if player_1["move_up"] and player_1["y"] > 0:
            player_1["y"] -= 10
        elif player_1["move_down"] and player_1["y"] < VH - PADDLE_HEIGHT:
            player_1["y"] += 10

        # player 2 movement
        if ball["x"] > VW / 4:
            target_y = ball["y"] + random.randint(-40, 40)
            if player_2["y"] + PADDLE_HEIGHT / 2 < target_y and player_2["y"] < VH - PADDLE_HEIGHT:
                player_2["y"] += random.uniform(5, 8)
            elif player_2["y"] + PADDLE_HEIGHT / 2 > target_y and player_2["y"] > 0:
                player_2["y"] -= random.uniform(5, 8)

        # player's collision with wall
        check_wall_collision(player_1)
        check_wall_collision(player_2)

        # ball movement
        ball["x"] += ball["d_x"]
        ball["y"] += ball["d_y"]

        # ball collision with the wall
        if ball_collision_with_wall():
            punched_corner = False

        # ball collision with the player 1 's paddle
        if ball["x"] < 100:
            if ball["x"] > 90:
                ball_collision_with_paddle(player_1, accelerated_x)
            # if ball punches the corner
            elif not punched_corner:
                if ball_collision_with_paddle_corner(player_1):
                    punched_corner = True

        # ball collision with the player 2's paddle
        if ball["x"] > 1160:
            if ball["x"] < 1170:
                ball_collision_with_paddle(player_2, accelerated_x)
            # if ball punches the corner
            elif not punched_corner:
                if ball_collision_with_paddle_corner(player_2):
                    punched_corner = True

        # scoring update
        scoring_result = scoring_points()
        if scoring_result == 1:
            score_1 += 1
            accelerated_x = False
        elif scoring_result == 2:
            score_2 += 1
            accelerated_x = False
    else:
        screen.fill(COLOR_BLACK)
        # drawing victory
        winner = 'Player 1' if score_1 > score_2 else 'Player 2'
        screen.blit(
            victory_font.render(f"{winner} VICTORY", True, COLOR_WHITE, COLOR_BLACK),
            victory_text_rect
        )
        update_screen()

pygame.quit()
