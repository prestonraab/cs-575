import networkx as nx
from networkx import edge_betweenness_centrality as betweenness


def test_hw7_problem_5() -> None:
    """
    Problem 5: Create a graph in which the edges (0,1), (2,3), (4,5)
    are ordered by edge betweenness from highest to lowest in that exact order.
    """

    # Build graph
    G: nx.Graph = nx.Graph()
    # TODO: Add vertices

    # TODO: Add edges

    # Validate required edges exist
    required_edges = [(0, 1), (2, 3), (4, 5)]
    for u, v in required_edges:
        assert G.has_edge(u, v), f"Missing required edge ({u}, {v})"

    # Compute edge betweenness
    edge_scores = betweenness(G)

    def score(u: int, v: int) -> float:
        return edge_scores.get((u, v), edge_scores.get((v, u)))

    scores = [score(u, v) for u, v in required_edges]
    assert all(s is not None for s in scores), "Failed to find all required edges"

    # Check ordering: highest to lowest in the given order
    assert scores[0] > scores[1] > scores[2]
