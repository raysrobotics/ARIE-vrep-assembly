from sim_manager import SimManager

import sys,os
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
parser.add_argument('--precision', type=float, default=1e-5, 
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
parser.add_argument('--file-name', type=str, default='output.csv', 
                    help='The name of the output csv file.')
args = parser.parse_args()

def loadJson(json_path):
    json_content = None
    with open(json_path) as file:
        json_content = json.load(file)
    return json_content

remoteIP     = args.ip_addr
remotePort   = args.port

model_name = args.model_name
conf_num   = args.conf_num

file_name = args.file_name

# create the simulation manager
sm = SimManager(remoteIP, remotePort)

# load model info from models.json
cur_path = os.path.dirname(os.path.realpath('./'))
json_path = f'{cur_path}/models/models.json'
model_info = loadJson(json_path)

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

x_range = np.arange(x_start, x_end, x_delta)
y_range = np.arange(y_start, y_end, y_delta)


## Delete all previous models
sm.clearObjects()

## Load peg and hold model to the scene
# obj_peg_path = '%s/%s' % (cur_path, model_info[model_name]['peg']['file_path'])
# obj_hol_path = '%s/%s' % (cur_path, model_info[model_name]['hole']['file_path'])
obj_peg_path = os.path.join(cur_path, model_info[model_name]['peg']['file_path'])
obj_hol_path = os.path.join(cur_path, model_info[model_name]['hole']['file_path'])
model_path = [obj_hol_path, obj_peg_path]
[h_hole, h_peg] = sm.loadParts(model_path)

## Set initial pose for the hole
obj_hol_init_pos = model_info[model_name]['hole']['config'][conf_num]['init_pos']
obj_hol_init_ore = np.deg2rad(model_info[model_name]['hole']['config'][conf_num]['init_ore']).tolist()
sm.setObjectPosition(obj_handle=h_hole, rel_handle=-1,
    position=obj_hol_init_pos)
sm.setObjectOrientation(obj_handle=h_hole, rel_handle=-1,
    orientation=obj_hol_init_ore)

## Set initial pose for the peg
obj_peg_init_pos = model_info[model_name]['peg']['config'][conf_num]['init_pos']
obj_peg_init_ore = np.deg2rad(model_info[model_name]['peg']['config'][conf_num]['init_ore']).tolist()
sm.setObjectPosition(obj_handle=h_peg, rel_handle=-1,
    position=obj_peg_init_pos)
sm.setObjectOrientation(obj_handle=h_peg, rel_handle=-1,
    orientation=obj_peg_init_ore)

## Set target pose for the peg
# x-axis
retCode,curr_pos = sm.getObjectOrientation(obj_handle=h_peg, rel_handle=-1)
new_pos = [curr_pos[0]+np.deg2rad(ore_x_peg), curr_pos[1], curr_pos[2]]
sm.setObjectOrientation(obj_handle=h_peg, rel_handle=-1,
    orientation=new_pos)
# y-axis
retCode,curr_pos = sm.getObjectOrientation(obj_handle=h_peg, rel_handle=-1)
new_pos = [curr_pos[0], curr_pos[1]+np.deg2rad(ore_y_peg), curr_pos[2]]
sm.setObjectOrientation(obj_handle=h_peg, rel_handle=-1,
    orientation=new_pos)
# z-axis
retCode,curr_pos = sm.getObjectOrientation(obj_handle=h_peg, rel_handle=-1)
new_pos = [curr_pos[0], curr_pos[1], curr_pos[2]+np.deg2rad(ore_z_peg)]
sm.setObjectOrientation(obj_handle=h_peg, rel_handle=-1,
    orientation=new_pos)

## Fit to view
sm.setCameraFitToView()

## Set output csv file path and get the handle
out_path = f'{cur_path}/results/{file_name}'
h_file = open(out_path, 'w+')

## Initialize loop variables
z_init = obj_peg_init_pos[2]

# progress_indicator
prog_i = 0 

# these vars are used to calculate the approximate running time of the program
is_first_five_runs = True 
five_counter = 0
average_time = 0.0
time_start = None

for x in x_range:
    
    prog_now = (x-x_start)/(x_end-x_start)
    if (prog_now - prog_i >= 0.01):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print('{0} - Progress: {1:.2%}'.format(timestamp, prog_now))
        prog_i = prog_now
    
    for y in y_range:
        if is_first_five_runs:
            time_start = time.time()
        
        retCode, result, next_z = sm.findLowestPoint(x, y, z_init, downward_depth, downward_precision)

        # Start next z from last simulation to save time        
        z_init = next_z if next_z != None else obj_peg_init_pos[2]
        h_file.write(result)

        if is_first_five_runs:
            time_end = time.time()
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
print('[{0}] has been saved!'.format(out_path))