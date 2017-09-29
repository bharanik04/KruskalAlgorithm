# Kruskal’s Minimum Spanning Tree Algorithm
1. Sort all the edges in non-decreasing order of their weight.
        #Step 1:  Sort all the edges in non-decreasing order of their
        # weight.  If we are not allowed to change the given graph, we
        # can create a copy of graph
2. Pick the smallest edge. Check if it forms a cycle with the spanning tree 
formed so far. If cycle is not formed, include this edge. Else, discard it. 
  # Step 2: Pick the smallest edge and increment the index
  # for next iteration

3. Repeat step#2 until there are (V-1) edges in the spanning tree
