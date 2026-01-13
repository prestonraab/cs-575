"""Utility functions for working with graphlets and graphlet visualization."""

from typing import Union, Callable
from itertools import combinations
import numpy as np
import networkx as nx # type: ignore
import networkx.algorithms.isomorphism as iso
import matplotlib.pyplot as plt


def show_graph(G: nx.Graph, 
               title: str, 
               labels: dict[Union[str, int], str],
               layout: Callable = nx.circular_layout,
               size: int = 2,
               node_color: str = 'cyan') -> None:
    """
    Display a graph with specified layout and styling.
    
    Parameters
    ----------
    G : nx.Graph
        The graph to display.
    title : str
        Title for the plot.
    labels : dict[Union[str, int], str]
        Dictionary mapping node identifiers to their display labels.
    layout : Callable, optional
        A networkx layout function (e.g., nx.circular_layout, nx.spring_layout).
        Default is nx.circular_layout.
    size : int, optional
        Figure size (size x size). Default is 2.
    node_color : str, optional
        Color for the nodes. Default is 'cyan'.
    """
    _ = plt.figure(figsize=(size, size))
    pos = layout(G)
    nx.draw(G, 
            pos, 
            node_color=node_color, 
            alpha=0.8, 
            node_size=300, 
            labels=labels)
    ax = plt.gca()
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.set_title(title)


def calculate_subplot_grid(num_graphs: int, num_cols: int = 4) -> tuple[int, int]:
    """
    Calculate the grid dimensions needed for displaying graphs in subplots.

    Parameters
    ----------
    num_graphs : int
        The number of graphs to display.
    num_cols : int, optional
        The desired number of columns in the grid. Default is 4.
        The actual number of columns will be the minimum of this value
        and num_graphs.

    Returns
    -------
    tuple[int, int]
        A tuple (num_rows, actual_num_cols) representing the grid dimensions.

    Raises
    ------
    ValueError
        If num_cols < 1.

    Examples
    --------
    >>> calculate_subplot_grid(5, 4)
    (2, 4)
    >>> calculate_subplot_grid(3, 5)
    (1, 3)
    >>> calculate_subplot_grid(9, 4)
    (3, 4)
    """
    if num_cols < 1:
        raise ValueError("num_cols must be at least 1")

    actual_cols = min(num_cols, num_graphs)
    num_rows = int(np.ceil(num_graphs / actual_cols))
    return num_rows, actual_cols


def get_axis_for_subplot(
    count: int, num_rows: int, num_cols: int
) -> tuple[str, Union[int, tuple[int, int]]]:
    """
    Determine which subplot axis to use for a given position in the grid.

    Parameters
    ----------
    count : int
        The index of the current subplot (0-indexed).
    num_rows : int
        The total number of rows in the grid.
    num_cols : int
        The total number of columns in the grid.

    Returns
    -------
    tuple[str, Union[int, tuple[int, int]]]
        A tuple (access_type, axis_index) where:
        - access_type is one of "gca" (for single subplot), "col" (for single row),
          or "cell" (for multi-row grid)
        - axis_index is either an int (column index or column index) or
          tuple[int, int] (row, col indices)

    Examples
    --------
    >>> get_axis_for_subplot(0, 1, 1)
    ('gca', None)
    >>> get_axis_for_subplot(2, 1, 3)
    ('col', 2)
    >>> get_axis_for_subplot(5, 2, 3)
    ('cell', (1, 2))
    """
    if num_rows == 1 and num_cols == 1:
        return "gca", None
    elif num_rows == 1 and num_cols > 1:
        col = count % num_cols
        return "col", col
    else:
        col = count % num_cols
        row = int(np.floor(count / num_cols))
        return "cell", (row, col)


