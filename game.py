# imports
import time

# Variables to store player data
agent_name = ""
money = 0
monthly_users = 0
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
def get_player_name():
    player_name = input("Welcome to GPT-incremental! Please enter your name: ")
    time.sleep(1)
    print(f"Hello, {player_name}!")

def tutorial():
    print()
    start_tutorial = input("Would you like to start the tutorial [y/n] (default is y): ")
    if start_tutorial != "n":
        print()
        time.sleep(0.25)
        print("GPT-incremental is a command-line incremental game revolving around building your own AI empire")
        time.sleep(2)
        print(f"Your goal is to make as much money as possible through purchasing upgrades that boost your AI's efficiency")
        time.sleep(2)
        print("There are several stats that you, as a player are required to understand:")
        time.sleep(2)
        print("Money: Money is the primary currency of the ")

            

# Game loop
get_player_name()
tutorial()

