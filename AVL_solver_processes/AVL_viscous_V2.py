import os 
import numpy as np 
from numpy.typing import NDArray
import subprocess
import matplotlib.pyplot as plt 
from scipy.interpolate import interp1d
from scipy import integrate 
from AVL_dataclasses.AVL_general_use_dataclasses import AeroSurfaces,StripData,SurfaceResults
from AVL_data_final.AVL_runcase_data_final import runcase_data_func
from AVL_data_final.AVL_geom_data_final import geometry_data_func


def Reynolds_calculation(AeroSurface : AeroSurfaces):
    """
    Reynolds Number calculator. A dataclass reffering to a surface serves as input , from which strip chords are derived.
    """
    reynolds=[]
    m_greek=1.81 * 10**(-5)  # dynamic viscocity, manual set
    reynolds=runcase_data_func().density * runcase_data_func().velocity * AeroSurface.strip_data_right.strip_chord /m_greek

    return np.array(reynolds)


def xfoil_viscous_process():
    """
    Xfoil sequence to run a viscous analysis with forced Reynolds and Cl value. Includes airfoil refinement and iteration number change for better convergence. 
    """

    xfoil_sequence="""
     LOAD {airfoil}.dat
     PANE
     OPER
     VISC
     {reynolds}
     PACC
     {aircraft_name}_viscous_strip{flag}.txt
    
     ITER 
     150
     CL
     {strip_cl}
     \n
     QUIT
     """
    
    return xfoil_sequence



def data_interpolations(strip_data_cd ,strip_data_y_coords : NDArray[np.float64], strip_data_chords : NDArray[np.float64]):   
    """
    Interpolates data . CD values derived from xfoil may include None values due to unconverged cases. CD values are cleaned from None values and interpolated
    quadratically. Y coordinates ,as well as chord values, get denser in order to complete the interpolation based on their size. Chord values get denser in order
    to compute the product of chord-times-Cd value( needed for the integrations). Inputs are data that are part of a  dataclass (type StripData)
    """
    #TOTAL CD VALUES QUADRATIC INTERPOLATION

    mask=strip_data_cd != None # boolean type mask .True when float ,false when None  
    strip_data_clean=strip_data_cd[mask].astype(float)
    y_clean=strip_data_y_coords[mask]     
    f=interp1d(y_clean,strip_data_clean,kind='quadratic')  # quadratic interpolation based the cleaned data 

    if y_clean[0]<0 : # if check, negative values create miss match between coords values and cd values-->reversed coord linspace
       y_dense = np.linspace(max(y_clean), min(y_clean), 40)  # create the dense data of your choice
    else:
       y_dense = np.linspace(min(y_clean), max(y_clean), 40)  # create the dense data of your choice 

    chord_dense=np.linspace(max(strip_data_chords),min(strip_data_chords),40)
    strip_data_cd_new = f(y_dense) 
    strip_data_c_cd=chord_dense*strip_data_cd_new
   
    return strip_data_cd_new,strip_data_c_cd,y_dense  # return the final interpolated data 

def trapezoid_integration(strip_data_type : NDArray[np.float64], y_coords_dense: NDArray[np.float64] ):  
     
     """
     Numerical integration with the trapezoid method for drag related data. Inputs used are interpolated data (type c*cd).
     """
     strip_data_integrated=integrate.trapezoid(strip_data_type ,x=abs(y_coords_dense)) / (geometry_data_func().Sref)
     
     return strip_data_integrated

def extract_visc_surface_results( surface_results : SurfaceResults, integrated_cdv: float, integrated_cdf: float, integrated_cdp : float):  # HALF SURFACE values are gonna be placed here so integrated CDv,CDf,CDp need to be already ready and input
   
   """
   Fully fill the SurfaceResults dataclass with the cd values. Function will be called for each half surface of the aircraft.
   """
   surface_results.CDvsurf=integrated_cdv
   surface_results.CDfsurf=integrated_cdf
   surface_results.CDpsurf=integrated_cdp
   
   return surface_results

