import networkx as nx
from typing import Tuple, Hashable, Set


def test_hw7_problem_4() -> None:
    """
    Problem 4: Create a graph and a partition of the nodes such that 0.5 <= Q <= 0.6.
    Graph must have >= 12 vertices, >= 2 edges, and partition must have >= 3 sets.
    """

    # Build graph
    G: nx.Graph = nx.Graph()
    # TODO: Add vertices

    # TODO: Add edges

    # TODO: Define partition
    partition: Tuple[Set[Hashable], ...] = ()

    # Validate structure
    assert isinstance(G, nx.Graph)
    assert G.number_of_nodes() >= 12
    assert G.number_of_edges() >= 2

    # Validate partition
    assert len(partition) >= 3
    assert all(len(group) > 0 for group in partition)
    union = set().union(*partition)
    assert union == set(G.nodes())
    assert sum(len(group) for group in partition) == len(union)

    # Check modularity
    q = nx.community.modularity(G, partition)
    assert 0.5 <= q <= 0.6
