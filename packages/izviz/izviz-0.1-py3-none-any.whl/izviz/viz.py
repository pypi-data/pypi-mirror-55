"""
viz.py

Examples
--------

"""

from izzy.misc import get_name, Refunction

import matplotlib.pyplot as plt
import pandas as pd


# Plot defaults
plot_defaults = {
    'add': False,
    'close': True,
    'color': None,
    'figsize': (20, 10),
    'style': 'solid',
    'title': None,
    'xlabel': None,
    'xmax': None,
    'xmin': None,
    'ylabel': None,
    'ymax': None,
    'ymin': None
}


# Current color
_current_color = 0


# Unpack optional plotting arguments
def _unpack(kwargs):
    # Make sure that kwargs has all defaults, and add if necessary
    for arg, value in plot_defaults.items():
        kwargs[arg] = kwargs.get(arg, value)

    # Separate internal _plot parameters from external plotter parameters
    kwargs_ext = {
        'color': kwargs['color']
    }
    del kwargs['color']

    # Return
    return kwargs_ext, kwargs


# Plot with plotters
def _plot(plotters, **kwargs):
    """
    Helper function to produce matplotlib plots.

    Parameters
    ----------
    plotters : list of Refunction instances
        Plotting functions to be called between figure and show (in matplotlib language).
    kwargs :
        Additional keyword arguments for the plotting functions.
    """

    # Unpack optional plotting arguments
    kwargs_ext, kwargs = _unpack(kwargs)

    # Create plot (if not add)
    if not kwargs['add']:
        plt.figure(figsize=kwargs['figsize'])

    # Plot
    for plotter in plotters:
        # plotter.function(*plotter.args, **plotter.kwargs)
        plotter.execute(**kwargs_ext)

    # Display?
    if kwargs['close']:
        # Change limits
        plt.xlim(left=kwargs['xmin'], right=kwargs['xmax'])
        plt.ylim(bottom=kwargs['ymin'], top=kwargs['ymax'])

        # Add axis labels and title
        plt.xlabel(kwargs['xlabel'])
        plt.ylabel(kwargs['ylabel'])
        plt.title(kwargs['title'])

        # Finally, show
        plt.show()


class Figure:
    def __init__(self):
        pass

    def __call__(self):
        pass


# Simple x vs y plot
# TODO should this be called quickplot? What if we want to do multiple lines? Matplotlib is the right library there.
def plot(x, y, **kwargs):
    # Get x and y name if necessary
    kwargs['xlabel'] = kwargs.get('xlabel', get_name(x, 'x'))
    kwargs['ylabel'] = kwargs.get('ylabel', get_name(y, 'y'))

    # Define plotters
    plotters = [Refunction(plt.plot, x, y)]

    # Call _plot helper function
    _plot(plotters, **kwargs)


# Allow users to set theme
def set_theme(theme):
    # Translate theme
    _theme = 'seaborn'
    if theme == 'dark':
        _theme = 'dark_background'

    # Style defaults
    plt.style.use('default')
    plt.style.use(_theme)
    plt.rcParams.update({
        'axes.labelsize': 18,
        'axes.titlesize': 18,
        'figure.titlesize': 18,
        'font.size': 18,
        'legend.fontsize': 18,
        'legend.title_fontsize': 18,
        'xtick.labelsize': 18,
        'ytick.labelsize': 18
    })


# By default, set the theme to light
set_theme('light')
