## 文件说明

```peg_tri_r_200_h_801.stl```

半径为20的圆的内接正五边形柱体，长度80

```hol_tri_r_201_h_901.stl```

外部为边长为200的正方形，内部为半径为20.1的圆的内接正五边形，长度为90

```\Cero_sourcefile```

该文件夹下为使用CERO绘制的零件源文件，上述.stl文件为导出文件



## vrep脚本初始化参数

```lua
obj_hol_init_pos = [0, 0, 0.046]
vrep.simxSetObjectPosition(clientID, h_hole, -1, obj_hol_init_pos, vrep.simx_opmode_blocking)

obj_peg_init_pos = [0, 0.005, 20e-2]
obj_peg_init_ore = [np.deg2rad(0), np.deg2rad(0), np.deg2rad(-90)]
vrep.simxSetObjectOrientation(clientID, h_peg, -1, obj_peg_init_ore, vrep.simx_opmode_blocking)
vrep.simxSetObjectPosition(clientID, h_peg, -1, obj_peg_init_pos, vrep.simx_opmode_blocking)

obj_peg_init_ore = [np.deg2rad(0), np.deg2rad(15), np.deg2rad(0)]
if (obj_peg_init_ore[0] != 0.0) and (obj_peg_init_ore[1] != 0.0):
    print ('peg-ore-x and peg-ore-y cannot be specified together. peg-ore-y will be omitted.')
    obj_peg_init_ore[1] = 0.0
vrep.simxSetObjectOrientation(clientID, h_peg, h_peg, obj_peg_init_ore, vrep.simx_opmode_blocking)
```





