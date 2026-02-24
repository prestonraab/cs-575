from network_utilities import adjacency_list_to_graph
import networkx as nx

def test_homework_problem_9() -> None:
    # What I expect
    desired_number_nodes: int = 6
    desired_minimum_density: float = 0.42
    desired_maximum_density: float = 0.46

    # when
    ## FIX THIS ADJACENCY LIST
    adjacency_list: dict[int, set[int]] = {1: {7,2,3},
                                           2: {1,3},
                                           3: {2,4,1},
                                           4: {3,5,6},
                                           5: {4,6},
                                           6: {4,5,7},
                                           7: {6,1}}
    G = adjacency_list_to_graph(adjacency_list)

    # then
    assert nx.is_connected(G)
    assert len(G.nodes()) >= desired_number_nodes
    assert nx.density(G) >= desired_minimum_density
    assert nx.density(G) <= desired_maximum_density