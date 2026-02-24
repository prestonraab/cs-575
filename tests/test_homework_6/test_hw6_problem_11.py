from network_utilities import adjacency_list_to_digraph
import networkx as nx
import numpy as np 
import matplotlib.pyplot as plt
import plotting_utilities as pu

def test_homework_problem_ev_vs_katz_collapse() -> None:
    """
    Students should design a directed graph with >= 6 nodes such that:
    - Eigenvector centrality assigns near-zero values to at least 3 nodes
    - Katz centrality assigns no near-zero values
    """

    # Create graph (STUDENT IMPLEMENTS THIS)
    adjacency_list: dict[int, set[int]] = {
        1: {5, 6},
        2: {5, 6},
        3: {5, 6},
        4: {5, 6},
        5: {6},
        6: {5},
    }
    G = adjacency_list_to_digraph(adjacency_list)

    nx.nx_pydot.graphviz_layout(G, prog="neato")
    pu.show_digraph(G)

    # Basic structural checks
    assert isinstance(G, nx.DiGraph)
    assert G.number_of_nodes() >= 6

    # Compute centralities
    eig = nx.eigenvector_centrality(G, max_iter=2000)
    print(eig)
    katz = nx.katz_centrality_numpy(G, alpha=0.1, beta=1.0)

    eig_vals = np.array(list(eig.values()))
    katz_vals = np.array(list(katz.values()))
    print(katz_vlaue)

    # Count near-zero eigenvector entries
    near_zero_eig = np.sum(eig_vals < 1e-3)

    # At least 3 nodes should collapse under eigenvector centrality
    assert near_zero_eig >= 3

    # Katz should assign no near-zero values
    assert np.all(katz_vals > 1e-3)


if __name__ == "__main__":
    test_homework_problem_ev_vs_katz_collapse()


