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

#-------------------
@dataclass
class GeometryFileData:
     
     aircraft_name: str

     #Main wing
     Sref: float
     Cref: float
     Bref: float
     Wing_incidence_angle: float 
     Wing_halfspan: float
     Wing_sweep: float 
     Wing_dih: float
     Wing_root_twist: float
     Wing_root_chord: float
     Wing_tip_twist: float
     Wing_taper: float
     Wing_airfoil: str

     #horizontal tail 
     X_pos_Htail: float
     Z_pos_Htail: float
     Htail_incidence_angle: float
     Htail_halfspan: float
     Htail_airfoil: str
     Htail_sweep: float
     Htail_root_twist: float
     Htail_root_chord: float
     Htail_tip_twist: float
     Htail_taper: float
     
     #vertical tail 
     X_pos_Vtail: float
     Vtail_sweep: float
     Vtail_root_chord: float
     Vtail_taper: float
     Vtail_span: float
     Vtail_airfoil: str

     def as_dict_main_wing(self)->dict : 
         """
         This function maps the keys(geometry template properties concerning main wing) to values.
         """
         return {'Sref': self.Sref, 'Bref':self.Bref, 'Cref':self.Cref, 'Wing_incidence_angle':self.Wing_incidence_angle,
                 'Wing_halfspan': self.Wing_halfspan, 'Wing_sweeped':math.tan(math.radians(self.Wing_sweep)) * (self.Wing_halfspan), 'Wing_dih': self.Wing_dih,
                 'Wing_root_twist': self.Wing_root_twist,'Wing_root_chord': self.Wing_root_chord, 'Wing_tip_twist': self.Wing_tip_twist,
                 'Wing_tip_chord':(self.Wing_taper)*self.Wing_root_chord, 'Wing_airfoil': self.Wing_airfoil
                 }
     
     def as_dict_h_tail(self)->dict : 
         """
         This function maps the keys(geometry template properties concenring horizontal tail) to values.
         """
         return {'X_pos_Htail': self.X_pos_Htail, 'Z_pos_Htail': self.Z_pos_Htail, 'Htail_incidence_angle': self.Htail_incidence_angle,
                 'Htail_halfspan':self.Htail_halfspan, 'Htail_airfoil':self.Htail_airfoil, 'Htail_sweeped':math.tan(math.radians(self.Htail_sweep)) * (self.Htail_halfspan),
                 'Htail_root_twist': self.Htail_root_twist, 'Htail_root_chord': self.Htail_root_chord, 'Htail_tip_twist': self.Htail_tip_twist,
                 'Htail_tip_chord': self.Htail_taper * self.Htail_root_chord
                 }

     def as_dict_v_tail(self)->dict : 
         """
         This function maps the keys(geometry template properties concerning vertical tail ) to values.
         """
         return {'X_pos_Vtail': self.X_pos_Vtail, 'Vtail_sweeped': math.tan(math.radians(self.Vtail_sweep)) * (self.Vtail_span),
                  'Vtail_root_chord': self.Vtail_root_chord,'Vtail_tip_chord':self.Vtail_taper * self.Vtail_root_chord, 
                  'Vtail_span': self.Vtail_span, 'Vtail_airfoil': self.Vtail_airfoil
                 }          

