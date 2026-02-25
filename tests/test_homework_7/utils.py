import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple, Hashable, Union, Literal
from numpy import linalg as linalg
from matplotlib.axes import Axes
# Edge betweenness scores for the edges
from networkx import edge_betweenness_centrality as betweenness

####################################
## Create datatype that specifies ##
## the style of the graph display ##
####################################
PlotType = Literal[
    "GRAPHVIZ",
    "CIRCULAR",
    "SPRING",
    "DOT"
]

#################################
## Show graph with node labels ##
## in a chosen set of axes     ##
#################################
def show_graph(G: nx.Graph,
               title: str = "",
               labels: Union[dict[int, str], None] = None,
               axes: Union[None, Axes] = None,
               node_color: Union[None, list[str]] = None,
               plot_style: PlotType = "GRAPHVIZ"
               ) -> dict[Hashable, Tuple[float, float]]:
    if labels is None:
        labels = {node: str(node) for node in G.nodes()}
    if axes is None:
        plt.figure(figsize=(4,4))
        axes: Axes = plt.gca()
    if node_color is None:
        node_color = ['y' for _ in G.nodes]
    node_positions: dict[Hashable, tuple[float, float]] = dict()
    if plot_style == "GRAPHVIZ":
        node_positions = nx.nx_pydot.graphviz_layout(G,prog='neato')
    elif plot_style == "DOT":
        node_positions = nx.nx_pydot.graphviz_layout(G,prog='dot')
    elif plot_style == "SPRING":
        node_positions = nx.spring_layout(G)
    else:
        node_positions = nx.circular_layout(G)

    nx.draw(G, 
        node_positions, 
        node_color = node_color, 
        with_labels = True, 
        labels = labels,
        node_size = 300,
        ax=axes, 
        alpha=0.8)
    
    axes.set_title(title)
    axes.set_aspect('equal')

    # Return the node positions in case I want to use them again
    return node_positions

def get_NCM_Figure3_14():
    G = nx.Graph()
    G.add_nodes_from(range(0,14))
    G.add_edges_from([(0,1),(0,2),(1,2),(3,4),(3,5),(4,5),(8,9),(8,10),(9,10),(11,12),(11,13),(12,13),(2,6),(5,6),(7,8),(7,11),(6,7)])
    pos = nx.spring_layout(G)
    return G, pos

def draw_edge_by_type(G, pos, edge, partition):
    edge_style = 'dashed'
    for part in partition:
        if edge[0] in part and edge[1] in part:
            edge_style = 'solid'
            break
    nx.draw_networkx_edges(G, pos, edgelist=[edge], style = edge_style)

def show_partitions(G,partition_list, pos = None):
    color_list = ['c','m','y','g','r']
    plt.figure()
    plt.axis('off')
    if pos is None: pos = nx.kamada_kawai_layout(G)
    for i in range(len(partition_list)):
        nx.draw_networkx_nodes(partition_list[i],pos,node_color=color_list[i%len(color_list)], alpha = 0.8)
    for edge in G.edges:
        draw_edge_by_type(G, pos, edge, partition_list)
    nx.draw_networkx_labels(G,pos)
    if len(G.edges) == 0:
        mod = 0
    else:
        mod = nx.algorithms.community.quality.modularity(G,partition_list)
    title = "Modularity = " + str(np.round(mod,2))
    plt.title(title)



def show_graph_with_edge_scores(
        G: nx.Graph, 
        title: str = "Graph with Edge Betweenness Scores",
        pos: Union[dict[Hashable, Tuple[float, float]], None] = None,
        plot_style: PlotType = "GRAPHVIZ",
        figsize: Tuple[float, float] = (10, 10),
        node_color: str = 'lightblue',
        node_size: int = 300,
        edge_alpha: float = 0.3,
        font_size: int = 7) -> None:
    """
    Display a graph with edge betweenness centrality scores labeled on edges.
    """
    edge_scores = betweenness(G)
    
    if pos is None:
        if plot_style == "GRAPHVIZ":
            pos = nx.nx_pydot.graphviz_layout(G, prog='neato')
        elif plot_style == "DOT":
            pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
        elif plot_style == "SPRING":
            pos = nx.spring_layout(G)
        else:
            pos = nx.circular_layout(G)

    # Create a figure and show the graph
    fig, ax = plt.subplots(figsize=figsize)

    # Draw the graph
    nx.draw_networkx_nodes(G, pos, node_color=node_color, node_size=node_size, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax)
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=edge_alpha)

    # Label edges with their betweenness scores (rounded to 2 decimal places)
    edge_labels = {edge: f"{score:.2f}" for edge, score in edge_scores.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax, font_size=font_size)

    ax.set_title(title)
    ax.axis('off')
    plt.tight_layout()