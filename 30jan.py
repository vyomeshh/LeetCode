import heapq

class Solution:
    def minimumCost(self, source: str, target: str, original: list[str], changed: list[str], cost: list[int]) -> int:
        n = len(source)
        # 1. Map unique strings to IDs
        nodes = list(set(original + changed))
        s_to_id = {s: i for i, s in enumerate(nodes)}
        num_nodes = len(nodes)
        
        # 2. Build adjacency list for Dijkstra
        adj = [[] for _ in range(num_nodes)]
        for o, c, z in zip(original, changed, cost):
            adj[s_to_id[o]].append((s_to_id[c], z))
            
        # 3. Pre-compute all-pairs shortest paths for strings
        # Given num_nodes <= 2000, we can run Dijkstra from each node
        conversion_costs = [[float('inf')] * num_nodes for _ in range(num_nodes)]
        for start_node in range(num_nodes):
            conversion_costs[start_node][start_node] = 0
            pq = [(0, start_node)]
            while pq:
                d, u = heapq.heappop(pq)
                if d > conversion_costs[start_node][u]: continue
                for v, weight in adj[u]:
                    if d + weight < conversion_costs[start_node][v]:
                        conversion_costs[start_node][v] = d + weight
                        heapq.heappush(pq, (conversion_costs[start_node][v], v))
        
        # 4. DP with Trie or Substring lookup
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        
        # Map original strings to their IDs for quick lookup
        # Optimization: Only consider substrings that exist in our conversion map
        valid_originals = set(original)
        
        for i in range(1, n + 1):
            # Option 1: Characters match
            if source[i-1] == target[i-1]:
                dp[i] = min(dp[i], dp[i-1])
            
            # Option 2: Substring transformation
            # Check all possible substrings ending at i
            for j in range(i):
                sub_s = source[j:i]
                sub_t = target[j:i]
                if sub_s in s_to_id and sub_t in s_to_id:
                    c = conversion_costs[s_to_id[sub_s]][s_to_id[sub_t]]
                    if c != float('inf'):
                        dp[i] = min(dp[i], dp[j] + c)
                        
        return dp[n] if dp[n] != float('inf') else -1