def combined_aerodynamic_results(self, main_wing : AeroSurfaces , horizontal_tail: AeroSurfaces):
    """
    File creation with the complete data from the aerodynamic analysis.
    """
    results_path=os.path.join(self.output_path,f"{self.uav_id}_aerodynamic_results.txt")
    

    with open(results_path,"w") as f :
       f.write(f"{self.uav_id} aircraft total aerodynamic analysis results:\n\n")
       f.write(f"Wing Airfoil:  {os.path.basename(geometry_data_func().Wing_airfoil)}\n")
       f.write(f"Horizontal Tail Airfoil:  {os.path.basename(geometry_data_func().Htail_airfoil)}\n")
       f.write(f"AoA:{runcase_data_func().AoA} degrees    Sideslip:{runcase_data_func().sideslip} degrees    Velocity:{runcase_data_func().velocity}\n")
       f.write(f"Pitch Rate:{runcase_data_func().pitch_rate}     Yaw Rate:{runcase_data_func().yaw_rate}    Roll rate:{runcase_data_func().roll_rate}    Climb angle:{runcase_data_func().climb_angle} degrees\n")
       f.write(f"Elevator deflection:{runcase_data_func().elevator_def} degrees    Aileron deflection:{runcase_data_func().aileron_def} degrees    Rudder deflection:{runcase_data_func().rudder_def} degrees\n\n")
       
       
       f.write("Main wing aerodynamic results are:\n")    
       f.write(f"Surface Area:{2*main_wing.section_relevant_right.surface_area:.5f}     ")
       f.write(f"Average Chord:{main_wing.section_relevant_right.avg_chord:.5f}\n")
       f.write(f"Right half wing CL:{main_wing.section_relevant_right.CLsurf:.5f}\n")
       f.write(f"Right half wing CDi:{main_wing.section_relevant_right.CDisurf:.5f}\n")
       f.write(f"Right half wing CDv:{main_wing.section_relevant_right.CDvsurf:.5f}\n")
       f.write(f"Right half wing CDf:{main_wing.section_relevant_right.CDfsurf:.5f}\n")
       f.write(f"Right half wing CDp:{main_wing.section_relevant_right.CDpsurf:.5f}\n\n")

       f.write(f"Left half wing CL:{main_wing.section_relevant_YDUP.CLsurf:.5f}\n")
       f.write(f"Left half wing CDi:{main_wing.section_relevant_YDUP.CDisurf:.5f}\n")
       f.write(f"Left half wing CDv:{main_wing.section_relevant_YDUP.CDvsurf:.5f}\n")
       f.write(f"Left half wing CDf:{main_wing.section_relevant_YDUP.CDfsurf:.5f}\n")
       f.write(f"Left half wing CDp:{main_wing.section_relevant_YDUP.CDpsurf:.5f}\n\n")
  
       f.write(f"Main wing CL:{main_wing.section_relevant_YDUP.CLsurf+main_wing.section_relevant_right.CLsurf:.5f}\n")
       f.write(f"Main wing CDi:{main_wing.section_relevant_YDUP.CDisurf+main_wing.section_relevant_right.CDisurf:.5f}\n")
       f.write(f"Main wing CDf:{main_wing.section_relevant_YDUP.CDfsurf+main_wing.section_relevant_right.CDfsurf:.5f}\n")
       f.write(f"Main wing CDp:{main_wing.section_relevant_YDUP.CDpsurf+main_wing.section_relevant_right.CDpsurf:.5f}\n")
       f.write(f"Main wing CDv:{main_wing.section_relevant_YDUP.CDvsurf+main_wing.section_relevant_right.CDvsurf:.5f}\n")
       f.write(f"Main wing total CD:{main_wing.section_relevant_YDUP.CDvsurf+main_wing.section_relevant_right.CDvsurf+main_wing.section_relevant_YDUP.CDisurf+main_wing.section_relevant_right.CDisurf:.5f}\n\n") 

       f.write("Horizontal Tail aerodynamic results are:\n")    
       f.write(f"Surface Area:{2*horizontal_tail.section_relevant_right.surface_area:.5f}     ")
       f.write(f"Average Chord:{horizontal_tail.section_relevant_right.avg_chord:.5f}\n")
       f.write(f"Right half hor. tail CL:{horizontal_tail.section_relevant_right.CLsurf:.5f}\n")
       f.write(f"Right half hor. tail CDi:{horizontal_tail.section_relevant_right.CDisurf:.5f}\n")
       f.write(f"Right half hor. tail CDv:{horizontal_tail.section_relevant_right.CDvsurf:.5f}\n")
       f.write(f"Right half hor. tail CDf:{horizontal_tail.section_relevant_right.CDfsurf:.5f}\n")
       f.write(f"Right half hor. tail CDp:{horizontal_tail.section_relevant_right.CDpsurf:.5f}\n\n")

       f.write(f"Left half hor. tail CL:{horizontal_tail.section_relevant_YDUP.CLsurf:.5f}\n")
       f.write(f"Left half hor. tail CDi:{horizontal_tail.section_relevant_YDUP.CDisurf:.5f}\n")
       f.write(f"Left half hor. tail CDv:{horizontal_tail.section_relevant_YDUP.CDvsurf:.5f}\n")
       f.write(f"Left half hor. tail CDf:{horizontal_tail.section_relevant_YDUP.CDfsurf:.5f}\n")
       f.write(f"Left half hor. tail CDp:{horizontal_tail.section_relevant_YDUP.CDpsurf:.5f}\n\n")

       f.write(f"Horizontal Tail CL:{horizontal_tail.section_relevant_YDUP.CLsurf+horizontal_tail.section_relevant_right.CLsurf:.5f}\n")
       f.write(f"Horizontal Tail CDi:{horizontal_tail.section_relevant_YDUP.CDisurf+horizontal_tail.section_relevant_right.CDisurf:.5f}\n")
       f.write(f"Horizontal Tail CDf:{horizontal_tail.section_relevant_YDUP.CDfsurf+horizontal_tail.section_relevant_right.CDfsurf:.5f}\n")
       f.write(f"Horizontal Tail CDp:{horizontal_tail.section_relevant_YDUP.CDpsurf+horizontal_tail.section_relevant_right.CDpsurf:.5f}\n")
       f.write(f"Horizontal Tail CDv:{horizontal_tail.section_relevant_YDUP.CDvsurf+horizontal_tail.section_relevant_right.CDvsurf:.5f}\n")
       f.write(f"Horizontal Tail total CD:{horizontal_tail.section_relevant_YDUP.CDvsurf+horizontal_tail.section_relevant_right.CDvsurf+horizontal_tail.section_relevant_YDUP.CDisurf+horizontal_tail.section_relevant_right.CDisurf:.5f}\n\n") 
       
       f.write(f"Total Aircraft combined aerodynamic results:\n")
       f.write(f"Aircraft CL:{main_wing.section_relevant_YDUP.CLsurf+main_wing.section_relevant_right.CLsurf+horizontal_tail.section_relevant_YDUP.CLsurf+horizontal_tail.section_relevant_right.CLsurf:.5f}\n")
       f.write(f"Aircraft CD:{main_wing.section_relevant_YDUP.CDisurf+main_wing.section_relevant_right.CDisurf+horizontal_tail.section_relevant_YDUP.CDisurf+horizontal_tail.section_relevant_right.CDisurf+main_wing.section_relevant_YDUP.CDvsurf+main_wing.section_relevant_right.CDvsurf+horizontal_tail.section_relevant_YDUP.CDvsurf+horizontal_tail.section_relevant_right.CDvsurf:.5f}")

      
    if not os.path.exists(results_path):
        raise FileNotFoundError("Error with the File creation")   

    return None 


