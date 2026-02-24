import networkx as nx  # type: ignore
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
import numpy as np
from numpy.typing import NDArray
from typing import Tuple

from network_utilities import get_degree_count_dictionary


####################
## Graph Plotting ##
####################

def show_graph(G: nx.Graph) -> None:
    node_positions: dict[int, tuple[float, float]] = nx.nx_pydot.graphviz_layout(
        G, prog="neato"
    )
    title: str = "My graph"
    plt.figure()
    ax: Axes = plt.gca()
    ax.set_title(title)
    nx.draw(
        G,
        node_positions,
        node_color=["lightblue" for node in G.nodes],
        with_labels=True,
        node_size=300,
        alpha=0.8,
    )
    plt.show()


def show_graph_with_eigenvector_centrality(G: nx.Graph, eigenvectors: NDArray) -> None:
    """Show graph with eigenvector centrality values next to each node."""
    node_positions: dict[int, tuple[float, float]] = nx.nx_pydot.graphviz_layout(
        G, prog="neato"
    )
    title: str = "My graph with eigenvector centrality"
    plt.figure()
    ax: Axes = plt.gca()
    ax.set_title(title)
    nx.draw(
        G,
        node_positions,
        node_color=["y" for node in G.nodes],
        with_labels=True,
        node_size=300,
        alpha=0.8,
    )

    xlow, xhigh = ax.get_xlim()
    ylow, yhigh = ax.get_ylim()
    xscale = (xhigh - xlow) * 0.05
    yscale = (yhigh - ylow) * 0.05

    data = {node: eigenvectors[node - 1] for node in G.nodes}
    for node, (x, y) in node_positions.items():
        plt.text(
            x + xscale,
            y + yscale,
            s=data[node],
            bbox={"facecolor": "red", "alpha": 0.5},
            horizontalalignment="center",
        )

    plt.show()


def show_digraph(
    G: nx.DiGraph, title: str = "My directed graph", layout: str = "spring"
) -> None:
    if layout not in ["spring", "circular", "random", "shell", "spectral", "neato"]:
        raise ValueError(
            "Invalid layout specified. Choose from 'spring', 'circular', 'random', 'shell', 'spectral' or 'neato'."
        )
    node_positions: dict[int, tuple[float, float]] = {}
    if layout == "spring":
        node_positions = nx.spring_layout(G)
    elif layout == "circular":
        node_positions = nx.circular_layout(G)
    elif layout == "random":
        node_positions = nx.random_layout(G)
    elif layout == "shell":
        node_positions = nx.shell_layout(G)
    elif layout == "spectral":
        node_positions = nx.spectral_layout(G)
    elif layout == "neato":
        node_positions = nx.nx_pydot.graphviz_layout(G, prog="neato")
    else:
        raise ValueError(
            "Invalid layout specified. Choose from 'spring', 'circular', 'random', 'shell', 'spectral' or 'neato'."
        )
    plt.figure()
    ax: Axes = plt.gca()
    ax.set_title(title)
    ax.set_aspect("equal")
    nx.draw_networkx_nodes(
        G,
        node_positions,
        node_color=["lightblue" for _ in G.nodes],
        node_size=300,
        alpha=0.8,
    )
    nx.draw_networkx_labels(G, node_positions, font_size=15)
    nx.draw_networkx_edges(
        G,
        node_positions,
        connectionstyle="arc3, rad=0.2",
        arrows=True,
        arrowsize=20,
        width=1,
    )
    plt.axis("off")
    plt.show()


def show_digraph_with_edge_labels(
    G: nx.DiGraph, title: str, edge_labels: dict[Tuple[int, int], float]
) -> None:
    node_positions: dict[int, tuple[float, float]] = nx.nx_pydot.graphviz_layout(
        G, prog="neato"
    )
    plt.figure()
    ax: Axes = plt.gca()
    ax.set_title(title)
    nx.draw_networkx_nodes(
        G,
        node_positions,
        node_color=["y" for node in G.nodes],
        node_size=300,
        alpha=0.8,
    )
    nx.draw_networkx_labels(G, node_positions, font_size=15)
    nx.draw_networkx_edges(
        G,
        node_positions,
        connectionstyle="arc3, rad=0.2",
        arrows=True,
        arrowsize=20,
        width=1,
    )
    nx.draw_networkx_edge_labels(
        G,
        node_positions,
        edge_labels=edge_labels,
        font_color="red",
        label_pos=0.2,
        font_size=6,
    )
    plt.show()


def show_degree_distribution(G: nx.Graph) -> None:
    """Plot a histogram of node degrees."""
    degree_count = get_degree_count_dictionary(G)
    _, ax = plt.subplots()
    ax.set_xlabel("Node degree")
    ax.set_ylabel("Number of nodes")
    plt.bar(
        [float(key) for key in degree_count.keys()],
        [float(value) for value in degree_count.values()],
    )
