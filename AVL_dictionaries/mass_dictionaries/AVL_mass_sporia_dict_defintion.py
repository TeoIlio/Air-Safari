#Dictionary definition for the sporia mass properties
"""
Define the non-main components  MASS dictionary used inside the MassFileData dataclass. Functions that compute  certain values are called.
Main idea is to define the dictionary and the computations that this dictionary needs, in different(external) modules . These 
will be called inside the .py that creates the dataclass. 

"""

from AVL_properties_calculations.AVL_mass_properties_calculations import compute_mass_sporia
from AVL_properties_calculations.AVL_mass_properties_calculations import compute_cg_position
from AVL_properties_calculations.AVL_mass_properties_calculations import compute_inertia

def create_mass_sporia_dict(self):   # input is mass_data which are the data inside the dataclass

    mass_sporia_dict= {
       'payload_mass': self.payload_mass , 
       'payload_Xcg':self.payload_Xcg,
       'payload_Ycg':self.payload_Ycg,
       'payload_Zcg':self.payload_Zcg,
       'Ixx_payload':self.Ixx_payload, 
       'Iyy_payload':self.Iyy_payload,
       'Izz_payload':self.Izz_payload,
       'battery_mass': self.battery_mass , 
       'battery_Xcg':self.battery_Xcg,
       'battery_Ycg':self.battery_Ycg,
       'battery_Zcg':self.battery_Zcg,
                
                }
    
    return mass_sporia_dict