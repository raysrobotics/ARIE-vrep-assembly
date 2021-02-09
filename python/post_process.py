import csv
import numpy as np
# import pandas as pd
import cv2
import matplotlib.pyplot as plt
from matplotlib import cm

from skimage.feature import peak_local_max

def csv2array(file_path):
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

    # convert the lists to numpy arrays
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    # z = np.nan_to_num(z, nan=0.0, posinf=0.0, neginf=0.0)

    return x, y, z

def local_minima(mat, x_label, y_label):
    coordinates = peak_local_max(-mat, min_distance=20)

    # coord_new = []
    # for i, c in enumerate(coordinates):
    #     if np.abs(mat[c[0], c[1]] - 0.002) > 0.001:
    #         coord_new.append(c)
    # coord_new = np.array(coord_new)
    coord_new = coordinates

    x = x_label[coord_new[:,1]]
    y = y_label[coord_new[:,0]]
    d = [mat[x[0],x[1]] for x in coord_new]

    fig, axes = plt.subplots(1, 2, figsize=(8, 3), sharex=True, sharey=True)
    ax = axes.ravel()

    ax[0].imshow(mat, cmap=plt.cm.gray)
    ax[0].axis('off')
    ax[0].set_title('Original')

    ax[1].imshow(mat, cmap=plt.cm.gray)
    ax[1].autoscale(False)
    ax[1].plot(coord_new[:,1],coord_new[:,0],'r.')
    ax[1].axis('off')
    ax[1].set_title('Peak local min')

    fig.tight_layout()
    plt.show()

    return x, y, d

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
        Z = np.nan_to_num(Z, nan=0.0, posinf=0.0, neginf=0.0)

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
    
    x, y, z = csv2array(file_path)

    draw_ARIE(x, y, z, plot_mode=plot_mode, slice=slice)

    x_unique = np.unique(x)
    y_unique = np.unique(y)

    Z = np.zeros((len(y_unique), len(x_unique)))
    k = 0
    for i in range(len(x_unique)):
        for j in range(len(y_unique)):
            Z[j, i] = z[k]
            k = k+1
    
    xx, yy, dd = local_minima(Z, x_unique, y_unique)

    R = np.array([xx, yy, dd])
    with np.printoptions(precision=4, suppress=True):
        print(R)


