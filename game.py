# imports
import time

# Variables to store player data
money = 0
daily_users = 0
player_experience = 0
processing_power = 0

# Stats output 
def display_stats():
    print("================================")
    print("Money: $", money)
    print("Experience: ", player_experience)
    print("Processing Power: ", processing_power)
    print("================================")

# Functions + stat calculations
def get_name():
    name = input("Welcome to GPT-incremental! Please enter a name for your AI agent: ")
    return name

player_name = get_name()

def tutorial(wait_time):
    time.sleep(wait_time/2.25)
    print()
    start_tutorial = input("Would you like to start the tutorial [y/n] (default is y): ")
    if start_tutorial != "n":
        print()
        time.sleep(wait_time/1.5)
        print("GPT-incremental is a command-line incremental game revolving around building your own AI empire")
        time.sleep(wait_time)
        print(f"Your goal is to make as much money as possible through purchasing upgrades that boost your AI's efficiency")
        time.sleep(wait_time)
        print("There are several stats that you, as a player are required to understand:")
        time.sleep(wait_time)
        print()
        print("Money: The primary currency of the game and can be used to purchase upgrades.")
        time.sleep(wait_time)
        print("Daily users: The amount of individuals using your AI services. Daily users directly impact the amount of money generated")
        time.sleep(wait_time)
        print("Processing power: The strength of your computers running your AI services. A better (higher) processing power allows for stronger intelligence models")
        time.sleep(wait_time)

# Game loop
get_name()
tutorial(3)