# take as input a dataclass AeroSurfaces--->fill it with rest of the data-----> needed when 2 half surface are made--> 2 stripData are fully created , then AeroSurface gets updated
def extract_visc_strip_data(self,strip_data : StripData , xfoil_viscous_sequence, reynolds : NDArray[np.float64]) :
    """
    Runs xfoil analysis iteratively,saves the output and collects the data in arrays which will fill a half-filled StripData dataclass.
    The fully-filled StripData dataclass will later be used to refresh an AeroSurface dataclass with all the correlated viscous data.
    """
    flag_v1=0
    strip_cdv, strip_cdf, strip_cdp, strip_top_transition, strip_bot_transition=[] , [] , [] , [] , []  # initialize lists ---> to be transformed to arrays
    for flag_v1, cl_value in enumerate(strip_data.strip_cl):   # iterate for every value in the array 
    # use flag as index, cl_val as CL value
        xfoil_params={
                      "airfoil" : geometry_data_func().Wing_airfoil,  # grab it from the stored data
                      "reynolds":reynolds[flag_v1],  # Re list is an attribute 
                      "aircraft_name":self.uav_id,    # uav_id is an attribute 
                      "flag": flag_v1, 
                      "strip_cl":cl_value   # strip cl 
                    }
      
        xfoil_commands = xfoil_viscous_sequence.format(**xfoil_params)
        process = subprocess.Popen(self.xfoil_exe_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,cwd=self.output_path)
        output, error = process.communicate(xfoil_commands)

        visc_file_path=os.path.join(self.output_path,f"{self.uav_id}_viscous_strip{flag_v1}.txt")  # xfoil analysis file 
        
        
        if not os.path.exists(visc_file_path):
            raise FileNotFoundError("Error, no xfoil analysis file found.")
      
        with open(visc_file_path,"r") as f :
            lines=f.readlines()
        
        flag_v2=0
        read_line=None
        for flag_v2,line in enumerate(lines):
            if "alpha" in line :
               read_line=flag_v2+2 # it starts reading at this point 
               break

        
        if  read_line==len(lines):
           
           strip_cdv.append(None)
           strip_cdf.append(None)
           strip_cdp.append(None)
           strip_top_transition.append(None)
           strip_bot_transition.append(None) 
        else: 
           data_line=lines[read_line].split()
           strip_cdv.append(float(data_line[2]))
           strip_cdf.append(float(data_line[2])-float(data_line[3]))
           strip_cdp.append(float(data_line[3]))
           strip_top_transition.append(float(data_line[5]))
           strip_bot_transition.append(float(data_line[6]))

        os.remove(visc_file_path)   # remove the analysis file 

     #Refresh the dataclass 
    strip_data.strip_cdv=np.array(strip_cdv,dtype=object) 
    strip_data.strip_cdf=np.array(strip_cdf,dtype=object) 
    strip_data.strip_cdp=np.array(strip_cdp,dtype=object) 
    strip_data.strip_top_transition=np.array(strip_top_transition,dtype=object) 
    strip_data.strip_bot_transition=np.array(strip_bot_transition,dtype=object)  

    return strip_data   # return the fully-filled dataclass (type StripData)--> for half surface


