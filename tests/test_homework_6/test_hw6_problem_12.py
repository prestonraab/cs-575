from network_utilities import adjacency_list_to_digraph
import networkx as nx
import numpy as np 

def test_homework_problem_katz_vs_pagerank() -> None:
    """
    Students should design a directed graph with >= 8 nodes such that:
    - Katz centrality is approximately uniform across nodes
    - PageRank distinguishes between hub nodes and nodes pointed to by hubs
    """

    # Create graph (STUDENT IMPLEMENTS THIS)
    adjacency_list: dict[int, set[int]] = {
        # Example structure students must design
        # 1: {...},
        # ...
    }
    G = adjacency_list_to_digraph(adjacency_list)

    # Basic structural checks
    assert isinstance(G, nx.DiGraph)
    assert G.number_of_nodes() >= 8

    # Compute centralities
    katz = nx.katz_centrality_numpy(G, alpha=0.1, beta=1.0)
    pagerank = nx.pagerank(G, alpha=0.85)

    katz_vals = np.array(list(katz.values()))
    pr_vals = np.array(list(pagerank.values()))

    # Katz should be approximately uniform
    # (small variance relative to mean)
    assert np.std(katz_vals) < 0.2 * np.mean(katz_vals)

    # PageRank should NOT be uniform
    assert np.std(pr_vals) > 0.2 * np.mean(pr_vals)

    # There should exist a hub node whose PageRank is higher
    max_pr = np.max(pr_vals)
    min_pr = np.min(pr_vals)
    assert max_pr > 2 * min_pr