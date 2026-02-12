'''You are given an integer array nums.

A subarray is called balanced if the number of distinct even numbers in the subarray is equal to the number of distinct odd numbers.

Return the length of the longest balanced subarray.

 

Example 1:

Input: nums = [2,5,4,3]

Output: 4

Explanation:

The longest balanced subarray is [2, 5, 4, 3].
It has 2 distinct even numbers [2, 4] and 2 distinct odd numbers [5, 3]. Thus, the answer is 4.
Example 2:

Input: nums = [3,2,2,5,4]

Output: 5

Explanation:

The longest balanced subarray is [3, 2, 2, 5, 4].
It has 2 distinct even numbers [2, 4] and 2 distinct odd numbers [3, 5]. Thus, the answer is 5.
Example 3:

Input: nums = [1,2,3,2]

Output: 3

Explanation:

The longest balanced subarray is [2, 3, 2].
It has 1 distinct even number [2] and 1 distinct odd number [3]. Thus, the answer is 3.
 

Constraints:

1 <= nums.length <= 105
1 <= nums[i] <= 105'''
import sys

# Increase recursion depth to handle deep Segment Trees for large N
sys.setrecursionlimit(200000)

class Solution:
    def longestBalanced(self, nums: list[int]) -> int:
        n = len(nums)
        
        # Segment Tree Arrays (4 * N size)
        # st_min and st_max track the minimum and maximum balance values in a range
        st_min = [0] * (4 * n)
        st_max = [0] * (4 * n)
        st_lazy = [0] * (4 * n)
        
        # Helper: Push lazy updates down to children
        def push(node):
            if st_lazy[node] != 0:
                lz = st_lazy[node]
                
                # Apply lazy value to left child
                st_lazy[2 * node] += lz
                st_min[2 * node] += lz
                st_max[2 * node] += lz
                
                # Apply lazy value to right child
                st_lazy[2 * node + 1] += lz
                st_min[2 * node + 1] += lz
                st_max[2 * node + 1] += lz
                
                # Reset current node lazy
                st_lazy[node] = 0

        # Helper: Range Update
        # Adds 'val' to all indices in range [l, r]
        def update(node, start, end, l, r, val):
            if l > end or r < start:
                return
            if l <= start and end <= r:
                st_lazy[node] += val
                st_min[node] += val
                st_max[node] += val
                return
            
            push(node)
            mid = (start + end) // 2
            update(2 * node, start, mid, l, r, val)
            update(2 * node + 1, mid + 1, end, l, r, val)
            
            st_min[node] = min(st_min[2 * node], st_min[2 * node + 1])
            st_max[node] = max(st_max[2 * node], st_max[2 * node + 1])

        # Helper: Find the leftmost index 'i' in [0, limit_idx] where value is 0
        def find_first_zero(node, start, end, limit_idx):
            # If the current range is completely beyond the limit, ignore it
            if start > limit_idx:
                return -1
            
            # Pruning: If 0 is impossible in this range (all > 0 or all < 0), return -1
            if st_min[node] > 0 or st_max[node] < 0:
                return -1
            
            # Leaf node check
            if start == end:
                return start if st_min[node] == 0 else -1
            
            push(node)
            mid = (start + end) // 2
            
            # Priority: Try to find 0 in the left child first (to get the leftmost index)
            res = find_first_zero(2 * node, start, mid, limit_idx)
            if res != -1:
                return res
            
            # If not found in left, try right
            return find_first_zero(2 * node + 1, mid + 1, end, limit_idx)

        last_pos = {}
        max_len = 0
        
        for right, num in enumerate(nums):
            # Determine update value: +1 for Even, -1 for Odd
            val = 1 if num % 2 == 0 else -1
            
            # Get the previous occurrence of this number
            prev = last_pos.get(num, -1)
            
            # Update the balance for all potential start indices.
            # We only affect subarrays starting AFTER the previous occurrence of this number.
            update(1, 0, n - 1, prev + 1, right, val)
            
            # Update last seen position
            last_pos[num] = right
            
            # Find the leftmost start index 'i' where balance is 0
            idx = find_first_zero(1, 0, n - 1, right)
            
            if idx != -1:
                max_len = max(max_len, right - idx + 1)
                
        return max_len