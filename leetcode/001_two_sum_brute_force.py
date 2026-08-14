"""
Problem: Two Sum
Link: https://leetcode.com/problems/two-sum/
Difficulty: Easy
Status: Solved
Date: 13 Aug 2026

Approach: Brute Force (Nested Loops)
- Check every pair of numbers
- Return indices when sum equals target

Time Complexity: O(n^2)
Space Complexity: O(1)
"""

from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []
