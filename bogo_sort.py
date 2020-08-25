import random

"""
    Bogosort implementation by @pauliusbaulius.
    15.05.2020
"""


def is_sorted(l):
    """Checks whether a list is in ascending sorted order."""
    for i in range(len(l) - 1):
        if l[i] > l[i + 1]:
            return False
    return True


def bogo_sort(l):
    """Sorts a list by shuffling its values.

    If you get lucky, this is the fastest algorithm possible,
    since if its best case is Ω(n). Best case is when first
    shuffle returns a sorted list. Extremely unlikely 8)

    How many different shuffled lists can you get? |list|!
    A list of 5 elements has 120 possibilities.
    A list of 10 elements has 3628800 possibilities.
    This does not mean that there will be max of 120 shuffles before you get
    a sorted list!

    So in each iteration, a list of 5 elements has 1 / 120 chance of being
    sorted right!
    """
    shuffles = 0
    while not is_sorted(l):
        random.shuffle(l)
        shuffles += 1
    return shuffles


if __name__ == "__main__":
    l = [1, 3, 5, 2, 4, 5, 8, 9, 10]
    print("before: ", l)
    shuffles = bogo_sort(l)
    print(f"after: {l} shuffles: {shuffles}")