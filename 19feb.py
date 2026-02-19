'''Given a binary string s, return the number of non-empty substrings that have the same number of 0's and 1's, and all the 0's and all the 1's in these substrings are grouped consecutively.

Substrings that occur multiple times are counted the number of times they occur.

 

Example 1:

Input: s = "00110011"
Output: 6
Explanation: There are 6 substrings that have equal number of consecutive 1's and 0's: "0011", "01", "1100", "10", "0011", and "01".
Notice that some of these substrings repeat and are counted the number of times they occur.
Also, "00110011" is not a valid substring because all the 0's (and 1's) are not grouped together.
Example 2:

Input: s = "10101"
Output: 4
Explanation: There are 4 substrings: "10", "01", "10", "01" that have equal number of consecutive 1's and 0's.
 

Constraints:

1 <= s.length <= 105
s[i] is either '0' or '1'.'''
class Solution:
    def countBinarySubstrings(self, s: str) -> int:
        total_substrings = 0
        prev_run = 0
        curr_run = 1
        
        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                # Continue the current run
                curr_run += 1
            else:
                # Character changed, add the min of the last two runs
                total_substrings += min(prev_run, curr_run)
                # Update prev_run and reset curr_run
                prev_run = curr_run
                curr_run = 1
                
        # Don't forget to add the valid substrings formed by the final two blocks
        total_substrings += min(prev_run, curr_run)
        
        return total_substrings