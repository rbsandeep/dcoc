"""
This program is used to prove that there are no deeply critical oriented cliques on 7 vertices.
For more details, please refer to the paper "On deeply critical oriented cliques" (Journal of Graph Theory)

Sample execution: python dcoc.py file-path

Input: A file containing graphs in g6 format.
Output: Lists of arcs of deeply critical oriented graphs among all possible orientations of edges of input graphs. 
Input (graphs of 7 vertices in g6 format) can be found at https://users.cecs.anu.edu.au/~bdm/data/graphs.html
"""

import networkx as nx
from itertools import product
import sys

def read_graph6(path):
    """Read simple undirected graphs in graph6 format from path.
    """
    with open(path, "rb") as infile:
        for line in infile:
            line = line.strip()
            if not len(line):
                continue
            yield nx.from_graph6_bytes(line)


def getNextOrientation(G):
    """
    Get the next orientation for the undirected graph G.
    1. Create a binary string of length m (number of edges in G)
    2. Let the ith edge in G be u,v. If the ith digit in the binary string is 0, then
    the orientation is set from u to v, otherwise from v to u.
    This is done for all possible binary strings of length m.
    """
    m = G.number_of_edges()
    edgesList = list(G.edges())
    W = product([0,1], repeat=m)
    for w in W:
        D = nx.DiGraph()
        for i in range(0, m):
            u,v = edgesList[i]
            if w[i] == 0:
                D.add_edge(u,v)
            else:
                D.add_edge(v,u)
        yield D
            
def isOriented(D, nodes, i, j):
    """
    Returns True if there is a directed path or a directed 2-path between vertices
    at indices i and j (of nodes - list of vertices of D). Returns false otherwise.
    """
    edges = list(D.edges())
    if (nodes[i], nodes[j]) in edges or (nodes[j], nodes[i]) in edges:
        return True
    for k in range(0, len(nodes)):
        if k==i or k==j:
            continue
        if (nodes[i], nodes[k]) in edges and (nodes[k], nodes[j]) in edges:
            return True
        if (nodes[j], nodes[k]) in edges and (nodes[k], nodes[i]) in edges:
            return True
    return False
    
def isOrientedClique(D):
    """
    Returns True if D (an oriented graph) is an oriented clique, False otherwise.
    """
    nodes = list(D.nodes())
    for i in range(0, len(nodes)-1):
        for j in range(i+1, len(nodes)):
            if not isOriented(D, nodes, i, j):
                return False
    return True

def criticalPairExists(D, nodes, i, j):
    """
    Input: D - a oriented graph; nodes - the list of vertices of D; i and j are indices of nodes.
    Returns True, if 
    (i) there exists a vertex x not same as nodes[i] such that there is no arc or a 2-dipath between x and node[j], and
    (ii) there exists a vertex y not same as nodes[j] such that there is no arc or 2-dipath between nodes[i] and y, and
    (iii) x not same as y
    """
    xfound = False
    yfound = False
    for k in range(0, len(nodes)):
        if k == i or k == j:
            continue
        if not isOriented(D, nodes, k, j):
            xfound = True
        elif not isOriented(D, nodes, i, k):
            yfound = True
    if xfound and yfound:
        return True
    return False

def isDeeplyCritical(D):
    """
    Input: D: An oriented clique
    Returns True if D is deeply critical, False otherwise.
    It can be easily proved that an oriented clique D is deeply critical 
    if and only if, for every arc uv, there exists two distinct vertices x, y distinct from {u,v}
    such that x and v can be colored the same and u and y can be colored the same in D-uv.
    """
    n = D.number_of_nodes()
    nodes = list(D.nodes())
    for i in range(0, n):
        u = nodes[i]
        for j in range(0, n):
            if i==j:
                continue
            v = nodes[j]
            if (u,v) not in D.edges():
                continue
            Dcopy = D.copy()
            Dcopy.remove_edge(u,v)
            if not criticalPairExists(Dcopy, nodes, i, j): 
                return False
    return True

if len(sys.argv) < 2:
    print("usage: 'python dcoc.py file-path'")
    exit()
for G in read_graph6(sys.argv[1]):
    Dlist = []				# list of all DCOCs
    if nx.diameter(G) > 2:		# if an undirected graph has diameter greater than 2, then none of its orientation will be an oriented clique.
        continue
    for D in getNextOrientation(G):
        if not isOrientedClique(D):
            continue
        if not isDeeplyCritical(D):
            continue
        flag = True
        for H in Dlist:
            if nx.is_isomorphic(D, H):
                flag = False		# the DCOC has already been found and is in the list.
                break
        if flag:
            Dlist.append(D)
    for D in Dlist:
        print(D.edges())   









