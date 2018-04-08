# Copyright 2006-2017 Coppelia Robotics GmbH. All rights reserved. 
# marc@coppeliarobotics.com
# www.coppeliarobotics.com
# 
# -------------------------------------------------------------------
# THIS FILE IS DISTRIBUTED "AS IS", WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY. THE USER WILL USE IT AT HIS/HER OWN RISK. THE ORIGINAL
# AUTHORS AND COPPELIA ROBOTICS GMBH WILL NOT BE LIABLE FOR DATA LOSS,
# DAMAGES, LOSS OF PROFITS OR ANY OTHER KIND OF LOSS WHILE USING OR
# MISUSING THIS SOFTWARE.
# 
# You are free to use/modify/distribute this file for whatever purpose!
# -------------------------------------------------------------------
#
# This file was automatically created for V-REP release V3.4.0 rev. 1 on April 5th 2017

# This example illustrates how to execute complex commands from
# a remote API client. You can also use a similar construct for
# commands that are not directly supported by the remote API.
#
# Load the demo scene 'remoteApiCommandServerExample.ttt' in V-REP, then 
# start the simulation and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')

import sys
import os
import json
#import ctypes
import time
try:
    import numpy as np
except:
    print ('--------------------------------------------------------------')
    print ('"numpy" could not be imported. Do you run this script in ')
    print ('Anaconda environment?')
    print ('--------------------------------------------------------------')
    print ('')

# remoteIP = '10.0.9.140'
# obj_peg_path = '/home/ray/MyModels/peg.obj'
# obj_hol_path = '/home/ray/MyModels/hole_40_2.obj'

remoteIP = '127.0.0.1'
model_name = "dual_round_peg_hole"#'pentagon_peg_hole' #'rectangle_peg_hole' #
conf_num = 0 # 0 - insert by edge 1 - insert by corner

# load model info from models.json
cur_path = os.path.dirname(os.path.realpath('./'))
json_path = '%s/models/models.json' % cur_path
model_info=json.load(open(json_path))

obj_peg_path = '%s/%s' % (cur_path, model_info[model_name]['peg']['file_path'])
obj_hol_path = '%s/%s' % (cur_path, model_info[model_name]['hole']['file_path'])

#obj_peg_path = 'D:/Projects/3D models/simbody_test/tri_peg_hole/peg_tri_r_200_h_801.stl'
#obj_hol_path = 'D:/Projects/3D models/simbody_test/tri_peg_hole/hol_tri_r_201_h_901.stl'

#obj_peg_init_pos = [0, 0, 20e-2]
#obj_peg_init_ore = [0, 0, 0] #-np.pi/2-np.pi/1
#obj_hol_init_pos = [0, 0, 0.046]

x_delta = 1e-3
y_delta = 1e-3

x_start = -0.04
x_end = 0.04
y_start = -0.04
y_end = 0.04

x_range = np.arange(x_start, x_end, x_delta)
y_range = np.arange(y_start, y_end, y_delta)

downward_depth = -0.08
downward_precision = 1e-4

print ('Program started')

vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart(remoteIP,19997,True,True,5000,5) # Connect to V-REP

if clientID == -1:
    print ('Failed connecting to remote API server')
    sys.exit(-1)


print ('Connected to remote API server')

emptyBuff = bytearray()

# Delete all previous models
res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_customizationscript,'clearObjects_function',[],[],[],emptyBuff,vrep.simx_opmode_blocking)

if res==vrep.simx_return_ok:
    print ('Objects removed!') 
    
res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_customizationscript,'loadModel_function',[4, 0],[0.0001, 0.001],[obj_hol_path],emptyBuff,vrep.simx_opmode_blocking)
if res==vrep.simx_return_ok:
    print ('Hole model loaded!')
    h_hole = retInts[0]

res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_customizationscript,'loadModel_function',[4, 0],[0.0001, 0.001],[obj_peg_path],emptyBuff,vrep.simx_opmode_blocking)
if res==vrep.simx_return_ok:
    print ('Peg model loaded!') 
    h_peg = retInts[0]

res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_customizationscript,'setObjectName_function',[h_hole],[],['hole'],emptyBuff,vrep.simx_opmode_blocking)
if res==vrep.simx_return_ok:
    print ('Hole name set!') 

res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_customizationscript,'setObjectName_function',[h_peg],[],['peg'],emptyBuff,vrep.simx_opmode_blocking)   
if res==vrep.simx_return_ok:
    print ('Peg name set!') 


#retCode,obj_hol_init_ore = vrep.simxGetObjectOrientation(clientID,h_hole, -1,vrep.simx_opmode_blocking)
#retCode,obj_peg_init_ore = vrep.simxGetObjectOrientation(clientID,h_peg, -1,vrep.simx_opmode_blocking)

obj_hol_init_pos = model_info[model_name]['hole']['config'][conf_num]['init_pos']
obj_hol_init_ore = np.deg2rad(model_info[model_name]['hole']['config'][conf_num]['init_ore']).tolist()
vrep.simxSetObjectPosition(clientID, h_hole, -1, obj_hol_init_pos, vrep.simx_opmode_oneshot)
vrep.simxSetObjectOrientation(clientID, h_hole, -1, obj_hol_init_ore, vrep.simx_opmode_oneshot)

obj_peg_init_pos = model_info[model_name]['peg']['config'][conf_num]['init_pos']
obj_peg_init_ore = np.deg2rad(model_info[model_name]['peg']['config'][conf_num]['init_ore']).tolist()
vrep.simxSetObjectPosition(clientID, h_peg, -1, obj_peg_init_pos, vrep.simx_opmode_oneshot)
vrep.simxSetObjectOrientation(clientID, h_peg, -1, obj_peg_init_ore, vrep.simx_opmode_oneshot)

