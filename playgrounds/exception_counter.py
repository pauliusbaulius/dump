sum = 0


def a():
    global sum
    sum += 1
    try:
        a()
    except RecursionError:
        return sum


a()
print(sum)