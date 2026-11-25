# imports
import time
import os

# Variables to store player data
money = 100
daily_users = 0
processing_power = 0

menu_option = 0

# Stats output 
def display_stats():
    print("================================")
    print("GPT-Incremental -", ai_name)
    print("Money: $", money)
    print("Daily users: ", daily_users)
    print("Processing Power: ", processing_power)
    print("================================")

# Menu output
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
    name = input("Welcome to GPT-incremental! Please enter a name for your AI agent: ")
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
        time.sleep(wait_time/2)

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
        print("purchase successful!")
        return True
    else:
        print("insufficient funds!")
        return False

def display_upgrades():
    print()
    print("1. Better datacenters (increase processing power) - $50")
    print("2. Better advertising (increase daily users) - $100")
    print("3. Exit upgrades menu")
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
            result = purchase_upgrade(50)
            if result: # run if result is true (result is stored as a bool)
                processing_power = processing_power + 1


    elif menu == "2":
        menu_option = 2
    elif menu == "3":
            menu_option = 3

