import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants for the display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 80, 27)  # Dark green
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")

# Load card images
def load_card_images():
    card_images = {}
    card_folder = 'C:/Users/darre/OneDrive/Documents/Work/Computational/Cards'
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


def main():
    pygame.init()
    card_images = load_card_images()
    deck = create_deck()
    player_balance = 1000  # Starting balance
    
    running = True
    while running:
        game_over = False
        # Start a new game or round with betting
        player_hand, dealer_hand, deck, bet, player_balance, bet_confirmed = new_game(deck, player_balance)
        
        
        if not bet_confirmed:
            running = False
            break  

        while not game_over and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:  # Hit
                        deal_card(deck, player_hand)
                        if calculate_hand_value(player_hand) > 21:
                            game_over = True
                    elif event.key == pygame.K_s:  # Stand
                        while calculate_hand_value(dealer_hand) < 17:
                            deal_card(deck, dealer_hand)
                        game_over = True

            # Clear the screen and redraw
            screen.fill(BACKGROUND_COLOR)
            draw_hands(player_hand, dealer_hand, card_images)
            draw_text(f"Player: {calculate_hand_value(player_hand)}", (100, 370), 36)
            draw_text(f"Balance: £{player_balance}", (600, 10), 24)
            
            if game_over:
                # Determine winner
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
                break  # Exit the loop to start a new game or end based on your game design.

            pygame.display.flip()
    
    pygame.quit()




if __name__ == "__main__":
    main()