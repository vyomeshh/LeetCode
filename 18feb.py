'''Given a positive integer, check whether it has alternating bits: namely, if two adjacent bits will always have different values.

 

Example 1:

Input: n = 5
Output: true
Explanation: The binary representation of 5 is: 101
Example 2:

Input: n = 7
Output: false
Explanation: The binary representation of 7 is: 111.
Example 3:

Input: n = 11
Output: false
Explanation: The binary representation of 11 is: 1011.
 

Constraints:

1 <= n <= 231 - 1'''
class Solution:
    def hasAlternatingBits(self, n: int) -> bool:
        # Step 1: Create a number 'x' that will be all 1s IF 'n' has alternating bits
        x = n ^ (n >> 1)
        
        # Step 2: Check if 'x' is entirely made of 1s
        # If x is 111...11, then x + 1 is 100...00, and their bitwise AND is 0
        return (x & (x + 1)) == 0