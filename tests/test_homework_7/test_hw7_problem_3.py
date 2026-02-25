import networkx as nx
from typing import Tuple, Hashable, Set
from network_utilities import adjacency_list_to_graph


def test_hw7_problem_3() -> None:
    """
    Problem 3: Create a graph and a partition of the nodes such that Q = -1/2.
    Graph must have >= 5 vertices, >= 2 edges, and partition must have >= 2 sets.
    """

    # Build graph
    adjacency_list: dict[int, set[int]] = {
        1: {6},
        2: {5, 6},
        3: {5, 6},
        4: {5, 6},
        5: {2, 3, 4},
        6: {1, 2, 3, 4},
    }
    G: nx.Graph = adjacency_list_to_graph(adjacency_list)

    # Define partition
    partition: Tuple[Set[Hashable], ...] = (set({1,2,3, 4}), set({5, 6}))

    # Validate structure
    assert isinstance(G, nx.Graph)
    assert G.number_of_nodes() >= 5
    assert G.number_of_edges() >= 2

    # Validate partition
    assert len(partition) >= 2
    assert all(len(group) > 0 for group in partition)
    union = set().union(*partition)
    assert union == set(G.nodes())
    assert sum(len(group) for group in partition) == len(union)

    # Check modularity
    q = nx.community.modularity(G, partition)
    assert abs(q - (-0.5)) < 0.01  # Q ≈ -1/2
