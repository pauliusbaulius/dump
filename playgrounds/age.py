import datetime

my_birthday = datetime.date(1996, 11, 01)
today = datetime.date.today()


def age(birthday):
    # how old i am today
    days = abs(my_birthday - today).days
    years = days / 365
    hours = days * 24
    seconds = hours * 60 * 60
    print("You are {:.2f} years old".format(years))
    print("You are {} days old.".format(days))
    print("You are {} hours old.".format(hours))
    print("You are {} seconds old.".format(seconds))


age(my_birthday)

# Print current datetime string.
current_datetime = datetime.datetime.utcnow()
print(f"Today is {current_datetime}.")
