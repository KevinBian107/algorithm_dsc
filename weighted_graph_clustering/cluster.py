def cluster(graph, weights, level):
    '''
    1. Graph is a weighted graph
    2. weights is a function
    3. level is a float number cutoff level
    s
    computes clusters for a weighted graph where the weights are the similarity
    Larger weights, more similar, we want to find weights above cerain cutoff threshold and return the two ndoes for such connection
    ---
    >>> import dsc40graph
    >>> def weights(x, y):
    ...     x, y = (x, y) if x < y else (y, x)
    ...     return {("a", "b"): 1, ("b", "c"): .3, ("c", "d"): .9, ("a", "d"): .2}[(x, y)]
    >>> edges = [('a', 'b'), ('b', 'c'), ('a', 'd'), ('c', 'd')]
    >>> graph = dsc40graph.DirectedGraph()
    >>> for edge in edges: graph.add_edge(*edge)
    >>> cluster(graph, weights, 0.4)
    frozenset({frozenset({'a', 'b'}), frozenset({'c', 'd'})})
    '''

    def full_dfs(graph, weights, level, cluster_set):
        status = {node: 'undiscovered' for node in graph.nodes}

        for node in graph.nodes:
            if status[node] == 'undiscovered':
                dfs(graph, node, status, weights, level, cluster_set)

    def dfs(graph, u, status, weights, level, cluster_set):
        status[u] = 'pending'
        for v in graph.neighbors(u):
            if status[v] == 'undiscovered':
                dfs(graph, v, status, weights, level, cluster_set)
            
            #Condition passing level and adding to list
            if weights(u,v) >= level:
                add = frozenset([u,v])
                cluster_set.append(add)

        status[u] = 'visited'
    
    cluster_set = list()
    full_dfs(graph, weights, level, cluster_set)

    return frozenset(cluster_set)