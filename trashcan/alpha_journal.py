#!/usr/bin/env python3
import json
import os
import re
import datetime
import random
from pathlib import Path

# todo short readme
"""
 ▄▄▄██▀▀▀▒█████   █    ██  ██▀███   ███▄    █  ▄▄▄       ██▓    
   ▒██  ▒██▒  ██▒ ██  ▓██▒▓██ ▒ ██▒ ██ ▀█   █ ▒████▄    ▓██▒    
   ░██  ▒██░  ██▒▓██  ▒██░▓██ ░▄█ ▒▓██  ▀█ ██▒▒██  ▀█▄  ▒██░    
▓██▄██▓ ▒██   ██░▓▓█  ░██░▒██▀▀█▄  ▓██▒  ▐▌██▒░██▄▄▄▄██ ▒██░    
 ▓███▒  ░ ████▓▒░▒▒█████▓ ░██▓ ▒██▒▒██░   ▓██░ ▓█   ▓██▒░██████▒
 ▒▓▒▒░  ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ░ ▒▓ ░▒▓░░ ▒░   ▒ ▒  ▒▒   ▓▒█░░ ▒░▓  ░
 ▒ ░▒░    ░ ▒ ▒░ ░░▒░ ░ ░   ░▒ ░ ▒░░ ░░   ░ ▒░  ▒   ▒▒ ░░ ░ ▒  ░
 ░ ░ ░  ░ ░ ░ ▒   ░░░ ░ ░   ░░   ░    ░   ░ ░   ░   ▒     ░ ░   
 ░   ░      ░ ░     ░        ░              ░       ░  ░    ░  ░
                                                                
                                            ___      
 __                                        /\_ \     
/\_\    ___   __  __  _ __    ___      __  \//\ \    
\/\ \  / __`\/\ \/\ \/\`'__\/' _ `\  /'__`\  \ \ \   
 \ \ \/\ \L\ \ \ \_\ \ \ \/ /\ \/\ \/\ \L\.\_ \_\ \_ 
 _\ \ \ \____/\ \____/\ \_\ \ \_\ \_\ \__/.\_\/\____\
/\ \_\ \/___/  \/___/  \/_/  \/_/\/_/\/__/\/_/\/____/
\ \____/                                             
 \/___/             
 
 
     ___        ___          ___          ___         ___          ___                 
   /  /\      /  /\        /__/\        /  /\       /__/\        /  /\                
  /  /:/     /  /::\       \  \:\      /  /::\      \  \:\      /  /::\               
 /__/::\    /  /:/\:\       \  \:\    /  /:/\:\      \  \:\    /  /:/\:\  ___     ___ 
 \__\/\:\  /  /:/  \:\  ___  \  \:\  /  /:/~/:/  _____\__\:\  /  /:/~/::\/__/\   /  /\
    \  \:\/__/:/ \__\:\/__/\  \__\:\/__/:/ /:/__/__/::::::::\/__/:/ /:/\:\  \:\ /  /:/
     \__\:\  \:\ /  /:/\  \:\ /  /:/\  \:\/:::::|  \:\~~\~~\/\  \:\/:/__\/\  \:\  /:/ 
     /  /:/\  \:\  /:/  \  \:\  /:/  \  \::/~~~~ \  \:\  ~~~  \  \::/      \  \:\/:/  
    /__/:/  \  \:\/:/    \  \:\/:/    \  \:\      \  \:\       \  \:\       \  \::/   
    \__\/    \  \::/      \  \::/      \  \:\      \  \:\       \  \:\       \__\/    
              \__\/        \__\/        \__\/       \__\/        \__\/                

                                 
"""


def load_json(settings_file):
    try:
        with open(settings_file, "r") as f:
            json_data = json.load(f)
        return json_data
    except FileNotFoundError:
        print(f"File {settings_file} does not exist in this directory.")
        return False
    except json.decoder.JSONDecodeError:
        print("Settings file is not valid json, was it tampered with?")
        return False


