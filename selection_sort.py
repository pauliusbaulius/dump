import random

l = [random.randint(0, 100) for _ in range(0, 20)]


def selection_sort(l):
    for i in range(0, len(l) - 2):
        print("i", i)
        k = i
        for j in range(i + 1, len(l)):
            print("j", j)
            if l[j] < l[k]:
                k = j
        l[i], l[k] = l[k], l[i]


selection_sort(l)
print(l)