@dataclass
class MassFileData:
    aircraft_name: str

    #Main wing mass properties 
    right_wing_mass: float
    right_wing_Xcg: float
    right_wing_Ycg: float
    right_wing_Zcg: float
    Ixx_right_wing: float
    Iyy_right_wing: float
    Izz_right_wing: float

    #Fuselage mass properties 
    fuselage_mass: float
    fuselage_Xcg: float
    fuselage_Ycg: float
    fuselage_Zcg: float
    Ixx_fuselage: float
    Iyy_fuselage: float
    Izz_fuselage: float
   
    #Horizontal tail mass properties 
    right_Hwing_mass: float
    right_Hwing_Xcg: float
    right_Hwing_Ycg: float
    right_Hwing_Zcg: float
    Ixx_right_Hwing: float
    Iyy_right_Hwing: float
    Izz_right_Hwing: float

    #Vertical tail mass properties 
    Vtail_mass: float
    Vtail_Xcg: float
    Vtail_Ycg: float
    Vtail_Zcg: float
    Ixx_Vtail:float
    Iyy_Vtail: float 
    Izz_Vtail: float

    #Sporia mass properties 
    payload_mass: float
    payload_Xcg: float
    payload_Ycg: float
    payload_Zcg: float
    Ixx_payload:float
    Iyy_payload: float 
    Izz_payload: float
    battery_mass: float
    battery_Xcg: float
    battery_Ycg: float
    battery_Zcg: float

    def as_dict_main_wing_mass(self) ->dict:
         """
         This function maps the keys(mass template properties concenring main wing ) to values.
         """
         return {'right_wing_mass': self.right_wing_mass , 'right_wing_Xcg':self.right_wing_Xcg,'right_wing_Ycg':self.right_wing_Ycg,'right_wing_Zcg':self.right_wing_Zcg,
                 'Ixx_right_wing':self.Ixx_right_wing, 'Iyy_right_wing':self.Iyy_right_wing,'Izz_right_wing':self.Izz_right_wing 
                }
    
    def as_dict_fuselage_mass(self) ->dict:
         """
         This function maps the keys(mass template properties concenring fuselage ) to values.
         """
         return {'fuselage_mass': self.fuselage_mass , 'fuselage_Xcg':self.fuselage_Xcg,'fuselage_Ycg':self.fuselage_Ycg,'fuselage_Zcg':self.fuselage_Zcg,
                 'Ixx_fuselage':self.Ixx_fuselage, 'Iyy_fuselage':self.Iyy_fuselage,'Izz_fuselage':self.Izz_fuselage
                }

    def as_dict_h_tail_mass(self) ->dict:
         """
         This function maps the keys(mass template properties concenring horizontal tail ) to values.
         """
         return {'right_Hwing_mass': self.right_Hwing_mass , 'right_Hwing_Xcg':self.right_Hwing_Xcg,'right_Hwing_Ycg':self.right_Hwing_Ycg,'right_Hwing_Zcg':self.right_Hwing_Zcg,
                 'Ixx_right_Hwing':self.Ixx_right_Hwing, 'Iyy_right_Hwing':self.Iyy_right_Hwing,'Izz_right_Hwing':self.Izz_right_Hwing
                }
    
    def as_dict_v_tail_mass(self) ->dict:
         """
         This function maps the keys(mass template properties concenring main wing ) to values.
         """
         return {'Vtail_mass': self.Vtail_mass , 'Vtail_Xcg':self.Vtail_Xcg,'Vtail_Ycg':self.Vtail_Ycg,'Vtail_Zcg':self.Vtail_Zcg,
                 'Ixx_Vtail':self.Ixx_Vtail, 'Iyy_Vtail':self.Iyy_Vtail,'Izz_Vtail':self.Izz_Vtail 
                }
    
    def as_dict_sporia_mass(self) ->dict:
         """
         This function maps the keys(mass template properties concenring the remaining components ) to values.
         """
         return {'payload_mass': self.payload_mass , 'payload_Xcg':self.payload_Xcg,'payload_Ycg':self.payload_Ycg,'payload_Zcg':self.payload_Zcg,
                 'Ixx_payload':self.Ixx_payload, 'Iyy_payload':self.Iyy_payload,'Izz_payload':self.Izz_payload,
                 'battery_mass': self.battery_mass , 'battery_Xcg':self.battery_Xcg,'battery_Ycg':self.battery_Ycg,'battery_Zcg':self.battery_Zcg,
                }

@dataclass
class RunCaseFileData: 

    # Flight conditions 
    aircraft_name: str
    runcase_number: float
    runcase_name: str
    AoA: float
    sideslip: float 
    roll_rate: float
    pitch_rate: float
    yaw_rate: float
    elevator_def: float
    rudder_def: float
    flap_def: float
    aileron_def: float
    bank_angle: float
    climb_angle: float
    heading_angle: float
    velocity: float
    density: float

    def as_dict_flight_conditions(self) ->dict:
         """
         This function maps the keys(runcase template properties concenring the flight conditions ) to values.
         """
         return {'runcase_number': self.runcase_number , 'runcase_name':self.runcase_name,'AoA':self.AoA,'sideslip':self.sideslip,
                 'roll_rate':self.roll_rate, 'pitch_rate':self.pitch_rate,'yaw_rate':self.yaw_rate,
                 'elevator_def': self.elevator_def , 'rudder_def':self.rudder_def,'flap_def':self.flap_def,'aileron_def':self.aileron_def,
                 'bank_angle': self.bank_angle, 'climb_angle': self.climb_angle, 'heading_angle':self.heading_angle, 'velocity':self.velocity,
                 'density': self.density
                 }


