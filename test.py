# example case


from AVL_combined_cases.AVL_automation_V2 import AVLsolver,AVLgeometry,AVLruncase,AVLmass,data
import numpy as np
from numpy.typing import NDArray
import os 
import matplotlib.pyplot as plt 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import AVL_combined_cases.paths
from AVL_combined_cases.paths import pathing

from  AVL_dataclasses.AVL_geometry_file_dataclass import GeometryFileData 
from AVL_dataclasses.AVL_mass_file_dataclass import MassFileData
from AVL_dataclasses.AVL_runcase_dataclass import RunCaseFileData
from AVL_dataclasses.AVL_general_use_dataclasses import Aircraft,batch_data

from AVL_file_generation.AVL_geometry_generation import geometry_gen
from AVL_file_generation.AVL_mass_generation import mass_gen
from AVL_file_generation.AVL_runcase_generation import runcase_gen

from AVL_data_final.AVL_geom_data_final import geometry_data_func
from AVL_data_final.AVL_mass_data_final import mass_data_func
from AVL_data_final.AVL_runcase_data_final import runcase_data_func

from AVL_solver_processes.AVL_stability_derivation import stability_derivation 
from AVL_solver_processes.AVL_surface_forces_derivation_V2 import surface_forces_main
from AVL_solver_processes.AVL_total_forces_derivation_V2 import total_forces_main
from AVL_solver_processes.AVL_strip_data_management import strip_data_main
from AVL_solver_processes.AVL_viscous_V2 import viscous_main


"""
Example aircraft 
"""

aircraft=data(geometry_data=geometry_data_func(), mass_data=mass_data_func(),runcase_data=runcase_data_func()).aircraft_init() # Initiate the type Aircraft object 
Output_path=pathing(geometry_data_func().aircraft_name)   # create the output path. This is the folder where all created files will be stored.

# create the .avl geometry file 
test_geom_file,test_geom_path=AVLgeometry(output_path=Output_path,uav_id=aircraft.geometry_data.aircraft_name,main_wing=aircraft.geometry_data.main_wing_dict(),h_tail=aircraft.geometry_data.h_tail_dict(), v_tail=aircraft.geometry_data.v_tail_dict()).geometry_generation()
print (f"Geometry file  was created at : {test_geom_path}")

# create the .mass file 
test_mass_file,test_mass_path=AVLmass(output_path=Output_path,uav_id=aircraft.mass_data.aircraft_name,main_wing_mass=aircraft.mass_data.main_wing_mass_dict(),fuselage_mass=aircraft.mass_data.fuselage_mass_dict(),h_tail_mass=aircraft.mass_data.h_tail_mass_dict(),
                            v_tail_mass=aircraft.mass_data.v_tail_mass_dict(),sporia_mass=aircraft.mass_data.sporia_mass_dict()).mass_generation()
print (f"Mass file  was created at : {test_mass_path}")

#create the .run file
test_runcase_file,test_runcase_path=AVLruncase(output_path=Output_path,uav_id=aircraft.runcase_data.aircraft_name,flight_conditions=aircraft.runcase_data.runcase_dict()).runcase_file_generation()
print(f"Runcase file was created at : {test_runcase_path} ")

#initiate the AVLSolver class 
avl_cracked=AVLsolver(
        uav_id=aircraft.geometry_data.aircraft_name,
        xfoil_exe_path=AVL_combined_cases.paths.xfoil_exe_path,
        avl_exe_path=AVL_combined_cases.paths.AVL_exe_path,
        avl_path=AVL_combined_cases.paths.AVL_path,
        output_path=Output_path,
        geometry_file=test_geom_path,
        mass_file=test_mass_path,
        runcase_file=test_runcase_path,
        velocity = 25,     # make sure each constant parameter is called from an external file.,
        cref=aircraft.geometry_data.Cref
        )

analysis_file_path=os.path.join(Output_path,f"{aircraft.geometry_data.aircraft_name}_analysis.txt") # file with stability related values and more 
stability_derivs=avl_cracked.stability_derivatives()         # STABILITY DERIVATIVES 
wing_batch=avl_cracked.surface(np.arange(0,9,1),'Main Wing',batched_data=batch_data()) # wing batch
tail_batch=avl_cracked.surface(np.arange(0,9,1),'Horizontal Tail',batched_data=wing_batch)  # horizontal tail batch
aircraft_batch=avl_cracked.total(np.arange(0,9,1),batched_data=tail_batch) # total aircraft batch 
wing=avl_cracked.strips('Main Wing')  # strip data processes for main wing 
tail=avl_cracked.strips('Horizontal tail') # strip data processes for horizontal tail 
wing,tail=avl_cracked.viscous(wing,tail)  # viscous drag computations for both main wing and horizontal tail 


# FINAL AIRCRAFT OBJECT HAS INHERITED ALL THE VALUABLE COMPUTED DATA
aircraft=Aircraft(main_wing_data=wing,horizontal_tail_data=tail,batched_data=aircraft_batch,stability_data=stability_derivs) # update the aircraft object that was created in line 38
print(type(aircraft))