def save_json(settings_file, data):
    try:
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as error:
        print(error, error.with_traceback())


# Get current date for filename.
date_today = datetime.datetime.today().date()
filename_format = "{}.txt".format(date_today)
settings_file = "settings.json"
# Load json data from settings.json into this variable for modifying.
settings_json = load_json("settings.json")


def add_modification_date():
    # todo check if program was opened for longer than 1min?
    current_time = str(datetime.datetime.now())
    settings_json["journaling_times"].append(current_time)
    save_json(settings_file, settings_json)


def handle_ui():
    # todo it works but deletes output of previous command, arba sleep arba confirmation to go back using [0] or [1] to repeat command
    os.system("clear")
    # todo or use some kind of counter? if global_counter = 0, then tell about last log-in!
    # Use amazing control unit for managing application logic.
    random_quote = get_quote()
    header = f"[PY]RSONAL JOURNAL\n\n {random_quote}\n"
    ui = f"[1]: Answer Daily Questions\n" \
         f"[2]: Free Format\n" \
         f"[3]: Enter New Questions\n" \
         f"[4]: Manage Questions\n" \
         f"[5]: Statistics\n" \
         f"[0]: Quit"

    print(header)
    print(ui)
    # Fool-proof input-validator.
    user_choice = fool_prof_choice_handler()
    # Open file.
    create_file()
    # Handle UI
    handle_choice(user_choice)
    # TIL Python has no switch statement, and they call it a "programming language"...
    # Handle question asking from questions.txt.


def handle_choice(user_choice):
    if user_choice == 1:
        handle_questionnaire()
    # Handle free-format entry.
    elif user_choice == 2:
        handle_free_input()
    # Handle new question input.
    elif user_choice == 3:
        handle_question_add()
    # Handle question management system.
    elif user_choice == 4:
        handle_question_del()
    elif user_choice == 5:
        handle_statistics()
    elif user_choice == 0:
        print_goodbye()


def fool_prof_choice_handler():
    # Fool-proof input-validator.
    try:
        user_choice = int(input("\n[INPUT]: "))
        # Add a new line, looks a bit better.
        print()
        return user_choice
    except ValueError:
        print("\nGive me a number, please.")
        fool_prof_choice_handler()


def handle_questionnaire():
    questions = read_questions()
    counter = 1

    if questions is not None:
        for question in questions:
            # Print question and its position in the list.
            print(f"[{counter} of {len(questions)}]: {question} ")
            user_input = input()
            answer = f"{question}\n {user_input}"
            write_to_file(answer)
            counter += 1
        # todo calculate all answer lengths and show at the end.
    print("\nThat's it, see you tomorrow!")
    input("\n[ENTER]: Continue... ")
    handle_ui()


def read_questions():
    """
    Reads questions from file, returns a list of questions from settings.json
    Returns None if no questions are found.
    """
    questions = settings_json["questions"]
    if len(questions) == 0:
        print("You haven't entered any questions yet.\n")
        return None
    else:
        return questions


def handle_free_input():
    message = f"""Type your text here, [CTRL+D] to save and exit."""
    print(message)
    answer = get_user_input()
    # Remove those trailing cancellation thingies.
    answer = answer.rstrip()
    write_to_file(f"Miscellaneous:\n {answer}")
    input("\nYour input was saved, [ENTER]: to continue...")
    handle_ui()


def get_user_input():
    """Returns user input as list, each new line is one list element."""
    # Thanks to https://stackoverflow.com/questions/30239092/how-to-get-multiline-input-from-user
    # for this nice trick. This revolutionizes this journaling app.)
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)

    # Format into one big string.
    content = ""
    for line in contents:
        content = content + line + "\n"
    return content + "\n"


def handle_question_add():
    question = input("Give me a new question: ")
    add_question(str(question))
    handle_ui()


