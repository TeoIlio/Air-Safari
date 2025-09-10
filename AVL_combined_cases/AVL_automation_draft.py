#AVL automation



import numpy as np
import os 
import subprocess
import matplotlib.pyplot as plt 
from dataclasses import dataclass
import math 
import paths
import sys
sys.path.append(paths.sys_path)
import re

from AVL_templates.AVL_geom_template import uav_geometry 
from  AVL_templates.AVL_mass_template import uav_mass_properties 
from  AVL_templates.AVL_RunCase_template import uav_runcase
from AVL_solver_processes.AVL_surface_forces_derivation import FN_batch_and_plots
from AVL_solver_processes.AVL_stability_derivation import stability_derivation 
from AVL_solver_processes.AVL_total_forces_derivation import total_forces_batch_and_plots
from  AVL_dataclasses.AVL_geometry_file_dataclass import GeometryFileData 
from AVL_dataclasses.AVL_mass_file_dataclass import MassFileData
from AVL_dataclasses.AVL_runcase_dataclass import RunCaseFileData
from AVL_file_generation.AVL_geometry_generation import geometry_gen
from AVL_file_generation.AVL_mass_generation import mass_gen
from AVL_file_generation.AVL_runcase_generation import runcase_gen
from AVL_data_final.AVL_geom_data_final import geometry_data_func
from AVL_data_final.AVL_mass_data_final import mass_data_func
from AVL_data_final.AVL_runcase_data_final import runcase_data_func
from AVL_solver_processes.AVL_lift_distribution import lift_distribution_derivation 
from AVL_solver_processes.AVL_lift_distribution import lift_dist_plots


#-------------------

class GeometryFileData(GeometryFileData): 
      pass
        

class MassFileData(MassFileData):
    pass
   

class RunCaseFileData(RunCaseFileData):  
   pass
 
         

class AVLgeometry: 

    """
     A class for the generation of geometry files based on the geometry template created externally.
    """
    def __init__(self,output_path,uav_id,main_wing: dict,h_tail: dict, v_tail: dict):
     
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
    Surface forces full: Run avl and extract aerodynamic forces for the specified surface (i.e horizontal tail,main wing).
    Total forces full :Run avl and exctract aerodynamic forces for the whole aircraft geometry.
    """
      
    def __init__(self,uav_id:str,avl_exe_path, avl_path,output_path, geometry_file: str, mass_file: str, runcase_file: str, velocity : float,cref : float):
        self.avl_exe_path= avl_exe_path
        self.uav_id=uav_id
        self.avl_path = avl_path
        self.output_path= output_path
        self.geometry_file = geometry_file
        self.mass_file = mass_file
        self.runcase_file = runcase_file
        self.velocity = velocity 
        self.cref=cref


    def stability_derivatives(self):
        output,error,stability_derivs_list=stability_derivation(self)
        return output,error,stability_derivs_list


    def surface_forces_full(self,AoA_range : np.ndarray,surface :str,plots : bool):
 
        CL_list,CD_list,CDi_list=FN_batch_and_plots(self,AoA_range,surface,plots)
        return CL_list,CD_list,CDi_list
    
    def total_forces_full(self,AoA_range : np.ndarray,plots : bool):

        CL_list_total,CD_list_total = total_forces_batch_and_plots(self,AoA_range,plots)
        return CL_list_total,CD_list_total
    
    def lift_distribution_full(self,surface: str,plots:bool):

        list_r,list_l=lift_distribution_derivation(self,surface)
        plot=lift_dist_plots(self,list_r,list_l,plots)
        return list_r,list_l,plot

     
                  
#--------------------------------------------------------------------------------------------
#example case

# Example geometry values (fill in with actual numbers/strings)
geometry_data = geometry_data_func()

# Example mass values (again, use real data)
mass_data = mass_data_func()

#example runcase values 
runcase_data=runcase_data_func()


if __name__ == "__main__":
 

    test_geom_file,test_geom_path=AVLgeometry(output_path=paths.Output_path,uav_id=geometry_data.aircraft_name,main_wing=geometry_data.main_wing_dict(),h_tail=geometry_data.h_tail_dict(), v_tail=geometry_data.v_tail_dict()).geometry_generation()
    print (f"Geometry file  was created at : {test_geom_path}")

    test_mass_file,test_mass_path=AVLmass(output_path=paths.Output_path,uav_id=mass_data.aircraft_name,main_wing_mass=mass_data.main_wing_mass_dict(),fuselage_mass=mass_data.fuselage_mass_dict(),h_tail_mass=mass_data.h_tail_mass_dict(),
                            v_tail_mass=mass_data.v_tail_mass_dict(),sporia_mass=mass_data.sporia_mass_dict()).mass_generation()
    print (f"Mass file  was created at : {test_mass_path}")

    test_runcase_file,test_runcase_path=AVLruncase(output_path=paths.Output_path,uav_id=runcase_data.aircraft_name,flight_conditions=runcase_data.runcase_dict()).runcase_file_generation()
    print(f"Runcase file was created at : {test_runcase_path} ")
  

    avl_cracked=AVLsolver(
        uav_id=geometry_data.aircraft_name,
        avl_exe_path=paths.AVL_exe_path,
        avl_path=paths.AVL_path,
        output_path=paths.Output_path,
        xfoil_exe_path=paths.xfoil_exe_path,
        geometry_file=test_geom_path,
        mass_file=test_mass_path,
        runcase_file=test_runcase_path,
        velocity = 25,     # make sure each constant parameter is called from an external file.
        cref=geometry_data.Cref
        )
    
    analysis_file_path=os.path.join(paths.Output_path,f"{geometry_data.aircraft_name}_analysis.txt")
    output,error,derivs=avl_cracked.stability_derivatives()         # STABILITY DERIVATIVES
    if os.path.exists(analysis_file_path):
      print(f"Analysis txt file was created  at : {analysis_file_path} ")
     # print("stdout is :",output) 
     
    CL,CD,CDi=avl_cracked.surface_forces_full(np.arange(0,3,1),'horizontal_tail',False)     #SURFACE FORCES COEFFS
    CLtotal,CDtotal=avl_cracked.total_forces_full(np.arange(0,3,1),True)  # total forces coeffs
    clll=avl_cracked.lift_distribution_full('main_wing',True)  #lift distribution 

#print(type(avl))