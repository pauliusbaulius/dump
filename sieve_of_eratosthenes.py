import time

print("Sieve of Eratosthenes")


# Generic function wrapper that times execution length.
def timer(f):
    def wrapper(*args):
        start = time.time()
        return_function = f(*args)
        end = time.time()
        print(f"function {f.__name__} took {(end - start) * 1000.0:.2f} ms to complete.")
        return return_function
    return wrapper


# Generate a list of wished length.
list_size = 1_000_000
numbers = [1 for x in range(0, list_size)]


@timer
def version_1(numbers: list) -> list:
    x_loops = 0
    # Simple version, no optimization.
    for i in range(2, len(numbers)):             # skip 0 and 1, since they are not prime.
        for x in range(i + 1, len(numbers)):     # for each number, iterate list from index of the number + 1.
            if x % i == 0:                       # if numbers divide without rest, it means they are multiples of same!
                numbers[x] = 0                   # set multiples to 0, since they are non-prime.
            x_loops += 1
    print(f"it took me {x_loops} x for-loops to remove non-prime numbers.")
    return numbers


@timer
def version_2(numbers: list) -> list:
    x_loops = 0
    for i in range(2, len(numbers)):
        if numbers[i] != 0:                         # Optimization 1: skip checking numbers that are already 0.
            for x in range(i + 1, len(numbers)):
                if x % i == 0:
                    numbers[x] = 0
                x_loops += 1
    print(f"it took me {x_loops} x for-loops to remove non-prime numbers.")
    return numbers


@timer
def version_3(numbers: list) -> list:
    #todo use vectors to set groups of multiples to false directly
    #todo use multiprocessing to do this, there is a limited amount of number groups.
    pass


# Pick your algorithm.
numbers = version_2(numbers)

# Small function to replace 1's in number list with actual index values and also fill primes list with prime numbers.
primes = []
for i in range(2, len(numbers)):
    if numbers[i] == 1:
        numbers[i] = i
        primes.append(i)

print(primes)

# TODO maybe compare to c with openmp? that should be faster than python with multiprocessing
