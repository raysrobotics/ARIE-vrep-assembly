import yaml
import subprocess
import time
import os
import numpy as np
import argparse

def loadYaml(config_path):
    yaml_content = None
    with open(config_path) as file:
        yaml_content = yaml.load(file, Loader=yaml.FullLoader)
    return yaml_content

def runVrepCmd(port, vrep_path, scene_path):
    timestamp = time.strftime('%Y-%m-%d-%H%M%S',time.localtime(time.time()))        
    with open(f'log_{timestamp}_{port}.txt', 'w') as f:
        process = subprocess.Popen(
            [vrep_path, f'-gREMOTEAPISERVERSERVICE_{port}_FALSE_TRUE', scene_path],
            stdout=f)

def runSimCmd(model_name, conf_num, 
        ip_addr, ip_port, 
        xy_pos,
        xyz_rot,
        depth, precision):
    process = subprocess.Popen(
                ['python', '../python/sim_plot_ph.py', 
                model_name, f'{xyz_rot[0]}', f'{xyz_rot[1]}', f'{xyz_rot[2]}',
                '--conf_num', f'{conf_num}',
                '--ip-addr', f'{ip_addr}', '--port', f'{ip_port}',
                '--peg-pos-x', f'{xy_pos[0]}', '--peg-pos-y', f'{xy_pos[1]}',
                '--depth', f'{depth}', '--precision', f'{precision}'])
    # process = subprocess.Popen(
    #             ['python', '../python/sim_plot_ph.py', 
    #             model_name, f'{xyz_rot[0]}', f'{xyz_rot[1]}', f'{xyz_rot[2]}',
    #             '--conf_num', f'{conf_num}',
    #             '--ip-addr', f'{ip_addr}', '--port', f'{ip_port}',
    #             '--peg-pos-x', f'{xy_pos[0]}', '--peg-pos-y', f'{xy_pos[1]}',
    #             '--depth', f'{depth}', '--precision', f'{precision}'], 
    #             creationflags=subprocess.CREATE_NEW_CONSOLE)

parser = argparse.ArgumentParser(description='Visualize the peg-hole configuration.')
parser.add_argument('--run-vrep', action="store_true", 
                    help='Run vrep when executing this script.')
args = parser.parse_args()
run_vrep = args.run_vrep

## load yaml
config_path = './config/rrec_plot_ph_corner.yaml'
config = loadYaml(config_path)

## run vrep
model_name = config['model_name']
conf_num = config['configuration_mode']

x_pos = config['peg_position']['x']
y_pos = config['peg_position']['y']

downward_depth = config['z_range']['z_end']
downward_precision = config['z_range']['z_precision']

x_rot = config['peg_orientation']['x_rot']
y_rot = config['peg_orientation']['y_rot']
z_rot = config['peg_orientation']['z_rot']

## run sim
if run_vrep:
    print('Launching CollepiaSim instances...')

    vrep_path = "C:/Program Files/CoppeliaRobotics/CoppeliaSimEdu/coppeliaSim.exe"
    # cur_path = os.path.dirname(os.path.realpath(__file__))
    scene_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
            '..', 'vrep', 'RemoteApi_ARIE_Assembly.ttt')
    port = 19997
    runVrepCmd(port, vrep_path, scene_path)

    # wait for 30 secs for vrep initialization
    print('Wait 10 secs to run the simulations...')
    time.sleep(10)

    print('Simulation started.')

xy_pos = [x_pos, y_pos]
xyz_rot = [x_rot, y_rot, z_rot]

runSimCmd(model_name=model_name, conf_num=conf_num,
    ip_addr='127.0.0.1', ip_port=19997,
    xy_pos=xy_pos,
    xyz_rot=xyz_rot,
    depth=downward_depth, precision=downward_precision
    )