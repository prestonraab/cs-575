"""Tests for find_subgraphs_containing_vertex function in graphlet_utilities."""

import pytest
import networkx as nx
from src.graphlet_utilities import find_subgraphs_containing_vertex


class TestFindSubgraphsContainingVertex:
    """Test suite for find_subgraphs_containing_vertex function."""

    def test_complete_graph_k3_2_nodes(self) -> None:
        """Test finding 2-node subgraphs in K3 (complete graph on 3 nodes)."""
        G = nx.complete_graph(3)
        subgraphs = find_subgraphs_containing_vertex(G, 2, 0)
        
        assert len(subgraphs) == 2  # Two 2-node connected subgraphs containing node 0
        assert all(isinstance(sg, nx.Graph) for sg in subgraphs)
        assert all(0 in sg.nodes() for sg in subgraphs)
        assert all(nx.is_connected(sg) for sg in subgraphs)

    def test_complete_graph_k4_3_nodes(self) -> None:
        """Test finding 3-node subgraphs in K4 (complete graph on 4 nodes)."""
        G = nx.complete_graph(4)
        subgraphs = find_subgraphs_containing_vertex(G, 3, 0)
        
        assert len(subgraphs) == 3  # Three 3-node subgraphs containing node 0
        assert all(0 in sg.nodes() for sg in subgraphs)
        assert all(len(sg.nodes()) == 3 for sg in subgraphs)
        assert all(nx.is_connected(sg) for sg in subgraphs)

    def test_path_graph_not_containing_vertex(self) -> None:
        """Test that no subgraphs are returned if vertex not in graph."""
        G = nx.path_graph(4)  # Linear graph 0-1-2-3
        subgraphs = find_subgraphs_containing_vertex(G, 2, 5)  # Node 5 doesn't exist
        
        assert len(subgraphs) == 0

    def test_path_graph_2_nodes_containing_0(self) -> None:
        """Test finding 2-node subgraphs in a path graph."""
        G = nx.path_graph(4)  # 0-1-2-3
        subgraphs = find_subgraphs_containing_vertex(G, 2, 0)
        
        # Node 0 is at an end, so it can only be in connected 2-node subgraphs with node 1
        assert len(subgraphs) == 1
        assert all(0 in sg.nodes() for sg in subgraphs)

    def test_path_graph_2_nodes_containing_middle(self) -> None:
        """Test finding 2-node subgraphs containing a middle node."""
        G = nx.path_graph(4)  # 0-1-2-3
        subgraphs = find_subgraphs_containing_vertex(G, 2, 2)
        
        # Node 2 is in the middle, can form 2-node subgraphs with nodes 1 and 3
        assert len(subgraphs) == 2
        assert all(2 in sg.nodes() for sg in subgraphs)

    def test_disconnected_graph(self) -> None:
        """Test with a disconnected graph."""
        G = nx.Graph()
        # Component 1: 0-1-2
        G.add_edges_from([(0, 1), (1, 2)])
        # Component 2: 3-4
        G.add_edges_from([(3, 4)])
        
        # Find 2-node subgraphs in component 1
        subgraphs = find_subgraphs_containing_vertex(G, 2, 0)
        
        # Only {0, 1} is a connected 2-node subgraph containing node 0
        # {0, 2} is not directly connected, so it's not included
        assert len(subgraphs) == 1
        assert all(0 in sg.nodes() for sg in subgraphs)
        assert all(nx.is_connected(sg) for sg in subgraphs)

    def test_cycle_graph_3_nodes(self) -> None:
        """Test finding 3-node subgraph in a cycle."""
        G = nx.cycle_graph(4)  # 0-1-2-3-0
        subgraphs = find_subgraphs_containing_vertex(G, 3, 0)
        
        # All 3-node connected induced subgraphs containing 0: {0,1,2}, {0,1,3}, {0,2,3}
        assert len(subgraphs) == 3
        assert all(0 in sg.nodes() for sg in subgraphs)
        assert all(len(sg.nodes()) == 3 for sg in subgraphs)
        assert all(nx.is_connected(sg) for sg in subgraphs)

    def test_single_node_subgraph(self) -> None:
        """Test finding 1-node subgraphs."""
        G = nx.complete_graph(3)
        subgraphs = find_subgraphs_containing_vertex(G, 1, 0)
        
        # Single nodes are trivially connected, so the single node {0} should be returned
        assert len(subgraphs) == 1
        assert set(subgraphs[0].nodes()) == {0}

    def test_entire_graph(self) -> None:
        """Test finding subgraphs equal to entire graph size."""
        G = nx.complete_graph(3)
        subgraphs = find_subgraphs_containing_vertex(G, 3, 0)
        
        # Only one 3-node connected subgraph containing 0: the entire K3
        assert len(subgraphs) == 1
        assert set(subgraphs[0].nodes()) == {0, 1, 2}

    def test_returns_induced_subgraphs(self) -> None:
        """Test that returned subgraphs are induced (contain all edges from original)."""
        G = nx.complete_graph(4)
        subgraphs = find_subgraphs_containing_vertex(G, 3, 0)
        
        for sg in subgraphs:
            # For complete graph, all 3-node induced subgraphs should have 3 edges
            assert sg.number_of_edges() == 3

    def test_vertex_with_integer_label(self) -> None:
        """Test with integer vertex labels."""
        G = nx.complete_graph(3)
        subgraphs = find_subgraphs_containing_vertex(G, 2, 1)
        
        assert len(subgraphs) == 2
        assert all(1 in sg.nodes() for sg in subgraphs)

    def test_vertex_with_string_label(self) -> None:
        """Test with string vertex labels."""
        G = nx.Graph()
        G.add_edges_from([('A', 'B'), ('B', 'C')])
        subgraphs = find_subgraphs_containing_vertex(G, 2, 'A')
        
        assert len(subgraphs) == 1
        assert 'A' in subgraphs[0].nodes()

    def test_star_graph(self) -> None:
        """Test with a star graph (hub and spokes)."""
        G = nx.star_graph(3)  # Center node 0 connected to 1, 2, 3
        subgraphs = find_subgraphs_containing_vertex(G, 2, 0)
        
        # Node 0 connected to each of nodes 1, 2, 3
        assert len(subgraphs) == 3
        assert all(0 in sg.nodes() for sg in subgraphs)

    def test_empty_result_disconnected_subgraph(self) -> None:
        """Test that disconnected subgraphs are not returned."""
        G = nx.Graph()
        # Add nodes 0, 1, 2 with no edges initially
        G.add_nodes_from([0, 1, 2])
        # Add edge connecting only 0-1
        G.add_edge(0, 1)
        
        # Try to find 3-node subgraphs containing 0
        subgraphs = find_subgraphs_containing_vertex(G, 3, 0)
        
        # The 3-node subgraph {0, 1, 2} would be disconnected, so should not be included
        assert len(subgraphs) == 0

    def test_subgraph_size_larger_than_neighbors(self) -> None:
        """Test requesting subgraph size larger than what's possible."""
        G = nx.path_graph(3)  # 0-1-2
        subgraphs = find_subgraphs_containing_vertex(G, 5, 0)
        
        # Graph only has 3 nodes, can't have 5-node subgraph
        assert len(subgraphs) == 0

    def test_connected_subgraphs_all_contain_vertex(self) -> None:
        """Verify all returned subgraphs contain the target vertex."""
        G = nx.complete_graph(5)
        vertex = 2
        subgraphs = find_subgraphs_containing_vertex(G, 3, vertex)
        
        assert all(vertex in sg.nodes() for sg in subgraphs)
        assert len(subgraphs) == 6  # C(4,2) = 6 three-node subgraphs containing node 2