peg_ore_x = 20
peg_ore_y = 0
peg_ore_z = 0

retCode,curr_pos=vrep.simxGetObjectOrientation(clientID,h_peg,-1,vrep.simx_opmode_blocking)
new_pos = [curr_pos[0]+np.deg2rad(peg_ore_x), curr_pos[1], curr_pos[2]];
vrep.simxSetObjectOrientation(clientID, h_peg, -1, new_pos, vrep.simx_opmode_oneshot )

retCode,curr_pos=vrep.simxGetObjectOrientation(clientID,h_peg,-1,vrep.simx_opmode_blocking)
new_pos = [curr_pos[0], curr_pos[1]+np.deg2rad(peg_ore_y), curr_pos[2]];
vrep.simxSetObjectOrientation(clientID, h_peg, -1, new_pos, vrep.simx_opmode_oneshot )

retCode,curr_pos=vrep.simxGetObjectOrientation(clientID,h_peg,-1,vrep.simx_opmode_blocking)
new_pos = [curr_pos[0], curr_pos[1], curr_pos[2]+np.deg2rad(peg_ore_z)];
vrep.simxSetObjectOrientation(clientID, h_peg, -1, new_pos, vrep.simx_opmode_oneshot )

#vrep.simxSetObjectPosition(clientID, h_hole, -1, obj_hol_init_pos, vrep.simx_opmode_blocking)
#vrep.simxSetObjectPosition(clientID, h_peg, -1, obj_peg_init_pos, vrep.simx_opmode_blocking)
#vrep.simxSetObjectOrientation(clientID, h_peg, -1, obj_peg_init_ore, vrep.simx_opmode_blocking)

# Fit to view
vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_customizationscript, 'setCameraFitToView_function',[h_peg, h_hole],[],[],emptyBuff,vrep.simx_opmode_blocking)


timestamp = time.strftime('%Y-%m-%d-%H%M',time.localtime(time.time()))
filename = 'results2' + timestamp + '.csv'

h_file=open(filename, 'w+')

# initialize loop variables
z_init = obj_peg_init_pos[2]

# progress_indicator
prog_i = 0 

# these vars are used to calculate the approximate running time of the program
is_first_five_runs = True 
five_counter = 0
average_time = 0.0

for x in x_range:
    
    prog_now = (x-x_start)/(x_end-x_start)
    if (prog_now - prog_i >= 0.01):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print('{0} - Progress: {1:.2%}'.format(timestamp, prog_now))
        prog_i = prog_now
    
    for y in y_range:
        if is_first_five_runs:
            time_start = time.clock()
        
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_customizationscript,'findLowestPoint2_function',[h_peg, h_hole],[downward_depth, downward_precision, x, y, z_init],[],emptyBuff,vrep.simx_opmode_blocking)   
        if res==vrep.simx_return_ok:
            if retInts[0] == 0:
                #fprintf(h_file,'%f, %f, %f\n',retFloats(1), retFloats(2), retFloats(3))
                h_file.write('{0[0]:.5f}, {0[1]:.5f}, {0[2]:.5f}\n'.format(retFloats))
                z_init = retFloats[2]                
            elif retInts[0] == -1:
                #fprintf(h_file,'%f, %f, Inf\n',retFloats(1), retFloats(2))
                h_file.write('{0[0]:.5f}, {0[1]:.5f}, Inf\n'.format(retFloats))
                z_init = obj_peg_init_pos[2]
            else:
                print('Find Lowest Point Error!\n')
                h_file.close()
                print('[{0}] has been partially saved!\n'.format(filename))
                sys.exit(-1)
        
        if is_first_five_runs:
            time_end = time.clock()
            average_time = average_time + (time_end-time_start)
            five_counter = five_counter + 1
            if five_counter >= 5:
                is_first_five_runs = False
                total_time = average_time/5*x_range.size*y_range.size
                if total_time >= 3600:
                    show_time = '{0:.2f} [hour]'.format(total_time/3600)
                elif total_time >= 60:
                    show_time = '{0:.2f} [min]'.format(total_time/60)
                else:
                    show_time = '{0:.2f} [sec]'.format(total_time)
                print ('Approximate running time of the program is: {0}'.format(show_time))
                

h_file.close()
print('[{0}] has been saved!'.format(filename))
                
vrep.simxSetObjectPosition(clientID, h_peg, -1, obj_peg_init_pos, vrep.simx_opmode_blocking)
vrep.simxSetObjectOrientation(clientID, h_peg, -1, obj_peg_init_ore, vrep.simx_opmode_blocking)
            
# Fit to view
vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_customizationscript, 'setCameraFitToView_function',[h_peg, h_hole],[],[],emptyBuff,vrep.simx_opmode_blocking)

vrep.simxFinish(clientID)
print ('Program ended')

# Data Visualization
from mpl_toolkits.mplot3d import Axes3D
import csv
from matplotlib import cm
import matplotlib.pyplot as plt
#import pandas as pd

def read_csv_col(file_location, i):  
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)  
        return [col[i] for col in reader]  

#xyz_dat = pd.read_csv(filename, encoding='utf-8')
#x = xyz_dat[0:]
#y = xyz_dat[1:]
#z = xyz_dat[2:]

x=read_csv_col(filename, 0)
y=read_csv_col(filename, 1)
z=read_csv_col(filename, 2)

X, Y = np.meshgrid(x_range, y_range)
Z = np.float64(np.reshape(z, (np.shape(X)), order='F'))


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, Z)
plt.show()
    