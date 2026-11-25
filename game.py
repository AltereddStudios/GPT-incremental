# imports
import time
import os

# Variables
money = 100
daily_users = 0
processing_power = 0

daily_users_cost = 100 # initial cost
processing_power_cost = 50 # initial cost

daily_users_level = 0
processing_power_level = 0

cost_multiplier = 1.3

menu_option = 0

# Display functions
def display_stats():
    print("================================")
    print("GPT-Incremental -", ai_name)
    print("Money: $", money)
    print("Daily users: ", daily_users)
    print("Processing Power: ", processing_power)
    print("================================")

def display_menu():
    print()
    print("Menu Options:")
    print()
    print("1. Upgrades")
    print("2. Import Save")
    print("3. Save code + Exit")
    print()
    menu_choice = input("Select a menu option: ")
    return menu_choice

# Starting functions
def get_name():
    name = input("Welcome to GPT-incremental! Please enter a name (max 20 chars) for your AI agent: ")
    name = name[:20]
    return name

def tutorial(wait_time):
    print()
    start_tutorial = input("Would you like to start the tutorial [y/n] (default is y): ").strip().lower()

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
        time.sleep(wait_time+3)

    else:
        print()

# Game functions
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def purchase_upgrade(upgrade_cost):
    global money
    
    if money >= upgrade_cost:
        money = money - upgrade_cost
        print()
        print("Purchase successful!")
        time.sleep(1)
        print()
        return True
    else:
        print()
        print("Insufficient funds!")
        time.sleep(1)
        print()
        return False

def display_upgrades():
    print()
    print("1. Better datacenters (increase processing power) - $",processing_power_cost)
    print("2. Better advertising (increase daily users) - $", daily_users_cost)
    print("3. Exit upgrades menu")
    print()
    upgrade_choice = input("Select an option: ").strip()
    return upgrade_choice

# Game loop
ai_name = get_name()
print("If you would like to load a save, go to menu 2 after the tutorial")

tutorial(3)

while menu_option != 3:
    display_stats()
    menu = display_menu()
    if menu == "1":
        menu_option = 1
        clear()
        display_stats()
        upgrade_choice = display_upgrades()
        if upgrade_choice == "1":
            result = purchase_upgrade(processing_power_cost)
            if result: # run if result is true (result is stored as a bool)
                processing_power = processing_power + 1
                processing_power_cost = round(processing_power_cost * cost_multiplier)
                processing_power_level = processing_power_level + 1

        if upgrade_choice == "2":
                    result = purchase_upgrade(daily_users_cost)
                    if result: # run if result is true (result is stored as a bool)
                        daily_users = daily_users + 1
                        daily_users_cost = round(daily_users_cost * cost_multiplier)
                        daily_users_level = daily_users_level + 1

    elif menu == "2":
        menu_option = 2

    elif menu == "3":
        # add save code output before adjusting menu option as it will end game loop
        menu_option = 3

    else:
        clear() # clears terminal if outputs dont match the integers

