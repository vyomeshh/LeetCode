'''You are given a string s consisting only of the characters 'a', 'b', and 'c'.

A substring of s is called balanced if all distinct characters in the substring appear the same number of times.

Return the length of the longest balanced substring of s.

 

Example 1:

Input: s = "abbac"

Output: 4

Explanation:

The longest balanced substring is "abba" because both distinct characters 'a' and 'b' each appear exactly 2 times.

Example 2:

Input: s = "aabcc"

Output: 3

Explanation:

The longest balanced substring is "abc" because all distinct characters 'a', 'b' and 'c' each appear exactly 1 time.

Example 3:

Input: s = "aba"

Output: 2

Explanation:

One of the longest balanced substrings is "ab" because both distinct characters 'a' and 'b' each appear exactly 1 time. Another longest balanced substring is "ba".

 

Constraints:

1 <= s.length <= 105
s contains only the characters 'a', 'b', and 'c'.'''
class Solution:
    def longestBalanced(self, s: str) -> int:
        n = len(s)
        max_len = 0
        
        # 1. Check for single character runs (e.g., "aaa")
        current_run = 0
        for i in range(n):
            if i > 0 and s[i] == s[i-1]:
                current_run += 1
            else:
                current_run = 1
            max_len = max(max_len, current_run)
            
        # 2. Check for 2-character substrings (e.g., 'a' and 'b' only)
        # We need to do this for pairs: (a,b), (b,c), (a,c)
        def check_pair(c1, c2, forbidden):
            local_max = 0
            # Map stores first index of a specific balance value
            # Initialize with balance 0 at index -1
            mapping = {0: -1}
            balance = 0
            
            for i, char in enumerate(s):
                if char == forbidden:
                    # Reset if we hit the forbidden char
                    mapping = {0: i}
                    balance = 0
                else:
                    if char == c1:
                        balance += 1
                    elif char == c2:
                        balance -= 1
                    
                    if balance in mapping:
                        local_max = max(local_max, i - mapping[balance])
                    else:
                        mapping[balance] = i
            return local_max

        max_len = max(max_len, check_pair('a', 'b', 'c'))
        max_len = max(max_len, check_pair('b', 'c', 'a'))
        max_len = max(max_len, check_pair('a', 'c', 'b'))
        
        # 3. Check for 3-character substrings (a, b, and c)
        # We need a == b == c.
        # This is equivalent to (a-b) == 0 AND (b-c) == 0 relative to start.
        # We track state (a-b, b-c).
        mapping = {(0, 0): -1}
        diff_ab = 0 # a - b
        diff_bc = 0 # b - c
        
        for i, char in enumerate(s):
            if char == 'a':
                diff_ab += 1
            elif char == 'b':
                diff_ab -= 1
                diff_bc += 1
            elif char == 'c':
                diff_bc -= 1
            
            state = (diff_ab, diff_bc)
            
            if state in mapping:
                max_len = max(max_len, i - mapping[state])
            else:
                mapping[state] = i
                
        return max_len