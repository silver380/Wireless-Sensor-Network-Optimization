import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from numpy import loadtxt
import pandas as pd

def user_satisfaction_score(min_stais, max_stais):
    scores = loadtxt('user_satisfaction_score.txt', delimiter=' ')
    sns.set_theme()
    f, ax = plt.subplots(figsize=(20, 20))
    s = sns.heatmap(scores, annot=True, fmt='.1f', linewidth=.5, ax=ax, vmin=min_stais, vmax=max_stais, cmap=sns.cubehelix_palette(as_cmap=True))
    s.invert_yaxis()
    plt.show()

def user_satisfaction_level():
    scores = loadtxt('user_satisfaction_level.txt', delimiter=' ')
    towers = loadtxt('towers.txt', delimiter=' ')
    x = []
    y = []
    for tower in towers:
        x.append(tower[0])
    for tower in towers:
        y.append(tower[1])
    sns.set_theme()
    f, ax = plt.subplots(figsize=(20, 20))
    # s = sns.heatmap(scores, annot=True, fmt='.1f', linewidth=.5, ax=ax, cmap=sns.cubehelix_palette(as_cmap=True))
    # s.invert_yaxis()

    ax2 = ax.twinx()
    s2 = sns.scatterplot(x=x,y=y, ax=ax)
    plt.show()
def tower_allocation():
    # Create a 2D array with random values
    grid = np.array(loadtxt('adj.txt', delimiter=' '), dtype="int")

    # grid = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    # Define a color map for the numbers
    cmap = sns.color_palette("Spectral", n_colors=33)
    f, ax = plt.subplots(figsize=(20, 20))

    # Create a heatmap using Seaborn
    sns.heatmap(grid, cmap=cmap, annot=True, fmt='d', ax=ax)

    # Display the plot
    plt.show()

def towers_location():
    # data = np.array(loadtxt('towers.txt', delimiter=' '), dtype="int")
    data = [1,2,3,0.9]
    x = [10,2,3,4,5,6,8,9,0]
    y = [20,4,6,2,6,2,7,5,6]
    f, ax = plt.subplots(figsize=(20, 20))
    sns.kdeplot(x=x, y=y, zorder=0, n_levels=6, shade=True,
                cbar=True, shade_lowest=False, cmap='viridis')
    plt.show()


if __name__ == '__main__':
    # user_satisfaction_score(-20, 40)
    user_satisfaction_level()
    # tower_allocation()
    # towers_location()