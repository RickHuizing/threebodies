import matplotlib.pyplot as plt


def init_plt_style():
    plt.style.use('classic')
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.size'] = 9
    plt.rcParams['legend.fontsize'] = 9
    plt.rcParams['text.usetex'] = True
    plt.rcParams["figure.figsize"] = [150/25.4, 100/25.4]
    plt.rcParams["figure.dpi"] = 144
    plt.rcParams["scatter.marker"] = '.'
    plt.rcParams["figure.autolayout"] = True