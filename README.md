# V-rep based ARIE Visualization
<p>
    <a href="https://github.com/raysrobotics/ARIE-matlab-rprh/blob/master/LICENSE"><img alt="Software License" src="https://img.shields.io/badge/license-CASIA-blue.svg"></a>
    <a><img alt="Python Version" src="https://img.shields.io/badge/python-3.7-yellow.svg"></a>
    <a><img alt="CoppeliaSim Version" src="https://img.shields.io/badge/CoppeliaSim-4.1.0-yellow.svg"></a>
</p>


ARIE visualization package based on v-rep simulation environment.

##### Description:

The simulation is used to visualize the 3D attractive region in environment in part-mating tasks. The simulation depends on V-Rep, a light-weight robot simulation environment. Using its collision detection and remote API, the contact state between the objects to be mated are extracted. 

Matlab or Python is used as the scripting language to write simulation logic, and communicates with V-Rep through TCP protocol.



## How to use

1. Install CoppeliaSim (>=4.1.0);
2. Install Python (>=3.7);
3. Clone this repository `https://github.com/raysworld/ARIE-vrep-simulation`;
4. Navigate to `simulation` folder, follow the example of `./config/rrec.yaml` to write a simulation configure file.
5. Follow `rrec.py` to write a simulation script.
6. Run the script:
   ```shell
   python ./rrec.py
   ```

## Cite

If you use this toolbox in your research please cite it:

```
@article{rui2017,
   author = {Li, Rui and Qiao, Hong},
   title = {Condition and Strategy Analysis for Assembly Based on Attractive Region in Environment},
   journal = {IEEE/ASME Transactions on Mechatronics},
   volume = {22},
   number = {5},
   pages = {2218-2228},
   ISSN = {1083-4435},
   DOI = {10.1109/TMECH.2017.2705180},
   year = {2017}
}

```

