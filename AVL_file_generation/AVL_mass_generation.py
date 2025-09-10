#Mass  file generation and save in a specified output path


import os 
from AVL_templates.AVL_mass_template import uav_mass_properties

def mass_gen(self):
    self.mass_file=uav_mass_properties(self.uav_id,self.main_wing_mass,self.fuselage_mass,self.h_tail_mass,self.v_tail_mass,self.sporia_mass)
          
        
    self.mass_file_path=os.path.join(self.output_path,f"{self.uav_id}.mass") 
    with open(self.mass_file_path, "w") as f: 
        f.write(self.mass_file)
        
          
    return self.mass_file,self.mass_file_path
    