def show_graphs_in_a_set(
    graphs: list[nx.Graph],
    labels: dict[Union[str, int], str] = {},
    num_cols: int = 4,
) -> None:
    """
    Visualize a set of graphs in a grid layout.

    This function displays multiple graphs in a subplot grid, making it easy to
    compare different graphs side by side. Each graph is drawn with a different color,
    and node labels can be optionally provided.

    Parameters
    ----------
    graphs : list[nx.Graph]
        A list of networkx Graph objects to visualize.
    labels : dict[Union[str, int], str], optional
        A dictionary mapping node identifiers to their display labels.
        If empty, nodes are displayed without labels. Default is {}.
    num_cols : int, optional
        The number of columns in the subplot grid. Default is 4.
        The actual number of columns will be the minimum of this value and
        the number of graphs to display.

    Raises
    ------
    ValueError
        If num_cols < 1.

    Notes
    -----
    - Graphs are arranged in a grid layout with a maximum of num_cols columns.
    - Grid dimensions are calculated using calculate_subplot_grid.
    - Each graph uses a circular layout for clarity.
    - If there are more grid positions than graphs, the extra subplots are hidden.
    - Colors are cycled through a predefined palette.
    """
    if num_cols < 1:
        raise ValueError("num_cols must be at least 1")

    num_rows, actual_cols = calculate_subplot_grid(len(graphs), num_cols)

    colors: list[str] = [
        "y",
        "lightblue",
        "lightgray",
        "salmon",
        "aquamarine",
        "lightpink",
        "violet",
        "linen",
    ]

    _, axs = plt.subplots(num_rows, actual_cols, figsize=(2 * actual_cols, 2 * num_rows))

    for count in range(num_rows * actual_cols):
        # Determine which axis to use
        access_type, axis_index = get_axis_for_subplot(count, num_rows, actual_cols)

        if access_type == "gca":
            axis = plt.gca()
        elif access_type == "col":
            axis = axs[axis_index]
        else:  # access_type == "cell"
            row, col = axis_index
            axis = axs[row, col]

        # If there are more spots in the grid layout than there are graphs then make some blank
        if count >= len(graphs):
            axis.set_visible(False)
            continue

        # Choose a circular layout because that makes it easy to see the nodes and edges for small graphs
        pos = nx.circular_layout(graphs[count])

        if len(labels) == 0:
            nx.draw(
                graphs[count],
                pos,
                ax=axis,
                node_color=colors[count % len(colors)],
                alpha=0.8,
                node_size=300,
            )
        else:
            sublabels = {
                node: label
                for node, label in labels.items()
                if node in graphs[count].nodes()
            }
            nx.draw(
                graphs[count],
                pos,
                ax=axis,
                node_color=colors[count % len(colors)],
                alpha=0.8,
                node_size=300,
                labels=sublabels,
            )

        axis.set_xlim(-1.2, 1.2)
        axis.set_ylim(-1.2, 1.2)
        axis.set_aspect("equal")


def find_subgraphs_containing_vertex(
    G: nx.Graph, size: int, vertex: Union[str, int]
) -> list[nx.Graph]:
    """
    Find all connected induced subgraphs of a given size containing a specific vertex.

    This function generates all possible induced subgraphs of a graph `G` with a
    specified number of nodes, filters for those that are connected and contain a
    target vertex, and returns them.

    Parameters
    ----------
    G : nx.Graph
        The input graph from which subgraphs are extracted.
    size : int
        The number of nodes in the desired subgraphs.
    vertex : Union[str, int]
        The vertex that must be present in all returned subgraphs.

    Returns
    -------
    list[nx.Graph]
        A list of networkx Graph objects representing all connected induced subgraphs
        of the specified size that contain the target vertex.

    Notes
    -----
    - Only connected subgraphs are returned.
    - Subgraphs are induced subgraphs, meaning all edges that exist in `G` between
      the subset of nodes are included in the subgraph.
    - The function uses networkx's `G.subgraph()` method, which automatically
      returns induced subgraphs.

    Examples
    --------
    >>> G = nx.complete_graph(4)  # K4 graph
    >>> subgraphs = find_subgraphs_containing_vertex(G, 3, 0)
    >>> len(subgraphs)  # Should find all 3-node induced subgraphs containing node 0
    4
    """
    from itertools import combinations

    subgraphs: list[nx.Graph] = []
    for nodes in combinations(G.nodes(), size):
        if vertex not in set(nodes):  # Skip subgraphs that don't contain the target vertex
            continue
        subgraph: nx.Graph = G.subgraph(nodes)
        # Single nodes are trivially connected; multi-node subgraphs must be connected
        if len(subgraph.nodes()) == 1 or nx.is_connected(subgraph):
            subgraphs.append(subgraph)
    return subgraphs


