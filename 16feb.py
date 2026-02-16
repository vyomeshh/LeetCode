'''Reverse bits of a given 32 bits signed integer.

 

Example 1:

Input: n = 43261596

Output: 964176192

Explanation:

Integer	Binary
43261596	00000010100101000001111010011100
964176192	00111001011110000010100101000000
Example 2:

Input: n = 2147483644

Output: 1073741822

Explanation:

Integer	Binary
2147483644	01111111111111111111111111111100
1073741822	00111111111111111111111111111110
 

Constraints:

0 <= n <= 231 - 2
n is even.'''
class Solution:
    def reverseBits(self, n: int) -> int:
        result = 0
        
        # We must process exactly 32 bits
        for _ in range(32):
            # Shift the result to the left to make room
            result <<= 1
            
            # Extract the least significant bit of n and add it to result
            result |= (n & 1)
            
            # Shift n to the right to process the next bit
            n >>= 1
            
        return result