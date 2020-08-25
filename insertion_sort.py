import random


def insertion_sort(l: "list with sortable elements") -> list:
    for j in range(1, len(l)):
        key = l[j]
        i = j - 1
        while i >= 0 and l[i] > key:
            l[i + 1] = l[i]
            i -= 1
        l[i + 1] = key
    return l


def insertion_sort_info(l: "list with sortable elements") -> list:
    swaps = 0
    for j in range(1, len(l)):
        key = l[j]
        i = j - 1
        while i >= 0 and l[i] > key:
            l[i + 1], swaps = l[i], swaps + 1
            i -= 1
        l[i + 1] = key
    return l


random = [5, 2, 4, 6, 1, 3]
reverse = [6, 5, 4, 3, 2, 1, 0]
sorted = [1, 2, 3, 4, 5, 6]
print(insertion_sort_info(reverse))
