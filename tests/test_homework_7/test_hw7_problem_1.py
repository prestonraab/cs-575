import networkx as nx
from typing import Tuple, Hashable, Set
from network_utilities import adjacency_list_to_graph


def test_hw7_problem_1() -> None:
    """
    Problem 1: Create a graph and a partition of the nodes such that Q = 0.
    Graph must have >= 5 vertices, >= 2 edges, and partition must have >= 2 sets.
    """

    # Build graph
    adjacency_list: dict[int, set[int]] = {
        1: {6,2,4},
        2: {1,3,5},
        3: {2,4,6},
        4: {3,5,1},
        5: {4,6,2},
        6: {5,1,3}
    }
    G: nx.Graph = adjacency_list_to_graph(adjacency_list)


    # Define partition
    partition: Tuple[Set[Hashable], ...] = (set({1,2}),set({3,4}), set({5,6}))

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
    assert abs(q - 0.0) < 0.01  # Q ≈ 0

    
    import matplotlib.pyplot as plt
    nx.draw_kamada_kawai(G, with_labels=True)
    plt.savefig("problem_1_partition.png")

if __name__ == "__main__":
    test_hw7_problem_1()
    print("Problem 1 test passed!")
    # Save picture to file
