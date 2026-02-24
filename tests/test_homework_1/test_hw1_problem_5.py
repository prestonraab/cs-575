from network_utilities import adjacency_list_to_graph
import networkx as nx

def test_homework_problem_5() -> None:
    # What I expect
    desired_node_degree: int = 2
    desired_node_eccentricty: int = 3
    desired_number_nodes: int = 7

    # Create graph
    ### FIX THIS ADJACENCY LIST
    adjacency_list: dict[int, set[int]] = {1: {2, 3},
                                           2: {1, 6, 7},
                                           3: {1, 4},
                                           4: {3, 5},
                                           5: {4},
                                           6: {2},
                                           7: {2}}
    G = adjacency_list_to_graph(adjacency_list)

    # when
    degree_dict = {node: degree for node,degree in G.degree()}
    eccentricity_dict = nx.eccentricity(G)

    # then
    assert nx.is_connected(G)
    assert len(G.nodes()) == desired_number_nodes
    assert any(degree_dict[key] == desired_node_degree and 
           eccentricity_dict[key] == desired_node_eccentricty 
           for key in degree_dict.keys())