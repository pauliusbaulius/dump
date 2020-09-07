import os
import datetime
import random

# todo short readme
"""
lmao bottom text
"""


# Get current date.
date_today = datetime.datetime.today().date()
filename_format = "{}.txt".format(date_today)
questions_file = "questions.txt"
# This is needed for initial print of statistics and stuff, so I could use one handle_ui function instead of two similar ones.
global_ui_counter = 0


def handle_ui():
    # todo create dir py_journal/ in called location.
    # todo have separate handle_start() so there would not be quote and stuff each time you do something.
    # todo or use some kind of counter? if global_counter = 0, then create file and print statistics, otherwise just handle ui
    # Use amazing control unit for managing application logic.
    #random_quote = get_random_quote()
    random_quote = "haha"
    header = f"[PY]RSONAL JOURNAL\n\n {random_quote}\n"
    ui = f"[1]: Answer Daily Questions\n" \
         f"[2]: Free Format\n" \
         f"[3]: Enter New Questions\n" \
         f"[4]: Manage Questions\n" \
         f"[0]: Quit"

    print(header)
    print(ui)
    # Fool-proof input-validator.
    user_choice = fool_prof_choice_handler()
    # todo do not create file if nothing is written.
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
    elif user_choice == 0:
        print_goodbye()


def get_random_quote():
    # todo generate a random quote from list or internet?
    pass

def fool_prof_choice_handler():
    # Fool-proof input-validator.
    try:
        user_choice = int(input("Choice:"))
        return user_choice
    except ValueError:
        print("Give me a number, please.")
        fool_prof_choice_handler()


def handle_questionnaire():
    questions = read_questions()
    if questions is not None:
        for question in questions:
            answer = f"{question}\n {input(question)}"
            write_to_file(answer)
        # todo calculate all answer lengths and show at the end.
        print("That's some quality writing, partner.\n")
    handle_ui()


def read_questions():
    """
    Reads questions from file, returns a list of questions from questions.txt
    Returns None if no questions are found/file does not exist.
    """
    try:
        # I know it's hardcoded, but it is not supposed to take custom question files, yet?
        with open(questions_file, "r") as f:
            questions = f.readlines()
            # Clear out non-questions like empty lines if there are any.
            questions = [question.strip() for question in questions if question.strip()]
            # Remove \n from lines.
            questions = [question.rstrip() for question in questions]
            # If file contains no legit questions.
            if len(questions) == 0:
                print("You haven't entered any questions yet.\n")
                return None
            return questions
    except FileNotFoundError:
        print("Could not find questions.txt in programs path, create one pls.\n")
        return None


def handle_free_input():
    answer = get_user_input()
    # Remove those trailing cancellation thingies.
    answer = answer.rstrip()
    write_to_file(f"Miscellaneous:\n {answer}")
    print("Thank you.")
    handle_ui()


def get_user_input():
    """Returns user input as list, each new line is one list element."""
    # Thanks to https://stackoverflow.com/questions/30239092/how-to-get-multiline-input-from-user
    # for this nice trick. This revolutionizes this journaling app.
    print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
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
        with open(questions_file, "a") as f:
            f.writelines(question + "\n")
            print("Added a new question.\n")
    else:
        print("That's... not a question?\n")


def handle_question_del():
    questions = read_questions()
    print("Select a question you want to delete:")
    # Print out all questions in numbered order.
    try:
        counter = 1
        for question in questions:
            print(f"[{counter}] {question}")
            counter += 1
        selection = fool_prof_choice_handler()
        if selection == 0:
            print("Aight.\n")
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
    # todo find matching question and delete it.
    # todo handle the thing if there are no questions
    with open(questions_file, "r") as f:
        lines = f.readlines()
    with open(questions_file, "w") as f:
        for line in lines:
            if line.strip("\n") != question:
                f.write(line)


def create_file():
    # If file exists, add separator at the end.
    if os.path.isfile(filename_format):
        with open(filename_format, "a") as f:
            f.write("")
    # Otherwise, create a new file.
    else:
        with open(filename_format, "w") as f:
            f.write(str(date_today))


def write_to_file(text):
    with open(filename_format, "a") as f:
        f.write("\n{}\n".format(text))


def print_goodbye():
    message_goodbye = ["Goodbye, my friend. Hope to see you tomorrow!",
                       "Bye, I swear this app is not a keylogger.",
                       "Sent a copy to the N(A)SA.",
                       "If you don't write an entry tomorrow, I'll download some ransomware.",
                       "I keep a log of your entries, bad things happen to those who skip journaling."
                       ]
    print(random.choice(message_goodbye))


def print_greeting():
    message_greeting = ["Hello, how are you today?",
                        ""
                        ]
    print(random.choice(message_greeting))


def cleanup_file():
    # todo open current day file and remove lines so that there is max 1 empty line between lines!
    # todo do it when user presses 0, clean up todays file.
    pass

def show_activity():
    # todo show frequency of entries and length of files
    # todo just iterate over notes and calculate stuff
    # todo print mini calendar? with X for days where u wrote entry
    # [5]: Stats
    pass

if __name__ == "__main__":
    handle_ui()
    # todo check date of last entry, if it was longer than week ago, print a mean statement
    # todo check date of last entry, show how many days passed#
    # todo restructure program in logic order, top-down approach, helper functions below their parent functions.
    # todo generate random quote instead of (insipired thing)

    # todo add usage videos in repo
    # todo write nice readme
    # todo ironic readme with gifs pls