def rooted_is_isomorphic(G1: nx.Graph, G2: nx.Graph, root: Union[str, int]) -> bool:
    """
    Check if two graphs are isomorphic with a fixed root vertex.
    
    This function determines whether two graphs are rooted isomorphic, meaning
    there exists an edge-preserving bijection φ: V(G1) → V(G2) such that
    φ(root) = root. In other words, the graphs must be isomorphic AND there
    must be at least one isomorphism mapping that keeps the root vertex fixed.
    
    Parameters
    ----------
    G1 : networkx.Graph
        The first graph to compare.
    G2 : networkx.Graph
        The second graph to compare.
    root : str or int
        The root vertex that must be fixed in the isomorphism mapping.
        This vertex must exist in both G1 and G2.
    
    Returns
    -------
    bool
        True if the graphs are rooted isomorphic (i.e., isomorphic with a
        root-fixing mapping), False otherwise.
    
    Notes
    -----
    The algorithm follows these steps:
    1. Check if G1 and G2 are isomorphic as unrooted graphs
    2. If they are, enumerate all possible isomorphism mappings
    3. Check if any mapping satisfies φ(root) = root
    4. Return True if such a mapping exists, False otherwise
    
    Examples
    --------
    >>> # Two path graphs: A-B-C and A-C-B
    >>> G1 = nx.Graph([('A','B'), ('B','C')])
    >>> G2 = nx.Graph([('A','C'), ('C','B')])
    >>> rooted_is_isomorphic(G1, G2, 'A')
    False  # A is at different positions in the two graphs
    """
    # Step 1: Create a GraphMatcher to check for isomorphism
    # This checks if there exists any edge-preserving bijection φ: V(G1) → V(G2)
    GM = iso.GraphMatcher(G1, G2)
    
    # Step 2: Check if the graphs are isomorphic (unrooted)
    if GM.is_isomorphic():
        # Step 3: Enumerate all possible isomorphism mappings φ
        for mapping in GM.isomorphisms_iter():
            # Step 4: Check if this mapping satisfies φ(root) = root
            if mapping[root] == root:
                # Found a root-fixing isomorphism!
                return True
    
    # No root-fixing isomorphism exists
    return False


def find_all_graphlets(nodes: list[Union[str, int]], root: Union[str, int]) -> list[nx.Graph]:
    """
    Find all non-isomorphic connected rooted graphs on a given set of nodes.
    
    This function generates all possible graphs that can be constructed from a given
    set of nodes, filters for connected graphs, and then removes all but one
    representative from each rooted isomorphism class. The result is a set of rooted
    graphlets - graphs that are pairwise non-isomorphic (with the root fixed) and connected.
    
    Parameters
    ----------
    nodes : list[Union[str, int]]
        A list of node identifiers. Can be strings, integers, or a mix.
    root : Union[str, int]
        The designated root vertex for the rooted isomorphism classification.
        This vertex must be present in the nodes list.
    
    Returns
    -------
    list[nx.Graph]
        A list of networkx Graph objects, where each graph represents one
        rooted isomorphism equivalence class. All graphs are connected and
        pairwise non-isomorphic (with respect to rooted isomorphism).
    
    Notes
    -----
    - The function generates all possible subsets of edges, which is exponential
      in the number of edges (2^n_edges possibilities).
    - Only connected graphs are retained.
    - Rooted isomorphism checking is performed to keep only one representative per class.
    - The root vertex is fixed during isomorphism checking, meaning two rooted
      graphlets are considered isomorphic only if they map to each other while
      keeping the root vertex fixed.
    
    Examples
    --------
    >>> graphlets = find_all_graphlets(['A', 'B', 'C'], 'A')
    >>> len(graphlets)  # Should be 4 rooted graphlets on 3 nodes with root A
    4
    """
    all_graphs = []
    # Generate all possible edges
    possible_edges = list(combinations(nodes, 2))

    # Generate all possible graphs
    for i in range(2**len(possible_edges)):
        edges = [possible_edges[j] for j in range(len(possible_edges)) if (i >> j) & 1]
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        if nx.is_connected(G):
            all_graphs.append(G)

    # Only keep one graph from each rooted isomorphism class
    unique_graphs = []
    for G in all_graphs:
        if not any(rooted_is_isomorphic(G, H, root) for H in unique_graphs):
            unique_graphs.append(G)
    return unique_graphs
