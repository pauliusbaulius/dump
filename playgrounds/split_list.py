
nums = [x for x in range(0, 100)]
print(nums)


def split_list(list_, n):
    return [list_[start::n] for start in range(n)]


new_nums = split_list(nums, 10)
print(new_nums)