class AVLgeometry: 

    """
     A class for the generation of geometry files based on the runcase template created externally.
    """
    def __init__(self,output_path,uav_id,main_wing: dict,h_tail: dict, v_tail: dict):
     
        self.output_path= output_path
        self.uav_id=uav_id
        self.main_wing=main_wing
        self.h_tail=h_tail
        self.v_tail=v_tail

    #geometry file generation/geometry creation 
    def geometry_gen(self):   
        self.geometry_file=uav_geometry(self.uav_id,self.main_wing,self.h_tail,self.v_tail)
        
      
         
        geom_file_path =os.path.join(self.output_path,f"{self.uav_id}.avl")  
        with open(geom_file_path,"w") as f: 
             f.write(self.geometry_file)
        
       
        return self.geometry_file,geom_file_path


class AVLmass:
    """
      A class for the generation of mass files based on the runcase template created externally.
    """
    def __init__(self,output_path,uav_id: str,main_wing_mass: dict, fuselage_mass: dict, h_tail_mass: dict, v_tail_mass: dict, sporia_mass: dict):
        self.output_path= output_path
        self.uav_id=uav_id
        self.main_wing_mass=main_wing_mass
        self.fuselage_mas=fuselage_mass
        self.h_tail_mass=h_tail_mass
        self.v_tail_mass=v_tail_mass
        self.sporia_mass=sporia_mass


   # mass file generation 
    def mass_file_gen(self):
        self.mass_file=uav_mass_properties(self.uav_id,self.main_wing_mass,self.fuselage_mas,self.h_tail_mass,self.v_tail_mass,self.sporia_mass)
          
        
        mass_file_path=os.path.join(self.output_path,f"{self.uav_id}.mass")   # error, needs change in the file pathing
        with open(mass_file_path, "w") as f: 
             f.write(self.mass_file)
        
          
        return self.mass_file,mass_file_path
    
class AVLruncase:  

    """
    A class for the generation of runcase files based on the runcase template created externally.
    """

    def __init__(self,output_path,uav_id: str,flight_conditions: dict):
        self.output_path= output_path
        self.uav_id=uav_id
        self.flight_conditions=flight_conditions
  
    def runcase_file_gen(self):
        self.runcase_file=uav_runcase(self.uav_id,self.flight_conditions)
       
        runcase_file_path=os.path.join(self.output_path,f"{self.uav_id}.RUN")
        with open(runcase_file_path,"w") as f:
             f.write(self.runcase_file)

        return self.runcase_file, runcase_file_path    

        
class AVLsolver:
    """
    Solver: will contain all processes regarding sequences etc...
    Stability derivatives: Run avl and execute a specified analysis. Exctract the results in a txt file. From this file ,derive only the required values.
    """
      
    def __init__(self,uav_id:str,avl_exe_path, avl_path,output_path, geometry_file: str, mass_file: str, runcase_file: str):
        self.avl_exe_path= avl_exe_path
        self.uav_id=uav_id
        self.avl_path = avl_path
        self.output_path= output_path
        self.geometry_file = geometry_file
        self.mass_file = mass_file
        self.runcase_file = runcase_file


    def stability_derivatives(self):
        output,error,stability_derivs_list=stability_derivation(self)
        return output,error,stability_derivs_list


    def surface_forces_full(self,velocity,AoA_range : np.ndarray,surface :str,plots : bool):
 
        CL_list,CD_list,CDi_list=FN_batch_and_plots(self,velocity,AoA_range,surface,plots)
        return CL_list,CD_list,CDi_list
    
    def total_forces_full(self,velocity,AoA_range : np.ndarray,plots : bool):

        CL_list_total,CD_list_total = total_forces_batch_and_plots(self,velocity,AoA_range,plots)
        return CL_list_total,CD_list_total

     
              
#--------------------------------------------------------------------------------------------
#example case


# Example geometry values (fill in with actual numbers/strings)
geom_data = GeometryFileData(
    aircraft_name="Golf",
    Sref=1.5,
    Cref=0.25,
    Bref=1.2,
    Wing_incidence_angle=2.0,
    Wing_halfspan=0.6,
    Wing_sweep=20.0,
    Wing_dih=0.0,
    Wing_root_twist=0.0,
    Wing_root_chord=0.3,
    Wing_tip_twist=-2.0,
    Wing_taper=0.5,
    Wing_airfoil="naca6412",
    X_pos_Htail=1.5,
    Z_pos_Htail=0.0,
    Htail_incidence_angle=0.0,
    Htail_halfspan=0.4,
    Htail_airfoil="naca6412",
    Htail_sweep=15.0,
    Htail_root_twist=0.0,
    Htail_root_chord=0.2,
    Htail_tip_twist=-1.0,
    Htail_taper=0.5,
    X_pos_Vtail=1.5,
    Vtail_sweep=25.0,
    Vtail_root_chord=0.2,
    Vtail_taper=0.4,
    Vtail_span=0.5,
    Vtail_airfoil="naca6412"
 )