def  plots(data_right : StripData, data_YDUP : StripData , CDv_right: NDArray[np.float64] , CDf_right: NDArray[np.float64] , CDp_right : NDArray[np.float64],CDv_YDUP: NDArray[np.float64] , CDf_YDUP: NDArray[np.float64] , CDp_YDUP : NDArray[np.float64],CCDv_right : NDArray[np.float64],CCDv_YDUP: NDArray[np.float64],CCDi_right: NDArray[np.float64],CCDi_YDUP : NDArray[np.float64],y_coords_dense : NDArray[np.float64] ):

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

def stuttgart(strip_data_type : NDArray[np.float64], y_coords: NDArray[np.float64], strip_data_chords : NDArray[np.float64],surface: str):
    """
    Claculation of drag values with Akamodell Stuttgart's methodology. This methodology uses local strip area. Strip surfaces are given from AVL during the strip analysis.
    Since data interpolation takes place , an approximation of local Si is going to be made: Si=chord*dy=chord*(y[i+1]-y[i]).The approximation does not give more than 5% deviation.
    Input any data type (cdv,cdf etc) , the corresponding surface wingspan coordinates (denser,after interpolation) and chord data.
    """
    if surface=='main wing':
       Bref=geometry_data_func().Bref
       Sref=geometry_data_func().Sref
       
    elif surface=='horizontal tail':
        Bref=geometry_data_func().Htail_halfspan*2
        Sref=geometry_data_func().Sref   
       
    chords=np.linspace(max(strip_data_chords),min(strip_data_chords),40)
    dy = []
    for i in range(len(y_coords)):
       if i == 0:
           dy_l = y_coords[i+1] - y_coords[i]
       elif i == len(y_coords) - 1:
          dy_l = (Bref/2) - y_coords[i]
       else:
           dy_l = y_coords[i+1] - y_coords[i]
       dy.append(dy_l) 

    Si=chords*dy 
    total_value=np.sum(strip_data_type * Si) / (Sref) 
   
    return total_value
  

