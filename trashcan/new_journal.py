import datetime
import json


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


def add_modification_date():
    # todo check if program was opened for longer than 1min?
    current_time = str(datetime.datetime.now())
    settings_json["journaling_times"].append(current_time)
    save_json(settings_file, settings_json)


def calendar():
    # todo print last 14 days activity
    # todo print yearly activity if wanted
    # todo add stats to text file? like add daily stats of STREAK, AGE IN DAYS, WEEK OF LIFE
    today = datetime.date.today()
    print("Statistics for past 7 days:\n")
    print(f"[ ] Average time you spent filling out your journal: X")
    print(f"[ ] Longest time spent journaling: X on X day")
    print(f"[ ] Average length of daily journal: X")
    print(f"[ ] Shortest entry: X on X day")
    print(f"[ ] Longest entry: X on X day\n")

    # Past seven days.
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        print(f"{date} | X if journaled | X time spent")

    #fool_prof_choice_handler()
    # if choice == 0: handle_ui()
    # if choice == 1:


# todo load at startup
settings_file = "settings.json"
settings_json = load_json("settings.json")

add_modification_date()
# todo add timer at start and end of program and store average session duration
calendar()