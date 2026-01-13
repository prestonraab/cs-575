"""Utility functions for working with graphlets and graph visualization."""

from typing import Union
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


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
