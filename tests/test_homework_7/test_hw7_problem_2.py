import networkx as nx
from typing import Tuple, Hashable, Set


def test_hw7_problem_2() -> None:
    """
    Problem 2: Create a graph and a partition of the nodes such that Q >= 0.95.
    Graph must have >= 5 vertices, >= 2 edges, and partition must have >= 2 sets.
    """

    # Build graph
    G: nx.Graph = nx.Graph()
    # TODO: Add vertices

    # TODO: Add edges

    # TODO: Define partition
    partition: Tuple[Set[Hashable], ...] = ()

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