# -*- coding: utf-8 -*-
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
import random

class Horse:
    def __init__(self, adjective, noun):
        self.adjective = adjective
        self.noun = noun
        self.win_probability = random.uniform(0.01, 0.99)

    def calculate_odds(self):
        self.odds = 1 / self.win_probability

def create_horses():
    adjectives = ["Colourful", "Swift", "Vibrant", "Playful", "Mysterious", "Graceful", "Dynamic", "Energetic", "Captivating", "Whimsical", "Magical", "Prolific", "Noble", "Furious", "Careful", "Corach", "Velvet", "Flimsy", "Long", "Tiny", "Wise", "Artificial", "Rushed", "Angry", "Powerful", "Tricky", "Bling", "Large", "Spontaneous", "Stupid", "Goofy", "Welsh", "Georgian", "Scouse", "Cockney", "Fashionable", "Sweaty", "Chatty", "Rambunctious"]

    nouns = ["Sunshine", "Moonlight", "Ocean", "Forest", "Mountain", "Adventure", "Dream", "Harmony", "Serenity", "Voyage", "Byron", "Kai", "Sigurd", "Loki", "Intelligence", "Yeats", "Rambler", "Dog", "Fella", "Geezer", "Lad", "Aswell", "Work", "Beach", "Elvis", "John", "Sea", "Bird", "Lady" ,"Harry", "Adam", "Luka", "Lana"]

    random.shuffle(adjectives)
    random.shuffle(nouns)

    horses = []

    for i in range(12):
        random_adjective = adjectives[i % len(adjectives)]
        random_noun = nouns[i % len(nouns)]
        horse = Horse(random_adjective, random_noun)
        horse.calculate_odds()
        horses.append(horse)

    return horses

def simulate_race(horses):
    # Simulate the race and determine the winner based on odds
    horse_weights = [1 / horse.odds for horse in horses]
    winner = random.choices(horses, weights=horse_weights)[0]
    return winner

class Bookies:
    def __init__(self, balance=1000):
        self.balance = round(balance, 2)
        self.bets = {}

    def place_bet(self, horse, amount):
        amount = round(amount, 2)
        
        if amount <= 0:
            print("Invalid bet amount. Please enter a positive value.")
            return

        if amount > self.balance:
            print("Insufficient balance.")
            return

        if horse not in self.bets:
            self.bets[horse] = 0

        self.bets[horse] += amount
        self.balance = round(self.balance - amount, 2)
        print(f"Bet placed on {horse.adjective} {horse.noun} for £{amount:.2f}. Remaining balance: £{self.balance:.2f}")

    def check_results(self, winner):
        if winner in self.bets:
            winnings = round(self.bets[winner] * winner.odds, 2)
            self.balance = round(self.balance + winnings, 2)
            print(f"Congratulations! You won £{winnings:.2f}. Updated balance: £{self.balance:.2f}")
        else:
            print(f"Sorry, you lost. Updated balance: £{self.balance:.2f}")


def get_user_bet_choice():
    while True:
        try:
            choice = int(input("Enter the number of the horse you want to bet on (1 to 12): "))
            if 1 <= choice <= 12:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def play_again():
    while True:
        choice = input("Do you want to play again? (y/n): ").lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")

horses = create_horses()
sorted_horses = sorted(horses, key=lambda x: x.odds, reverse=False)

for index, horse in enumerate(sorted_horses):
    print(f"{index + 1}. {horse.adjective} {horse.noun}: Odds - {horse.odds:.2f}")

user_choice = get_user_bet_choice()
chosen_horse = sorted_horses[user_choice - 1]

betting_agent = Bookies(balance=1000)
bet_amount = float(input("Enter the amount you want to bet: "))
betting_agent.place_bet(chosen_horse, bet_amount)

race_winner = simulate_race(horses)

print(f"The simulated winner is: {race_winner.adjective} {race_winner.noun}")
betting_agent.check_results(race_winner)

while True:
    play_again_option = input("Do you want to play again or cash out? (play/cash): ").lower()
    if play_again_option == 'play':
        horses = create_horses()
        sorted_horses = sorted(horses, key=lambda x: x.odds, reverse=False)

        for index, horse in enumerate(sorted_horses):
            print(f"{index + 1}. {horse.adjective} {horse.noun}: Odds - {horse.odds:.2f}")

        user_choice = get_user_bet_choice()
        chosen_horse = sorted_horses[user_choice - 1]

        # Example usage
        bet_amount = float(input("Enter the amount you want to bet: "))
        betting_agent.place_bet(chosen_horse, bet_amount)

        race_winner = simulate_race(horses)

        print(f"The simulated winner is: {race_winner.adjective} {race_winner.noun}")
        betting_agent.check_results(race_winner)
    elif play_again_option == 'cash':
        print(f"Your final balance: ${betting_agent.balance}")
        sys.exit()
    else:
        print("Invalid choice. Please enter 'play' or 'cash'.")
        
        


