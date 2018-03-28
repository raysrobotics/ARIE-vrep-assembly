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
# This file was created for V-REP release V3.4.0 rev. 1
#
# Load the demo scene 'RemoteApi_ARIE_Assembly.ttt' in V-REP, then run this 
# program.
#
# Usage:
#   python run_sim.py [init_angle_peg] [remoteIP] [remotePort]


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

import sys,os
#import ctypes
import json
import time
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Generate ARIE for the parts.')
parser.add_argument('model_name', type=str, 
                    help='the name of the model')
parser.add_argument('--conf_num', type=int, default=0, # 0 - insert by edge 1 - insert by corner
                    help='the port of the vrep server')
parser.add_argument('--ip-addr', type=str, default='127.0.0.1', 
                    help='the IP address of the vrep server')
parser.add_argument('--port', type=int, default=19997, 
                    help='the port of the vrep server')
parser.add_argument('peg_ore_x', type=float, default=0.0, 
                    help='the orientation of the peg around its axis. Cannot be specified together with peg-pre-y')
parser.add_argument('peg_ore_y', type=float, default=0.0, 
                    help='the orientation of the peg around y-axis. Cannot be specified together with peg-pre-x')
parser.add_argument('peg_ore_z', type=float, default=0.0, 
                    help='the orientation of the peg around z-axis.')
parser.add_argument('--depth', type=float, default=-0.08, 
                    help='the downward depth of the peg')
parser.add_argument('--precision', type=float, default=1e-4, 
                    help='the downward precision of the simulation')
parser.add_argument('--precision-x', type=float, default=1e-3, 
                    help='the precision along x-axis of the simulation')
parser.add_argument('--precision-y', type=float, default=1e-3, 
                    help='the precision along y-axis of the simulation')
parser.add_argument('--x-start', type=float, default=-0.6, 
                    help='the start value along x-axis during simulation')
parser.add_argument('--x-end', type=float, default=0.6, 
                    help='the end value along x-axis during simulation')
parser.add_argument('--y-start', type=float, default=-0.6, 
                    help='the start value along y-axis during simulation')
parser.add_argument('--y-end', type=float, default=0.6, 
                    help='the end value along y-axis during simulation')
parser.add_argument('--plot', action="store_true", 
                    help='plot the figure after the simulation')

args = parser.parse_args()

remoteIP     = args.ip_addr
remotePort   = args.port

model_name = args.model_name
conf_num   = args.conf_num
# load model info from models.json
cur_path = os.path.dirname(os.path.realpath('./'))
json_path = '%s/models/models.json' % cur_path
model_info=json.load(open(json_path))

#obj_peg_path = args.peg_path #'D:/Projects/ADAMS/WYZTB/vrep_model/zhudonghuan1.stl'
#obj_hol_path = args.hol_path #'D:/Projects/ADAMS/WYZTB/vrep_model/beidonghuan1.stl'
obj_peg_path = '%s/%s' % (cur_path, model_info[model_name]['peg']['file_path'])
obj_hol_path = '%s/%s' % (cur_path, model_info[model_name]['hole']['file_path'])

x_delta = args.precision_x
y_delta = args.precision_y

x_start = args.x_start
x_end = args.x_end
y_start = args.y_start
y_end = args.y_end

downward_depth = args.depth
downward_precision = args.precision

ore_x_peg = args.peg_ore_x
ore_y_peg = args.peg_ore_y
ore_z_peg = args.peg_ore_z

#######################

#remoteIP     = "127.0.0.1"
#remotePort   = 19997
#obj_peg_path = "D:/Projects/3D models/simbody_test/tri_peg_hole/peg_tri_r_200_h_801.stl"
#obj_hol_path = "D:/Projects/3D models/simbody_test/tri_peg_hole/hol_tri_r_201_h_901.stl"
#
#x_delta = 5e-4
#y_delta = 5e-4
#
#x_start = -0.04
#x_end = 0.04
#y_start = -0.04
#y_end = 0.04
#
#downward_depth = -0.08
#downward_precision = 1e-4
#
## in degree
#ore_x_peg = 0
#ore_y_peg = 10
#ore_z_peg = 0

#######################


x_range = np.arange(x_start, x_end, x_delta)
y_range = np.arange(y_start, y_end, y_delta)

print ('Program started. IP: {0}, Port:{1}'.format(remoteIP, remotePort))

vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart(remoteIP,remotePort,True,True,5000,5) # Connect to V-REP

if clientID == -1:
    print ('Failed connecting to remote API server')
    sys.exit(-1)


print ('Connected to remote API server, client ID: {0}'.format(clientID))

emptyBuff = bytearray()

