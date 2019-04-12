# V-rep based ARIE Visualization
ARIE visualization package based on v-rep simulation environment.

##### Description:

The simulation is used to visualize the 3D attractive region in environment in part-mating tasks. The simulation depends on V-Rep, a light-weight robot simulation environment. Using its collision detection and remote API, the contact state between the objects to be mated are extracted. 

Matlab or Python is used as the scripting language to write simulation logic, and communicates with V-Rep through TCP protocol.



## How to use

1. Install V-REP (>=3.4.0);
2. Install Python (>=3.5);
3. Clone this repository `https://github.com/raysworld/ARIE-vrep-simulation`;
4. Run `/vrep_files/run_vrep.ps1` to launch the server. Each instance corresponds to a simulation. You may access different simulations via different port numbers.
5. Run `/python_files/run_sim.bat` to start the simulation



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

