#AVL surface forces derivation 
import os
import numpy as np
from numpy.typing import NDArray
import subprocess
import matplotlib.pyplot as plt 
import matplotlib.ticker as tick
from AVL_dataclasses.AVL_general_use_dataclasses import batch_data

"""
This script will run a process on avl in order to derive forces acting upon (lifting) surfaces. A txt file is going to be exctracted
and values of coefficients (CL,CD,Cm,Cn,Cl etc) are going to be derived from it . The function will be used in a loop 
in order to implement a batch analysis for a specified angle of attack range. 
"""



def surface_forces(self, AoA: float,surface : str):
    """
    Derive CL and CDi for a specific surface of the aircraft and for a specific angle of attack.
    """

    surface_forces_sequence="""
     LOAD {geometry_file}
     MASS {mass_file}
     OPER
     M
     V {velocity}
     D 1.225
     G 9.81
     
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

    surface_dict={ 'Main Wing': 1 ,'Horizontal Tail': 3 , 'Vertical Tail':5 }   # match the input string with the surface numbering of the AVL analysis file
    CL_list , CDi_list = [] , []

    if not  os.path.exists(surface_forces_path):
        raise FileNotFoundError("No analysis file found.")
    
    with open(surface_forces_path,"r") as f:
        file=f.readlines()
        for f,line in enumerate(file): 
            if line.strip().startswith(f'{surface_dict[surface]}'):  
                data_right=line.split()   
                if len(data_right)>=10:  # make sure the line is correct
                    if surface_dict[surface]==5 :
                      CL_list.append(float(data_right[2]))   #derive data for vertical 
                      CDi_list.append(float(data_right[8]))
                      
                    else:
                      data_YDUP= file[f+1].split()  #only true for non vertical surfaces
                      CL_list.append(float(data_right[2])+float(data_YDUP[2]))   #derive data for any other type of surface 
                      CDi_list.append(float(data_right[8])+float(data_YDUP[8]))
           


    os.remove(surface_forces_path)
    return np.array(CL_list), np.array(CDi_list)   

def batch_analysis_surface(self,AoA_range: NDArray[np.float64], surface : str):
    """
    Complete a batch analysis for the whole aircraft and place the derived data in a dataclass(type:batch_data)
    """

    CL_list_surface, CDi_list_surface , batched_CL ,batched_CDi = [] , [] , [], []

    for AoA in AoA_range:
        batch_analysis_CL,batch_analysis_CDi=surface_forces(self,AoA,surface)
        CL_list_surface.append((f"{AoA}",float(batch_analysis_CL)))
        CDi_list_surface.append((f"{AoA}",float(batch_analysis_CDi)))
        batched_CL.append(float(batch_analysis_CL))
        batched_CDi.append(float(batch_analysis_CDi))
    
    if surface=='Main Wing':
        return  batch_data(AoA_range_wing=AoA_range, batch_wing_CL=np.array(batched_CL), batch_wing_CDi=np.array(batched_CDi))    
    elif surface=='Horizontal Tail':
        return  batch_data(AoA_range_tail=AoA_range, batch_tail_CL=np.array(batched_CL), batch_tail_CDi=np.array(batched_CDi)) 

def txt_file(self,batch_data : batch_data,surface : str):
    """
    Txt file creation with batched data.
    """
    surface_forces_path=os.path.join(self.output_path,f"{surface}_batch_{self.uav_id}.txt")  
    if os.path.exists(surface_forces_path):
        os.remove(surface_forces_path)
  
    with open(surface_forces_path,"w") as f: 
        if surface=='Main Wing':     
           # create a txt file with CL values for the AoA range
           f.write(f"{self.uav_id} {surface} batch analysis:\n\n")     
           for AoA,CL,CDi in zip(batch_data.AoA_range_wing,batch_data.batch_wing_CL,batch_data.batch_wing_CDi):
                f.write(f"AoA:{AoA:.1f}==> CL={CL:.4f} , CDi={CDi:4f}\n")
        elif surface=='Horizontal Tail':
             # create a txt file with CL values for the AoA range
           f.write(f"{self.uav_id} {surface} batch analysis:\n\n")     
           for AoA,CL,CDi in zip(batch_data.AoA_range_tail,batch_data.batch_tail_CL,batch_data.batch_tail_CDi):
                f.write(f"AoA:{AoA:.1f} ==> CL={CL:.4f} , CDi={CDi:4f}\n")
                    
       
    return surface_forces_path       


def plot(batch_data :batch_data,surface: str):
    """
    Plotting of CL-AoA, CDi-AoA, CL-CDi, CL/CDi-AoA for a surface.
    """
    fig, axs= plt.subplots(2, 2 ,figsize=(20,10),layout='constrained')
    
    if surface=='Main Wing':
    #CL-AoA
        plt.grid(True)
        axs[0,0].plot(batch_data.AoA_range_wing,batch_data.batch_wing_CL,marker='o',color='b')
        axs[0,0].set_xlabel("Angle of Attack")
        axs[0,0].set_ylabel("Main wing CL")
        axs[0,0].set_title("Coefficient of Lift (CL) of Main Wing - Angle of Attack")
        axs[0,0].grid(True)
    
        #CDi-AoA
        axs[0,1].plot(batch_data.AoA_range_wing,batch_data.batch_wing_CDi,marker='o',color='r')
        axs[0,1].set_xlabel("Angle of Attack")
        axs[0,1].set_ylabel("Main wing CDi")
        axs[0,1].set_title("Coefficient of induced Drag (CDi) of Main Wing - Angle of Attack")
        axs[0,1].grid(True)
    
 
        #CL-CDi
        axs[1,0].plot(batch_data.batch_wing_CL,batch_data.batch_wing_CDi,marker='o',color='g')
        axs[1,0].set_xlabel(" CL")
        axs[1,0].set_ylabel(" CDi")
        axs[1,0].set_title("Coefficient of Lift (CL) of Main wing - Coefficient of induced drag (CDi) of Main Wing")
        axs[1,0].grid(True)

        #CL/CDi- AoA
        axs[1,1].plot(batch_data.AoA_range_wing,batch_data.batch_wing_CL/batch_data.batch_wing_CDi,marker='o',color='y')
        axs[1,1].set_xlabel(" Angle of Attack")
        axs[1,1].set_ylabel(" CL/CDi")
        axs[1,1].set_title(" CL/CDi of Main Wing- Angle of attack")
        axs[1,1].grid(True)
    
        plt.close(fig)

        return fig
    
    elif surface=='Horizontal Tail':
    #CL-AoA
        plt.grid(True)
        axs[0,0].plot(batch_data.AoA_range_tail,batch_data.batch_tail_CL,marker='o',color='b')
        axs[0,0].set_xlabel("Angle of Attack")
        axs[0,0].set_ylabel("Horizontal Tail CL")
        axs[0,0].set_title("Coefficient of Lift (CL) of Horizontal Tail - Angle of Attack")
        axs[0,0].grid(True)
    
        #CDi-AoA
        axs[0,1].plot(batch_data.AoA_range_tail,batch_data.batch_tail_CDi,marker='o',color='r')
        axs[0,1].set_xlabel("Angle of Attack")
        axs[0,1].set_ylabel("Horizontal Tail CDi")
        axs[0,1].set_title("Coefficient of induced Drag (CDi) of Horizontal Tail- Angle of Attack")
        axs[0,1].grid(True)
    
 
        #CL-CDi
        axs[1,0].plot(batch_data.batch_tail_CL,batch_data.batch_tail_CDi,marker='o',color='g')
        axs[1,0].set_xlabel(" CL")
        axs[1,0].set_ylabel(" CDi")
        axs[1,0].set_title("Coefficient of Lift (CL) of Horizontal Tail - Coefficient of induced drag (CDi) of Horizontal Tail")
        axs[1,0].grid(True)

        #CL/CDi- AoA
        axs[1,1].plot(batch_data.AoA_range_tail,batch_data.batch_tail_CL/batch_data.batch_tail_CDi,marker='o',color='y')
        axs[1,1].set_xlabel(" Angle of Attack")
        axs[1,1].set_ylabel(" CL/CDi")
        axs[1,1].set_title(" CL/CDi of Horizontal Tail- Angle of attack")
        axs[1,1].grid(True)
    
        plt.close(fig)
    
        return fig    

def surface_forces_main(self,AoA_range : NDArray[np.float64], surface: str , batched_data: batch_data):
    surface_batch=batch_analysis_surface(self,AoA_range=AoA_range,surface=surface) 
    txt_file(self,batch_data=surface_batch,surface=surface)
    fig_surface=plot(batch_data=surface_batch,surface=surface)
    

    fig_path=os.path.join(self.output_path,f"{self.uav_id}_{surface}_batch_plots.png")
    if os.path.exists(fig_path):
        os.remove(fig_path)

    fig_surface.savefig(fig_path,dpi=300)
    
    if surface=='Main Wing':
        surface_batch.plot_wing_forces=fig_surface
        batched_data.plot_wing_forces=surface_batch.plot_wing_forces

        batched_data.AoA_range_wing=surface_batch.AoA_range_wing
        batched_data.batch_wing_CDi=surface_batch.batch_wing_CDi
        batched_data.batch_wing_CL=surface_batch.batch_wing_CL 
    elif surface=='Horizontal Tail':
        surface_batch.plot_tail_forces=fig_surface

        batched_data.plot_tail_forces=surface_batch.plot_tail_forces
        batched_data.AoA_range_tail=surface_batch.AoA_range_tail
        batched_data.batch_tail_CDi=surface_batch.batch_tail_CDi
        batched_data.batch_tail_CL=surface_batch.batch_tail_CL 

    return batched_data 

