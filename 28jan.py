'''You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.'''
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        # Dummy node to simplify the creation of the result list
        dummy = ListNode(0)
        curr = dummy
        carry = 0
        
        # Continue as long as there are nodes to process or a carry remains
        while l1 or l2 or carry:
            # Get values from nodes, or 0 if we've reached the end of a list
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0
            
            # Calculate total and new carry
            total = v1 + v2 + carry
            carry = total // 10
            val = total % 10
            
            # Add new node to the result list
            curr.next = ListNode(val)
            
            # Move pointers forward
            curr = curr.next
            if l1: l1 = l1.next
            if l2: l2 = l2.next
            
        return dummy.next