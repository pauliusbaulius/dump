import math


# https://adventofcode.com/2019/day/1
def fuel_mass(puzzle_input):
    fuel =  math.floor(puzzle_input / 3) - 2
    return fuel if fuel >= 0 else 0


def total_fuel_mass(list_of_modules):
    sum = 0
    for module in list_of_modules:
        sum += fuel_mass(module)
    return sum


# For part two
def fuel_mass_with_mass(fuel):
    sum = 0
    while fuel_mass(fuel) != 0:
        sum += fuel_mass(fuel)
        fuel = fuel_mass(fuel)
    return sum


def total_fuel_mass_with_mass(list_of_modules):
    sum = 0
    for module in list_of_modules:
        sum += fuel_mass_with_mass(module)
    return sum


# All modules are saved in a text file. Read each line as one element and append to the list of modules.
modules = []
with open("day_1.txt", "r") as f:
    for line in f:
        modules.append(int(line))

print("All modules of the ship are", modules)
total = total_fuel_mass(modules)
print("Total mass of fuel is", total)

new_total = total_fuel_mass_with_mass(modules)
print("Total mass of fuel with its fuel is", new_total)