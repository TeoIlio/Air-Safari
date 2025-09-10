import os 
import numpy as np
import subprocess
import re
import matplotlib.pyplot as plt
from AVL_dataclasses.AVL_general_use_dataclasses import AeroSurfaces,StripData,SurfaceResults
from AVL_data_final.AVL_runcase_data_final import runcase_data_func
from AVL_data_final.AVL_geom_data_final import geometry_data_func




def AVL_strip_execution(self):  

    """
     Run AVL with the proper geometry,mass and runcase files of the parent/aircraft object. Execute the sectional analysis and derive the output in txt file.
    """
    StripData_seq="""
     LOAD {geometry_file}
     MASS {mass_file}
     CASE {runcase_file}
     OPER 
     X
     FS {aircraft_name}_strips.txt
     O

     QUIT
     """
    
    StripData_seq_params={
            "geometry_file": self.geometry_file,
            "mass_file": self.mass_file,
            "runcase_file": self.runcase_file,
            "aircraft_name": self.uav_id
             }
    

    StripData_file_path=os.path.join(self.output_path,f"{self.uav_id}_strips.txt")
   
    StripData_output = StripData_seq.format(**StripData_seq_params)
    process=subprocess.Popen(self.avl_exe_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,cwd=self.output_path)
    output, error = process.communicate(StripData_output)

    return StripData_file_path



def extract_surface_values(start_line , lines):
    """
     Exctracts needed values for each surface( Area,avg chord,CLsurf etc...) and return a dataclass of type:SurfaceResults
    """
    #keys---> names of the soon to be derived values , values--> IRT search in the file 
    relevant_vals=[]
    for line in lines[start_line : start_line+7]:
        extract_dict={
                       key:re.search(rf"{key}\s*=\s*([-+]?\d*\.\d+|\d+)",line)
                       for key in ["Surface area","Ave. chord","CLsurf","CDsurf"]
                     }
        for  key, match in extract_dict.items():
            if match:
               relevant_vals.append(float(match.group(1)))
            
    
    
    return SurfaceResults(surface_area=relevant_vals[0] , avg_chord=relevant_vals[1], CLsurf=relevant_vals[2],CDisurf=relevant_vals[3])         
    
def extract_strip_data(lines,start_line: int): 

    """
     Reads the AVL strip analysis file and derives the wanted data for a specific surface.
    """        
    strip_number,y_coords, strip_chord, strip_ccl, strip_cl, strip_ai, strip_cdi,strip_cp=[] , [] , [] , [] , [] ,[] ,[] , []
    for line in lines[start_line :]:
        data=line.split()

        if not data or line.startswith("---"): 
            break
        else:
            strip_number.append(int(data[0]))
            y_coords.append(float(data[1]))
            strip_chord.append(float(data[2]))
            strip_ccl.append(float(data[4]))
            strip_ai.append(float(data[5]))
            strip_cl.append(float(data[7]))
            strip_cdi.append(float(data[8]))
            strip_cp.append(float(data[12]))

    return StripData(strip_number=strip_number,y_coords=np.array(y_coords), strip_chord=np.array(strip_chord), strip_ccl=np.array(strip_ccl), strip_ai=np.array(strip_ai), strip_cl=np.array(strip_cl), strip_cdi=np.array(strip_cdi), strip_cp=np.array(strip_cp))


def txt_file_creation(surface: str, file_path:str, StripData: StripData):  

    """
    Creates a txt file where Strip Data are dumped, in order to later be accesses with ease.
    """
    
    with open(file_path,"a") as f:  #!!!!!!!!!!!check the append issue in combination with the delete you do --->wrong process
        f.write(f"\nStrip Data derived for the {surface}:\n" )
        f.write("Strip     Yle     Chord        c cl        ai         cl        cdi       C.Px/c\n")
        for t in range(len(StripData.strip_number)):
            f.write(f"{StripData.strip_number[t]}     {StripData.y_coords[t]}     {StripData.strip_chord[t]:.4f}     {StripData.strip_ccl[t]:.4f}     {StripData.strip_ai[t]:.4f}     {StripData.strip_cl[t]:.4f}     {StripData.strip_cdi[t]:.4f}     {StripData.strip_cp[t]:.4f}\n")

    if not os.path.exists(file_path):
        raise FileNotFoundError("Error,  no file found to dump the StripData")
    
    return None  
            
def lift_per_span(StripData_right : StripData, StripData_YDUP : StripData):

    """
    Calculates the lift force (N/m) in order to find how lift is distributed along the span.    
    """
    q=0.5*runcase_data_func().density*(runcase_data_func().velocity**2)
  
    lift = {
              "lift_right": StripData_right.strip_ccl * q ,
              "YDUP_lift": StripData_YDUP.strip_ccl * q 
            }
    return lift

   

def dimensionless_lift(StripData_right : StripData, StripData_YDUP : StripData):

    """"
    Calculates the dimensionless (normalized) lift in order to find the dimensionless lift distribution.
    **All values are referred to the reference values of the geometry template(Sref,Cref etc)
    """
    q=0.5*runcase_data_func().density*(runcase_data_func().velocity**2)    
    dless_lift = {
                   "dless_lift_right": StripData_right.strip_ccl * q / geometry_data_func().Cref,
                   "YDUP_dless_lift": StripData_YDUP.strip_ccl * q / geometry_data_func().Cref
                }
    return dless_lift


