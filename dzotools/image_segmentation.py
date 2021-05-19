# AUTOGENERATED! DO NOT EDIT! File to edit: 06_image_segmentation.ipynb (unless otherwise specified).

__all__ = ['quantize_image', 'rescale', 'get_maxflow_graph']

# Cell
import numpy as np
import maxflow
from numpy.linalg import norm

# Cell
def quantize_image(arr):
    """Make the colors perfect and exact RGB values."""
    stacked = np.stack([
        norm(arr - WHITE, axis=-1),
        norm(arr - BLUE, axis=-1),
        norm(arr - GREEN, axis=-1)],
        axis=-1
    )

    # Broadcast into higher dimension to make numpy where happy
    indexes = np.argmin(stacked, axis=-1)[..., None]

    return np.where(indexes == 0, WHITE, (np.where(indexes == 1, BLUE, GREEN)))

# Cell
rescale = lambda v: 255 * np.exp(-v*v / 32)

# Cell
def get_maxflow_graph(back: np.ndarray, color: np.ndarray) -> (np.ndarray, maxflow.GraphInt):
    """Calculate the segmentation using maxflow graph optimization.

    Assumes that the color array only contains 2 colors
    where one of them is blue and the other one green.
    """
    TERMINAL_MULTIPLIER = 40

    graph = maxflow.Graph[int](0, 0)
    nodeids = graph.add_grid_nodes(back.shape)

    graph.add_grid_tedges(
        nodeids,
        np.all(color == BLUE, axis=-1) * TERMINAL_MULTIPLIER,
        np.all(color == GREEN, axis=-1) * TERMINAL_MULTIPLIER,
    )

    minx = rescale(255 - np.minimum(back[:, 1:], back[:, :-1]))
    miny = rescale(255 - np.minimum(back[1:, :], back[:-1, :]))

    edgex = np.array(
        [[0, 0, 0],
         [0, 0, 1],
         [0, 0, 0]]
    )
    edgey = np.array(
        [[0, 0, 0],
         [0, 0, 0],
         [0, 1, 0]]
    )

    graph.add_grid_edges(nodeids[:, :-1], minx, edgex, symmetric=True)
    graph.add_grid_edges(nodeids[:-1, :], miny, edgey, symmetric=True)

    return nodeids, graph