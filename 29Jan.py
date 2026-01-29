'''You are given two 0-indexed strings source and target, both of length n and consisting of lowercase English letters. You are also given two 0-indexed character arrays original and changed, and an integer array cost, where cost[i] represents the cost of changing the character original[i] to the character changed[i].

You start with the string source. In one operation, you can pick a character x from the string and change it to the character y at a cost of z if there exists any index j such that cost[j] == z, original[j] == x, and changed[j] == y.

Return the minimum cost to convert the string source to the string target using any number of operations. If it is impossible to convert source to target, return -1.'''

class Solution:
    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        # Ensure nums1 is the shorter array to optimize binary search range
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
            
        m, n = len(nums1), len(nums2)    
        low, high = 0, m
        
        while low <= high:
            partition1 = (low + high) // 2
            partition2 = (m + n + 1) // 2 - partition1
            
            # Boundary elements for nums1
            l1 = nums1[partition1 - 1] if partition1 > 0 else float('-inf')
            r1 = nums1[partition1] if partition1 < m else float('inf')
            
            # Boundary elements for nums2
            l2 = nums2[partition2 - 1] if partition2 > 0 else float('-inf')
            r2 = nums2[partition2] if partition2 < n else float('inf')
            
            # Check if we found the correct partition
            if l1 <= r2 and l2 <= r1:
                # Odd total elements
                if (m + n) % 2 == 1:
                    return max(l1, l2)
                # Even total elements
                else:
                    return (max(l1, l2) + min(r1, r2)) / 2.0
            
            elif l1 > r2:
                # Move left in nums1
                high = partition1 - 1
            else:
                # Move right in nums1
                low = partition1 + 1
                
        return 0.0