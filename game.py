
import os
import json
import time
import threading

from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style


# Variables
money = 100.0
daily_users = 1
processing_power = 1

daily_users_cost = 100
processing_power_cost = 50

daily_users_level = 1
processing_power_level = 1

cost_multiplier = 1.3

ai_name = "My AI"

running = True
money_lock = threading.Lock()
save_lock = threading.Lock()

current_screen = "main"
message = ""


# Game calculations
def money_update():
    global money

    interval = 0.1
    next_update = time.monotonic() + interval

    while running:
        delay = next_update - time.monotonic()

        if delay > 0:
            time.sleep(delay)

        if not running:
            break

        with money_lock:
            income = (
                0.25 * (daily_users ** 0.75) * (processing_power ** 0.85)
            )

            money += income * interval

        next_update += interval

        app.invalidate()


def purchase_upgrade(upgrade_type):
    global money
    global daily_users, processing_power
    global daily_users_level, processing_power_level
    global daily_users_cost, processing_power_cost
    global message

    with money_lock:

        if upgrade_type == "processing":
            cost = processing_power_cost

            if money >= cost:
                money -= cost
                processing_power += 1
                processing_power_level += 1
                processing_power_cost = round(
                    processing_power_cost * cost_multiplier
                )

                message = "Processing power upgraded!"

            else:
                message = "Insufficient funds!"

        elif upgrade_type == "users":
            cost = daily_users_cost

            if money >= cost:
                money -= cost
                daily_users += 1
                daily_users_level += 1
                daily_users_cost = round(
                    daily_users_cost * cost_multiplier
                )

                message = "Daily users upgraded!"

            else:
                message = "Insufficient funds!"

    app.invalidate()


# Save functions
def get_save_data():
    with money_lock:
        return {
            "ai_name": ai_name,
            "money": money,
            "daily_users": daily_users,
            "processing_power": processing_power,
            "daily_users_level": daily_users_level,
            "processing_power_level": processing_power_level,
            "daily_users_cost": daily_users_cost,
            "processing_power_cost": processing_power_cost
        }


def save_game():
    save_path = "save.json"
    temp_path = "save.json.tmp"

    try:
        with save_lock:
            save = get_save_data()

            with open("save.json", "w", encoding="utf-8") as file:
                json.dump(save, file, indent=4)

            os.replace(temp_path, save_path)

        return True

    except (OSError, TypeError, ValueError):
        return False

def load_game():
    global ai_name
    global money
    global daily_users
    global processing_power
    global daily_users_level
    global processing_power_level
    global daily_users_cost
    global processing_power_cost
    global message

    try:
        with save_lock:
            with open("save.json", "r", encoding="utf-8") as file:
                save = json.load(file)

            with money_lock:
                ai_name = save["ai_name"]
                money = save["money"]
                daily_users = save["daily_users"]
                processing_power = save["processing_power"]
                daily_users_level = save["daily_users_level"]
                processing_power_level = save["processing_power_level"]
                daily_users_cost = save["daily_users_cost"]
                processing_power_cost = save["processing_power_cost"]

        message = "Save loaded successfully!"
        return True

    except FileNotFoundError:
        message = "No save found!"
        return False

    except (json.JSONDecodeError, KeyError,TypeError, ValueError, OSError):
        message = "Save file is invalid or could not be read!"
        return False

def autosave():
    global message

    while running:
        time.sleep(10)

        if not running:
            break

        if not save_game():
            app.invalidate()


# Interface
def get_display():

    with money_lock:
        current_money = money
        current_users = daily_users
        current_power = processing_power
        current_users_cost = daily_users_cost
        current_power_cost = processing_power_cost

        current_income = (
            0.25 * (daily_users ** 0.75) * (processing_power ** 0.85)
        )

    if current_screen == "main":

        return FormattedText([
            ("", "================================\n"),
            ("", "       GPT-INCREMENTAL\n"),
            ("", f"       {ai_name}\n"),
            ("", "================================\n\n"),

            ("fg:green bold", f"Money: ${current_money:.2f}\n"),
            ("", f"Income:  ${current_income:.2f}/second\n\n"),

            ("", f"Daily users: {current_users}\n"),
            ("", f"Processing power: {current_power}\n\n"),

            ("bold", "MAIN MENU\n"),
            ("", "1. Upgrades\n"),
            ("", "2. Load save\n"),
            ("", "5. Save and exit\n\n"),

            ("fg:cyan", "Select an option: "),
            ("", message),
        ])

    elif current_screen == "upgrades":

        return FormattedText([
            ("", "================================\n"),
            ("", "          UPGRADES\n"),
            ("", "================================\n\n"),

            ("fg:green bold", f"Money: ${current_money:.2f}\n"),
            ("", f"Income: ${current_income:.2f}/second\n\n"),

            ("", f"Daily users: {current_users}\n"),
            ("", f"Processing power: {current_power}\n\n"),


            ("", f"1. Better datacenters - ${current_power_cost}\n"),
            ("", "   Increases processing power\n\n"),

            ("", f"2. Better advertising - ${current_users_cost}\n"),
            ("", "   Increases daily users\n\n"),

            ("", "3. Return to main menu\n\n"),

            ("fg:cyan", "Select an upgrade: "),
            ("", message),
        ])


# Input handling
bindings = KeyBindings()


@bindings.add("1")
def option_one(event):
    global current_screen, message

    message = ""

    if current_screen == "main":
        current_screen = "upgrades"
    else:
        purchase_upgrade("processing")

    event.app.invalidate()


@bindings.add("2")
def option_two(event):
    global current_screen, message

    if current_screen == "main":
        load_game()
    else:
        message = ""
        purchase_upgrade("users")

    event.app.invalidate()

@bindings.add("3")
def option_three(event):
    global current_screen, message

    if current_screen == "upgrades":
        current_screen = "main"
        message = ""

    event.app.invalidate()


@bindings.add("5")
def option_five(event):
    global current_screen, message

    if current_screen == "main":
        event.app.exit()

    event.app.invalidate()


@bindings.add("escape")
def go_back(event):
    global current_screen, message

    current_screen = "main"
    message = ""

    event.app.invalidate()


# Application
control = FormattedTextControl(get_display)

layout = Layout(
    HSplit([
        Window(content=control),
    ])
)

style = Style.from_dict({
    "": "#ffffff",
})

app = Application(
    layout=layout,
    key_bindings=bindings,
    style=style,
    full_screen=True,
    refresh_interval=0.1,
)


# Starting the game
if not load_game():
    ai_name = input(
        "Welcome to GPT-Incremental! Enter your AI's name: "
    )[:20]


money_thread = threading.Thread(target=money_update, daemon=True)
money_thread.start()

autosave_thread = threading.Thread(target=autosave, daemon = True)
autosave_thread.start()

try:
    app.run()

finally:
    running = False
    money_thread.join()
    autosave_thread.join()

if save_game():
    print("\nGame saved successfully!")
else:
    print("\nCould not save game!")
