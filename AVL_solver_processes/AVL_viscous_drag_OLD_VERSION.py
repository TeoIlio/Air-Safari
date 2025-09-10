#Calculation of viscous drag. The estimation will be made with the use of AVL and xfoil
#Main idea is to derive the loca/sectional cl values of the wing/surface and force them for an airfoil in xfoil. 
# In this way ,the local/sectional viscous drag can be derived. The process will be don for each strip. 
#Upon completion, the viscous drag distribution can be plotted (N/m) and the total viscous drag can be derived with integration.

import os 
import numpy as np
import subprocess
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
from scipy import integrate
from scipy.interpolate import interp1d
from AVL_solver_processes.AVL_lift_distribution import lift_distribution_derivation 
from AVL_solver_processes.AVL_lift_distribution import lift_dist_plots
from AVL_data_final.AVL_geom_data_final import geometry_data_func




def re_calculation(self):
    chord_list=np.array(self.chord_values)
    reynolds=np.array([])
    reynolds=1.225*self.velocity*chord_list/(1.81*(10**-5))
    length=len(chord_list)
    print(reynolds)
    return reynolds    


def viscous_drag(self):
    
    xfoil_visc_seq="""
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
    

    cd_total_values=[]
    cd_press_values=[]
    cd_friction_values=[]
    top_trans_values=[]
    bot_trans_values=[]
    
    for flag, cl_val in enumerate(self.cl_values_right):   # iterate for every value in the array 
    # use flag as index, cl_val as CL value
      xfoil_visc_params={
        "airfoil" : geometry_data_func().Wing_airfoil,  # grab it from the stored data
        "reynolds":self.reynolds[flag],  # Re list is an attribute 
        "aircraft_name":self.uav_id,    # uav_id is an attribute 
        "flag": flag, 
        "strip_cl":cl_val
 
        }
      
      xfoil_commands = xfoil_visc_seq.format(**xfoil_visc_params)
      process = subprocess.Popen(self.xfoil_exe_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,cwd=self.output_path)
      output, error = process.communicate(xfoil_commands)

      visc_file_path=os.path.join(self.output_path,f"{self.uav_id}_viscous_strip{flag}.txt")
      

      if os.path.exists(visc_file_path):
        with open(visc_file_path,"r") as f:  # open the file , read the lines and find the starting line 
            lines=f.readlines()
            for t, line in enumerate(lines):
                if "alpha" in line:
                    read=t+2    # flag type variable, represents the starting line 
                    break
                           
            
            
            #print(len(lines))
            #print("read is",read)
            if  read==len(lines) :    # this case means that the analysis has failed/did not converge
              cd_total_values.append(None)
              cd_press_values.append(None)
              cd_friction_values.append(None)
              top_trans_values.append(None)
              bot_trans_values.append(None)
            elif read==len(lines)-1:   # analysis has converged
              values=lines[read].split()  
              cd_total_values.append(float(values[2]))
              cd_press_values.append(float(values[3]))
              cd_friction_values.append(float(values[2])-float(values[3]))
              top_trans_values.append(float(values[5]))
              bot_trans_values.append(float(values[6]))
               
                    
        read=0
        t=0
        os.remove(visc_file_path)   # remove the analysis file 
      else:
          print('Error, no file found')
    
    cd_values_path=os.path.join(self.output_path,f"{self.uav_id}_cd_values.txt")
    with open(cd_values_path,"w") as f:
       for cd_val in cd_total_values:
          f.write(f"{cd_val}\n")

    

    return cd_total_values,cd_press_values,cd_friction_values,top_trans_values,bot_trans_values



def acts_and_plots(self):

  """
   This function includes the numerical integrations of CL and CD. Two Newton-Cotes methods are going to be used from scipy library. Also this function includes the
   plots. For the plots and integration , a quadratic interpolation of the original data is going to be executed. The interpolated data will be used for plots and
   for integration with simpson rule.
  """
  
  """
  For the quadratic interpolation: Use of interp1d method. Create an array with elements that are type: object. In this way if NONE values exist they are included.
  Create a mask variable that is type:BOOLEAN and is true only for float elements and False for None elements. Create a new array (so called clean) that will include
  only the float elements. Based on the clean version of the data, a quadratic interpolation will take place with interp1d. 
  """

  #TOTAL CD VALUES QUADRATIC INTERPOLATION
  cd_total_array=np.array(self.cd_list,dtype=object)  # set array elements as type object so they can include None values. self.cd_list attribute taken from class
  y_array=np.array(self.y_values_right) # y values are the positions of strips in the wing -> attribute of the class
  mask1=cd_total_array != None # boolean type mask .True when float ,false when None  
  cd_clean=cd_total_array[mask1].astype(float)
  y_clean=y_array[mask1]     
  f=interp1d(y_clean,cd_clean,kind='quadratic')  # quadratic
  y_dense = np.linspace(min(y_clean), max(y_clean), 100)
  cd_new = f(y_dense)


  # FRICTION CD QUADRATIC INTERPOLATION
  cd_friction_array=np.array(self.cd_friction_list,dtype=object)  
  mask2=cd_friction_array != None 
  cd_friction_clean=cd_friction_array[mask2].astype(float) 
  f=interp1d(y_clean,cd_friction_clean,kind='quadratic')  # quadratic
  cd_friction_new = f(y_dense)


  #PRESSURE CD QUADRATIC INTERPOLATION
  cd_press_array=np.array(self.cd_press_list,dtype=object)    
  mask3=cd_press_array != None 
  cd_press_clean=cd_press_array[mask3].astype(float)       
  f=interp1d(y_clean,cd_press_clean,kind='quadratic')  # quadratic
  cd_pressure_new = f(y_dense)
  
  f=interp1d(self.y_values_right,self.c_cl_values_right,kind='quadratic')
  c_cl_new_right_wing=f(y_dense)
  f=interp1d(self.y_values_right,self.c_cl_values_left,kind='quadratic')
  c_cl_new_left_wing=f(y_dense)

  # INTEGRATIONS
    
  CLtotal_right_wing=integrate.trapezoid(c_cl_new_right_wing ,x=y_dense)/(geometry_data_func().Sref)
  print("CLtotal  is :",CLtotal_right_wing)
  CLtotal_left_wing=integrate.trapezoid(c_cl_new_left_wing,x=y_dense)/geometry_data_func().Sref
  print("CLtotal Left wing is:",CLtotal_left_wing)
  print("CLtotal for the wing is:",CLtotal_left_wing+CLtotal_right_wing)
  CDind_right=integrate.trapezoid(self.cd_values_right*self.chord_values,x=self.y_values_right)/geometry_data_func().Sref
  CDind_left=integrate.trapezoid(self.cd_values_left*self.chord_values,x=self.y_values_right)/geometry_data_func().Sref
  print("CD induced for the wing is :",CDind_right+CDind_left) 
  
  


  #TOTAL CD-HALFSPAN LINEAR 
  plt.figure(figsize=(10,6),facecolor='red')
  plt.title('Total cd viscous (linear)')
  plt.plot(self.y_values_right,self.cd_list,marker='o',linestyle='-',color='black')
  plt.xlabel("Wingspan strip position")
  plt.ylabel("Total viscous drag coefficient")  
  plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))
  plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.0005))
  plt.grid(True)
  plt.show

  #TOTAL CD-HALFSPAN QUADRATIC
  plt.figure(figsize=(10,6),facecolor='red')
  plt.title('Total cd viscous (quadratic)')
  plt.plot(y_dense,cd_new,marker='o',linestyle='-',color='black')
  plt.xlabel("Wingspan strip position")
  plt.ylabel("Total viscous drag coefficient")  
  plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))
  plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.0005))
  plt.grid(True)
  plt.show

  #FRICTION CD-HALFSPAN   LINEAR
  plt.figure(figsize=(10,6),facecolor='blue')
  plt.title("Cd friction (linear)")
  plt.plot(self.y_values_right,self.cd_friction_list,marker='o',linestyle='-',color='black')
  plt.xlabel("Wingspan strip position")
  plt.ylabel("Friction drag coefficient")  
  plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))
  plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.0005))
  plt.grid(True)
  plt.show

  
  # FRICTION CD-HALFSPAN QUADRATIC 
  plt.figure(figsize=(10,6),facecolor='blue')
  plt.title("Cd friction (quadrartic)")
  plt.plot(y_dense,cd_friction_new,marker='o',linestyle='-',color='black')
  plt.xlabel("Wingspan strip position")
  plt.ylabel("Friction drag coefficient")
  plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))
  plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.0005))
  plt.grid(True)
  plt.show


  #PRESSURE CD-HALFSPAN LINEAR
  plt.figure(figsize=(10,6),facecolor='yellow')
  plt.title("cd pressure (linear)")
  plt.plot(self.y_values_right,self.cd_press_list,marker='o',linestyle='-',color='black')
  plt.xlabel("Wingspan strip position")
  plt.ylabel("Pressure drag coefficient")  
  plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))
  plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.0005))
  plt.grid(True)
  plt.show  

  
  # PRESSURE CD- HALFSPAN QUADRATIC
  plt.figure(figsize=(10,6),facecolor='yellow')
  plt.title("cd pressure (quadratic)")
  plt.plot(y_dense,cd_pressure_new,marker='o',linestyle='-',color='black')
  plt.xlabel("Wingspan strip position")
  plt.ylabel("Pressure drag coefficient")  
  plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))
  plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.0005))
  plt.grid(True)
  plt.show
  
                
  #Top transition point per strip 
  plt.figure(figsize=(10,6),facecolor='grey')
  plt.title('Top transition points')
  plt.plot(self.y_values_right,self.top_trans_list,marker='o',linestyle='',color='black')
  plt.xlabel("Wingspan strip position")
  plt.ylabel("Top transition points")  
  plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))
  plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.05))
  plt.grid(True)
  plt.show          

    
    