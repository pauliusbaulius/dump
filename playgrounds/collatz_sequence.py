# Calculates the Collatz sequence
# AutomateTheBoringStuff Chapter3 - last exercise
import sys


def _collatz(number):
    # if its even
    if number % 2 == 0:
        value = number // 2
        print(value)
        return value
    # if its odd
    else:
        value = 3 * number + 1
        print(value)
        return value


def collatz_sequence():
    print("give a positive integer:")
    value = input()

    try:
        # run until the value becomes 1
        while value != 1:
            # check if its negative number
            # if it is, return to start!
            if int(value) < 0:
                print("no negative numbers!")
                collatz_sequence()
            # recursive call collatz
            value = _collatz(int(value))
    # catch error if input is not integer!
    except ValueError:
        print("integers only!")
        collatz_sequence()


# run program
collatz_sequence()

# todo probably need to implement counter in _collatz to calculate steps!
def shortest_sequence(range):
    # dictionary with key=sequence lenght and value as number

    # dictionary
    for i in range(1, range):

    # return smallest sequence
    min(collatz_sequence())
    