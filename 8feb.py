'''110. Balanced Binary Tree
Easy
Topics
premium lock icon
Companies
Given a binary tree, determine if it is height-balanced.

 

Example 1:


Input: root = [3,9,20,null,null,15,7]
Output: true
Example 2:


Input: root = [1,2,2,3,3,null,null,4,4]
Output: false
Example 3:

Input: root = []
Output: true
 

Constraints:

The number of nodes in the tree is in the range [0, 5000].
-104 <= Node.val <= 104'''
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        
        def check_height(node):
            if not node:
                return 0
            
            # Check left subtree
            left_height = check_height(node.left)
            if left_height == -1:
                return -1
            
            # Check right subtree
            right_height = check_height(node.right)
            if right_height == -1:
                return -1
            
            # Check if current node is balanced
            if abs(left_height - right_height) > 1:
                return -1
            
            # Return height of current node
            return max(left_height, right_height) + 1
            
        return check_height(root) != -1