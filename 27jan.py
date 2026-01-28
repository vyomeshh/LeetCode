'''You are given a directed, weighted graph with n nodes labeled from 0 to n - 1, and an array edges where edges[i] = [ui, vi, wi] represents a directed edge from node ui to node vi with cost wi.
Each node ui has a switch that can be used at most once: when you arrive at ui and have not yet used its switch, you may activate it on one of its incoming edges vi → ui reverse that edge to ui → vi and immediately traverse it.

The reversal is only valid for that single move, and using a reversed edge costs 2 * wi.

Return the minimum total cost to travel from node 0 to node n - 1. If it is not possible, return -1.'''

import heapq
from collections import defaultdict

class Solution:
    def minCost(self, n: int, edges: list[list[int]]) -> int:
        # 1. Build Adjacency Lists
        adj = defaultdict(list)
        rev_adj = defaultdict(list)
        
        for u, v, w in edges:
            adj[u].append((v, w))
            rev_adj[v].append((u, w)) # Incoming edges to v (can be reversed at v)
            
        # 2. Dijkstra setup
        # dist[u] = min cost to reach node u
        dist = [float('inf')] * n
        dist[0] = 0
        pq = [(0, 0)] # (current_cost, current_node)
        
        # 3. Track if a node's switch has been used
        # Since the switch is used "at" a node to leave it, 
        # we mark it as used when we process that node from the PQ.
        switched = [False] * n

        while pq:
            d, u = heapq.heappop(pq)
            
            if d > dist[u]:
                continue
                
            # Option 1: Standard traversal (u -> v)
            for v, w in adj[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heapq.heappush(pq, (dist[v], v))
            
            # Option 2: Use the switch at node u
            # Reverse an incoming edge (v -> u) to (u -> v)
            if not switched[u]:
                switched[u] = True
                for v, w in rev_adj[u]:
                    if d + 2 * w < dist[v]:
                        dist[v] = d + 2 * w
                        heapq.heappush(pq, (dist[v], v))
                        
        return dist[n-1] if dist[n-1] != float('inf') else -1