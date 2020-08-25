import random

l = [random.randint(0, 100) for _ in range(0, 20)]


def random_partition(l, p, r):
    i = random.randint(p, r)
    l[r], l[i] = l[i], l[r]
    return partition(l, p, r)


def partition(l, p, r):
    x = l[r]
    i = p - 1
    for j in range(p, r):   # for j=p to r - 1
        if l[j] <= x:
            i += 1
            l[i], l[j] = l[j], l[i]
    l[i + 1], l[r] = l[r], l[i + 1]
    return i + 1


def _quick_sort(l, p, r):
    if p < r:
        q = random_partition(l, p, r)
        _quick_sort(l, p, q - 1)
        _quick_sort(l, q + 1, r)


def quick_sort(l):
    _quick_sort(l, 0, len(l) - 1)

print(l)
quick_sort(l)
print(l)