def viscous_main(self,main_wing: AeroSurfaces , horizontal_tail: AeroSurfaces ):  # fill the AeroSurfaces dataclasses
    
    reynolds_main_wing=Reynolds_calculation(main_wing)
    reynolds_hor_tail=Reynolds_calculation(horizontal_tail)
    xfoil_seq=xfoil_viscous_process()

    main_wing.strip_data_right=extract_visc_strip_data(self,strip_data=main_wing.strip_data_right,xfoil_viscous_sequence=xfoil_seq,reynolds=reynolds_main_wing) #right wing
    main_wing.strip_data_YDUP=extract_visc_strip_data(self,strip_data=main_wing.strip_data_YDUP,xfoil_viscous_sequence=xfoil_seq,reynolds=reynolds_main_wing) # Left wing
    horizontal_tail.strip_data_right=extract_visc_strip_data(self,strip_data=horizontal_tail.strip_data_right,xfoil_viscous_sequence=xfoil_seq,reynolds=reynolds_hor_tail)
    horizontal_tail.strip_data_YDUP=extract_visc_strip_data(self,strip_data=horizontal_tail.strip_data_YDUP,xfoil_viscous_sequence=xfoil_seq,reynolds=reynolds_hor_tail)
 

 #Data Interpolation  
    # Main Wing interpolated data
    main_wing_right_cdv,main_wing_right_cCDv,y_wing_right_CDv=data_interpolations(main_wing.strip_data_right.strip_cdv,main_wing.strip_data_right.y_coords,main_wing.strip_data_right.strip_chord) # right cdv wing 
    main_wing_YDUP_cdv,main_wing_YDUP_cCDv,y_wing_YDUP_CDv=data_interpolations(main_wing.strip_data_YDUP.strip_cdv,main_wing.strip_data_YDUP.y_coords, main_wing.strip_data_YDUP.strip_chord) # YDUP cdv wing
    

    main_wing_right_cdf,main_wing_right_cCDf,y_wing_right_CDf=data_interpolations(main_wing.strip_data_right.strip_cdf,main_wing.strip_data_right.y_coords, main_wing.strip_data_right.strip_chord) # right cdf wing 
    main_wing_YDUP_cdf,main_wing_YDUP_cCDf,y_wing_YDUP_CDf=data_interpolations(main_wing.strip_data_YDUP.strip_cdf,main_wing.strip_data_YDUP    .y_coords, main_wing.strip_data_YDUP.strip_chord) # YDUP cdf wing

    main_wing_right_cdp,main_wing_right_cCDp,y_wing_right_CDp=data_interpolations(main_wing.strip_data_right.strip_cdp,main_wing.strip_data_right.y_coords, main_wing.strip_data_right.strip_chord) # right cdp wing 
    main_wing_YDUP_cdp,main_wing_YDUP_cCDp,y_wing_YDUP_CDp=data_interpolations(main_wing.strip_data_YDUP.strip_cdp,main_wing.strip_data_YDUP.y_coords, main_wing.strip_data_YDUP.strip_chord) # YDUP cdp wing

    main_wing_right_cdi,main_wing_right_cCDi,y_wing_right_CDi=data_interpolations(main_wing.strip_data_right.strip_cdi,main_wing.strip_data_right.y_coords, main_wing.strip_data_right.strip_chord) # right cdi wing 
    main_wing_YDUP_cdi,main_wing_YDUP_cCDi,y_wing_YDUP_CDi=data_interpolations(main_wing.strip_data_YDUP.strip_cdi,main_wing.strip_data_YDUP.y_coords, main_wing.strip_data_YDUP.strip_chord) # YDUP cdi wing

    # Horizontal Tail Interpolated Data
    hor_tail_right_cdv,hor_tail_right_cCDv,y_tail_right_CDv=data_interpolations(horizontal_tail.strip_data_right.strip_cdv,horizontal_tail.strip_data_right.y_coords, horizontal_tail.strip_data_right.strip_chord) # tail cdv 
    hor_tail_YDUP_cdv,hor_tail_YDUP_cCDv,y_tail_YDUP_CDv=data_interpolations(horizontal_tail.strip_data_YDUP.strip_cdv,horizontal_tail.strip_data_YDUP.y_coords,  horizontal_tail.strip_data_YDUP.strip_chord)  # tail cdv YDUP

    hor_tail_right_cdf,hor_tail_right_cCDf,y_tail_right_CDf=data_interpolations(horizontal_tail.strip_data_right.strip_cdf,horizontal_tail.strip_data_right.y_coords, horizontal_tail.strip_data_right.strip_chord) # tail cdf 
    hor_tail_YDUP_cdf,hor_tail_YDUP_cCDf,y_tail_YDUP_CDf=data_interpolations(horizontal_tail.strip_data_YDUP.strip_cdf,horizontal_tail.strip_data_YDUP.y_coords, horizontal_tail.strip_data_YDUP.strip_chord)  # tail cdf YDUP

    hor_tail_right_cdp,hor_tail_right_cCDp,y_tail_right_CDp=data_interpolations(horizontal_tail.strip_data_right.strip_cdp,horizontal_tail.strip_data_right.y_coords, horizontal_tail.strip_data_right.strip_chord) # tail cdp 
    hor_tail_YDUP_cdp,hor_tail_YDUP_cCDp,y_tail_YDUP_CDp=data_interpolations(horizontal_tail.strip_data_YDUP.strip_cdp,horizontal_tail.strip_data_YDUP.y_coords, horizontal_tail.strip_data_YDUP.strip_chord)  # tail cdp YDUP


    hor_tail_right_cdi,hor_tail_right_cCDi,y_tail_right_CDi=data_interpolations(horizontal_tail.strip_data_right.strip_cdi,horizontal_tail.strip_data_right.y_coords, horizontal_tail.strip_data_right.strip_chord) # tail cdi 
    hor_tail_YDUP_cdi,hor_tail_YDUP_cCDi,y_tail_YDUP_CDi=data_interpolations(horizontal_tail.strip_data_YDUP.strip_cdi,horizontal_tail.strip_data_YDUP.y_coords, horizontal_tail.strip_data_YDUP.strip_chord)  # tail cdi YDUP

 # INTEGRATIONS 
    
    main_wing_right_CDv_integ=trapezoid_integration(main_wing_right_cCDv,y_wing_right_CDv) 
    main_wing_YDUP_CDv_integ=trapezoid_integration(main_wing_YDUP_cCDv,y_wing_YDUP_CDv)

    main_wing_right_CDf_integ=trapezoid_integration(main_wing_right_cCDf,y_wing_right_CDf)
    main_wing_YDUP_CDf_integ=trapezoid_integration(main_wing_YDUP_cCDf,y_wing_YDUP_CDf)

    main_wing_right_CDp_integ=trapezoid_integration(main_wing_right_cCDp,y_wing_right_CDp)
    main_wing_YDUP_CDp_integ=trapezoid_integration(main_wing_YDUP_cCDp,y_wing_YDUP_CDp)

    #only for benchmark purposes
    main_wing_right_CDi_integ=trapezoid_integration(main_wing_right_cCDi,y_wing_right_CDi)
    main_wing_YDUP_CDi_integ=trapezoid_integration(main_wing_YDUP_cCDi,y_wing_YDUP_CDi)

    hor_tail_right_CDv_integ=trapezoid_integration(hor_tail_right_cCDv,y_tail_right_CDv)
    hor_tail_YDUP_CDv_integ=trapezoid_integration(hor_tail_YDUP_cCDv,y_tail_YDUP_CDv)

    hor_tail_right_CDf_integ=trapezoid_integration(hor_tail_right_cCDf,y_tail_right_CDf)
    hor_tail_YDUP_CDf_integ=trapezoid_integration(hor_tail_YDUP_cCDf,y_tail_YDUP_CDf)

    hor_tail_right_CDp_integ=trapezoid_integration(hor_tail_right_cCDp,y_tail_right_CDp)
    hor_tail_YDUP_CDp_integ=trapezoid_integration(hor_tail_YDUP_cCDp,y_tail_YDUP_CDp)
 
    #only for benchmark purposes
    hor_tail_right_CDi_integ=trapezoid_integration(hor_tail_right_cCDi,y_tail_right_CDi)
    hor_tail_YDUP_CDi_integ=trapezoid_integration(hor_tail_YDUP_cCDi,y_tail_YDUP_CDi)

 #Stuttgart method

 
    main_wing_right_stut_cdv=stuttgart(main_wing_right_cdv,y_wing_right_CDv , main_wing.strip_data_right.strip_chord,'main wing')
    main_wing_YDUP_stut_cdv=stuttgart(main_wing_YDUP_cdv,y_wing_right_CDv, main_wing.strip_data_YDUP.strip_chord,'main wing')


    main_wing_right_stut_cdf=stuttgart(main_wing_right_cdf,y_wing_right_CDf , main_wing.strip_data_right.strip_chord,'main wing')
    main_wing_YDUP_stut_cdf=stuttgart(main_wing_YDUP_cdf,y_wing_right_CDf, main_wing.strip_data_YDUP.strip_chord,'main wing')


    main_wing_right_stut_cdp=stuttgart(main_wing_right_cdp,y_wing_right_CDp , main_wing.strip_data_right.strip_chord,'main wing')
    main_wing_YDUP_stut_cdp=stuttgart(main_wing_YDUP_cdp,y_wing_right_CDp, main_wing.strip_data_YDUP.strip_chord,'main wing')

    hor_tail_right_stut_cdv=stuttgart(hor_tail_right_cdv,y_tail_right_CDv , horizontal_tail.strip_data_right.strip_chord,'horizontal tail')
    hor_tail_YDUP_stut_cdv=stuttgart(hor_tail_YDUP_cdv,y_tail_right_CDv, horizontal_tail.strip_data_YDUP.strip_chord,'horizontal tail')


    hor_tail_right_stut_cdf=stuttgart(hor_tail_right_cdf,y_tail_right_CDf , horizontal_tail.strip_data_right.strip_chord,'horizontal tail')
    hor_tail_YDUP_stut_cdf=stuttgart(hor_tail_YDUP_cdf,y_tail_right_CDf, horizontal_tail.strip_data_YDUP.strip_chord,'horizontal tail')


    hor_tail_right_stut_cdp=stuttgart(hor_tail_right_cdp,y_tail_right_CDp , horizontal_tail.strip_data_right.strip_chord,'horizontal tail')
    hor_tail_YDUP_stut_cdp=stuttgart(hor_tail_YDUP_cdp,y_tail_right_CDp, horizontal_tail.strip_data_YDUP.strip_chord,'horizontal tail')


    #MAIN WING AND HORIZONTAL TAIL FINAL SECTION RELATED DATA
    main_wing.section_relevant_right=extract_visc_surface_results(surface_results=main_wing.section_relevant_right,integrated_cdv=main_wing_right_CDv_integ,integrated_cdf=main_wing_right_CDf_integ,integrated_cdp=main_wing_right_CDp_integ)
    main_wing.section_relevant_YDUP=extract_visc_surface_results(surface_results=main_wing.section_relevant_YDUP,integrated_cdv=main_wing_YDUP_CDv_integ,integrated_cdf=main_wing_YDUP_CDf_integ,integrated_cdp=main_wing_YDUP_CDp_integ)

    horizontal_tail.section_relevant_right=extract_visc_surface_results(surface_results=horizontal_tail.section_relevant_right,integrated_cdv=hor_tail_right_CDv_integ,integrated_cdf=hor_tail_right_CDf_integ,integrated_cdp=hor_tail_right_CDp_integ)
    horizontal_tail.section_relevant_YDUP=extract_visc_surface_results(surface_results=horizontal_tail.section_relevant_YDUP,integrated_cdv=hor_tail_YDUP_CDv_integ,integrated_cdf=hor_tail_YDUP_CDf_integ,integrated_cdp=hor_tail_YDUP_CDp_integ)

    combined_aerodynamic_results(self,main_wing=main_wing, horizontal_tail=horizontal_tail)
    fig_wing=plots(data_right=main_wing.strip_data_right,
                   data_YDUP=main_wing.strip_data_YDUP,
                   CDv_right=main_wing_right_cdv,
                   CDf_right=main_wing_right_cdf,
                   CDp_right=main_wing_right_cdp,
                   CDv_YDUP=main_wing_YDUP_cdv,
                   CDf_YDUP=main_wing_YDUP_cdf,
                   CDp_YDUP=main_wing_YDUP_cdp,
                   CCDv_right=main_wing_right_cCDv,
                   CCDv_YDUP=main_wing_YDUP_cCDv,
                   CCDi_right=main_wing_right_cCDi,
                   CCDi_YDUP=main_wing_YDUP_cCDi,
                   y_coords_dense=y_wing_right_CDv
                   )
    if os.path.exists(os.path.join(self.output_path,f"{self.uav_id}_main_wing_drag_plots.png")):
        os.remove(os.path.join(self.output_path,f"{self.uav_id}_main_wing_drag_plots.png"))

    fig_wing.savefig(os.path.join(self.output_path,f"{self.uav_id}_main_wing_drag_plots.png"),dpi=300)
    main_wing.plot_viscous=fig_wing
    
    fig_tail=plots(data_right=horizontal_tail.strip_data_right,
                   data_YDUP=horizontal_tail.strip_data_YDUP,
                   CDv_right=hor_tail_right_cdv,
                   CDf_right=hor_tail_right_cdf,
                   CDp_right=hor_tail_right_cdp,
                   CDv_YDUP=hor_tail_YDUP_cdv,
                   CDf_YDUP=hor_tail_YDUP_cdf,
                   CDp_YDUP=hor_tail_YDUP_cdp,
                   CCDv_right=hor_tail_right_cCDv,
                   CCDv_YDUP=hor_tail_YDUP_cCDv,
                   CCDi_right=hor_tail_right_cCDi,
                   CCDi_YDUP=hor_tail_YDUP_cCDi,
                   y_coords_dense=y_tail_right_CDv
                   )
    if os.path.exists(os.path.join(self.output_path,f"{self.uav_id}_hor_tail_drag_plots.png")):
        os.remove(os.path.join(self.output_path,f"{self.uav_id}_hor_tail_drag_plots.png"))

    fig_tail.savefig(os.path.join(self.output_path,f"{self.uav_id}_hor_tail_drag_plots.png"),dpi=300)
    horizontal_tail.plot_viscous=fig_tail

    return main_wing,horizontal_tail

