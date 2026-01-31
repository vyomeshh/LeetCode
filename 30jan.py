import heapq

class Solution:
    def minimumCost(self, source: str, target: str, original: list[str], changed: list[str], cost: list[int]) -> int:
        n = len(source)
        
        # 1. Map unique strings to IDs for the graph
        unique_strs = list(set(original + changed))
        s_to_id = {s: i for i, s in enumerate(unique_strs)}
        num_nodes = len(unique_strs)
        
        # 2. Dijkstra for all-pairs shortest paths between unique strings
        adj = [[] for _ in range(num_nodes)]
        for o, c, z in zip(original, changed, cost):
            adj[s_to_id[o]].append((s_to_id[c], z))
            
        dist = [[float('inf')] * num_nodes for _ in range(num_nodes)]
        for i in range(num_nodes):
            dist[i][i] = 0
            pq = [(0, i)]
            while pq:
                d, u = heapq.heappop(pq)
                if d > dist[i][u]: continue
                for v, w in adj[u]:
                    if d + w < dist[i][v]:
                        dist[i][v] = d + w
                        heapq.heappush(pq, (dist[i][v], v))
        
        # 3. Build a Trie for all 'original' strings to speed up DP
        # Each leaf in the Trie stores the ID of the string it represents
        trie = {}
        for s in unique_strs:
            node = trie
            for char in s:
                node = node.setdefault(char, {})
            node['#'] = s_to_id[s]
            
        # 4. DP with Trie traversal
        # dp[i] = min cost to convert source[i:] to target[i:]
        dp = [float('inf')] * (n + 1)
        dp[n] = 0
        
        for i in range(n - 1, -1, -1):
            # Option 1: Characters already match
            if source[i] == target[i]:
                dp[i] = dp[i + 1]
            
            # Option 2: Substring transformation starting at i
            # Traverse source and target simultaneously in the Trie
            node_s, node_t = trie, trie
            for j in range(i, n):
                if source[j] not in node_s or target[j] not in node_t:
                    break
                node_s = node_s[source[j]]
                node_t = node_t[target[j]]
                
                # If both substrings exist in our unique_strs mapping
                if '#' in node_s and '#' in node_t:
                    u, v = node_s['#'], node_t['#']
                    if dist[u][v] != float('inf'):
                        dp[i] = min(dp[i], dist[u][v] + dp[j + 1])
                        
        return dp[0] if dp[0] != float('inf') else -1