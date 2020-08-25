import sys
print("Egyptian multiplication")
a = int(input("Give a: "))
b = int(input("Give b: "))
print("Should be " + str(a * b))

product = 0

if b < 0:
    b = ~b
    b += 1
    a = a * -1

if (a & 1) == 1:
    product = a

if (b & 1) == 0:
    product = 0

if b == 0 and a == 0:
    print("Result is 0")
    sys.exit()

while b != 1:
    a = a << 1
    b = b >> 1
    if (b & 1) == 1:
        product = product + a


print("Result of a*b is " + str(product))



