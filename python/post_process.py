import csv
import numpy as np
# import pandas as pd
import cv2
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

        surf = ax.plot_surface(X, Y, Z, cmap=parula(), antialiased=True)

        zz = np.sort(np.unique(z))
        zz_range = np.linspace(zz[0], zz[-1], 4)
        ax.set_zticks(zz_range)
        ax.set_zlim((zz[0], zz[-1]))

        ax.zaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.3f}"))
    else: # plot_mode == 1
        print('len(x)={}\nlen(y)={}\nlen(z)={}'.format(len(x),len(y),len(z)))
        points = ax.scatter(x[::slice], y[::slice], z[::slice], c=z[::slice], cmap=cm.coolwarm, marker='.')
    
    ax.set(
        xlabel='$(O_p O_h)_x$ (mm)', 
        ylabel='$(O_p O_h)_y$ (mm)',
        zlabel='$(O_p O_h)_z$ (mm)')
    
    # Show the plot
    # plt.show()

def parula():
    from matplotlib.colors import LinearSegmentedColormap

    cm_data = [ [0.2081, 0.1663, 0.5292], 
                [0.2116238095, 0.1897809524, 0.5776761905], 
                [0.212252381, 0.2137714286, 0.6269714286], 
                [0.2081, 0.2386, 0.6770857143], 
                [0.1959047619, 0.2644571429, 0.7279], 
                [0.1707285714, 0.2919380952, 0.779247619], 
                [0.1252714286, 0.3242428571, 0.8302714286], 
                [0.0591333333, 0.3598333333, 0.8683333333], 
                [0.0116952381, 0.3875095238, 0.8819571429], 
                [0.0059571429, 0.4086142857, 0.8828428571], 
                [0.0165142857, 0.4266, 0.8786333333], 
                [0.032852381, 0.4430428571, 0.8719571429], 
                [0.0498142857, 0.4585714286, 0.8640571429], 
                [0.0629333333, 0.4736904762, 0.8554380952], 
                [0.0722666667, 0.4886666667, 0.8467], 
                [0.0779428571, 0.5039857143, 0.8383714286], 
                [0.079347619, 0.5200238095, 0.8311809524], 
                [0.0749428571, 0.5375428571, 0.8262714286], 
                [0.0640571429, 0.5569857143, 0.8239571429], 
                [0.0487714286, 0.5772238095, 0.8228285714], 
                [0.0343428571, 0.5965809524, 0.819852381], 
                [0.0265, 0.6137, 0.8135], 
                [0.0238904762, 0.6286619048, 0.8037619048], 
                [0.0230904762, 0.6417857143, 0.7912666667],  
                [0.0227714286, 0.6534857143, 0.7767571429], 
                [0.0266619048, 0.6641952381, 0.7607190476], 
                [0.0383714286, 0.6742714286, 0.743552381], 
                [0.0589714286, 0.6837571429, 0.7253857143], 
                [0.0843, 0.6928333333, 0.7061666667], 
                [0.1132952381, 0.7015, 0.6858571429], 
                [0.1452714286, 0.7097571429, 0.6646285714], 
                [0.1801333333, 0.7176571429, 0.6424333333], 
                [0.2178285714, 0.7250428571, 0.6192619048], 
                [0.2586428571, 0.7317142857, 0.5954285714], 
                [0.3021714286, 0.7376047619, 0.5711857143], 
                [0.3481666667, 0.7424333333, 0.5472666667], 
                [0.3952571429, 0.7459, 0.5244428571], 
                [0.4420095238, 0.7480809524, 0.5033142857], 
                [0.4871238095, 0.7490619048, 0.4839761905], 
                [0.5300285714, 0.7491142857, 0.4661142857], 
                [0.5708571429, 0.7485190476, 0.4493904762], 
                [0.609852381, 0.7473142857, 0.4336857143], 
                [0.6473, 0.7456, 0.4188], 
                [0.6834190476, 0.7434761905, 0.4044333333], 
                [0.7184095238, 0.7411333333, 0.3904761905], 
                [0.7524857143, 0.7384, 0.3768142857], 
                [0.7858428571, 0.7355666667, 0.3632714286], 
                [0.8185047619, 0.7327333333, 0.3497904762], 
                [0.8506571429, 0.7299, 0.3360285714], 
                [0.8824333333, 0.7274333333, 0.3217], 
                [0.9139333333, 0.7257857143, 0.3062761905], 
                [0.9449571429, 0.7261142857, 0.2886428571], 
                [0.9738952381, 0.7313952381, 0.266647619], 
                [0.9937714286, 0.7454571429, 0.240347619], 
                [0.9990428571, 0.7653142857, 0.2164142857], 
                [0.9955333333, 0.7860571429, 0.196652381], 
                [0.988, 0.8066, 0.1793666667], 
                [0.9788571429, 0.8271428571, 0.1633142857], 
                [0.9697, 0.8481380952, 0.147452381], 
                [0.9625857143, 0.8705142857, 0.1309], 
                [0.9588714286, 0.8949, 0.1132428571], 
                [0.9598238095, 0.9218333333, 0.0948380952], 
                [0.9661, 0.9514428571, 0.0755333333], 
                [0.9763, 0.9831, 0.0538]]

    parula_map = LinearSegmentedColormap.from_list('parula', cm_data)

    return parula_map

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
    dd = np.array(dd)

    idxx = np.logical_and(xx>=-0.01, xx<=0.01)
    xxx = xx[idxx]
    yyy = yy[idxx]
    ddd = dd[idxx]

    R = np.array([xxx, yyy, ddd])
    with np.printoptions(precision=4, suppress=True):
        print(R)

    plt.show()


