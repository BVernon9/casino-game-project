import pygame
import time
import sys
import random

width, height = 60, 30

background_colour = (30,80,27)
skull_img = pygame.image.load('C:/Users/darre/OneDrive/Documents/Work/Computational/PNGS/skull.png')# Load the image
skull_img = pygame.transform.scale(skull_img, (width, height))

class Horse:
    def __init__(self, adjective, noun, colour, x, y):
        self.adjective = adjective
        self.noun = noun
        self.win_probability = random.uniform(0.01, 0.99)
        self.visual_horse = VisualHorse(colour, x, y)
        self.dead = False

    def calculate_odds(self):
        self.odds = 1 / self.win_probability

def create_horses(start_y=50,gap=50):
    adjectives = ["Colourful", "Swift", "Vibrant", "Playful", "Mysterious", "Graceful", "Dynamic", "Energetic", "Captivating", "Whimsical", "Magical", "Prolific", "Noble", "Furious", "Careful", "Corach", "Velvet", "Flimsy", "Long", "Tiny", "Wise", "Artificial", "Rushed", "Angry", "Powerful", "Tricky", "Bling", "Large", "Spontaneous", "Stupid", "Goofy", "Welsh", "Georgian", "Scouse", "Cockney", "Fashionable", "Sweaty", "Chatty", "Rambunctious", "Beaten", "Ferocious", "Naked"]

    nouns = ["Sunshine", "Moonlight", "Ocean", "Forest", "Mountain", "Adventure", "Dream", "Harmony", "Serenity", "Voyage", "Byron", "Kai", "Sigurd", "Loki", "Intelligence", "Yeats", "Rambler", "Dog", "Fella", "Geezer", "Lad", "Aswell", "Work", "Beach", "Elvis", "John", "Sea", "Bird", "Lady" ,"Harry", "Adam", "Luca", "Al", "Jasper", "XL Bully", "Maggie Thatcher", "Lizzie"]

    colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255,128,0),(255,255,0), (128,255,0), (0,255,128), (0,255,255), (0,128,255), (128,0,255), (255,0,255), (255,0,128), (128,128,128), (0,0,0), (255,255,255)]

    random.shuffle(adjectives)
    random.shuffle(nouns)
    random.shuffle(colours)
    horses = []
    x = 50

    for i in range(10):

        y = start_y + i * gap  # Calculate Y position based on a starting point and a gap
        colour = colours[i % len(colours)]
        horse = Horse(adjectives[i % len(adjectives)], nouns[i % len(nouns)], colour, x, y)
        horse.calculate_odds()
        horses.append(horse)
        
    return horses

# Example of a simple horse representation
class VisualHorse:
    def __init__(self, color, x, y, width=60, height=30, radius=15):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)  # Keep the rectangle for the alive state
        self.radius = radius  # Radius for the dead state circle
        self.skull_img = skull_img
    
    def draw(self, surface, dead=False):
        if not dead:
            # Draw the horse as a rectangle if it's alive
            pygame.draw.rect(surface, self.color, self.rect)
        else:
            # Draw the horse as a circle if it's dead
            # The circle's center is the center of the rectangle
            ##center = self.rect.center
            skull_x = self.rect.centerx - self.skull_img.get_width() / 2
            skull_y = self.rect.centery - self.skull_img.get_height() / 2
            surface.blit(self.skull_img, (skull_x, skull_y))
            
            ##pygame.draw.circle(surface, self.color, center, self.radius)

