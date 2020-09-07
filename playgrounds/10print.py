from random import randint


def ten_print(length: int) -> str:
    return "".join(["╱" if randint(0, 1) == 0 else "╲" for _ in range(0, length)])


print(ten_print(10000))