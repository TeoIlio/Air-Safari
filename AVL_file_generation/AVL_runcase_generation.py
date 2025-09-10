#runcase  file generation and save in a specified output path


import os 
from AVL_templates.AVL_RunCase_template import uav_runcase

def runcase_gen(self):

    self.runcase_file=uav_runcase(self.uav_id,self.flight_conditions)
       
    self.runcase_file_path=os.path.join(self.output_path,f"{self.uav_id}.RUN")
    with open(self.runcase_file_path,"w") as f:
        f.write(self.runcase_file)

    return self.runcase_file, self.runcase_file_path  
