from dsf import DisjointSetForest

def slc(graph, d, k):
    '''
    Input:
    1. graph (An instance of dsc40graph.UndirectedGraph)
    2. d (A function of two arguments which takes in two nodes and returns the distance (or dissimilarity) between them)
    3. k (A positive integer describing the number of clusters which should be found)

    Return:
    Perform single linkage clustering using Kruskal's Algorithm and returns
    1. frozenset of k frozensets, each representing a cluster of the graph
    
    -----
    >>> import dsc40graph
    >>> g = dsc40graph.UndirectedGraph()
    >>> edges = [('a', 'b'), ('a', 'c'), ('c', 'd'), ('b', 'd')]
    >>> for edge in edges: g.add_edge(*edge)
    >>> def d(edge):
    ...     u, v = sorted(edge)
    ...     return {
    ...         ('a', 'b'): 1,
    ...         ('a', 'c'): 4,
    ...         ('b', 'd'): 3,
    ...         ('c', 'd'): 2,
    ...     }[(u, v)]
    >>> slc(g, d, 2)
    frozenset({frozenset({'a', 'b'}), frozenset({'c', 'd'})})
    >>> slc(g, d, 1)
    frozenset({frozenset({'a', 'b', 'c', 'd'})})
    ''' 
    #Put components in a disjoint set dictionary
    components = DisjointSetForest(graph.nodes)
    length = len(graph.nodes)
        
    #Sort all edge pairs, further weights means further away
    sorted_edges = sorted(graph.edges, key = d)
    
    #getting the right connected component
    for (u, v) in sorted_edges:
        if not components.in_same_set(u, v):
            components.union(u, v)
            
            #after there is a union, it either don't do anything or go to the same set, so check again
            if components.in_same_set(u,v):
                #fuse, -1 inner set
                length -= 1

            #fuse to the number of cluster
            if length == k:
                break
    
    #for each connected components detetcted, put them into a frozen set
    #find representative first, representtaive same for nodes in the same data set
    
    cluster_set = list()
    copy = list(graph.nodes)
    
    for i in range(k):
        cluster = list()
        for n in graph.nodes:
            #print(copy)
            #check for same represenattives or maybe check same set element as the root?
            if (len(cluster) != 0) & (n in copy):
                #print(components.find_set(n))
                if (components.find_set(n) == components.find_set(cluster[0])): # rep same with existing node's rep
                    cluster.append(n)
                    copy.remove(n)
                    #print("out")
            

            if (len(cluster) == 0) & (n in copy): #base case, first node
                #print(components.find_set(n))
                cluster.append(n)
                copy.remove(n)
                #print("out")

                #remove function miss up the iterations, so do an separate list for just removing and set the condition of when n in copy
                #print at each levels of operation is very important & seeing if the delete and representation value match expectation
        cluster_set.append(frozenset(cluster))
    
    return frozenset(cluster_set)