#Dictionary definition for the horizontal tail mass properties
"""
Define the horizontal tail MASS dictionary used inside the MassFileData dataclass. Functions that compute  certain values are called.
Main idea is to define the dictionary and the computations that this dictionary needs, in different(external) modules . These 
will be called inside the .py that creates the dataclass. 

"""
from AVL_properties_calculations.AVL_mass_properties_calculations import compute_mass_htail
from AVL_properties_calculations.AVL_mass_properties_calculations import compute_cg_position
from AVL_properties_calculations.AVL_mass_properties_calculations import compute_inertia

def create_mass_h_tail_dict(self):   # input is mass_data which are the data inside the dataclass

    mass_h_tail_dict= {
        'right_Hwing_mass': self.right_Hwing_mass , 
        'right_Hwing_Xcg':self.right_Hwing_Xcg,
        'right_Hwing_Ycg':self.right_Hwing_Ycg,
        'right_Hwing_Zcg':self.right_Hwing_Zcg,
        'Ixx_right_Hwing':self.Ixx_right_Hwing, 
        'Iyy_right_Hwing':self.Iyy_right_Hwing,
        'Izz_right_Hwing':self.Izz_right_Hwing
                }
         
                
    
    return mass_h_tail_dict



