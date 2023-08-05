import matplotlib.pyplot as plt
import numpy as np
import logging
from pyrolite.util.meta import subkwargs

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def stem(x, y, ax=None, orientation="horizontal", color="0.5", figsize=None, **kwargs):
    """
    Create a stem (or 'lollipop') plot, with optional orientation.

    Parameters
    -----------
    x, y : :class:`numpy.ndarray`
        1D arrays for independent and dependent axes.
    ax : :class:`matplotlib.axes.Axes`, :code:`None`
        The subplot to draw on.
    orientation : :class:`str`
        Orientation of the plot (horizontal or vertical).
    color : :class:`str`
        Color of lines and markers (unless otherwise overridden).
    figsize : :class:`tuple`
        Size of the figure, where an axis is not specified.

    Returns
    -------
    :class:`matplotlib.axes.Axes`
        Axes on which the stem diagram is plotted.
    """
    if ax is None:
        fig, ax = plt.subplots(1, figsize=figsize)

    orientation = orientation.lower()
    xs, ys = [x, x], [np.zeros_like(y), y]
    positivey = (y > 0 | ~np.isfinite(y)).all() | np.allclose(y, 0)
    if "h" in orientation:
        ax.plot(xs, ys, color=color, **subkwargs(kwargs, ax.plot))
        ax.scatter(x, y, **{"c": color, **subkwargs(kwargs, ax.scatter)})
        if positivey:
            ax.set_ylim(0, ax.get_ylim()[1])
    else:
        ax.plot(ys, xs, color=color, **subkwargs(kwargs, ax.plot))
        ax.scatter(y, x, **{"c": color, **subkwargs(kwargs, ax.scatter)})
        if positivey:
            ax.set_xlim(0, ax.get_xlim()[1])

    return ax
