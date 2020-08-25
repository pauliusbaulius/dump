import random
import math
import sys

l = [random.randint(0, 100) for _ in range(0, 20)]

def merge_sort(l):
    _merge_sort(l, 0, len(l) - 1)


def _merge_sort(l, p, r):
    if p < r:
        q = math.floor((p + r) / 2)
        _merge_sort(l, p, q)
        _merge_sort(l, q + 1, r)
        merge(l, p, q, r)


def merge(l, q, p, r):
   n1 = p - q + 1
   n2 = r - p
   # create arrays
   L = [0] * (n1)
   R = [0] * (n2)
   # Copy data to arrays
   for i in range(0 , n1):
      L[i] = l[q + i]
   for j in range(0 , n2):
      R[j] = l[p + 1 + j]
   i = 0 # first half of array
   j = 0 # second half of array
   k = q # merges two halves
   while i < n1 and j < n2 :
      if L[i] <= R[j]:
         l[k] = L[i]
         i += 1
      else:
         l[k] = R[j]
         j += 1
      k += 1
   # copy the left out elements of left half
   while i < n1:
      l[k] = L[i]
      i += 1
      k += 1
   # copy the left out elements of right half
   while j < n2:
      l[k] = R[j]
      j += 1
      k += 1


print(l)
merge_sort(l)
print(l)