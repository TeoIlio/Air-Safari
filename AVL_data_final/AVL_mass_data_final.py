# mass data for the GeometryFileData dataclass 
"""
Contains the values for an instance concerning all mass properties required for mass dataclass
"""
from AVL_dataclasses.AVL_mass_file_dataclass import MassFileData

def mass_data_func():

    mass_data = MassFileData(
    aircraft_name="Echo", right_wing_mass=1.0, right_wing_Xcg=0.3, right_wing_Ycg=0.6, right_wing_Zcg=0.0,
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

    return mass_data    
    