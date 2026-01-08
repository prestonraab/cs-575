"""
Tests for creating graphs from vertex and edge sets.

This module demonstrates testing patterns for the vertex/edge set graph creation utilities.
"""

import sys
from pathlib import Path

import pytest

# Add src/ to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from network_utilities import IllegalGraphRepresentation
import network_utilities as nu


class TestVertexEdgeSetGraphCreationFailures:
    """Negative tests: invalid vertex/edge combinations that should raise errors."""

    def test_empty_vertex_set(self) -> None:
        """Test that an empty vertex set raises IllegalGraphRepresentation."""
        with pytest.raises(IllegalGraphRepresentation) as exc_info:
            _ = nu.vertex_edge_sets_to_graph(set(), {(1, 2)})

        assert str(exc_info.value) == "Vertex set cannot be empty"

    def test_edge_references_nonexistent_vertex(self) -> None:
        """
        Test that an edge referencing a vertex not in the vertex set raises an error.

        If vertices are {1, 2} but edges include (1, 3), vertex 3 is not in the set.
        """
        with pytest.raises(IllegalGraphRepresentation) as exc_info:
            _ = nu.vertex_edge_sets_to_graph({1, 2}, {(1, 2), (1, 3)})

        assert "not in vertex set" in str(exc_info.value)


class TestVertexEdgeSetGraphCreationSuccess:
    """Positive tests: valid vertex/edge combinations that should create graphs."""

    def test_two_vertex_undirected_graph(self) -> None:
        """
        Test creation of a simple undirected graph with two vertices and one edge.

        Vertices: {1, 2}
        Edges: {(1,2), (2,1)} (symmetric for undirected graphs)
        """
        vertices = {1, 2}
        edges = {(1, 2), (2, 1)}  # Symmetric edges required for undirected graphs

        G = nu.vertex_edge_sets_to_graph(vertices, edges)

        # Verify vertices
        assert set(G.nodes()) == vertices

        # Verify edges (normalized since undirected)
        expected_edges = {(1, 2)}
        actual_edges = set(tuple(sorted(edge)) for edge in G.edges())
        assert actual_edges == expected_edges

    def test_three_vertex_undirected_graph(self) -> None:
        """
        Test creation of an undirected graph with three vertices and multiple edges.

        Vertices: {1, 2, 3}
        Edges form a path: 1-2-3 (with symmetric pairs)
        """
        vertices = {1, 2, 3}
        # For undirected, must include both directions: (1,2), (2,1), (2,3), (3,2)
        edges = {(1, 2), (2, 1), (2, 3), (3, 2)}

        G = nu.vertex_edge_sets_to_graph(vertices, edges)

        # Verify vertices
        assert set(G.nodes()) == vertices

        # Verify edges (normalized)
        expected_edges = {(1, 2), (2, 3)}
        actual_edges = set(tuple(sorted(edge)) for edge in G.edges())
        assert actual_edges == expected_edges

    def test_three_vertex_directed_graph(self) -> None:
        """
        Test creation of a directed graph with three vertices.

        Vertices: {1, 2, 3}
        Edges: 1→2, 2→1, 1→3 (asymmetric edges allowed in directed graphs)
        """
        vertices = {1, 2, 3}
        edges = {(1, 2), (2, 1), (1, 3)}

        G = nu.vertex_edge_sets_to_digraph(vertices, edges)

        # Verify vertices
        assert set(G.nodes()) == vertices

        # Verify edges (no normalization for directed graphs)
        assert set(G.edges()) == edges

    def test_empty_edge_set_with_vertices(self) -> None:
        """
        Test that an empty edge set is allowed (creates isolated vertices).

        A graph can have no edges but must have at least one vertex.
        """
        vertices = {1, 2, 3}
        edges: set[tuple[int, int]] = set()  # No edges

        G = nu.vertex_edge_sets_to_graph(vertices, edges)

        # Verify vertices exist
        assert set(G.nodes()) == vertices

        # Verify no edges
        assert len(G.edges()) == 0


class TestVertexEdgeSetDigraphCreationSuccess:
    """Positive tests for directed graph creation from vertex/edge sets."""

    def test_two_vertex_directed_graph(self) -> None:
        """Test creation of a simple directed graph with two vertices."""
        vertices = {1, 2}
        edges = {(1, 2)}  # Asymmetric edges allowed in directed graphs

        G = nu.vertex_edge_sets_to_digraph(vertices, edges)

        assert set(G.nodes()) == vertices
        assert set(G.edges()) == edges

    def test_three_vertex_directed_graph_with_cycle(self) -> None:
        """Test creation of a directed graph with a cycle: 1→2→3→1."""
        vertices = {1, 2, 3}
        edges = {(1, 2), (2, 3), (3, 1)}

        G = nu.vertex_edge_sets_to_digraph(vertices, edges)

        assert set(G.nodes()) == vertices
        assert set(G.edges()) == edges

    def test_directed_graph_empty_edge_set(self) -> None:
        """Test that a directed graph can have isolated vertices with no edges."""
        vertices = {1, 2, 3}
        edges: set[tuple[int, int]] = set()

        G = nu.vertex_edge_sets_to_digraph(vertices, edges)

        assert set(G.nodes()) == vertices
        assert len(G.edges()) == 0


class TestVertexEdgeSetDigraphCreationFailures:
    """Negative tests for invalid directed graph specifications."""

    def test_empty_vertex_set_digraph(self) -> None:
        """Test that an empty vertex set raises IllegalGraphRepresentation."""
        with pytest.raises(IllegalGraphRepresentation) as exc_info:
            _ = nu.vertex_edge_sets_to_digraph(set(), {(1, 2)})

        assert str(exc_info.value) == "Vertex set cannot be empty"

    def test_edge_references_nonexistent_vertex_digraph(self) -> None:
        """Test that edges referencing nonexistent vertices raise an error."""
        with pytest.raises(IllegalGraphRepresentation) as exc_info:
            _ = nu.vertex_edge_sets_to_digraph({1, 2}, {(1, 3)})

        assert "not in vertex set" in str(exc_info.value)
