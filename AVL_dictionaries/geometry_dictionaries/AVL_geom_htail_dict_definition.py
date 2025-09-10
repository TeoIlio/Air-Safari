#Dictionary definition for the horizontal tail 
"""
Define the main wing dictionary used inside the GeometryFileData dataclass. Functions that compute  certain values are called.
Main idea is to define the dictionary and the computations that this dictionary needs, in different(external) modules . These 
will be called inside the dataclass of the main script. 

"""
from AVL_properties_calculations.AVL_geom_properties_calculations import compute_sweeped
from AVL_properties_calculations.AVL_geom_properties_calculations import compute_tip_chord


def create_geom_h_tail_dict(self): 
         
         Htail_dict= {
                 'X_pos_Htail': self.X_pos_Htail,
                 'Z_pos_Htail': self.Z_pos_Htail, 
                 'Htail_incidence_angle': self.Htail_incidence_angle,
                 'Htail_halfspan':self.Htail_halfspan, 
                 'Htail_airfoil':self.Htail_airfoil,
                 'Htail_sweeped': compute_sweeped(self.Htail_sweep,2*self.Htail_halfspan),
                 'Htail_root_twist': self.Htail_root_twist, 
                 'Htail_root_chord': self.Htail_root_chord,
                 'Htail_tip_twist': self.Htail_tip_twist,
                 'Htail_tip_chord': compute_tip_chord(self.Htail_taper,self.Htail_root_chord)
                 }
         
         return Htail_dict