import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from numpy import loadtxt

def user_satisfaction_score(min_stais, max_stais):
    scores = np.array(loadtxt('user_satisfaction_score.txt', delimiter=' '), dtype="int")
    sns.set_theme()
    f, ax = plt.subplots(figsize=(20, 20))
    s = sns.heatmap(scores, annot=True, linewidth=.5, ax=ax, vmin=min_stais, vmax=max_stais, cmap=sns.cubehelix_palette(as_cmap=True))
    # s.invert_yaxis()
    plt.show()

def user_satisfaction_level(x_locs, y_locs, r):
    levels = np.array(loadtxt('user_satisfaction_level.txt', delimiter=' '), dtype="float")
    sns.set_theme()
    f, ax = plt.subplots(figsize=(20, 20))
    s = sns.heatmap(levels, annot=True, fmt='.1f', linewidth=.5, ax=ax, cmap=sns.cubehelix_palette(as_cmap=True))
    # s.invert_yaxis()
    # sns.scatterplot(x=x_locs,y=y_locs, ax=ax)
    plt.yticks(np.arange(21),np.arange(21),rotation=0, fontsize="10", va="center")
    plt.xticks(np.arange(21),np.arange(21),rotation=0, fontsize="10", va="center")
    plt.scatter(y_locs, x_locs, color='black', s=100)
    # for i in range(len(x_locs)):
    #     if i == 35 or i == 5:
    #         circle = plt.Circle((y_locs[i], x_locs[i]), radius=r[i], fill=False)
    #         plt.gca().add_patch(circle)
    # plt.xlim(min(y_locs)-5, max(y_locs)+5)
    # plt.ylim(min(x_locs)-5, max(x_locs)+5)

    plt.show()

def tower_allocation(x_locs, y_locs, r):
    grid = np.array(loadtxt('adj.txt', delimiter=' '), dtype="int")
    n_colors = grid.max() + 1
    cmap = sns.color_palette("Spectral", n_colors=n_colors)
    f, ax = plt.subplots(figsize=(30, 30))
    s = sns.heatmap(grid, cmap=cmap, annot=True, ax=ax)
    plt.yticks(np.arange(21),np.arange(21),rotation=0, fontsize="10", va="center")
    plt.xticks(np.arange(21),np.arange(21),rotation=0, fontsize="10", va="center")
    plt.scatter(y_locs, x_locs, color='black', s=40)
    for i in range(len(x_locs)):
        circle = plt.Circle((y_locs[i], x_locs[i]), radius=r[i], fill=False)
        plt.gca().add_patch(circle)
    plt.xlim(min(y_locs)-5, max(y_locs)+5)
    plt.ylim(min(x_locs)-5, max(x_locs)+5)
    plt.show()

    # plt.show()

def towers_location(x_locs, y_locs, r):
    plt.scatter(x_locs, y_locs, color='red', s=50)
    for i in range(len(x_locs)):
        circle = plt.Circle((x_locs[i], y_locs[i]), radius=r[i], fill=False)
        plt.gca().add_patch(circle)
    plt.xlim(min(x_locs), max(x_locs))
    plt.ylim(min(y_locs), max(y_locs))
    plt.show()

def get_towers():
    towers = np.array(loadtxt('towers.txt', delimiter=' '), dtype="float")
    x_locs, y_locs, r = [], [], []
    x_locs = [tower[0] for tower in towers]
    y_locs = [tower[1] for tower in towers]
    r = [tower[2] for tower in towers]
    return x_locs, y_locs, r

def avg_fitness():
    df = pd.read_csv('histories.csv', header=None)
    df.loc['mean'] = df.mean()
    df.loc['min'] = df.min()
    df.loc['max'] = df.max()
    fig, ax = plt.subplots(figsize =(20,20))
    ax.plot(df.columns,df.loc['mean'])
    ax.fill_between(df.columns, df.loc['min'], df.loc['max'], alpha=0.2)
    ax.set_xlabel('Generations')
    ax.set_ylabel('Average Fitness')
    plt.xticks(range(0, len(df.columns),25))
    plt.show()
    #print(df)


if __name__ == '__main__':
    x_locs, y_locs, r = get_towers()
    user_satisfaction_score(0, 40)
    user_satisfaction_level(x_locs, y_locs, r)
    tower_allocation(x_locs, y_locs, r)
    towers_location(x_locs, y_locs, r)
    avg_fitness()