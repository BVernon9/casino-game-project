## for you byron

import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Roulette Simulation")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)

# Fonts
font = pygame.font.Font(None, 24)

# Game variables
player_balance = 1000
bet_amount = 50
bet_type = None
bet_choice = None
winning_number = None
angle = 0
ball_position = (0, 0)
current_speed = 0
game_state = 'betting'
winning_text = ""
bet_placed = False
input_text = ""

# Define red and black numbers
red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
black_numbers = set(range(1, 37)) - red_numbers

# Initialize wheel segments
wheel_segments = [
    (GREEN, '0'), *[(RED if n in red_numbers else BLACK, str(n)) for n in range(1, 37)]
]

# Wheel and ball parameters
wheel_radius = 150
wheel_center = (400, 300)
num_segments = 37  # Including 0
segment_angle = 360 / num_segments
ball_radius = 8



def show_welcome_screen():
    welcome_running = True
    while welcome_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press space to continue to the game.
                    welcome_running = False
        
        screen.fill(DARK_GREEN)
        # Instructions text
        instructions_text = [
            "Welcome to Roulette!",
            "Press 'R' to bet on Red.",
            "Press 'B' to bet on Black.",
            "Press 'H' to bet on House.",
            "Press 'O' to bet on Odd.",
            "Press 'E' to bet on Even.",
            "Use UP and DOWN arrows to adjust bet amount.",
            "Press SPACE to start playing."
        ]
        
        y_offset = 100
        for line in instructions_text:
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(screen_width / 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 30  # Adjust spacing as needed
        
        pygame.display.flip()
        pygame.time.wait(100)


def draw_wheel():
    for i, (color, number) in enumerate(wheel_segments):
        start_angle = (360 / num_segments) * i - 90
        end_angle = start_angle + (360 / num_segments)
        pygame.draw.polygon(screen, color, [
            wheel_center,
            (wheel_center[0] + wheel_radius * math.cos(math.radians(start_angle)), wheel_center[1] + wheel_radius * math.sin(math.radians(start_angle))),
            (wheel_center[0] + wheel_radius * math.cos(math.radians(end_angle)), wheel_center[1] + wheel_radius * math.sin(math.radians(end_angle)))
        ])
        angle_mid = start_angle + (360 / num_segments) / 2
        x = wheel_center[0] + (wheel_radius - 20) * math.cos(math.radians(angle_mid))
        y = wheel_center[1] + (wheel_radius - 20) * math.sin(math.radians(angle_mid))
        text = font.render(number, True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

def handle_key_events():
    global bet_amount, game_state, current_speed, bet_placed, input_text, bet_choice, bet_type, player_balance
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_state == "betting":
                if event.key == pygame.K_RETURN and game_state == 'betting' and input_text:
                    process_bet_input()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_UP:
                    bet_amount += 10
                    update_bet_display()
                elif event.key == pygame.K_DOWN:
                    bet_amount = max(10, bet_amount - 10)
                    update_bet_display()
                elif event.key in (pygame.K_r, pygame.K_b, pygame.K_h, pygame.K_o, pygame.K_e):
                    input_text = {'r': 'red', 'b': 'black', 'h': 'house', 'o': 'odd', 'e': 'even'}[pygame.key.name(event.key)]
                    process_bet_input()

def process_bet_input():
    global bet_amount, game_state, current_speed, bet_placed, input_text, bet_choice, bet_type, player_balance
    valid_bets = {'red', 'black', 'house', 'odd', 'even'}
    if input_text in valid_bets:
        bet_choice = input_text
        bet_type = 'number' if input_text == 'house' else 'color' if input_text in ['red', 'black'] else 'evenodd'
        player_balance -= bet_amount
        bet_placed = True
        game_state = 'spinning'
        speed_min = 10
        speed_max = 15
        current_speed = random.uniform(speed_min, speed_max)
        input_text = ""  # Clear input after processing

def draw_current_bet():
    if bet_placed:
        bet_text = f"Bet: {bet_choice.upper()} - Amount: £{bet_amount}"
    else:
        bet_text = "No bet placed"
    bet_info_text = font.render(bet_text, True, WHITE)
    bet_info_rect = bet_info_text.get_rect(left=10, top=20)
    screen.blit(bet_info_text, bet_info_rect)
    balance_text = font.render(f"Balance: £{player_balance}", True, WHITE)
    balance_rect = balance_text.get_rect(left=10, top=40)
    screen.blit(balance_text, balance_rect)
    
def draw_ball():
    global ball_position
    pygame.draw.circle(screen, WHITE, ball_position, ball_radius)

def spin_wheel():
    global angle, ball_position, current_speed, game_state, winning_number, winning_text
    if game_state != 'spinning':
        return

    angle += current_speed
    if current_speed > 0:
        dec_min = 0.95
        dec_max = 0.999
        deceleration = random.uniform(dec_min, dec_max)
        current_speed *= deceleration  # Deceleration effect
    if current_speed <= 0.2 and current_speed > 0:
        current_speed = 0
        # Normalize the stopping angle of the wheel considering the -90 degrees offset when the segments are drawn
        normalized_angle = (angle + 90) % 360
        # Find the index of the segment where the ball has stopped
        segment_index = int(normalized_angle / segment_angle)
        # Adjust index based on wheel layout, if necessary
        # Use a lookup here if the numbers are not sequential
        winning_number = segment_index
        color = "Red" if winning_number in red_numbers else "Black" if winning_number != 0 else "Green"
        winning_text = f"Winning number is {color} {winning_number}"
        #print(f"Debug: Angle: {angle}, Index: {segment_index}, Number: {winning_number}")
        game_state = 'result'
        display_result()  # Call display_result to show the winning number
    rad_angle = math.radians(angle)
    ball_position = (
        int(wheel_center[0] + math.cos(rad_angle) * (wheel_radius - ball_radius)),
        int(wheel_center[1] + math.sin(rad_angle) * (wheel_radius - ball_radius)))

    # More code (if any)...



def draw_bet_amount():
    bet_text = f"Current Bet: £{bet_amount}"
    bet_display = font.render(bet_text, True, WHITE)
    bet_rect = bet_display.get_rect(left=10, top=60)  # Position it on the screen as needed
    screen.blit(bet_display, bet_rect)


def update_bet_display():
    bet_text = f"Current Bet: £{bet_amount}"
    screen.fill(DARK_GREEN)
    bet_display = font.render(bet_text, True, WHITE)
    bet_rect = bet_display.get_rect(left=10, top=60)
    screen.blit(bet_display, bet_rect)
    pygame.display.flip()


def update_balance_and_reset():
    global player_balance, winning_number, bet_type, bet_choice, bet_amount, game_state
    if bet_placed:
        won = False
        if bet_type == 'color' and ((bet_choice == 'red' and winning_number in red_numbers) or (bet_choice == 'black' and winning_number in black_numbers)):
            won = True
        elif bet_type == 'evenodd' and ((bet_choice == 'even' and winning_number % 2 == 0) or (bet_choice == 'odd' and winning_number % 2 != 0)):
            won = True
        elif bet_type == 'number' and bet_choice == str(winning_number):
            won = True

        if won:
            if bet_type == 'number':
                winnings = bet_amount * 35  # Paying 35 to 1 for straight-up bet
            else:
                winnings = bet_amount * 2  # Paying 1 to 1 for color or even/odd bet
            player_balance += winnings  # Adding winnings and refunding the initial bet amount
            result_text = f"You won £{winnings}!"
        else:
            result_text = "You lost!"  # No need to deduct bet_amount as it was already deducted

        result_text = font.render(result_text, True, WHITE)
        result_rect = result_text.get_rect(center=(screen_width / 2, screen_height / 2 + 30))
        screen.blit(result_text, result_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

    reset_game()


def reset_game():
    global angle, player_balance, bet_amount, bet_type, bet_choice, game_state, current_speed, bet_placed, winning_text
    player_balance = player_balance
    bet_amount = 50
    bet_type = None
    bet_choice = None
    game_state = 'betting'
    current_speed = 0
    angle = 0
    bet_placed = False
    winning_text = ""


def display_result():
    if game_state == 'result':
        result_text = font.render(winning_text, True, WHITE)
        result_rect = result_text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(result_text, result_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        update_balance_and_reset()

def game_loop():
    running = True
    while running:
        screen.fill(DARK_GREEN)
        handle_key_events()
        draw_wheel()
        draw_current_bet()
        draw_bet_amount()
        if game_state == 'spinning':
            spin_wheel()
            draw_ball()
        elif game_state == 'result':
            display_result()
        pygame.display.flip()
        pygame.time.wait(10)

# Uncomment the line below to run the game loop
show_welcome_screen()
game_loop()