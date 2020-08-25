import sys

# calculate square root using approximation
# enumeration
def calculate_square_root(x):
    guess, loop = 1, 1
    previous_guess = None
    while guess * guess != x:
        # save previous guess for loop check
        previous_guess = guess
        guess = (guess + x / guess) / 2
        # prevent infinite loop when approximation limit is reached.
        if previous_guess == guess:
            break
        else:
            print("[" + str(loop) + "]" + " = " + str(guess))
            loop += 1


# using bisection search
def calculate_square_root_2(x):
    epsilon = 0.1  # approximation tolerance
    loop = 1
    low = 0
    high = max(1, x)
    result = (high + low) / 2
    while abs(result**2 - x) >= epsilon:
        print("[" + str(loop) + "]" + " = " + str(result))
        loop += 1
        if result**2 < x:
            low = result
        else:
            high = result
        result = (high + low) / 2


# newton-raphson method of sqrt(x)
def calculate_square_root_3(x):
    epsilon = 0.001
    guess = x / 2
    loop = 1
    while abs(guess * guess - x) >= epsilon:
        guess = guess - (((guess**2) - x) / (2 * guess))
        print("[" + str(loop) + "]" + " = " + str(guess))
        loop += 1


calculate_square_root(25)
print("----")
calculate_square_root_3(25)
big_number = 13832193218312381027301273012730127301339423672364823842372

calculate_square_root_3(big_number)
