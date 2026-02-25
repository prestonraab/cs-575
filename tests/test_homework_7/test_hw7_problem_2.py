import networkx as nx
from typing import Tuple, Hashable, Set


def test_hw7_problem_2() -> None:
    """
    Problem 2: Create a graph and a partition of the nodes such that Q >= 0.95.
    Graph must have >= 5 vertices, >= 2 edges, and partition must have >= 2 sets.
    """

    clique_size = 3
    num_communities = 100
    cliques = [nx.complete_graph(clique_size) for _ in range(num_communities)]
    
    # Combine them into a single disconnected graph
    G: nx.Graph = nx.disjoint_union_all(cliques)
    
    partition = [
        set(range(i * clique_size, (i + 1) * clique_size)) 
        for i in range(num_communities)
    ]

    # Basic structural checks
    assert isinstance(G, nx.Graph)
    assert G.number_of_nodes() >= 5
    assert G.number_of_edges() >= 2

    # Partition validity checks
    assert len(partition) >= 2
    assert all(len(group) > 0 for group in partition)
    union = set().union(*partition)
    assert union == set(G.nodes())
    assert sum(len(group) for group in partition) == len(union)

    # Modularity check
    q = nx.community.modularity(G, partition)
    assert q >= 0.95    # Q >= 0.95

if __name__ == "__main__":
    test_hw7_problem_2()
    print("Tests pass!")