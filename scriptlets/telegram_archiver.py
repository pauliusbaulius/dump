from bs4 import BeautifulSoup as bs
import os
import csv
import argparse
import sqlite3
import time

OUTPUT_TYPES = ["SQL", "CSV"]
WORKING_DIR = None
OUTPUT_FILENAME = "telegram_messages"


def open_file(filename):
    with open(filename) as f:
        soup = bs(f, features="html.parser")
    return soup


def find_messages(filename):
    """
    Given a filename, it tries to extract divs that contain messages. Telegram messages are stored in html files.
    Each message "block" aka div has class="message default clearfix" or class"message default clearfix" when it is
    a 2nd or nth message from the same sender in a row.
    """
    messages = open_file(filename)
    matched_messages = messages.find_all("div", class_="message default clearfix")
    matched_messages += messages.find_all("div", class_="message default clearfix joined")
    return matched_messages


def parse_message_file(filename):
    """
    Takes html filename as input, assumes that it is a telegram html output file containing messages.
    Returns a list of messages found in the given file as a list

    Each message has unique id. Each message also has div of class="pull_right date details" which contains attribute
    title with timestamp of message sending date and time.
    There are 2 more child div's in this block which contain the sender's name and text which was sent.
    """

    html_messages = find_messages(filename)
    parsed_messages = []

    for message in html_messages:
        try:
            message_id = message.get("id")
            message_date = message.find(attrs={"class": "pull_right date details"}).get("title")
            # .text gets content without tags, .strip() removes newlines and whitespace at start/end of text
            message_sender = message.find(attrs={"class": "from_name"}).text.strip()
            message_text = message.find(attrs={"class": "text"}).text.strip()
            parsed_messages.append([message_id, message_date, message_sender, message_text])

        # If message type is not text, AttributeError is raised, since it is class="title bold" instead of class="text"
        # Happens because we try to find class="text" to put in message_text.
        except AttributeError:
            try:    # Look if it is a joined message from same sender
                message_text = message.find(attrs={"class": "text"}).text.strip()
            except AttributeError:
                try:    # Look if it is a sticker
                    message_text = message.find(attrs={"class": "title bold"}).text.strip()
                except AttributeError:  # If not sticker, it can only be media file.
                    #todo file location instead of this string.
                    message_text = "Picture/Video/Audio"

            # Remove that via @gif from sender name and write content as "Gif".
            if message_sender.find("@gif") != -1:
                message_sender = message_sender[:-10]
                message_text = "Gif"
            parsed_messages.append([message_id, message_date, message_sender, message_text])

    return parsed_messages


def parse_all_files(directory):
    """
    Goes over all files in the given directory and extracts messages.
    """
    message_files = find_message_files(directory)
    parsed_messages = []
    start = time.perf_counter()
    for i in message_files:
        m = parse_message_file(i)
        parsed_messages.extend(m)
    end = time.perf_counter()
    print("It took {}s to parse all messages.".format(round(end - start, 2)))
    return sorted(parsed_messages)


def parse_all_files_multithread(directory):
    # todo multiprocessing
    # split message_files in equal sized lists
    # run each of those lists on a thread
    # split by cpu_count() !
    message_files = find_message_files(directory)
    split_message_files = split_list(message_files, 5)
    parsed_messages = []
    start = time.perf_counter()
    for i in message_files:
        m = parse_message_file(i)
        parsed_messages.extend(m)
    end = time.perf_counter()
    print("Time taken: {}s".format(round(end - start, 2)))
    return sorted(parsed_messages)


def split_list(list_, n):
    return [list_[start::n] for start in range(n)]


def find_message_files(directory):
    """
    Looks for html files in given directory. Telegram backup will only have html files with messages.
    Returns a list of paths to those files.
    """
    message_files = []
    for file in os.listdir(directory):
        if file.endswith(".html"):
            message_files.append(os.path.join(directory, file))
    return message_files


def create_csv(output, directory):
    """
    Creates a csv file with all parsed messages.
    Overwrites existing file with same name.
    Default file name will be output.csv and it will look in current dir if nothing is specified.
    """
    parsed_messages = parse_all_files(directory)
    with open(output, "w") as f:
        writer = csv.writer(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_ALL)
        for i in parsed_messages:
            writer.writerow(i)
    print("A total of {} messages have been parsed and written to '{}'.".format(len(parsed_messages), output))


def create_database():
    parsed_messages = parse_all_files(WORKING_DIR)
    db = sqlite3.connect(OUTPUT_FILENAME)
    try:
        db.execute("""DROP TABLE messages""")
    except: # todo figure out how to delete if database exists.. this works but isnt clean
        pass
    db.execute("""CREATE TABLE messages(message_id TEXT PRIMARY KEY, datetime TEXT, sender TEXT, message TEXT)""")
    for i in parsed_messages:
        db.execute("""INSERT INTO messages(message_id, datetime, sender, message) VALUES(?,?,?,?)""", (i[0], i[1], i[2], i[3]))
    db.commit()
    db.close()
    print("Database was successfully created and filled!")


def create_path(dir_name, file_type):
    default_filename = OUTPUT_FILENAME
    filename = os.path.join(dir_name, default_filename + "." + file_type)
    return filename


def parse_filename(arguments):
    global OUTPUT_FILENAME
    if arguments.output is None:
        print("No output file specified, will create a new file.")
    else:
        OUTPUT_FILENAME = arguments.output


def parse_directory(arguments):
    global WORKING_DIR
    if args.directory is None:
        WORKING_DIR = os.getcwd()
        print("No directory given, will look in current directory: {}".format(WORKING_DIR))
    else:
        WORKING_DIR = args.directory
        print("Will work in directory: {}".format(WORKING_DIR))


def handle_user_input(data_type): # very bad name
    """
    Sets global filename and directory variables and prints information to terminal.
    """
    global OUTPUT_FILENAME
    parse_directory(args)
    parse_filename(args)
    OUTPUT_FILENAME = create_path(WORKING_DIR, data_type)
    print("Creating a {} file: {}".format(data_type, OUTPUT_FILENAME))
    print("Might take a while...")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Telegram Message Parser")
    ap.add_argument("-d", "--directory", required=False, help="Directory of your Telegram export files. Uses current directory if none is specified.")
    ap.add_argument("-o", "--output", required=False, help="Output filename. A new file telegram_messages.<type> will be created by default.")
    ap.add_argument("-t", "--type", required=True, help="Type of output, -t sql or -t csv")
    args = ap.parse_args()

    if args.type.lower() == "csv":
        handle_user_input("csv")
        create_csv(OUTPUT_FILENAME, WORKING_DIR)
    elif args.type.lower() == "sql":
        handle_user_input("sqlite3")
        create_database()
    else:
        print("Please specify a valid output type, available options are: {}".format(", ".join(OUTPUT_TYPES)))
