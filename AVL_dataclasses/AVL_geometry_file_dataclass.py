# AVL geometry file dataclass

"""
The purpose of this module is to create a dataclass for the data required for the geometry template.
In the module , three functions are imported from external modules , in order to define properly 
the dictionaries that the data are correlated with.
"""

from dataclasses import dataclass 
from AVL_dictionaries.geometry_dictionaries.AVL_geom_mainwing_dict_definition import create_geom_main_wing_dict #dict
from AVL_dictionaries.geometry_dictionaries.AVL_geom_htail_dict_definition import create_geom_h_tail_dict  #dict
from AVL_dictionaries.geometry_dictionaries.AVL_geom_vtail_dict_definition import create_geom_v_tail_dict  #dict



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

     def main_wing_dict(self)->dict :   #dict creation by calling each function 
         return create_geom_main_wing_dict(self)
         
     
     def h_tail_dict(self)->dict : 
         return create_geom_h_tail_dict(self)

     def v_tail_dict(self)->dict : 
         return create_geom_v_tail_dict(self)