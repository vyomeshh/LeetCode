'''You are given an integer array nums of length n.

A trionic subarray is a contiguous subarray nums[l...r] (with 0 <= l < r < n) for which there exist indices l < p < q < r such that:

nums[l...p] is strictly increasing,
nums[p...q] is strictly decreasing,
nums[q...r] is strictly increasing.
Return the maximum sum of any trionic subarray in nums.

 

Example 1:

Input: nums = [0,-2,-1,-3,0,2,-1]

Output: -4

Explanation:

Pick l = 1, p = 2, q = 3, r = 5:

nums[l...p] = nums[1...2] = [-2, -1] is strictly increasing (-2 < -1).
nums[p...q] = nums[2...3] = [-1, -3] is strictly decreasing (-1 > -3)
nums[q...r] = nums[3...5] = [-3, 0, 2] is strictly increasing (-3 < 0 < 2).
Sum = (-2) + (-1) + (-3) + 0 + 2 = -4.
Example 2:

Input: nums = [1,4,2,7]

Output: 14

Explanation:

Pick l = 0, p = 1, q = 2, r = 3:

nums[l...p] = nums[0...1] = [1, 4] is strictly increasing (1 < 4).
nums[p...q] = nums[1...2] = [4, 2] is strictly decreasing (4 > 2).
nums[q...r] = nums[2...3] = [2, 7] is strictly increasing (2 < 7).
Sum = 1 + 4 + 2 + 7 = 14.
 

Constraints:

4 <= n = nums.length <= 105
-109 <= nums[i] <= 109
It is guaranteed that at least one trionic subarray exists.'''
class Solution:
    def maxSumTrionic(self, nums: list[int]) -> int:
        n = len(nums)
        # Constraint check (though problem guarantees valid input exists)
        if n < 4:
            return 0
            
        # 1. Precompute Max Strictly Increasing Sum Ending at i (Left Ascents)
        # inc[i] stores the max sum of a strictly increasing subarray ending at index i
        inc = [0] * n
        inc[0] = nums[0]
        for i in range(1, n):
            if nums[i] > nums[i-1]:
                # If extending is beneficial (positive prefix), extend. Otherwise start new.
                inc[i] = nums[i] + max(0, inc[i-1])
            else:
                inc[i] = nums[i]
                
        # 2. Precompute Max Strictly Increasing Sum Starting at i (Right Ascents)
        # dec[i] stores the max sum of a strictly increasing subarray starting at index i
        dec = [0] * n
        dec[n-1] = nums[n-1]
        for i in range(n - 2, -1, -1):
            if nums[i] < nums[i+1]:
                dec[i] = nums[i] + max(0, dec[i+1])
            else:
                dec[i] = nums[i]

        # 3. Prefix Sums for O(1) range sum queries of the middle decreasing part
        prefix_sum = [0] * (n + 1)
        for i in range(n):
            prefix_sum[i+1] = prefix_sum[i] + nums[i]
            
        def get_range_sum(start, end):
            return prefix_sum[end+1] - prefix_sum[start]

        max_trionic_sum = float('-inf')

        # 4. Iterate to find strictly decreasing segments (Bridges)
        # A trionic bridge starts at a peak 'p' and ends at a valley 'q'
        i = 1
        while i < n - 1:
            # Check for Peak: nums[i-1] < nums[i] (Ascent ending) AND nums[i] > nums[i+1] (Descent starting)
            if nums[i-1] < nums[i] and nums[i] > nums[i+1]:
                p = i
                curr = i
                
                # Walk down the descent to find the valley 'q'
                while curr < n - 1 and nums[curr] > nums[curr+1]:
                    curr += 1
                q = curr
                
                # Check for Valley: We must have an ascent after 'q' (nums[q] < nums[q+1])
                if q < n - 1 and nums[q] < nums[q+1]:
                    # Calculate Trionic Sum:
                    # 1. Left Ascent (ending at p-1)
                    left_sum = inc[p-1] 
                    # 2. Middle Descent (p to q)
                    middle_sum = get_range_sum(p, q) 
                    # 3. Right Ascent (starting at q+1)
                    right_sum = dec[q+1]
                    
                    total = left_sum + middle_sum + right_sum
                    if total > max_trionic_sum:
                        max_trionic_sum = total
                
                # Optimization: Skip past this descent as it cannot contain another peak
                i = q
            else:
                i += 1
                
        return max_trionic_sum