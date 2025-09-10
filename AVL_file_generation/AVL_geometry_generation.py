#geometry file generation and save in a specified output path
import os 
from AVL_templates.AVL_geom_template import uav_geometry


def geometry_gen(self):
    self.geometry_file=uav_geometry(self.uav_id,self.main_wing,self.h_tail,self.v_tail)
        
      
         
    self.geom_file_path =os.path.join(self.output_path,f"{self.uav_id}.avl")  
    with open(self.geom_file_path,"w") as f: 
        f.write(self.geometry_file)
        
       
    return self.geometry_file,self.geom_file_path