# Delete all previous models
res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_customizationscript,'clearObjects_function',[],[],[],emptyBuff,vrep.simx_opmode_blocking)

if res==vrep.simx_return_ok:
    print ('Scene cleared :-)') 
else:
    print ('Remote API Error!')
    
res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_customizationscript,'loadModel_function',[4, 0],[0.0001, 0.001],[obj_hol_path],emptyBuff,vrep.simx_opmode_blocking)
if res==vrep.simx_return_ok:
    h_hole = retInts[0]
    print ('Hole model loaded, handle: {0}'.format(h_hole))

res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_customizationscript,'loadModel_function',[4, 0],[0.0001, 0.001],[obj_peg_path],emptyBuff,vrep.simx_opmode_blocking)
if res==vrep.simx_return_ok:
    h_peg = retInts[0]
    print ('Peg model loaded, handle: {0}'.format(h_peg))

res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_customizationscript,'setObjectName_function',[h_hole],[],['hole'],emptyBuff,vrep.simx_opmode_blocking)
if res==vrep.simx_return_ok:
    print ('Hole name set!') 

res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_customizationscript,'setObjectName_function',[h_peg],[],['peg'],emptyBuff,vrep.simx_opmode_blocking)   
if res==vrep.simx_return_ok:
    print ('Peg name set!') 

# Set initial pose for the peg and hole
obj_hol_init_pos = model_info[model_name]['hole']['config'][conf_num]['init_pos']
obj_hol_init_ore = np.deg2rad(model_info[model_name]['hole']['config'][conf_num]['init_ore']).tolist()
vrep.simxSetObjectPosition(clientID, h_hole, -1, obj_hol_init_pos, vrep.simx_opmode_oneshot)
vrep.simxSetObjectOrientation(clientID, h_hole, -1, obj_hol_init_ore, vrep.simx_opmode_oneshot)


obj_peg_init_pos = model_info[model_name]['peg']['config'][conf_num]['init_pos']
obj_peg_init_ore = np.deg2rad(model_info[model_name]['peg']['config'][conf_num]['init_ore']).tolist()
vrep.simxSetObjectPosition(clientID, h_peg, -1, obj_peg_init_pos, vrep.simx_opmode_oneshot)
vrep.simxSetObjectOrientation(clientID, h_peg, -1, obj_peg_init_ore, vrep.simx_opmode_oneshot)

# Set target pose for the peg
retCode,curr_pos=vrep.simxGetObjectOrientation(clientID,h_peg,-1,vrep.simx_opmode_blocking)
new_pos = [curr_pos[0]+np.deg2rad(ore_x_peg), curr_pos[1], curr_pos[2]];
vrep.simxSetObjectOrientation(clientID, h_peg, -1, new_pos, vrep.simx_opmode_oneshot)

retCode,curr_pos=vrep.simxGetObjectOrientation(clientID,h_peg,-1,vrep.simx_opmode_blocking)
new_pos = [curr_pos[0], curr_pos[1]+np.deg2rad(ore_y_peg), curr_pos[2]];
vrep.simxSetObjectOrientation(clientID, h_peg, -1, new_pos, vrep.simx_opmode_oneshot)

retCode,curr_pos=vrep.simxGetObjectOrientation(clientID,h_peg,-1,vrep.simx_opmode_blocking)
new_pos = [curr_pos[0], curr_pos[1], curr_pos[2]+np.deg2rad(ore_z_peg)];
vrep.simxSetObjectOrientation(clientID, h_peg, -1, new_pos, vrep.simx_opmode_oneshot)


# Fit to view
vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_customizationscript, 'setCameraFitToView_function',[h_peg, h_hole],[],[],emptyBuff,vrep.simx_opmode_blocking)


timestamp = time.strftime('%Y-%m-%d-%H%M',time.localtime(time.time()))
filename = 'results' + timestamp + '_port{0}'.format(remotePort) + '.csv'
cur_path = os.path.dirname(os.path.realpath(__file__))
file_and_path = '%s/../results/%s' % (cur_path, filename)

h_file=open(file_and_path, 'w+')

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


if args.plot:
    # Data Visualization
#    from mpl_toolkits.mplot3d import Axes3D
    import csv
#    from matplotlib import cm
    import matplotlib.pyplot as plt
    #import pandas as pd
    
    def read_csv_col(file_location, i):  
        with open(filename, encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)  
            return [col[i] for col in reader]  
        
    x=read_csv_col(filename, 0)
    y=read_csv_col(filename, 1)
    z=read_csv_col(filename, 2)
    
    X, Y = np.meshgrid(x_range, y_range)
    Z = np.float64(np.reshape(z, (np.shape(X)), order='F'))
    
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z)
    plt.show()
else:
    pass

print ('Program ended')