# geometry data for the GeometryFileData dataclass 

"""
Contains the values for an instance concerning all geometry properties required for geometryfiledata dataclass
"""

from AVL_dataclasses.AVL_geometry_file_dataclass import GeometryFileData
import AVL_combined_cases.paths
import os

def geometry_data_func():
    
    geometry_data=GeometryFileData(
    aircraft_name="Echo",
    Sref=0.48,
    Cref=0.161,
    Bref=2.98,
    Wing_incidence_angle=2.0,
    Wing_halfspan=1.49,
    Wing_sweep=0.0,
    Wing_dih=0.0,
    Wing_root_twist=2.0,
    Wing_root_chord=0.215,
    Wing_tip_twist=-0.0,
    Wing_taper=0.5,
    Wing_airfoil=os.path.join(AVL_combined_cases.paths.airfoil_path,"naca6412"),
    X_pos_Htail=0.986,
    Z_pos_Htail=0.373,
    Htail_incidence_angle=0.0,
    Htail_halfspan=0.1885,
    Htail_airfoil=os.path.join(AVL_combined_cases.paths.airfoil_path,"naca6412"),
    Htail_sweep=0.0,
    Htail_root_twist=0.0,
    Htail_root_chord=0.138,
    Htail_tip_twist=0.0,
    Htail_taper=0.54,
    X_pos_Vtail=0.986,
    Vtail_sweep=0.0,
    Vtail_root_chord=0.215,
    Vtail_taper=0.6,
    Vtail_span=0.373,
    Vtail_airfoil=os.path.join(AVL_combined_cases.paths.airfoil_path,"naca6412"))

    return geometry_data