def simulate_race_visual(horses, screen, font, betting_agent, bet_horse):
    finish_line = screen.get_width() - 100  # Finish line position
    font = pygame.font.Font(None, 36)
    
    race_over = False
    winner = None

    while not race_over:
        screen.fill(background_colour)  # Desired background color

        # Draw the finish line
        pygame.draw.line(screen, (255, 0, 0), (finish_line + 60, 0), (finish_line + 60, screen.get_height()), 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            
        for horse in horses:
            if not horse.dead:
                # Adjust variance for each horse based on its win probability
                # Higher win probability (favorites) results in less variance, and vice versa
                variance_factor = random.uniform(0.01, 1.99 - horse.win_probability)  #variance to boost unfavourites, if horse has 0.99 win probability the most variance can be is 1
                variance = random.uniform(0.5, 1.5 + (variance_factor*0.5))
                base_movement = 3 + (horse.win_probability * 3)
                movement = base_movement * (1.2 * (variance**2))  # Base movement adjusted by variance
                
                deathchance = random.randint(1, int(1000*(horse.odds/2)))
                if deathchance == 1:
                    horse.dead = True 
                if horse.noun == "Maggie Thatcher":
                    horse.dead = True
                
                ###movement = horse.win_probability * 5 + random.randint(1, 3)
                ###horse.visual_horse.rect.x += movement
    
                horse.visual_horse.rect.x += movement
                horse.visual_horse.draw(screen, dead=horse.dead)
    
                if horse.visual_horse.rect.x >= finish_line and not winner:
                    winner = horse
                    race_over = True
                    
            else:
                
                horse.visual_horse.draw(screen, dead=horse.dead)
                

        pygame.display.flip()
        pygame.time.delay(100)

    if winner:
        net_winnings = betting_agent.check_results(winner)  # Get net winnings and update balance
        screen.fill(background_colour)  # Maintain background color consistency
        # Re-draw the finish line to keep it visible
        pygame.draw.line(screen, (255, 0, 0), (finish_line + 60, 0), (finish_line + 60, screen.get_height()), 5)
        
        messages = [
            f"The winner is: {winner.adjective} {winner.noun}!",
            f"Your net winnings: {'£{:.2f}'.format(net_winnings)}",
            f"Updated balance: {'£{:.2f}'.format(betting_agent.balance)}"
        ]
        for i, message in enumerate(messages):
            text = font.render(message, True, (255, 255, 255))
            screen.blit(text, (100, 100 + i * 30))
        
        pygame.display.flip()
        pygame.time.delay(5000)


class Bookies:
    def __init__(self, balance=1000):
        self.balance = balance
        self.bets = {}
        self.bet_amount = 0  # Track the bet amount for the current race

    def place_bet(self, horse, amount):
        self.bets[horse] = amount
        self.bet_amount = amount  # Remember the amount bet

    def check_results(self, winner):
        if winner in self.bets:
            winnings = self.bets[winner] * winner.odds
            self.balance += winnings - self.bet_amount # Update balance with winnings
            return winnings - self.bet_amount  # Return net winnings
        else:
            self.balance = self.balance - self.bet_amount
            return -self.bet_amount

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Horse Racing Game")

# Initialize the font for text rendering
pygame.font.init()
font = pygame.font.SysFont(None, 24)

# Function to create and display horses for selection
def display_horses(horses, screen):
    screen.fill((0, 0, 0))
    y_start = 20
    for index, horse in enumerate(horses):
        text = font.render(f"{index + 1}. {horse.adjective} {horse.noun}: Odds - {horse.odds:.2f}", True, (255, 255, 255))
        screen.blit(text, (20, y_start + (index * 30)))
    pygame.display.flip()
    
def get_betting_amount(screen, font, betting_amount):
    input_str = str(betting_amount)  # Convert initial amount to string
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False  # Exit loop when Enter is pressed
                elif event.key == pygame.K_BACKSPACE:
                    input_str = input_str[:-1]  # Remove last character
                elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    input_str += event.unicode  # Add character to input_str
                # Optionally, handle other keys (e.g., to allow decimal points or clear the input)

        screen.fill((background_colour))  # Clear screen (or set a specific background)
        prompt_text = font.render("Enter your bet amount and press Enter:", True, (255, 255, 255))
        input_text = font.render(input_str, True, (255, 255, 255))
        screen.blit(prompt_text, (50, 100))
        screen.blit(input_text, (50, 150))
        pygame.display.flip()

    return int(input_str) if input_str.isdigit() else 0
    
    
    
def display_horses_for_betting(horses, screen, font):
    y_start = 50
    gap = 40
    selected_horse = None
    betting_amount = 100  # Example fixed bet amount, could be made dynamic

    running = True
    while running:
        screen.fill(background_colour)  # Clear screen with background color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_horse = max(0, selected_horse - 1) if selected_horse is not None else 0
                elif event.key == pygame.K_DOWN:
                    selected_horse = min(len(horses) - 1, selected_horse + 1) if selected_horse is not None else 0
                elif event.key == pygame.K_RETURN and selected_horse is not None:
                    betting_amount = get_betting_amount(screen, font, betting_amount)
                    running = False  # Proceed to bet on the selected horse

        for index, horse in enumerate(horses):
            color_text = "Selected" if index == selected_horse else "Not Selected"
            horse_text = f"{index + 1}. {horse.adjective} {horse.noun} - Odds: {horse.odds:.2f} - {color_text}"
            text_surface = font.render(horse_text, True, (255, 255, 255))
            screen.blit(text_surface, (50, y_start + index * gap))

            # Draw a color block for each horse
            pygame.draw.rect(screen, horse.visual_horse.color, pygame.Rect(10, y_start + index * gap, 30, 20))

        pygame.display.flip()

    # Return the selected horse and betting amount
    return horses[selected_horse], betting_amount

def end(screen, font):
    screen.fill(background_colour)
    
    # Display options
    play_again_text = font.render("Press 'P' to play again or 'C' to cash out and exit.", True, (255, 255, 255))
    text_rect = play_again_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.blit(play_again_text, text_rect)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return True  # User chose to play again
                elif event.key == pygame.K_c:
                    return False  # User chose to cash out

def bankrupt(screen, font):
    message = "Well done! You've lost the mortgage, the wife and kids have left'. Press any key to exit."
    text = font.render(message, True, (255, 255, 255))
    screen.fill(background_colour)  # Clear the screen or set to a game over background
    screen.blit(text, (100, screen_height // 2))
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN):
                waiting_for_input = False

# Main game function
def main():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Horse Racing Game")
    font = pygame.font.SysFont(None, 24)

    running = True
    betting_agent = Bookies(balance=1000)

    while running:
        horses = create_horses()
        horses = sorted(horses, key=lambda x: x.odds, reverse=False)# Assuming this returns a list of horse objects properly initialized

        chosen_horse, bet_amount = display_horses_for_betting(horses, screen, font)
        betting_agent.place_bet(chosen_horse, bet_amount)

        simulate_race_visual(horses, screen, font, betting_agent, chosen_horse)
        
        if betting_agent.balance < 0:
            print("Game over! Your balance has become negative.")
            bankrupt(screen, font)  # Assume end_game is a function that handles game over scenario
            break  # Exit the game loop
        
        play_again = end(screen,font)
        if not play_again:
            print(f"Final balance: £{betting_agent.balance:.2f}")
            running = False
            


if __name__ == "__main__":
    main()

pygame.quit()
sys.exit()