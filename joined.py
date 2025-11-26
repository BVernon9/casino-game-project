# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 14:23:55 2024

@author: darre
"""

import pygame
import sys
import os
import random
import time
# Initialize Pygame
pygame.init()

# Screen dimensions and setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Casino Games")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Define font for text
font = pygame.font.SysFont("arial", 36)

# Global balance
player_balance = 1000

def main_menu():
    global player_balance
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    blackjack_game()  # Call your Blackjack game function
                elif event.key == pygame.K_2:
                    slot_machine_game()  # Call your Slot Machine game function
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))
        menu_text = font.render("Press 1 for Blackjack, 2 for Slots, ESC to Exit", True, WHITE)
        balance_text = font.render(f"Balance: £{player_balance}", True, GREEN)
        screen.blit(menu_text, (50, 200))
        screen.blit(balance_text, (50, 300))
        pygame.display.flip()


# Load card images
def load_card_images():
    card_images = {}
    card_folder = 'Cards'
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

    card_width = 90  # Adjust width as needed
    card_height = 140  # Adjust height as needed

    for suit in suits:
        for rank in ranks:
            filename = f"{rank.lower()}_of_{suit.lower()}.png"
            filepath = os.path.join(card_folder, filename)
            card_key = f"{rank} of {suit}"
            try:
                original_image = pygame.image.load(filepath).convert_alpha()
                scaled_image = pygame.transform.scale(original_image, (card_width, card_height))
                card_images[card_key] = scaled_image
            except pygame.error as e:
                print(f"Error loading image: {filepath} - {e}")
    return card_images

# Card values
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'jack': 10, 'queen': 10, 'king': 10, 'ace': 11
}

# Simple function to draw text on the screen
def draw_text(text, position, font_size=12, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Create a deck of cards
def create_deck():
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    return [f"{rank} of {suit}" for suit in suits for rank in ranks]

# Shuffle the deck
def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

# Deal a card from the deck
def deal_card(deck, hand):
    card = deck.pop()
    hand.append(card)
    return card

# Calculate the value of a hand
def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        rank = card.split(' of ')[0]
        value += card_values[rank]
        if rank == 'ace':
            aces += 1
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

# Draw the hands
def draw_hands(player_hand, dealer_hand, card_images):
    y_offset = 400
    for card in player_hand:
        card_image = card_images[card]
        x_offset = player_hand.index(card) * 60
        screen.blit(card_image, (100 + x_offset, y_offset))
    
    y_offset = 100
    for card in dealer_hand:
        card_image = card_images[card]
        x_offset = dealer_hand.index(card) * 60
        screen.blit(card_image, (100 + x_offset, y_offset))

# Start a new game with betting
def new_game(deck, player_balance):
    bet, bet_confirmed = get_bet_graphically(player_balance)
    if not bet_confirmed:  # If the bet was not confirmed, return a signal to not proceed with the game
        return [], [], deck, 0, player_balance, False

    player_hand = []
    dealer_hand = []
    deck = shuffle_deck(create_deck())
    deal_card(deck, player_hand)
    deal_card(deck, dealer_hand)
    deal_card(deck, player_hand)
    deal_card(deck, dealer_hand)
    player_balance -= bet
    return player_hand, dealer_hand, deck, bet, player_balance, True


def get_bet_graphically(player_balance):
    bet = 0
    betting = True
    bet_confirmed = False  # Add a flag to indicate bet confirmation
    while betting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                betting = False
                bet_confirmed = False  # Handle quitting during betting
                break  # Exit the loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and bet < player_balance:
                    bet += 10
                elif event.key == pygame.K_DOWN and bet > 0:
                    bet -= 10
                elif event.key == pygame.K_RETURN:
                    betting = False
                    bet_confirmed = True  # Confirm bet
                elif event.key == pygame.K_ESCAPE:
                    betting = False
                    bet = 0
                    bet_confirmed = False  # Bet canceled
                
        screen.fill(BACKGROUND_COLOR)
        draw_text("Place your bet", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60), 36)
        draw_text(f"Bet: £{bet}", (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2), 36)
        draw_text("Use UP/DOWN arrows to adjust, ENTER to confirm, ESC to cancel.", (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 60), 24)
        pygame.display.flip()

    return bet, bet_confirmed

BACKGROUND_COLOR = (30, 80, 27)  # Dark green
def blackjack_game():
    global player_balance
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    BACKGROUND_COLOR = (30, 80, 27)  # Dark green

    pygame.display.set_caption("Blackjack")

    card_images = load_card_images()
    deck = create_deck()
    bet = 0
    bet_confirmed = False
    running = True
    game_over = False

    while running:
        if not bet_confirmed:
            bet, bet_confirmed = get_bet_graphically(player_balance)
            if bet_confirmed:
                player_balance -= bet
                player_hand, dealer_hand, deck, bet, player_balance, bet_confirmed = new_game(deck, player_balance)
            else:
                break  # Return to the main menu if bet not confirmed

        while not game_over and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:  # Hit
                        deal_card(deck, player_hand)
                        if calculate_hand_value(player_hand) > 21:
                            game_over = True
                    elif event.key == pygame.K_s:  # Stand
                        while calculate_hand_value(dealer_hand) < 17:
                            deal_card(deck, dealer_hand)
                        game_over = True

            screen.fill(BACKGROUND_COLOR)
            draw_hands(player_hand, dealer_hand, card_images)
            draw_text(f"Player: {calculate_hand_value(player_hand)}", (100, 370), 36)
            draw_text(f"Balance: £{player_balance}", (600, 10), 24)

            if game_over:
                dealer_score = calculate_hand_value(dealer_hand)
                player_score = calculate_hand_value(player_hand)
                draw_text(f"Dealer: {dealer_score}", (100, 70), 36)
                if player_score > 21 or (dealer_score <= 21 and dealer_score > player_score):
                    winner = "Dealer"
                elif dealer_score > 21 or player_score > dealer_score:
                    winner = "Player"
                    player_balance += bet * 2
                elif player_score == dealer_score:
                    winner = "No one"
                    player_balance += bet
                
                draw_text(f"{winner} Wins", (300, SCREEN_HEIGHT // 2), 48)
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait for 2 seconds before proceeding
                game_over = True  # End game loop

        running = False

    # Return to main menu
    main_menu()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (105, 105, 105)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Define symbol sizes and load images, resizing them
SYMBOL_SIZE = (80, 120)  # Desired width and height of symbol images
symbols_images = {
    name: pygame.transform.scale(pygame.image.load(f"{name}.png"), SYMBOL_SIZE)
    for name in ["banana", "cherry", "orange", "apple", "seven"]
}

# Define font for text
font = pygame.font.SysFont("arial", 24)

# Define slots and positions
slot_positions = [
    (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 100),
    (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 100),
    (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - 100),
]

# Payouts and player balance
payouts = {"banana": 50, "cherry": 80, "orange": 150, "apple": 300, "seven": 1000}
player_balance = 1000

# Initial last spun symbols
last_spin_symbols = [None, None, None]
outcome_message = ""

def spin_reels():
    symbols = ["banana", "cherry", "orange", "apple", "seven"]
    weights = [40, 30, 20, 10, 1]  # banana is most common, seven is rarest
    return [random.choices(symbols, weights)[0] for _ in range(3)]

def calculate_payout(symbols):
    if len(set(symbols)) == 1:
        return payouts[symbols[0]]
    return 0

def draw_slot_machine(spin_active):
    # Main body of the slot machine
    pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150, 300, 300))
    pygame.draw.rect(screen, DARK_GRAY, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 140, 280, 280))

    # Slots for symbols
    for x, y in slot_positions:
        pygame.draw.rect(screen, WHITE, (x, y, SYMBOL_SIZE[0], SYMBOL_SIZE[1]))

    # Control panel
    pygame.draw.rect(screen, LIGHT_GRAY, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 160, 300, 30))
    button_color = GREEN if spin_active else RED
    pygame.draw.circle(screen, button_color, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 175), 15)
    text_surface = font.render("Press to Spin!", True, WHITE)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200))
    screen.blit(text_surface, text_rect)

def check_button_pressed(pos):
    button_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 175)
    distance = ((pos[0] - button_center[0]) ** 2 + (pos[1] - button_center[1]) ** 2) ** 0.5
    return distance <= 15

def display_balance_and_symbols():
    # Display player balance
    balance_text = font.render(f"Balance: £{player_balance}", True, WHITE)
    screen.blit(balance_text, (10, 10))
    # Display outcome message
    outcome_text = font.render(outcome_message, True, YELLOW)
    screen.blit(outcome_text, (10, 40))
    # Display symbols
    for i, symbol in enumerate(last_spin_symbols):
        if symbol:
            symbol_img = symbols_images[symbol]
            screen.blit(symbol_img, slot_positions[i])

def animate_reels():
    global last_spin_symbols, outcome_message
    symbols_list = list(symbols_images.keys())
    for _ in range(10):  # Number of frames to show before stopping
        for i in range(3):
            last_spin_symbols[i] = random.choice(symbols_list)
        display_balance_and_symbols()
        pygame.display.flip()
        time.sleep(0.1)  # Delay to simulate spinning
    last_spin_symbols = spin_reels()
    payout = calculate_payout(last_spin_symbols)
    if payout > 0:
        outcome_message = f"You Win! Payout: £{payout}"
    else:
        outcome_message = "You Lose!"

def slot_machine_game():
    global player_balance
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SYMBOL_SIZE = (80, 120)  # Symbol dimensions
    symbols_images = {
        name: pygame.transform.scale(pygame.image.load(f"{name}.png"), SYMBOL_SIZE)
        for name in ["banana", "cherry", "orange", "apple", "seven"]
    }

    slot_positions = [
        (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 100),
        (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 100),
        (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - 100),
    ]

    payouts = {"banana": 50, "cherry": 80, "orange": 150, "apple": 300, "seven": 1000}
    outcome_message = ""
    last_spin_symbols = [None, None, None]

    spin_active = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if check_button_pressed(pygame.mouse.get_pos()):
                    if player_balance >= 20 and not spin_active:
                        player_balance -= 20
                        spin_active = True
                        animate_reels()
                        spin_active = False
                        pygame.display.flip()

        screen.fill(BLACK)
        draw_slot_machine(spin_active)
        display_balance_and_symbols()
        pygame.display.flip()

    # Return to main menu
    main_menu()

if __name__ == "__main__":
    main_menu()