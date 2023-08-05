import numpy as np
import matplotlib.pyplot as plt

from .logger import get_logger

logger = get_logger(__name__)


def plot_pca_result(explained_variance_ratio, title=None, xlabel=None, ylabel=None, figsize=(7, 5), legend_comps=None, loc=7):
    """Plot the PCA explained variance ratio vs. number of components

    Args:
        explained_variance_ratio:
        title:
        xlabel:
        ylabel:
        figsize:
        legend_comps:
        loc:

    Returns:
        None
    """
    explained_variance_ratio = np.array(explained_variance_ratio)
    n_comps = len(explained_variance_ratio)
    total_variance_ratio = sum(explained_variance_ratio)
    n_components_list = []
    if n_comps > 10:
        n_components_list.extend(list(range(1, 10)))
    else:
        n_components_list = list(range(1, n_comps))
    if n_comps > 50:
        n_components_list.extend(list(range(10, 50, 5)))
    else:
        n_components_list.extend(list(range(10, n_comps, 5)))
    if n_comps > 300:
        n_components_list.extend(list(range(50, 300, 50)))
    else:
        n_components_list.extend(list(range(50, n_comps, 50)))
    if n_comps > 500:
        n_components_list.extend(list(range(300, 500, 50)))
        n_components_list.extend(list(range(500, n_comps, 50)))
    else:
        n_components_list.extend(list(range(300, n_comps, 50)))
    n_components_list.append(n_comps)
    if legend_comps is not None:
        assert isinstance(legend_comps, int) and (legend_comps <= n_comps)
        if legend_comps not in n_components_list:
            n_components_list.append(legend_comps)
            n_components_list.sort()

    logger.debug(f"List of components to plot: {n_components_list}")
    pca_result = {(i + 1): ratio for i, ratio in enumerate(explained_variance_ratio.cumsum())}
    pca_result_subset = {k: v for k, v in pca_result.items() if k in n_components_list}
    plt.figure(figsize=figsize)
    plt.plot(list(pca_result_subset.keys()), list(pca_result_subset.values()), '--bo')
    plt.title(title or f'Explained Variance Ratio {round(total_variance_ratio, 3)} using {n_comps} Components')
    plt.xlabel(xlabel or 'N Components')
    plt.ylabel(ylabel or 'Explained Variance Ratio')
    if legend_comps:
        plt.vlines(legend_comps, 0, pca_result_subset[legend_comps], linestyles='--')
        plt.hlines(
            pca_result_subset[legend_comps], 0, legend_comps, linestyles='--',
            label=f'explained variance ratio using {legend_comps} Components: {round(pca_result_subset[legend_comps], 3)}'
        )
        plt.legend(loc=loc)
