#Dictionary definition for the vertical tail

"""
Define the vertical tail dictionary used inside the GeometryFileData dataclass. Functions that compute  certain values are called.
Main idea is to define the dictionary and the computations that this dictionary needs, in different(external) modules . These 
will be called inside the dataclass of the main script. 

"""

from AVL_properties_calculations.AVL_geom_properties_calculations import compute_sweeped
from AVL_properties_calculations.AVL_geom_properties_calculations import compute_tip_chord

def create_geom_v_tail_dict(self) : 
       
         v_tail_dict= {'X_pos_Vtail': self.X_pos_Vtail,
                  'Vtail_sweeped': compute_sweeped(self.Vtail_sweep,2*self.Vtail_span),
                  'Vtail_root_chord': self.Vtail_root_chord,
                  'Vtail_tip_chord': compute_tip_chord(self.Vtail_taper,self.Vtail_root_chord), 
                  'Vtail_span': self.Vtail_span,
                  'Vtail_airfoil': self.Vtail_airfoil
                   }      
         
         return v_tail_dict