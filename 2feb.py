'''You are given a 0-indexed array of integers nums of length n, and two positive integers k and dist.

The cost of an array is the value of its first element. For example, the cost of [1,2,3] is 1 while the cost of [3,4,1] is 3.

You need to divide nums into k disjoint contiguous subarrays, such that the difference between the starting index of the second subarray and the starting index of the kth subarray should be less than or equal to dist. In other words, if you divide nums into the subarrays nums[0..(i1 - 1)], nums[i1..(i2 - 1)], ..., nums[ik-1..(n - 1)], then ik-1 - i1 <= dist.

Return the minimum possible sum of the cost of these subarrays.

 

Example 1:

Input: nums = [1,3,2,6,4,2], k = 3, dist = 3Output: 5Explanation: The best possible way to divide nums into 3 subarrays is: [1,3], [2,6,4], and [2]. This choice is valid because ik-1 - i1 is 5 - 2 = 3 which is equal to dist. The total cost is nums[0] + nums[2] + nums[5] which is 1 + 2 + 2 = 5.

It can be shown that there is no possible way to divide nums into 3 subarrays at a cost lower than 5.

Example 2:

Input: nums = [10,1,2,2,2,1], k = 4, dist = 3Output: 15Explanation: The best possible way to divide nums into 4 subarrays is: [10], [1], [2], and [2,2,1]. This choice is valid because ik-1 - i1 is 3 - 1 = 2 which is less than dist. The total cost is nums[0] + nums[1] + nums[2] + nums[3] which is 10 + 1 + 2 + 2 = 15.

The division [10], [1], [2,2,2], and [1] is not valid, because the difference between ik-1 and i1 is 5 - 1 = 4, which is greater than dist.

It can be shown that there is no possible way to divide nums into 4 subarrays at a cost lower than 15.

Example 3:

Input: nums = [10,8,18,9], k = 3, dist = 1Output: 36Explanation: The best possible way to divide nums into 4 subarrays is: [10], [8], and [18,9]. This choice is valid because ik-1 - i1 is 2 - 1 = 1 which is equal to dist.The total cost is nums[0] + nums[1] + nums[2] which is 10 + 8 + 18 = 36.

The division [10], [8,18], and [9] is not valid, because the difference between ik-1 and i1 is 3 - 1 = 2, which is greater than dist.

It can be shown that there is no possible way to divide nums into 3 subarrays at a cost lower than 36.

 

Constraints:

3 <= n <= 105

1 <= nums[i] <= 109

3 <= k <= n

k - 2 <= dist <= n - 2'''
class FenwickTree:
    def __init__(self, size):
        self.tree = [0] * (size + 1)

    def update(self, i, delta):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

class Solution:
    def minimumCost(self, nums: list[int], k: int, dist: int) -> int:
        # We need to pick k-1 elements from nums[1:] 
        # such that they fit in a window of size dist + 1.
        target_count = k - 1
        window_size = dist + 1
        
        # 1. Coordinate Compression
        # Map values to ranks 1..M
        sorted_unique = sorted(list(set(nums[1:])))
        rank_map = {val: i + 1 for i, val in enumerate(sorted_unique)}
        max_rank = len(sorted_unique)
        
        # 2. Initialize BITs
        count_bit = FenwickTree(max_rank)
        sum_bit = FenwickTree(max_rank)
        
        def add(val):
            r = rank_map[val]
            count_bit.update(r, 1)
            sum_bit.update(r, val)
            
        def remove(val):
            r = rank_map[val]
            count_bit.update(r, -1)
            sum_bit.update(r, -val)
            
        def get_smallest_k_sum(k):
            # Binary Search (or Binary Lifting) over BIT to find rank
            # such that we have exactly k elements.
            # Using binary search over the ranks:
            lo, hi = 1, max_rank
            idx = -1
            
            # Find the smallest rank 'r' where count(r) >= k
            while lo <= hi:
                mid = (lo + hi) // 2
                if count_bit.query(mid) >= k:
                    idx = mid
                    hi = mid - 1
                else:
                    lo = mid + 1
            
            if idx == -1: return float('inf')
            
            # Calculate sum
            total_cnt = count_bit.query(idx)
            total_sum = sum_bit.query(idx)
            
            # We might have taken too many copies of the value at 'idx'
            # (e.g., we needed 2 '5's but there were 3 '5's in the window)
            excess = total_cnt - k
            val_at_idx = sorted_unique[idx-1]
            return total_sum - (excess * val_at_idx)

        # 3. Initial Window
        # Add the first 'dist+1' elements from nums[1:]
        # Note: constraints say k-2 <= dist, so window is large enough for k-1 items.
        
        current_window_elements = nums[1:]
        min_cost = float('inf')
        
        # Fill first window
        for i in range(min(window_size, len(current_window_elements))):
            add(current_window_elements[i])
            
        if len(current_window_elements) >= target_count:
             min_cost = min(min_cost, get_smallest_k_sum(target_count))
        
        # 4. Slide the window
        for i in range(window_size, len(current_window_elements)):
            # Remove element that is sliding out
            out_elem = current_window_elements[i - window_size]
            remove(out_elem)
            
            # Add new element
            in_elem = current_window_elements[i]
            add(in_elem)
            
            min_cost = min(min_cost, get_smallest_k_sum(target_count))
            
        return min_cost + nums[0]