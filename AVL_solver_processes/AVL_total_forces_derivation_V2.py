#AVL total forces derivation process

import os
import numpy as np
from numpy.typing import NDArray
import subprocess
import matplotlib.pyplot as plt 
import matplotlib.ticker as tick
from AVL_dataclasses.AVL_general_use_dataclasses import batch_data

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
    # Extract CL from AVL output.In the standard output, find CLtot and derive each value. Same for CDi.
    CL_total , CDi_total= [] , []

    for line in output.split("\n"):
        if "CLtot" in line:
            try:
                CL_total.append(float(line.split()[-1]))
            except: pass   
        if "CDtot" in line:
            try:
                CDi_total.append(float(line.split()[-1]))
                
            except : pass
          
    return np.array(CL_total),np.array(CDi_total)  

def batch_analysis_total(self,AoA_range: NDArray[np.float64]):
    """
    Complete a batch analysis for the whole aircraft and place the derived data in a dataclass(type:batch_data)
    """

    CL_list_total, CDi_list_total , batched_CL ,batched_CDi = [] , [] , [], []

    for AoA in AoA_range:
        batch_analysis_CL,batch_analysis_CDi=total_forces(self,AoA)
        CL_list_total.append((f"{AoA}",float(batch_analysis_CL)))
        CDi_list_total.append((f"{AoA}",float(batch_analysis_CDi)))
        batched_CL.append(float(batch_analysis_CL))
        batched_CDi.append(float(batch_analysis_CDi))

    return  batch_data(AoA_range_total=AoA_range, batch_total_CL=np.array(batched_CL), batch_total_CDi=np.array(batched_CDi))

def txt_file(self,batch_data : batch_data):
    """
    Txt file creation with batched data.
    """
    
    if os.path.exists(os.path.join(self.output_path,f"total_forces_{self.uav_id}.txt")):
        os.remove(os.path.join(self.output_path,f"total_forces_{self.uav_id}.txt"))

    total_forces_path=os.path.join(self.output_path,f"total_batch_{self.uav_id}.txt")    
    with open(total_forces_path,"w") as f: 
        # create a txt file with CL values for the AoA range
         f.write(f"{self.uav_id} aircraft batch analysis:\n\n")     
         for AoA,CL,CDi in zip(batch_data.AoA_range_total,batch_data.batch_total_CL,batch_data.batch_total_CDi):
            f.write(f"AoA:{AoA:.1f} ==> CL={CL:.4f} , CDi={CDi:4f}\n") 
       
    return total_forces_path   



def plot(batch_data :batch_data):
    
    fig, axs= plt.subplots(2, 2 ,figsize=(20,10),layout='constrained')
    
    #CL-AoA
    plt.grid(True)
    axs[0,0].plot(batch_data.AoA_range_total,batch_data.batch_total_CL,marker='o',color='b')
    axs[0,0].set_xlabel("Angle of Attack")
    axs[0,0].set_ylabel("Total aircraft CL")
    axs[0,0].set_title("Coefficient of Lift (CL) - Angle of Attack")
    axs[0,0].grid(True)
    
    #CDi-AoA
    axs[0,1].plot(batch_data.AoA_range_total,batch_data.batch_total_CDi,marker='o',color='r')
    axs[0,1].set_xlabel("Angle of Attack")
    axs[0,1].set_ylabel("Total aircraft CDi")
    axs[0,1].set_title("Coefficient of induced Drag (CDi) - Angle of Attack")
    axs[0,1].grid(True)
    
 
    #CL-CDi
    axs[1,0].plot(batch_data.batch_total_CL,batch_data.batch_total_CDi,marker='o',color='g')
    axs[1,0].set_xlabel(" CL")
    axs[1,0].set_ylabel(" CDi")
    axs[1,0].set_title("Coefficient of Lift (CL) - Coefficient of induced drag (CDi)")
    axs[1,0].grid(True)

    #CL/CDi- AoA
    axs[1,1].plot(batch_data.AoA_range_total,batch_data.batch_total_CL/batch_data.batch_total_CDi,marker='o',color='y')
    axs[1,1].set_xlabel(" Angle of Attack")
    axs[1,1].set_ylabel(" CL/CDi")
    axs[1,1].set_title(" CL/CDi - Angle of attack")
    axs[1,1].grid(True)
       
    plt.close(fig)
    
    return fig    

def total_forces_main(self,AoA_range: NDArray[np.float64],batched_data : batch_data):
    aircraft_batch=batch_analysis_total(self,AoA_range=AoA_range) 
    txt_file(self,batch_data=aircraft_batch)
    fig_total=plot(batch_data=aircraft_batch)

    if os.path.exists(os.path.join(self.output_path,f"{self.uav_id}_total_batch_plots.png")):
        os.remove(os.path.join(self.output_path,f"{self.uav_id}_total_batch_plots.png"))

    fig_total.savefig(os.path.join(self.output_path,f"{self.uav_id}_total_batch_plots.png"),dpi=300)
    aircraft_batch.plot_total_forces=fig_total

    batched_data.plot_total_forces=aircraft_batch.plot_total_forces
    batched_data.AoA_range_total=aircraft_batch.AoA_range_total
    batched_data.batch_total_CDi=aircraft_batch.batch_total_CDi
    batched_data.batch_total_CL=aircraft_batch.batch_total_CL

    return batched_data 





