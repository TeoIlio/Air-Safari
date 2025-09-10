#AVL surface forces derivation 
import os
import numpy as np
import subprocess
import matplotlib.pyplot as plt 
import matplotlib.ticker as tick

"""
This script will run a process on avl in order to derive forces acting upon (lifting) surfaces. A txt file is going to be exctracted
and values of coefficients (CL,CD,Cm,Cn,Cl etc) are going to be derived from it . The function will be used in a loop 
in order to implement a batch analysis for a specified angle of attack range. 
"""



def surface_forces(self, AoA: float,surface : str):

    surface_forces_sequence="""
     LOAD {geometry_file}
     MASS {mass_file}
     M
     V {velocity}
     D 1.225
     G 9.81
     OPER
     A 
     A {AoA}
     X 
     FN  {aircraft_name}_{AoA}_surface_forces.txt

     QUIT
     """
        
    forces_sequence_params={
        "geometry_file" : self.geometry_file,
        "mass_file": self.mass_file,
        "velocity": self.velocity,
        "AoA": AoA,
        "aircraft_name": self.uav_id
        }
    
    surface_forces_path=os.path.join(self.output_path,f"{self.uav_id}_{AoA}_surface_forces.txt")
    if os.path.exists(surface_forces_path):
      os.remove(surface_forces_path)

    surface_forces_output=surface_forces_sequence.format(**forces_sequence_params)
    process=subprocess.Popen(self.avl_exe_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,cwd=self.output_path)
    output, error = process.communicate(surface_forces_output)

    surface_dict={ 'main_wing': 1 ,'horizontal_tail': 3 , 'vertical_tail':5 ,'total': None }   # match the input string with the surface numbering of the geometry file
    coeffs_list=[]

    if os.path.exists(surface_forces_path):
        with open(surface_forces_path,"r") as f:
            file=f.readlines()
        for line in file: 
            if line.strip().startswith(f'{surface_dict[surface]}'):  
                coeffs=line.split()
                if len(coeffs)>=10:  # make sure the line is correct
                    if surface_dict[surface]==5 :
                      coeffs_list.append(('CL',float(coeffs[2])))   #derive CL which is the 3rd value showing in the file 
                      coeffs_list.append(('CD',float(coeffs[3]))) 
                      coeffs_list.append(('CDi',float(coeffs[8])))
                      coeffs_list.append(('CDv',float(coeffs[9])))
                    else:
                      coeffs_list.append(('CL',2*float(coeffs[2])))   #derive CL which is the 3rd value showing in the file 
                      coeffs_list.append(('CD',2*float(coeffs[3]))) 
                      coeffs_list.append(('CDi',2*float(coeffs[8])))
                      coeffs_list.append(('CDv',2*float(coeffs[9])))
            
           


        os.remove(surface_forces_path)
    return coeffs_list   
    

def FN_batch_and_plots(self,AoA_range:np.ndarray,surface, plots: bool):
    #init the lists with the values 
    CL_list=[]
    CD_list=[]
    CDi_list=[]
    CDv_list=[]
    for AoA in AoA_range:
        batch_analysis=surface_forces(self,AoA,surface)
        if len(batch_analysis) >= 4:
         CL_list.append((f'{AoA}', batch_analysis[0][1])) # create new lists with new tuples as in: (AoA=1 , 0.7)
         CD_list.append((f'{AoA}', batch_analysis[1][1]))
         CDi_list.append((f'{AoA}', batch_analysis[2][1]))
         CDv_list.append((f'{AoA}', batch_analysis[3][1]))
        else:
         print(f"Error")
           
    
    fn_file_path=os.path.join(self.output_path,f"final_surface_forces_{self.uav_id}.txt")
    with open(fn_file_path,"w") as f: 
        # create a txt file with CL values for the AoA range
         f.write("CL values:\n")     
         for item in CL_list:
            f.write(f"AoA:{item[0]} = {item[1]}\n") 
        # append in the same file the CD values for the AoA range (inviscid)
         f.write("CD values:\n")     
         for item in CD_list:
            f.write(f"AoA:{item[0]} = {item[1]}\n")   
    if plots:
      #CL-AoA
      plt.figure(figsize=(8, 5))
      plt.plot(AoA_range,[item[1] for item in CL_list], marker='o', linestyle='-', color='r')
      plt.xlabel("Angle of attack")
      plt.ylabel("CL")
      if surface=="horizontal_tail" :
        plt.title(f"CL-AoA graph for horizontal tail")
      elif surface=="main_wing":  
        plt.title(f"CL-AoA graph for main wing")
      else:
         pass  
      plt.gca().xaxis.set_major_locator(tick.MultipleLocator(1))  
      plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.1))
      plt.grid(True)
      plt.show()     

      #CD-AoA
      plt.figure(figsize=(8, 5))
      plt.plot(AoA_range,[item[1] for item in CD_list], marker='o', linestyle='-', color='r')
      plt.xlabel("Angle of attack")
      plt.ylabel("CD")
      if surface=="horizontal_tail" :
        plt.title(f"CD-AoA graph for horizontal tail")
      elif surface=="main_wing":  
        plt.title(f"CD-AoA graph for main wing")
      else:
         pass  
      plt.gca().xaxis.set_major_locator(tick.MultipleLocator(1))  
      plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.005))
      plt.grid(True)
      plt.show()  

      #CL-CD
      plt.figure(figsize=(8, 5))
      plt.plot([item[1] for item in CL_list],[item[1] for item in CD_list], marker='o', linestyle='-', color='r')
      plt.xlabel("CL")
      plt.ylabel("CD")
      if surface=="horizontal_tail" :
        plt.title(f"CL-CD graph for horizontal tail")
      elif surface=="main_wing":  
        plt.title(f"CL-CD graph for main wing")
      else:
         pass  
      plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.1))  
      plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.005))
      plt.grid(True)
      plt.show()



    return CL_list,CD_list,CDi_list