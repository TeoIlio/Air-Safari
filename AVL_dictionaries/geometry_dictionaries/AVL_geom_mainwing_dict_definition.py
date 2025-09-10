#Dictionary definition for the main wing
"""
Define the main wing dictionary used inside the GeometryFileData dataclass. Functions that compute  certain values are called.
Main idea is to define the dictionary and the computations that this dictionary needs, in different(external) modules . These 
will be called inside the .py that creates the dataclass. 

"""

#from AVL_geometry_file_dataclass import GeometryFileData
from AVL_properties_calculations.AVL_geom_properties_calculations import compute_halfspan 
from AVL_properties_calculations.AVL_geom_properties_calculations import compute_sweeped
from AVL_properties_calculations.AVL_geom_properties_calculations import compute_tip_chord

def create_geom_main_wing_dict(self):
   
   geom_main_wing_dict={
           'Sref': self.Sref, 
           'Bref': self.Bref,
           'Cref': self.Cref, 
           'Wing_incidence_angle': self.Wing_incidence_angle,
           'Wing_halfspan': compute_halfspan(self.Bref),       # imported, defined in an external script
           'Wing_sweeped': compute_sweeped(self.Wing_sweep,self.Bref),  #same 
           'Wing_dih': self.Wing_dih,
           'Wing_root_twist': self.Wing_root_twist,
           'Wing_root_chord': self.Wing_root_chord,
           'Wing_tip_twist': self.Wing_tip_twist,
           'Wing_tip_chord':compute_tip_chord(self.Wing_taper,self.Wing_root_chord),  #same 
           'Wing_airfoil': self.Wing_airfoil
                 }
   
   return geom_main_wing_dict