import csv
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from matplotlib import cm


def load_saved_data(file_path):
    '''
    Load the csv file and return the values as lists

    Data format in .csv file:
    x, y, d

    return:
    x, y, d
    '''
    x, y, z = [], [], []
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            x.append(float(row[0]))
            y.append(float(row[1]))
            z.append(float(row[2]))

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    # csvframe = pd.read_csv(file_path, 
    #     names=['x', 'y', 'd'], 
    #     na_values='Inf')

    # x = csvframe['x'].to_numpy()
    # y = csvframe['y'].to_numpy()
    # z = csvframe['d'].to_numpy()

    return x, y, z


def draw_ARIE(x, y, z, plot_mode = 0, slice=1):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    if plot_mode == 0:
        num_x = len(np.unique(x))
        num_y = len(np.unique(y))

        if (num_x * num_y != len(x)):
            print('num_x={}\nnum_y={}\nlen(x)={}'.format(num_x, num_y, len(x)))
            print('Incomplete data file, please use `--plot-mode 1` to draw the figure.')
            exit(-1)

        X = np.reshape(x, (num_x, num_y))
        Y = np.reshape(y, (num_x, num_y))
        Z = np.reshape(z, (num_x, num_y))

        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, antialiased=True)
    else: # plot_mode == 1
        print('len(x)={}\nlen(y)={}\nlen(z)={}'.format(len(x),len(y),len(z)))
        points = ax.scatter(x[::slice], y[::slice], z[::slice], c=z[::slice], cmap=cm.coolwarm, marker='.')
    # Show the plot
    plt.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Visualize the generated ARIE.')
    parser.add_argument('csv_path', type=str, 
                        help='The path to the saved .csv file')
    parser.add_argument('--plot-mode', type=int, default=0, 
                    help='0 - draw the surface | 1 - draw the scatter')
    parser.add_argument('--slice', type=int, default=1,
                    help='If plot_mode=1, set list slice to N (N>1) to reduce memory usage.')
    args = parser.parse_args()

    file_path = args.csv_path
    plot_mode = args.plot_mode
    slice = args.slice
    
    x, y, z = load_saved_data(file_path)

    draw_ARIE(x, y, z, plot_mode=plot_mode, slice=slice)
