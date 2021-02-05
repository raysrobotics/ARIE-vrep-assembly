import yaml
import subprocess
import time
import os
import numpy as np

def loadYaml(config_path):
    yaml_content = None
    with open(config_path) as file:
        yaml_content = yaml.load(file, Loader=yaml.FullLoader)
    return yaml_content

def runVrepCmd(port, scene_path):
    timestamp = time.strftime('%Y-%m-%d-%H%M%S',time.localtime(time.time()))        
    with open(f'log_{timestamp}_{port}.txt', 'w') as f:
        process = subprocess.Popen(
            [vrep_path, '-h', f'-gREMOTEAPISERVERSERVICE_{port}_FALSE_TRUE', scene_path],
            stdout=f)

def runSimCmd(model_name, conf_num, 
        ip_addr, ip_port, 
        x_start, x_end, x_delta,
        y_start, y_end, y_delta,
        xyz_rot,
        depth, precision,
        output_name):
    process = subprocess.Popen(
                ['python', '../python/run_sim.py', 
                model_name, f'{xyz_rot[0]}', f'{xyz_rot[1]}', f'{xyz_rot[2]}',
                '--conf_num', f'{conf_num}',
                '--ip-addr', f'{ip_addr}', '--port', f'{ip_port}',
                '--precision-x', f'{x_delta}', '--precision-y', f'{y_delta}',
                '--x-start', f'{x_start}', '--x-end', f'{x_end}',
                '--y-start', f'{y_start}', '--y-end', f'{y_end}',
                '--depth', f'{depth}', '--precision', f'{precision}',
                '--file-name', f'{output_name}'], 
                creationflags=subprocess.CREATE_NEW_CONSOLE)
    # process = subprocess.Popen(
    #         ['python', '../python/run_sim.py', 
    #         model_name, f'--conf_num {conf_num}',
    #         f'--ip-addr {ip_addr}', f'--port {ip_port}',
    #         f'{xyz_rot[0]} {xyz_rot[1]} {xyz_rot[2]}',
    #         f'--precision-x {x_delta}', f'--precision-y {y_delta}',
    #         f'--x-start {x_start}', f'--x-end {x_end}',
    #         f'--y-start {y_start}', f'--y-end {y_end}',
    #         f'--depth {depth}', f'--precision {precision}',
    #         f'--file-name {output_name}'], 
    #         creationflags=subprocess.CREATE_NEW_CONSOLE)

## load yaml
config_path = './config/rrec.yaml'
config = loadYaml(config_path)

## run vrep
model_name = config['model_name']
conf_num = config['configuration_mode']

x_start = config['x_range']['x_begin']
x_end = config['x_range']['x_end']
x_delta = config['x_range']['x_precision']

y_start = config['y_range']['y_begin']
y_end = config['y_range']['y_end']
y_delta = config['y_range']['y_precision']

downward_depth = config['z_range']['z_end']
downward_precision = config['z_range']['z_precision']

x_rot = 0.0
y_rot = 0.0
z_rot = 0.0
if 'x_rot_range' in config.keys():
    iter_mode = 'x'
elif 'y_rot_range' in config.keys():
    iter_mode = 'y'
elif 'z_rot_range' in config.keys():
    iter_mode = 'z'
    x_rot = config['z_rot_range']['x_rot']
    y_rot = config['z_rot_range']['y_rot']
else:
    iter_mode = None
    exit(-1)

loop_begin = config[f'{iter_mode}_rot_range'][f'{iter_mode}_rot_begin']
loop_end = config[f'{iter_mode}_rot_range'][f'{iter_mode}_rot_end']
loop_step = config[f'{iter_mode}_rot_range'][f'{iter_mode}_rot_precision']
loop_num = int((loop_end-loop_begin)/loop_step)

loop_list = np.linspace(loop_begin, loop_end, loop_num)

## run sim
print('Launching CollepiaSim instances...')

vrep_path = "C:/Program Files/CoppeliaRobotics/CoppeliaSimEdu/coppeliaSim.exe"
# cur_path = os.path.dirname(os.path.realpath(__file__))
scene_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
        '..', 'vrep', 'RemoteApi_ARIE_Assembly.ttt')
port_list = range(19997, 19997+loop_num)
for idx, port in enumerate(port_list):
    runVrepCmd(port, scene_path)

# wait for 30 secs for vrep initialization
print('Wait 10 secs to run the simulations...')
time.sleep(10)

print('Simulation started.')
for idx, angle in enumerate(loop_list):
    output_name = f'result_{iter_mode}_{angle:.2f}.csv'

    if iter_mode == 'x':
        xyz_rot = [angle, y_rot, z_rot]
    elif iter_mode == 'y':
        xyz_rot = [x_rot, angle, z_rot]
    else: # iter_mode == 'z'
        xyz_rot = [x_rot, y_rot, angle]

    runSimCmd(model_name=model_name, conf_num=conf_num,
        ip_addr='127.0.0.1', ip_port=port_list[idx],
        x_start=x_start, x_end=x_end, x_delta=x_delta,
        y_start=y_start, y_end=y_end, y_delta=y_delta,
        xyz_rot=xyz_rot,
        depth=downward_depth, precision=downward_precision,
        output_name=output_name
        )