def plot(data_right : StripData, data_YDUP : StripData ,LiftData_per_span_right : list ,LiftData_per_span_YDUP: list, dimensionless_LiftData_right : list, dimensionless_LiftData_YDUP : list):

    fig, axs= plt.subplots(2 , 2 ,figsize=(20,10),layout='constrained')

    plt.grid(True)
    axs[0,0].plot(data_right.y_coords,data_right.strip_cl,marker='o',color='b')
    axs[0,0].plot(data_YDUP.y_coords,data_YDUP.strip_cl,marker='o',color='b')
    axs[0,0].set_xlabel("Wingspan (m)")
    axs[0,0].set_ylabel("Sectional cl")
    axs[0,0].set_title("Sectional coefficient of lift (cl) - Wingspan")
    axs[0,0].grid(True)
    

    axs[0,1].plot(data_right.y_coords,data_right.strip_cdi,marker='o',color='r')
    axs[0,1].plot(data_YDUP.y_coords,data_YDUP.strip_cdi,marker='o',color='r')
    axs[0,1].set_xlabel("Wingspan (m)")
    axs[0,1].set_ylabel("Sectional induced drag cdi")
    axs[0,1].set_title("Sectional coefficient of induced drag (cdi) - Wingspan")
    axs[0,1].grid(True)
    

    axs[1,0].plot(data_right.y_coords,LiftData_per_span_right,marker='o',color='g')
    axs[1,0].plot(data_YDUP.y_coords,LiftData_per_span_YDUP,marker='o',color='g')
    axs[1,0].set_xlabel("Wingspan (m)")
    axs[1,0].set_ylabel("Lift Force Distribution (N/m)")
    axs[1,0].set_title("Lift Force distribution (N/m) - Wingspan")
    axs[1,0].grid(True)
    

    axs[1,1].plot(data_right.y_coords,dimensionless_LiftData_right,marker='o',color='c')
    axs[1,1].plot(data_YDUP.y_coords,dimensionless_LiftData_YDUP,marker='o',color='c')
    axs[1,1].set_xlabel("Wingspan (m)")
    axs[1,1].set_ylabel("Dimensionless Lift Force Distribution")
    axs[1,1].set_title("Dimensionless Lift Force distribution  - Wingspan")
    axs[1,1].grid(True)
   
    plt.close(fig)
    

    return fig         

def strip_data_main(self, surface: str):

    """
     Opens the AVL file and exctract all the values needed with the help of the above functions.As output, create an object (type:AeroSurfaces) that has 
     attributes like surface specific coefficients as well as sectional.strip specific data.
    """
    StripDataPath=AVL_strip_execution(self)

    if not os.path.exists(StripDataPath): 
       raise FileNotFoundError("Error: AVL analysis file not found. Try running the sectional analysis first.")
    
    with open(StripDataPath,"r") as f :
        lines=f.readlines() 
        #file= "".join(lines)  


        #create file , if it previously existed then it will get deleted    
        StripData_txt_file_path=os.path.join(self.output_path,f"{self.uav_id}_StripData.txt")

         # initialize to None
        section_relevant_right = None
        strip_data_right = None
        section_relevant_YDUP = None
        strip_data_YDUP = None

        for flag,line in enumerate(lines):
            if f"{surface}" in line:
                section_relevant_right=extract_surface_values(start_line=flag,lines=lines)
                strip_data_right=extract_strip_data(lines=lines,start_line=flag+14)
                txt_file_creation(surface,StripData_txt_file_path,strip_data_right)
                break
        
        flag=0
        for flag,line in enumerate(lines):
            if f"{surface} (YDUP)" in line:
                section_relevant_YDUP=extract_surface_values(start_line=flag, lines=lines)
                strip_data_YDUP=extract_strip_data(lines=lines,start_line=flag+14)
                txt_file_creation(f"{surface}_YDUP",StripData_txt_file_path,strip_data_YDUP)
                break   

    lift=lift_per_span(StripData_right=strip_data_right, StripData_YDUP=strip_data_YDUP)
    dless_lift=dimensionless_lift(StripData_right=strip_data_right, StripData_YDUP=strip_data_YDUP)
    lift_right=lift["lift_right"]  
    lift_YDUP=lift["YDUP_lift"]
    dless_lift_right=dless_lift["dless_lift_right"]
    dless_YDUP_lift=dless_lift["YDUP_dless_lift"]

    figure=plot(data_right=strip_data_right, data_YDUP=strip_data_YDUP,LiftData_per_span_right=lift_right, LiftData_per_span_YDUP=lift_YDUP,dimensionless_LiftData_right=dless_lift_right, dimensionless_LiftData_YDUP=dless_YDUP_lift) 
    if os.path.exists(os.path.join(self.output_path,f"{self.uav_id}_{surface}_plots.png")):
        os.remove(os.path.join(self.output_path,f"{self.uav_id}_{surface}_plots.png"))

    figure.savefig(os.path.join(self.output_path,f"{self.uav_id}_{surface}_plots.png"),dpi=300)

    return AeroSurfaces(name=self.uav_id, surface=surface, 
                        section_relevant_right=section_relevant_right, 
                        section_relevant_YDUP=section_relevant_YDUP,
                        strip_data_right=strip_data_right ,
                        strip_data_YDUP=strip_data_YDUP,
                        plot_lift=figure
                        )       




