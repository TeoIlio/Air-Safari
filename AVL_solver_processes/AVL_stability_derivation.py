# AVL_stability_derivation
import os 
import re
import subprocess
from AVL_dataclasses.AVL_general_use_dataclasses import StabilityData




def stability_derivation(self):

    """
    Runs an AVL analysis and derives specific data like stability derivatives etc... in order to later feed them in a stability analysis module
    """
    analysis_seq="""
     LOAD {geometry_file}
     MASS {mass_file}
     CASE {runcase_file}
     OPER 
     X
     ST {aircraft_name}_analysis.txt
     O

     QUIT
     """
    analysis_seq_params={
            "geometry_file": self.geometry_file,
            "mass_file": self.mass_file,
            "runcase_file": self.runcase_file,
            "aircraft_name": self.uav_id
             }
    
    analysis_output = analysis_seq.format(**analysis_seq_params)
    process=subprocess.Popen(self.avl_exe_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,cwd=self.output_path)
    output, error = process.communicate(analysis_output)
        

    analysis_file_path=os.path.join(self.output_path,f"{self.uav_id}_analysis.txt")
    stability_derivs_list=[]   # initialize list that will consist of derivatives , list will contain tuples
    data_only=[]
        
    if not os.path.exists(analysis_file_path):
        raise FileNotFoundError("AVL analysis file not found.")
    with open(analysis_file_path,"r") as f:
        file=f.read() 
        #dictionary with all the values that need to be exctracted
        deriv_dict={  
                  key: re.search(rf"{key}\s*=\s*([-+]?\d*\.\d+|\d+)", file)
                  for key in ["CLtot",'CDtot','Cmtot','CLa','Cma','CYb','Clb','Cnb','CYp','Clp','Cnp','CLq','Cmq','CYr','Clr','Cnr']
                }

        for key , match in deriv_dict.items():
            if match:
                stability_derivs_list.append((key,float(match.group(1))))  # creation of tuples with pairs between keys-values as in derivative-value
                data_only.append(float(match.group(1))) # data only list 

        deriv_file_path =os.path.join(self.output_path,f"derivs_{self.uav_id}.txt")  
        with open(deriv_file_path,"w") as f: 
        # create a txt file with the required values 
            for item in stability_derivs_list:
                 f.write(f"{item[0]} = {item[1]}\n")   
                   

    return StabilityData(CLtot=data_only[0],
                        CDtot=data_only[1],
                        Cmtot=data_only[2],
                        CLa=data_only[3],
                        Cma=data_only[4],
                        CYb=data_only[5],
                        Clb=data_only[6],
                        Cnb=data_only[7],
                        CYp=data_only[8],
                        Clp=data_only[9],
                        Cnp=data_only[10],
                        CLq=data_only[11],
                        Cmq=data_only[12],
                        CYr=data_only[13],
                        Clr=data_only[14],
                        Cnr=data_only[15]
                        )