def add_question(question):
    """Given a question that is no empty, adds it to questions.txt file."""
    # todo test1 if \n string is appended, if "" is appended, test appending lol.
    # Adds question to the question list.
    # Remove \n chars and other trickery. We want a clean question file.
    question = question.rstrip()
    # Empty questions are not wanted. If you want to have question "b", you can.
    if len(question) > 0:
        settings_json["questions"].append(question)
        save_json(settings_file, settings_json)
        print("\nAdded a new question.")
    else:
        print("\nNot a valid questions, make it at least 1 character long.")
    input("\n[ENTER]: Continue... ")


def handle_question_del():
    questions = read_questions()
    print("Select a question you want to delete:")
    # Print out all questions in numbered order.
    try:
        counter = 1
        for question in questions:
            print(f"[{counter}]: {question}")
            counter += 1
        print("[0]: Cancel")
        selection = fool_prof_choice_handler()
        if selection == 0:
            handle_ui()
        else:
            print(f"Will remove: {questions[selection - 1]}\n")
            # -1, because arrays start with 0, but 0 is used to quit. For consistency purposes.
            remove_question(questions[selection - 1])
    except TypeError:
        pass
    finally:
        handle_ui()


def remove_question(question):
    if len(settings_json["questions"]) > 0:
        settings_json["questions"].remove(question)
        save_json(settings_file, settings_json)
    else:
        print("You haven't defined questions yet!\n")
        input("[ENTER]: Continue... ")
        return False


def handle_statistics():
    print("TODO")
    input("[ENTER]: Continue... ")
    handle_ui()


def create_file():
    # If file exists, add separator at the end.
    if os.path.isfile(filename_format):
        with open(filename_format, "a") as f:
            f.write("")
    # Otherwise, create a new file.
    else:
        with open(filename_format, "w") as f:
            f.write(str(date_today) + "\n")


def write_to_file(text):
    with open(filename_format, "a") as f:
        f.write("\n{}\n".format(text))


def print_goodbye():
    message_goodbye = ["Goodbye, my friend. Hope to see you tomorrow!",
                       "Bye, I swear this app is not a keylogger.",
                       "Sent a copy to the NASA, or NSA, whatever...",
                       "If you don't write an entry tomorrow, I'll download some ransomware.",
                       "I keep a log of your entries, bad things happen to those who skip journaling.",
                       "Do you want to buy our discounted premium subscription for only 5€/day?",
                       "This program goes against every chapter of Clean Code. I hope you haven't seen its source code.",
                       "Execute me with sudo rights, nothing will happen, I swear."
                       ]
    print(f"[SYSTEM]: {random.choice(message_goodbye)}\n")


def get_quote():
    # Return a random quote from settings.json.
    return random.choice(settings_json["quotes"])


def show_activity():
    # todo show frequency of entries and length of files
    # todo just iterate over notes and calculate stuff
    # todo print mini calendar? with X for days where u wrote entry
    # [5]: Stats
    pass
    # todo extract year, month, day
    # then calculate current month days
    # then look up current day
    # This week you have written entries for x out of 7 days.
    # This month you have written x out of 30 entries.
    # This year you have written X entries in total.
    # todo count words in entries in separate function...
    # todo


def find_entries():
    # Finds all entries in current directory matching predefined entry format.
    regex_pattern = re.compile("\\d{4}-\\d\\d-\\d\\d")
    text_files = list(Path(".").glob("**/*.txt"))
    found_dates = []
    for file in text_files:
        # Only consider dates matching our naming convention.
        if re.match(regex_pattern, file.stem):
            found_dates.append(file.stem)
    # print(found_dates)


if __name__ == "__main__":
    try:
        handle_ui()
    except Exception as error:
        print(error)
    finally:
        # todo handle ctrl+c exit with a nice message
        pass
    # todo check date of last entry, show how many days passed#
    # todo add usage videos in repo
    # todo clear console after each handle_ui to make it clean and nice!
