'''Intuition
The brute force way checks every pair, which is slow.
I realised that if I store every number and its position dictionary first,I can look whether my "need" exists?
The need for any number is target - current_number.
Approach
Create an empty dictionary called seen to store number:index pairs.
1:Loop through the array.Store each number and its index in seen.
2:Loop through again.For each number calculate need=target-nums[i].
Check if need exists in seen AND seen[need] is not the same as i.
If both conditions are true return [i,seen[need]]
Complexity
Time complexity: O(n)

1: n operations to fill the dictionary.

2: n opertions to find need.

Dictionary look up O(1) average case.

Total: n + n = 2(n) -> O(n).

Space complexity: O(n)

The dictionary stores at most n number-index pairs.

Code'''
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

    # 1: remeber every number and where it lives
        seen = {}
        for i in range(len(nums)):
            seen[nums[i]] = i

    # 2: Find the need
        for i in range(len(nums)):
            need = target - nums[i]

            if need is seen and seen != i:
               return[i,seen[need]]

        return[]
         
