#Dictionary definition for the fuselage mass properties
"""
Define the fuselage MASS dictionary used inside the MassFileData dataclass. Functions that compute  certain values are called.
Main idea is to define the dictionary and the computations that this dictionary needs, in different(external) modules . These 
will be called inside the .py that creates the dataclass. 

"""
from AVL_properties_calculations.AVL_mass_properties_calculations import compute_mass_htail
from AVL_properties_calculations.AVL_mass_properties_calculations import compute_cg_position
from AVL_properties_calculations.AVL_mass_properties_calculations import compute_inertia

def create_mass_fuselage_dict(self):   # input is mass_data which are the data inside the dataclass

    mass_fuselage_dict= {
        'fuselage_mass': self.fuselage_mass , 
        'fuselage_Xcg':self.fuselage_Xcg,
        'fuselage_Ycg':self.fuselage_Ycg,
        'fuselage_Zcg':self.fuselage_Zcg,
        'Ixx_fuselage':self.Ixx_fuselage, 
        'Iyy_fuselage':self.Iyy_fuselage,
        'Izz_fuselage':self.Izz_fuselage
                }
    return mass_fuselage_dict