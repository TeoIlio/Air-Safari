

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

class data:
  
    def __init__(self,geometry_data : GeometryFileData, mass_data: MassFileData, runcase_data :RunCaseFileData):
           self.geometry_data=geometry_data
           self.mass_data=mass_data
           self.runcase_data=runcase_data
    
    def aircraft_init(self):
       return Aircraft(uav_id=self.geometry_data.aircraft_name,geometry_data=self.geometry_data,mass_data=self.mass_data,runcase_data=self.runcase_data)


class AVLgeometry: 

    """
     A class for the generation of geometry files based on the geometry template created externally.
    """
    def __init__(self,output_path,uav_id : str, main_wing: dict,h_tail: dict, v_tail: dict):
     
        self.output_path= output_path
        self.uav_id=uav_id
        self.main_wing=main_wing
        self.h_tail=h_tail
        self.v_tail=v_tail

    #geometry file generation/geometry creation 
    def geometry_generation(self):   
        geometry_gen(self)
       
        return self.geometry_file,self.geom_file_path

class AVLmass:
    """
      A class for the generation of mass files based on the mass template created externally.
    """
    def __init__(self,output_path,uav_id: str,main_wing_mass: dict, fuselage_mass: dict, h_tail_mass: dict, v_tail_mass: dict, sporia_mass: dict):
        self.output_path= output_path
        self.uav_id=uav_id
        self.main_wing_mass=main_wing_mass
        self.fuselage_mass=fuselage_mass
        self.h_tail_mass=h_tail_mass
        self.v_tail_mass=v_tail_mass
        self.sporia_mass=sporia_mass

           # mass file generation 
    def mass_generation(self):
        mass_gen(self)
          
        return self.mass_file,self.mass_file_path

class AVLruncase:  

    """
    A class for the generation of runcase files based on the runcase template created externally.
    """

    def __init__(self,output_path,uav_id: str,flight_conditions: dict):
        self.output_path= output_path
        self.uav_id=uav_id
        self.flight_conditions=flight_conditions
  
    def runcase_file_generation(self):
        runcase_gen(self)
        return self.runcase_file, self.runcase_file_path    

class AVLsolver:
    """
    Solver: will contain all processes regarding sequences etc...
    Stability derivatives: Run avl and execute a specified analysis. Exctract the results in a txt file. From this file ,derive only the required values.
    Surface forces : Run avl and extract aerodynamic forces for the specified surface (i.e horizontal tail,main wing).
    Total forces  :Run avl and exctract aerodynamic forces for the whole aircraft geometry.
    """
      
    def __init__(self,uav_id:str,avl_exe_path, avl_path, xfoil_exe_path,output_path, geometry_file: str, mass_file: str, runcase_file: str, velocity : float,cref: float):
        self.avl_exe_path= avl_exe_path
        self.xfoil_exe_path=xfoil_exe_path
        self.uav_id=uav_id
        self.avl_path = avl_path
        self.output_path= output_path
        self.geometry_file = geometry_file
        self.mass_file = mass_file
        self.runcase_file = runcase_file
        self.velocity = velocity 
        self.cref = cref


    def stability_derivatives(self):
        stability_derivs=stability_derivation(self)

        return stability_derivs 

    
    def surface(self,AoA_range : np.ndarray,surface :str, batched_data : batch_data):
        surface_batch=surface_forces_main(self,AoA_range=AoA_range,surface=surface,batched_data=batched_data)
        
        return batched_data
    
 
    
    def total(self,AoA_range : NDArray[np.float64], batched_data: batch_data):
        aircraft_batch=total_forces_main(self,AoA_range=AoA_range ,batched_data=batched_data)
        
        
        return batched_data
             
    def strips(self,surface: str):
        surface_type=strip_data_main(self,surface)

        return surface_type    
    
    def viscous(self,main_wing,horizontal_tail):
        
        main_wing,horizontal_tail=viscous_main(self,main_wing,horizontal_tail)

        return main_wing, horizontal_tail
    
#example case

aircraft=data(geometry_data=geometry_data_func(), mass_data=mass_data_func(),runcase_data=runcase_data_func()).aircraft_init()
Output_path=pathing(geometry_data_func().aircraft_name)

test_geom_file,test_geom_path=AVLgeometry(output_path=Output_path,uav_id=aircraft.geometry_data.aircraft_name,main_wing=aircraft.geometry_data.main_wing_dict(),h_tail=aircraft.geometry_data.h_tail_dict(), v_tail=aircraft.geometry_data.v_tail_dict()).geometry_generation()
print (f"Geometry file  was created at : {test_geom_path}")


test_mass_file,test_mass_path=AVLmass(output_path=Output_path,uav_id=aircraft.mass_data.aircraft_name,main_wing_mass=aircraft.mass_data.main_wing_mass_dict(),fuselage_mass=aircraft.mass_data.fuselage_mass_dict(),h_tail_mass=aircraft.mass_data.h_tail_mass_dict(),
                            v_tail_mass=aircraft.mass_data.v_tail_mass_dict(),sporia_mass=aircraft.mass_data.sporia_mass_dict()).mass_generation()
print (f"Mass file  was created at : {test_mass_path}")

test_runcase_file,test_runcase_path=AVLruncase(output_path=Output_path,uav_id=aircraft.runcase_data.aircraft_name,flight_conditions=aircraft.runcase_data.runcase_dict()).runcase_file_generation()
print(f"Runcase file was created at : {test_runcase_path} ")

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

analysis_file_path=os.path.join(Output_path,f"{aircraft.geometry_data.aircraft_name}_analysis.txt")
stability_derivs=avl_cracked.stability_derivatives()         # STABILITY DERIVATIVES
wing_batch=avl_cracked.surface(np.arange(0,9,1),'Main Wing',batched_data=batch_data()) # wing batch
tail_batch=avl_cracked.surface(np.arange(0,9,1),'Horizontal Tail',batched_data=wing_batch)  # horizontal tail batch
aircraft_batch=avl_cracked.total(np.arange(0,9,1),batched_data=tail_batch) # total aircraft batch 
wing=avl_cracked.strips('Main Wing')  # strip data processes for main wing 
tail=avl_cracked.strips('Horizontal tail') # strip data processes for horizontal tail 
wing,tail=avl_cracked.viscous(wing,tail)  # viscous drag computations for both main wing and horizontal tail 


# FINAL AIRCRAFT OBJECT HAS INHERITED ALL THE VALUABLE COMPUTED DATA
aircraft=Aircraft(main_wing_data=wing,horizontal_tail_data=tail,batched_data=aircraft_batch,stability_data=stability_derivs)
print(type(aircraft))