# Example mass values (again, use real data)
mass_data = MassFileData(
    aircraft_name="Golf", right_wing_mass=1.0, right_wing_Xcg=0.3, right_wing_Ycg=0.6, right_wing_Zcg=0.0,
    Ixx_right_wing=0.01, Iyy_right_wing=0.02, Izz_right_wing=0.03,
    fuselage_mass=2.0, fuselage_Xcg=0.7, fuselage_Ycg=0.0, fuselage_Zcg=0.0,
    Ixx_fuselage=0.1, Iyy_fuselage=0.2, Izz_fuselage=0.3,
    right_Hwing_mass=0.5, right_Hwing_Xcg=1.2, right_Hwing_Ycg=0.3, right_Hwing_Zcg=0.0,
    Ixx_right_Hwing=0.01, Iyy_right_Hwing=0.02, Izz_right_Hwing=0.03,
    Vtail_mass=0.4, Vtail_Xcg=1.3, Vtail_Ycg=0.0, Vtail_Zcg=0.2,
    Ixx_Vtail=0.01, Iyy_Vtail=0.015, Izz_Vtail=0.02,
    payload_mass=0.8, payload_Xcg=0.8, payload_Ycg=0.0, payload_Zcg=0.0,
    Ixx_payload=0.01, Iyy_payload=0.01, Izz_payload=0.01,
    battery_mass=0.6, battery_Xcg=0.5, battery_Ycg=0.0, battery_Zcg=0.0
)

#example runcase values 
runcase_data=RunCaseFileData(
    aircraft_name="Golf",
    runcase_name="forrest gump",
    runcase_number=1,
    AoA=3.0,                    
    sideslip=0.0,               
    pitch_rate=0.0,             
    yaw_rate=0.0,               
    roll_rate=0.0,              
    elevator_def=-2.0,          
    rudder_def=0.0,             
    flap_def=0.0,               
    aileron_def=0.0,            
    bank_angle=0.0,             
    climb_angle=0.0,            
    heading_angle=0.0,          
    velocity=25.0,              
    density=1.225       )


if __name__ == "__main__":
 

    test_geom_file,test_geom_path=AVLgeometry(output_path=paths.Output_path,uav_id=geom_data.aircraft_name,main_wing=geom_data.as_dict_main_wing(),h_tail= geom_data.as_dict_h_tail(), v_tail=geom_data.as_dict_v_tail()).geometry_gen()
    print (f"Geometry file  was created at : {test_geom_path}")

    test_mass_file,test_mass_path=AVLmass(output_path=paths.Output_path,uav_id=mass_data.aircraft_name,main_wing_mass=mass_data.as_dict_main_wing_mass(),fuselage_mass=mass_data.as_dict_fuselage_mass(),h_tail_mass= mass_data.as_dict_h_tail_mass(),
                            v_tail_mass=mass_data.as_dict_v_tail_mass(),sporia_mass=mass_data.as_dict_sporia_mass()).mass_file_gen()
    print (f"Mass file  was created at : {test_mass_path}")

    test_runcase_file,test_runcase_path=AVLruncase(output_path=paths.Output_path,uav_id=runcase_data.aircraft_name,flight_conditions=runcase_data.as_dict_flight_conditions()).runcase_file_gen()
    print(f"Runcase file was created at : {test_runcase_path} ")
  

    avl_cracked=AVLsolver(
        uav_id=geom_data.aircraft_name,
        avl_exe_path=paths.AVL_exe_path,
        avl_path=paths.AVL_path,
        output_path=paths.Output_path,
        geometry_file=test_geom_path,
        mass_file=test_mass_path,
        runcase_file=test_runcase_path
        )
    
    analysis_file_path=os.path.join(paths.Output_path,f"{geom_data.aircraft_name}_analysis.txt")
    output,error,derivs=avl_cracked.stability_derivatives()         # STABILITY DERIVATIVES
    if os.path.exists(analysis_file_path):
      print(f"Analysis txt file was created  at : {analysis_file_path} ")
     # print("stdout is :",output) 
     
    CL,CD,CDi=avl_cracked.surface_forces_full(25,np.arange(0,3,1),'horizontal_tail',False)     #SURFACE FORCES COEFFS
    CLtotal,CDtotal=avl_cracked.total_forces_full(25,np.arange(0,3,1),True)  # total forces coeffs
#print(type(avl))