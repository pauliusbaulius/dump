def add_up_to_n(n: "Any positive integer") -> int:
    """Given n, returns sum of n + previous whole numbers until 0.

    Gaußsche Summenformel.
    https://de.wikipedia.org/wiki/Gau%C3%9Fsche_Summenformel
    Negative and zero n values will return 0.

    >>>add_up_to_n(3)
    6
    >>>add_up_to_n(10)
    55
    >>>add_up_to_n(-10)
    0
    """
    return 0 if n <= 0 else int(n * (n + 1) / 2)


if __name__ == "__main__":
    print(add_up_to_n(-10))
