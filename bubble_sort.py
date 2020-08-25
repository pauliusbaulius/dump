import random

l = [random.randint(0, 100) for _ in range(0, 20)]


def bubble_sort(l):
    n = len(l)
    for i in range(0, len(l) - 2):
        for j in range(len(l) - 1, i, -1):
            if l[j] < l[j - 1]:
                l[j], l[j - 1] = l[j - 1], l[j]


bubble_sort(l)
print(l)
