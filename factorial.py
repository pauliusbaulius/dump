# Calculate factorials in iterations.
def generate_fac(amount=100):
    fac_list = [1, 1]
    for i in range(2, amount):
        fac_list.append(i * fac_list[i-1])
    return fac_list


def print_fac_list(array):
    for i in range(len(array)):
        print("[{}] = {}".format(i, array[i]))


arr = generate_fac(5000)
print_fac_list(arr)

