#Dictionary definition for the main wing mass properties
"""
Define the main wing MASS dictionary used inside the MassFileData dataclass. Functions that compute  certain values are called.
Main idea is to define the dictionary and the computations that this dictionary needs, in different(external) modules . These 
will be called inside the .py that creates the dataclass. 

"""
from AVL_properties_calculations.AVL_mass_properties_calculations import compute_mass_mainwing
from AVL_properties_calculations.AVL_mass_properties_calculations import compute_cg_position
from AVL_properties_calculations.AVL_mass_properties_calculations import compute_inertia

def create_mass_mainwing_dict(self):   # input is mass_data which are the data inside the dataclass

    mass_mainwing_dict= {
       'right_wing_mass': self.right_wing_mass , 
       'right_wing_Xcg':self.right_wing_Xcg,
       'right_wing_Ycg':self.right_wing_Ycg,
       'right_wing_Zcg':self.right_wing_Zcg,
       'Ixx_right_wing':self.Ixx_right_wing, 
       'Iyy_right_wing':self.Iyy_right_wing,
       'Izz_right_wing':self.Izz_right_wing 
                }
                
    return mass_mainwing_dict
    