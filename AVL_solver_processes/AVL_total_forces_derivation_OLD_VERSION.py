#AVL total forces derivation process

import os
import numpy as np
import subprocess
import matplotlib.pyplot as plt 
import matplotlib.ticker as tick

"""
The main goal of this script is to derive the total CL and CD coefficient for the full aircraft geometry.A batch analysis is going 
to be implemented and results will be plotted and saved in a txt file. 
"""



def total_forces(self, AoA: float):
    """
    Derive total CL and induced CD for the given aircraft and compute a batch analysis for a given range of AoA.
    """

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
    
     QUIT
     """
        
    forces_sequence_params={
        "geometry_file" : self.geometry_file,
        "mass_file": self.mass_file,
        "velocity": self.velocity,
        "AoA": AoA
        }
    
    total_forces_output=surface_forces_sequence.format(**forces_sequence_params)
    process=subprocess.Popen(self.avl_exe_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,cwd=self.output_path)
    output, error = process.communicate(total_forces_output)
     # Extract CL from AVL output.In the standard output, find CLtot and derive each value to cl.
    CL_total=[]
    CD_total=[]
    for line in output.split("\n"):
        if "CLtot" in line:
            try:
                CL_total.append((f"{AoA}",float(line.split()[-1])))
            except: pass   
        if "CDtot" in line:
            try:
                CD_total.append((f"{AoA}",float(line.split()[-1])))
                
            except : pass
          
    return CL_total,CD_total  
    

def total_forces_batch_and_plots(self,AoA_range:np.ndarray, plots: bool):
     #init the lists with the values 
    CL_list_total=[]
    CD_list_total=[]

    for AoA in AoA_range:
        batch_analysis_CL,batch_analysis_CD=total_forces(self,AoA) 
        CL_list_total.append((f"{AoA}",float(batch_analysis_CL[0][1])))
        CD_list_total.append((f"{AoA}",float(batch_analysis_CD[0][1])))
    
    
    total_forces_file_path=os.path.join(self.output_path,f"total_forces_{self.uav_id}.txt")
    with open(total_forces_file_path,"w") as f: 
        # create a txt file with CL values for the AoA range
         f.write("CL values:\n")     
         for item in CL_list_total:
            f.write(f"AoA:{item[0]} = {item[1]}\n") 
        # append in the same file the CD values for the AoA range (inviscid)
         f.write("CD values:\n")     
         for item in CD_list_total:
            f.write(f"AoA:{item[0]} = {item[1]}\n")   
    if plots:
      #CL-AoA
      plt.figure(figsize=(8, 5))
      plt.plot(AoA_range,[item[1] for item in CL_list_total], marker='o', linestyle='-', color='r')
      plt.xlabel("Angle of attack")
      plt.ylabel("CL")
      plt.title(f"CL-AoA graph for {self.uav_id}")
      plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.5))  
      plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.1))
      plt.grid(True)
      plt.show()     

      #CD-AoA
      plt.figure(figsize=(8, 5))
      plt.plot(AoA_range,[item[1] for item in CD_list_total], marker='o', linestyle='-', color='r')
      plt.xlabel("Angle of attack")
      plt.ylabel("CD") 
      plt.title(f"CD-AoA graph for {self.uav_id}") 
      plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.5))  
      plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.005))
      plt.grid(True)
      plt.show()  

     #CL-CD
      plt.figure(figsize=(8, 5))
      plt.plot([item[1] for item in CL_list_total],[item[1] for item in CD_list_total], marker='o', linestyle='-', color='r')
      plt.xlabel("CL")
      plt.ylabel("CD") 
      plt.title(f"CL-CD graph for {self.uav_id}") 
      plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.1))  
      plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.005))
      plt.grid(True)
      plt.show()  

      #CL/CD -ΑοΑ

      cl_values = np.array([item[1] for item in CL_list_total])
      cd_values = np.array([item[1] for item in CD_list_total])

      plt.figure(figsize=(8, 5),facecolor='grey')
      plt.plot(AoA_range,cl_values/cd_values, marker='o', linestyle='-', color='r')
      plt.xlabel("Angle of Attack")
      plt.ylabel("CL/CD") 
      plt.title(f"CL/CD - AoA graph for {self.uav_id}") 
      plt.gca().xaxis.set_major_locator(tick.MultipleLocator(1))  
      plt.gca().yaxis.set_major_locator(tick.MultipleLocator(4))
      plt.grid(True)
      plt.show()

    return CL_list_total,CD_list_total


def plot_batch():
 # cdv,cdf,cdp  , top sep ,bot sep !, total ccd,ccdv and ccdi together
    fig, axs= plt.subplots(2, 3 ,figsize=(20,10),layout='constrained')
    
    #CDV
    plt.grid(True)
    axs[0,0].plot(y_coords_dense,CDv_right,marker='o',color='b')
    axs[0,0].plot(-y_coords_dense,CDv_YDUP,marker='o',color='b')
    axs[0,0].set_xlabel("Wingspan (m)")
    axs[0,0].set_ylabel("Sectional viscous Cd (Cdv)")
    axs[0,0].set_title("Sectional  Cdv - Wingspan")
    axs[0,0].grid(True)
    
    #CDf
    axs[0,1].plot(y_coords_dense,CDf_right,marker='o',color='r')
    axs[0,1].plot(-y_coords_dense,CDf_YDUP,marker='o',color='r')
    axs[0,1].set_xlabel("Wingspan (m)")
    axs[0,1].set_ylabel("Sectional friction Cd (Cdf)")
    axs[0,1].set_title("Sectional Cdf - Wingspan")
    axs[0,1].grid(True)
    
    #CDp
    axs[0,2].plot(y_coords_dense,CDp_right,marker='o',color='g')
    axs[0,2].plot(-y_coords_dense,CDp_YDUP,marker='o',color='g')
    axs[0,2].set_xlabel("Wingspan (m)")
    axs[0,2].set_ylabel("Sectional pressure Cd (Cdp)")
    axs[0,2].set_title("Sectional Cdp - Wingspan")
    axs[0,2].grid(True)
    
    #ccdv ccdi combo
    axs[1,0].plot(y_coords_dense,CCDv_right,label='c*Cdviscous',marker='o',color='b')
    axs[1,0].plot(-y_coords_dense,CCDv_YDUP,marker='o',color='b')
    axs[1,0].plot(y_coords_dense,CCDi_right,label='c*Cdinduced',marker='o',color='r')
    axs[1,0].plot(-y_coords_dense,CCDi_YDUP,marker='o',color='r')
    axs[1,0].set_xlabel("Wingspan (m)")
    axs[1,0].set_ylabel("Sectional coefficient of drag")
    axs[1,0].set_title("Combined sectional Cdv and Cdi - Wingspan")
    axs[1,0].legend()
    axs[1,0].grid(True)

    #Total CD
    axs[1,1].plot(y_coords_dense,(CCDv_right+CCDi_right),marker='o',color='c')
    axs[1,1].plot(-y_coords_dense,(CCDv_YDUP+CCDi_YDUP),marker='o',color='c')
    axs[1,1].set_xlabel("Wingspan (m)")
    axs[1,1].set_ylabel("Sectional  total coefficient of drag  (Cd)")
    axs[1,1].set_title("Sectional total Cd - Wingspan")
    axs[1,1].grid(True)
    
    #transition
    axs[1,2].plot(data_right.y_coords,data_right.strip_top_transition,marker='o',color='y')
    axs[1,2].plot(data_YDUP.y_coords,data_YDUP.strip_top_transition,marker='o',color='y')
    axs[1,2].set_xlabel("Wingspan (m)")
    axs[1,2].set_ylabel("Sectional transition point ")
    axs[1,2].set_title("Sectional transition(x/c) - Wingspan")
    axs[1,2].grid(True)

   
    plt.close(fig)
    

    return fig    
