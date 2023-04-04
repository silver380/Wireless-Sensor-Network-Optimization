import matplotlib.pyplot as plt
import seaborn as sns
from numpy import loadtxt

def user_satisfaction_score(min_stais, max_stais):
    scores = loadtxt('user_satisfaction_score.txt', delimiter=' ')
    sns.set_theme()
    f, ax = plt.subplots(figsize=(20, 20))
    s = sns.heatmap(scores, annot=True, fmt='.1f', linewidth=.5, ax=ax, vmin=min_stais, vmax=max_stais, cmap=sns.cubehelix_palette(as_cmap=True))
    s.invert_yaxis()
    plt.show()

if __name__ == '__main__':
    user_satisfaction_score(-20, 40)