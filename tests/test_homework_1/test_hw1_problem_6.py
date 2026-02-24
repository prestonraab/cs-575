from network_utilities import adjacency_list_to_graph
import networkx as nx

def test_homework_problem_6() -> None:
    # What I expect
    desired_diameter: int = 6
    desired_radius: int = 3
    desired_number_nodes: int = 7

    # when
    ### FIX THIS ADJACENCY LIST
    adjacency_list: dict[int, set[int]] = {1: {2},
                                           2: {1, 3},
                                           3: {2, 4},
                                           4: {3, 5},
                                           5: {4, 6},
                                           6: {5, 7},
                                           7: {6}}
    G = adjacency_list_to_graph(adjacency_list)

    # then
    assert nx.is_connected(G)
    assert len(G.nodes()) == desired_number_nodes
    assert nx.diameter(G) == desired_diameter
    assert nx.radius(G) == desired_radius