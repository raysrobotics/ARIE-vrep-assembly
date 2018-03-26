@echo off

start python run_sim.py "D:/Projects/3D models/simbody_test/tri_peg_hole/peg_tri_r_200_h_801.stl" "D:/Projects/3D models/simbody_test/tri_peg_hole/hol_tri_r_201_h_901.stl" 0.0 10.0 0.0 --ip-addr "127.0.0.1" --port 19997 --precision-x 5e-4 --precision-y 5e-4 --plot --x-start -0.04 --x-end 0.04 --y-start -0.04 --y-end 0.04

start python run_sim.py "D:/Projects/3D models/simbody_test/tri_peg_hole/peg_tri_r_200_h_801.stl" "D:/Projects/3D models/simbody_test/tri_peg_hole/hol_tri_r_201_h_901.stl" 0.0 10.0 5.0 --ip-addr "127.0.0.1" --port 19998 --precision-x 5e-4 --precision-y 5e-4 --plot --x-start -0.04 --x-end 0.04 --y-start -0.04 --y-end 0.04

start python run_sim.py "D:/Projects/3D models/simbody_test/tri_peg_hole/peg_tri_r_200_h_801.stl" "D:/Projects/3D models/simbody_test/tri_peg_hole/hol_tri_r_201_h_901.stl" 0.0 10.0 10.0 --ip-addr "127.0.0.1" --port 19999 --precision-x 5e-4 --precision-y 5e-4 --plot --x-start -0.04 --x-end 0.04 --y-start -0.04 --y-end 0.04

start python run_sim.py "D:/Projects/3D models/simbody_test/tri_peg_hole/peg_tri_r_200_h_801.stl" "D:/Projects/3D models/simbody_test/tri_peg_hole/hol_tri_r_201_h_901.stl" 0.0 10.0 15.0 --ip-addr "127.0.0.1" --port 20000 --precision-x 5e-4 --precision-y 5e-4 --plot --x-start -0.04 --x-end 0.04 --y-start -0.04 --y-end 0.04