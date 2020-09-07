class Solution(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # Uses XOR to find the non-duplicate number.
        # Works because we have max of 2 duplicates of same number,
        # and two equal numbers will return 0 when XOR is applied.
        # For-loop will XOR all elements of array, and all duplicates will be eliminated.
        number = nums[0]
        for x in range(1, len(nums)):
            number = number ^ nums[x]
        return number
        
# Even more concise solution from https://leetcode.com/problems/single-number/discuss/558767/Python-Space-O(1)-XOR%2BReduce-Very-Simple-One-Liner
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        return reduce(lambda x, y: x^y, nums, 0)
