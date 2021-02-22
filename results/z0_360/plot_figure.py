import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def loadCSV(file_path):
    csv_file = pd.read_csv(file_path)
    rot_x = csv_file['rot_x'].to_numpy()
    rot_y = csv_file['rot_y'].to_numpy()
    rot_z = csv_file['rot_z'].to_numpy()
    x = csv_file['x'].to_numpy()
    y = csv_file['y'].to_numpy()
    z = csv_file['z'].to_numpy()

    return rot_x, rot_y, rot_z, x, y, z

fig, axs = plt.subplots(nrows=1, ncols=2)


csv_corner = './z0_360_mode_corner.csv'
rot_x, rot_y, rot_z, x, y, z = loadCSV(csv_corner)

axs[0].plot(rot_z, z, 'o-b')

axs[0].set(xlabel='rotational angle ($\degree$)', ylabel='insert depth (mm)',
       title='Relationship between $\\theta_z$ and insert depth\n(insert by corner)')
axs[0].grid()


csv_edge = './z0_360_mode_edge.csv'
rot_x, rot_y, rot_z, x, y, z = loadCSV(csv_edge)

axs[1].plot(rot_z, z, 'o-b')

axs[1].set(xlabel='rotational angle ($\degree$)', ylabel='insert depth (mm)',
       title='Relationship between $\\theta_z$ and insert depth\n(insert by edge)')
axs[1].grid()


plt.show()