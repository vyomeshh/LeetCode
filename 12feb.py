'''You are given a string s consisting of lowercase English letters.

A substring of s is called balanced if all distinct characters in the substring appear the same number of times.

Return the length of the longest balanced substring of s.

 

Example 1:

Input: s = "abbac"

Output: 4

Explanation:

The longest balanced substring is "abba" because both distinct characters 'a' and 'b' each appear exactly 2 times.

Example 2:

Input: s = "zzabccy"

Output: 4

Explanation:

The longest balanced substring is "zabc" because the distinct characters 'z', 'a', 'b', and 'c' each appear exactly 1 time.​​​​​​​

Example 3:

Input: s = "aba"

Output: 2

Explanation:

​​​​​​​One of the longest balanced substrings is "ab" because both distinct characters 'a' and 'b' each appear exactly 1 time. Another longest balanced substring is "ba".

 

Constraints:

1 <= s.length <= 1000
s consists of lowercase English letters.'''
class Solution:
    def longestBalanced(self, s: str) -> int:
        n = len(s)
        max_len = 0
        
        # Iterate over all possible starting points
        for i in range(n):
            freq = {}
            max_freq = 0
            
            # Expand the substring from i to j
            for j in range(i, n):
                char = s[j]
                
                # Update frequency map
                freq[char] = freq.get(char, 0) + 1
                
                # Track the maximum frequency in the current window
                max_freq = max(max_freq, freq[char])
                
                # Check if the substring is balanced:
                # If all distinct characters appear 'max_freq' times, then:
                # distinct_chars * max_freq should equal the total length
                current_len = j - i + 1
                if max_freq * len(freq) == current_len:
                    max_len = max(max_len, current_len)
                    
        return max_len