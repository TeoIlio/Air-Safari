#Dictionary definition for the vertical tail mass properties
"""
Define the vertical tail MASS dictionary used inside the MassFileData dataclass. Functions that compute  certain values are called.
Main idea is to define the dictionary and the computations that this dictionary needs, in different(external) modules . These 
will be called inside the .py that creates the dataclass. 

"""
from AVL_properties_calculations.AVL_mass_properties_calculations import compute_mass_v_tail
from AVL_properties_calculations.AVL_mass_properties_calculations import compute_cg_position
from AVL_properties_calculations.AVL_mass_properties_calculations import compute_inertia

def create_mass_v_tail_dict(self):   # input is mass_data which are the data inside the dataclass

    mass_v_tail_dict= {
         'Vtail_mass': self.Vtail_mass , 
         'Vtail_Xcg':self.Vtail_Xcg,
         'Vtail_Ycg':self.Vtail_Ycg,
         'Vtail_Zcg':self.Vtail_Zcg,
         'Ixx_Vtail':self.Ixx_Vtail, 
         'Iyy_Vtail':self.Iyy_Vtail,
         'Izz_Vtail':self.Izz_Vtail
                }
    
    return mass_v_tail_dict