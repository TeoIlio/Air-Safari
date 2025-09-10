# AVL mass file dataclass

"""
The purpose of this module is to create a dataclass for the data required for the mass template.
In the module , functions are imported from external modules , in order to define properly 
the dictionaries that the data are correlated with.
"""
from dataclasses import dataclass
from AVL_dictionaries.mass_dictionaries.AVL_mass_mainwing_dict_definition import create_mass_mainwing_dict
from AVL_dictionaries.mass_dictionaries.AVL_mass_htail_dict_definition import create_mass_h_tail_dict
from AVL_dictionaries.mass_dictionaries.AVL_mass_vtail_dict_defintion import create_mass_v_tail_dict
from AVL_dictionaries.mass_dictionaries.AVL_mass_fuselage_dict_definition import create_mass_fuselage_dict
from AVL_dictionaries.mass_dictionaries.AVL_mass_sporia_dict_defintion import create_mass_sporia_dict



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

    
    def main_wing_mass_dict(self)->dict:
        return create_mass_mainwing_dict(self)
    
    def h_tail_mass_dict(self)->dict:
        return create_mass_h_tail_dict(self)
    
    def v_tail_mass_dict(self)->dict:
        return create_mass_v_tail_dict(self)
    
    def fuselage_mass_dict(self)->dict:
        return create_mass_fuselage_dict(self)
    
    def sporia_mass_dict(self)->dict:
        return create_mass_sporia_dict(self)