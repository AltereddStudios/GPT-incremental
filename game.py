# imports
import os
import threading
import time
import json

from prompt_toolkit import PromptSession

# Variables
money = 100
daily_users = 1
processing_power = 1

daily_users_cost = 100 # initial cost
processing_power_cost = 50 # initial cost

daily_users_level = 1
processing_power_level = 1

cost_multiplier = 1.3

menu_option = 0

session = PromptSession()
running = True

money_lock = threading.Lock()

# Display functions
def display_stats():
    with money_lock:
        current_money = money
        current_daily_users = daily_users
        current_processing_power = processing_power

    print("================================")
    print("GPT-Incremental -", ai_name)
    print("Money: $", round(current_money, 2))
    print("Daily users: ", current_daily_users)
    print("Processing Power: ", current_processing_power)
    print("================================")

def display_menu():
    print()
    print("Menu Options:")
    print()
    print("1. Upgrades")
    print("2. Import Save")
    print("3. Save code + Exit")
    print()
    menu_choice = session.prompt("Select a menu option: ")
    return menu_choice

# Starting functions
def get_name():
    name = session.prompt("Welcome to GPT-incremental! Please enter a name (max 20 chars) for your AI agent: ")
    name = name[:20]
    return name

def tutorial(wait_time):
    print()
    start_tutorial = session.prompt("Would you like to start the tutorial [y/n] (default is y): ").strip().lower()

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

# Save functions
def get_save_data():
    with money_lock:
        data = {
            "ai_name": ai_name,
            "money": money,
            "daily_users": daily_users,
            "processing_power": processing_power,
            "daily_users_level": daily_users_level,
            "processing_power_level": processing_power_level,
            "daily_users_cost": daily_users_cost,
            "processing_power_cost": processing_power_cost
        }
    return data

def save_game():
    save = get_save_data()

    with open("save.json", "w", encoding="utf-8") as file:
        json.dump(save, file, indent=4)

# Game functions
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def purchase_upgrade(upgrade_cost):
    global money

    if money >= upgrade_cost:
        money -= upgrade_cost
        return True
    else:
        return False

def display_upgrades():
    print()
    print("1. Better datacenters (increase processing power) - $",processing_power_cost)
    print("2. Better advertising (increase daily users) - $", daily_users_cost)
    print("3. Exit upgrades menu")
    print()
    upgrade_choice = session.prompt("Select an option: ").strip()
    return upgrade_choice

def upgrade_menu():
    global processing_power, processing_power_level, processing_power_cost
    global daily_users, daily_users_level, daily_users_cost
    
    while True:
        clear()
        display_stats()

        upgrade_choice = display_upgrades()

        if upgrade_choice == "1":
            with money_lock:
                result = purchase_upgrade(processing_power_cost)
                            
                if result: # run if result is true (result is stored as a bool)
                    processing_power += 1
                    processing_power_level += 1
                    processing_power_cost = round(processing_power_cost * cost_multiplier)
                        
                if result:
                    print()
                    print("Purchase successful!")
                    print()
                        
                else:
                    print()
                    print("Insufficient funds!")
                    print()
            
            time.sleep(1)

        elif upgrade_choice == "2":
            with money_lock:
                result = purchase_upgrade(daily_users_cost)
                            
                if result: # run if result is true (result is stored as a bool)
                    daily_users += 1
                    daily_users_level += 1
                    daily_users_cost = round(daily_users_cost * cost_multiplier)
            
                if result:
                    print()
                    print("Purchase successful!")
                    print()
            
                else:
                    print()
                    print("Insufficient funds!")
                    print()
            
            time.sleep(1)

        elif upgrade_choice == "3":
            break

        else:
            print("Invalid option!")
            time.sleep(1)

def money_update():
    global money

    interval = 0.5
    next_update = time.monotonic() + interval

    while running:
        delay = next_update - time.monotonic()

        if delay > 0:
            time.sleep(delay)
            
        if not running:
            break

        with money_lock:
            income = 0.15 * (daily_users ** 0.75) * (processing_power ** 0.85)
            money += income * interval

        next_update += interval

# User name + tutorial
ai_name = get_name()
print("If you would like to load a save, go to menu 2 after the tutorial")

tutorial(3)

# Money thread
money_thread = threading.Thread(target=money_update, daemon=True)
money_thread.start()

# Game loop
while menu_option != 3:
    display_stats()
    menu = display_menu()
    if menu == "1":
        upgrade_menu()

    elif menu == "2":
        menu_option = 2

    elif menu == "3":
        # add save code output before adjusting menu option as it will end game loop
        running = False
        money_thread.join()
        save_game()
        menu_option = 3

    else:
        clear() # clears terminal if outputs dont match the integers

