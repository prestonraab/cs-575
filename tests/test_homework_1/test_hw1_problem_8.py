from network_utilities import adjacency_list_to_graph
import networkx as nx

def test_homework_problem_8() -> None:
    # What I expect
    desired_number_nodes: int = 6
    desired_minimum_density: float = 0.21
    desired_maximum_density: float = 0.23

    # when
    ## FIX THIS ADJACENCY LIST
    adjacency_list: dict[int, set[int]] = {1: {2},
                                           2: {1, 3},
                                           3: {2, 4},
                                           4: {3, 5},
                                           5: {4, 6},
                                           6: {5, 7},
                                           7: {6, 8},
                                           8: {7, 9},
                                           9: {8}}
    G = adjacency_list_to_graph(adjacency_list)

    # then
    assert nx.is_connected(G)
    assert len(G.nodes()) >= desired_number_nodes
    assert nx.density(G) >= desired_minimum_density
    assert nx.density(G) <= desired_maximum_density