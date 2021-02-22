## 文件夹介绍

**matlab**：已弃用

**models**：仿真轴孔模型

./xxx_peg_hole文件夹中存放轴和孔的stl格式三维模型

./models.json中描述每个文件夹中存放轴和孔的详细信息，如

```json
"dual_round_peg_hole": {
    "peg": {
      "file_path": "models/dual_rnd_peg_hole/dual_peg.stl",
      "config": [
        {
          "description": "insert by edge",
          "init_pos": [0,0,0.16],
          "init_ore": [0,0,0]
        },
        {
          "description": "insert by corner",
          "init_pos": [0,0,0.16],
          "init_ore": [0,0,0]
        }
      ]
    },
    "hole": {
      "file_path": "models/dual_rnd_peg_hole/dual_hole.stl",
      "config": [
        {
          "description": "insert by edge",
          "init_pos": [0,0,0.047],
          "init_ore": [0,0,0]
        },
        {
          "description": "insert by corner",
          "init_pos": [0,0,0.047],
          "init_ore": [0,0,0]
        }
      ]
    },
    "description_file_path": "models/dual_rnd_peg_hole/model_readme.md"
  },
```
"dual_round_peg_hole"指定了在python脚本中调用时该模型的名称。"peg"字段中指定了三维模型的相对文件路径（"file_path"），在按照边装配（"insert by edge"）和按照角装配（"insert by corner"）过程中的轴/孔初始位置和姿态，以及针对改组轴孔的说明文件相对路径（"description_file_path"，可不提供）
**python**：仿真API接口、后处理脚本等

./legacy 已弃用脚本暂存

./vrep.py | ./vrepConst.py | ./remoteAPI.dll VREP官方提供的Python API接口，兼容新版本CoppeliaSim

./sim_manager.py 仿真过程所需调用的API

./sim_plot_ph.py 仿真轴孔状态可视化脚本

./run_sim.py 仿真轴孔过程脚本

./post_process.py 对仿真数据进行后处理脚本

**results**：仿真输出的数据文件存放目录

**simulation：**仿真配置文件和实际仿真过程执行脚本目录

./config 存放每次仿真过程的参数配置文件

./rrec.py 以输出仿真数据为目的的可执行仿真脚本文件（调用run_sim.py）

./rrec_plot_ph.py 以可视化轴孔状态为目的的可执行仿真脚本文件（调用sim_plot_ph.py）

**vrep**：存放仿真场景ttt文件

./legacy 已弃用文件暂存

./RemoteApi_ARIE_Assembly.ttt VREP仿真场景文件，仿真过程中需要被启动

./remoteApi.lua ttt仿真场景文件中的脚本，提供仿真API

## 仿真流程

![图片](https://uploader.shimo.im/f/oTI90jDWXrkE6Vrd.png!thumbnail?fileGuid=88X9wcP6yKC3gcxR)

如图所示，CoppeliaSim（V-REP）开启ttt仿真环境，通过SimManager加载仿真过程中的轴孔零件，并通过不同的脚本文件控制仿真流程，或是展示轴孔可视化状态

