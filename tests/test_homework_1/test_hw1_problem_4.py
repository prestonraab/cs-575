from network_utilities import adjacency_list_to_graph
import networkx as nx
import numpy as np 

def test_homework_problem_4() -> None:
    # What I expect
    desired_distances = np.array([[0., 1., 2., 2., 1.],
                  [1., 0., 1., 2., 2.],
                  [2., 1., 0., 1., 2.],
                  [2., 2., 1., 0., 1.],
                  [1., 2., 2., 1., 0.]])

    # Create graph
    ### FIX THIS ADJACENCY LIST
    adjacency_list: dict[int, set[int]] = {1: {2, 5},
                                           2: {1, 3},
                                           3: {2, 4},
                                           4: {3, 5},
                                           5: {1, 4}}
    G = adjacency_list_to_graph(adjacency_list)

    # when
    actual_distances = nx.floyd_warshall_numpy(G)

    # then
    assert nx.is_connected(G)
    assert np.allclose(actual_distances, desired_distances)