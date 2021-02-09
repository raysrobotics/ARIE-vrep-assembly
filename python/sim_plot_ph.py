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
parser.add_argument('--peg-pos-x', type=float, default=0.0, 
                    help='The x position of the peg.')
parser.add_argument('--peg-pos-y', type=float, default=0.0, 
                    help='The y position of the peg.')
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


# create the simulation manager
sm = SimManager(remoteIP, remotePort)

# load model info from models.json
cur_path = os.path.dirname(os.path.realpath('./'))
json_path = f'{cur_path}/models/models.json'
model_info = loadJson(json_path)

x_pos = args.peg_pos_x
y_pos = args.peg_pos_y

downward_depth = args.depth
downward_precision = args.precision

ore_x_peg = args.peg_ore_x
ore_y_peg = args.peg_ore_y
ore_z_peg = args.peg_ore_z

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

## Initialize loop variables
z_init = obj_peg_init_pos[2]
        
retCode, result, next_z = sm.findLowestPoint(
    x_pos, y_pos, z_init, 
    downward_depth, downward_precision)

## Fit to view
sm.setCameraFitToView()

print(f'Return Code: {retCode}')
print(f'Result: {result}')