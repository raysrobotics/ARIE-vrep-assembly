import csv
import numpy as np
# import pandas as pd
import cv2
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import cm

import os

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

def csv2outname(file_path):
    '''
    Input load file path, output a output name string

    e.g. Input:  ../results/result_001.csv
         Output: ../resutls/result_001.png
    '''
    return file_path.replace('.csv', '.png')


def local_minima2(mat, x_label, y_label):
    '''
    Input 2d matrix, return the only one local minimum which 
    should be the bottom of the ARIE
    '''
    coordinates = peak_local_max(-mat, min_distance=20)

    coord_new = coordinates

    x = x_label[coord_new[:,1]]
    y = y_label[coord_new[:,0]]
    d = [mat[x[0],x[1]] for x in coord_new]

    # find the only one local minia that could be the bottom of the ARIE
    # rule: the point that is closest to the origin
    dist = np.sqrt(np.square(x) + np.square(y))
    min_idx = np.argmin(dist)

    return coord_new[:,1], coord_new[:,0], min_idx, [x, y, d] # x_indexes, y_indexes, min_idx, [x,y,d]

def plot_local_minima(mat, x_idxs, y_idxs, min_idx, save_path_and_name):
    fig, ax = plt.subplots()

    ax.imshow(mat, cmap=plt.cm.gray)
    ax.autoscale(False)
    ax.plot(x_idxs, y_idxs,'r.')
    ax.plot(x_idxs[min_idx], y_idxs[min_idx],'b*')
    ax.axis('off')
    ax.set_title('Peak local min')

    plt.savefig(save_path_and_name)
    plt.close()

if __name__ == "__main__":

    input_folder = './z0_360_corner'
    for path, subdirs, files in os.walk(input_folder):
        for name in files:
            if not name.endswith('.csv'):
                continue

            file_path = os.path.join(path, name)
    
            x, y, z = csv2array(file_path)

            x_unique = np.unique(x)
            y_unique = np.unique(y)

            Z = np.zeros((len(y_unique), len(x_unique)))
            k = 0
            for i in range(len(x_unique)):
                for j in range(len(y_unique)):
                    Z[j, i] = z[k]
                    k = k+1
            
            x_indexes, y_indexes, min_idx, xyd = local_minima2(Z, x_unique, y_unique)

            output_fig_path = csv2outname(file_path)
            plot_local_minima(Z, x_indexes, y_indexes, min_idx, output_fig_path)
            print(f'{output_fig_path} generated.')


