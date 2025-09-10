# AVL lift distribution calculation 

import os 
import subprocess
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.ticker as tick


def lift_distribution_derivation(self,surface):
     
    lift_distribution_seq="""
     LOAD {geometry_file}
     MASS {mass_file}
     CASE {runcase_file}
     OPER 
     X
     FS {aircraft_name}_strips.txt
     O

     QUIT
     """
    
    lift_distribution_seq_params={
            "geometry_file": self.geometry_file,
            "mass_file": self.mass_file,
            "runcase_file": self.runcase_file,
            "aircraft_name": self.uav_id
             }
    
    lift_distribution_file_path=os.path.join(self.output_path,f"{self.uav_id}_strips.txt")
   

    lift_distribution_output = lift_distribution_seq.format(**lift_distribution_seq_params)
    process=subprocess.Popen(self.avl_exe_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,cwd=self.output_path)
    output, error = process.communicate(lift_distribution_output)
        
    #lift_distribution_dict ={ 'main_wing': "main_wing" , 'horizontal_tail':'horizontal_tail'}
                            
    start= None  # type->flag ,for line reading operation 
    values_list_right_wing= [[[] for _ in range(6)] for _ in range(19)]  # 19 rows for 19 strips and 6 colums for the 6 parameters. This is a list of lists.Each row has 6 tuples.
    values_list_left_wing= [[[] for _ in range(6)] for _ in range(19)]
    values_list_right_tail= [[[] for _ in range(6)] for _ in range(19)]
    values_list_left_tail= [[[] for _ in range(6)] for _ in range(19)]
    flag=0
    if os.path.exists(lift_distribution_file_path):
        with open(lift_distribution_file_path,"r") as f:
            file=f.readlines()
            
        for t, line in enumerate(file): 
            if "j" in line and "Yle" in line: 
                 start=t+1   # starter point
                 
                 break

        for line in file[start:]:
           values=line.split()
           
           if  not len(values)>12:  # make sure the line is correct
            
            stop=start+flag  #line that strip values for right wing stop
           
            break
           else :
           #derive values in the correct order as shown in the file 
            values_list_right_wing[flag][0].append(('Yle',float(values[1])))  # y point in wing   
            values_list_right_wing[flag][1].append(('Chord',float(values[2])))  # local strip chord
            values_list_right_wing[flag][2].append(('c cl',float(values[4])))  # local strip chord multiplied with local cl value
            values_list_right_wing[flag][3].append(('ai',float(values[5]))) # local strip incidence angle 
            values_list_right_wing[flag][4].append(('cl',float(values[7])))  # local strip cl 
            values_list_right_wing[flag][5].append(('cd',float(values[8]))) # local strip cd (inviscid)

            flag+=1   


        flag =0
        for line in file[stop :]:   # Repeat operation for left wing 
             if "j" in line and "Yle" in line: 
                 start=stop+flag+1 
                 
                 break   
             flag+=1

        flag=0
        for line in file[start:]:
           values=line.split()
           
           if  not len(values)>12:  # make sure the line is correct

            stop=start+flag  #line that strip values for right wing stop

            break
           else :
            #derive values in the correct order as shown in the file 
            values_list_left_wing[flag][0].append(('Yle',float(values[1])))   
            values_list_left_wing[flag][1].append(('Chord',float(values[2]))) 
            values_list_left_wing[flag][2].append(('c cl',float(values[4])))
            values_list_left_wing[flag][3].append(('ai',float(values[5])))
            values_list_left_wing[flag][4].append(('cl',float(values[7])))
            values_list_left_wing[flag][5].append(('cd',float(values[8])))

            flag+=1   

# FOR HORIZONTAL TAILLLLL
        flag =0
        for line in file[stop :]:   # Repeat operation for horizontal tail, iterate through lines until the starting point is found
             if "j" in line and "Yle" in line: 
                 start=stop+flag+1  # starting line for data derivation
                 print(start)
                 break   
             flag+=1

        flag=0
        for line in file[start:]:
           values=line.split()
           
           if  not len(values)>12:  # make sure the line is correct
            stop=start+flag  #line that strip values for right wing stop
            print(stop)
            break
           
           else :
            #derive values in the correct order as shown in the file 
            values_list_right_tail[flag][0].append(('Yle',float(values[1])))   
            values_list_right_tail[flag][1].append(('Chord',float(values[2]))) 
            values_list_right_tail[flag][2].append(('c cl',float(values[4])))
            values_list_right_tail[flag][3].append(('ai',float(values[5])))
            values_list_right_tail[flag][4].append(('cl',float(values[7])))
            values_list_right_tail[flag][5].append(('cd',float(values[8])))

            flag+=1    

        flag =0
        for line in file[stop :]:   # Repeat operation for left wing 
             if "j" in line and "Yle" in line: 
                 start=stop+flag+1 
                 print(start)
                 break   
             flag+=1

        flag=0
        for line in file[start:]:
           values=line.split()
           
           if  not len(values)>12:  # make sure the line is correct
        
            break
           else :
            #derive values in the correct order as shown in the file 
            values_list_left_tail[flag][0].append(('Yle',float(values[1])))   
            values_list_left_tail[flag][1].append(('Chord',float(values[2]))) 
            values_list_left_tail[flag][2].append(('c cl',float(values[4])))
            values_list_left_tail[flag][3].append(('ai',float(values[5])))
            values_list_left_tail[flag][4].append(('cl',float(values[7])))
            values_list_left_tail[flag][5].append(('cd',float(values[8])))

            flag+=1      

   
    lift_dist_file_path=os.path.join(self.output_path,f"final_strips_{self.uav_id}.txt")
    with open(lift_dist_file_path,"w") as f: 
         f.write("MAIN WING:\nExctracted values for the right wing(halfspan):\n")
        # create a txt file and dump the values that were previously collected      
         for item in values_list_right_wing:
            f.write(f"{item[0][0][0]} = {item[0][0][1]}         {item[1][0][0]} = {item[1][0][1]}                 {item[2][0][0]} = {item[2][0][1]}         {item[3][0][0]} = {item[3][0][1]}           {item[4][0][0]} = {item[4][0][1]}         {item[5][0][0]} = {item[5][0][1]}\n")

         f.write("Exctracted values for the left wing(halfspan):\n")    
         for item in values_list_left_wing:
            f.write(f"{item[0][0][0]} = {item[0][0][1]}         {item[1][0][0]} = {item[1][0][1]}                 {item[2][0][0]} = {item[2][0][1]}         {item[3][0][0]} = {item[3][0][1]}            {item[4][0][0]} = {item[4][0][1]}         {item[5][0][0]} = {item[5][0][1]}\n")

         f.write("HORIZONTAL TAIL:\nExctracted values for the right wing of the horizontal tail(halfspan):\n")
        # create a txt file and dump the values that were previously collected      
         for item in values_list_right_tail:
            f.write(f"{item[0][0][0]} = {item[0][0][1]}         {item[1][0][0]} = {item[1][0][1]}                 {item[2][0][0]} = {item[2][0][1]}         {item[3][0][0]} = {item[3][0][1]}           {item[4][0][0]} = {item[4][0][1]}         {item[5][0][0]} = {item[5][0][1]}\n")

         f.write("Exctracted values for the left wing of the horizontal tail(halfspan):\n")    
         for item in values_list_left_tail:
            f.write(f"{item[0][0][0]} = {item[0][0][1]}         {item[1][0][0]} = {item[1][0][1]}                 {item[2][0][0]} = {item[2][0][1]}         {item[3][0][0]} = {item[3][0][1]}            {item[4][0][0]} = {item[4][0][1]}         {item[5][0][0]} = {item[5][0][1]}\n")    

                   
    return values_list_right_wing,values_list_left_wing,values_list_right_tail,values_list_left_tail  

def lift_dist_plots(self,values_list_right_wing,values_list_left_wing,values_list_right_tail,values_list_left_tail,plots:bool):
    # initiate individual matrices for plotting (left/right wing values)
    wing_y_values_right=[]
    wing_chord_values=[]
    wing_cl_values_right=[]
    wing_c_cl_values_right=[]
    wing_cd_values_right=[]

    wing_y_values_left=[]
    wing_cl_values_left=[]
    wing_c_cl_values_left=[]
    wing_cd_values_left=[]
    
    tail_y_values_right=[]
    tail_chord_values=[]
    tail_cl_values_right=[]
    tail_c_cl_values_right=[]
    tail_cd_values_right=[]

    tail_y_values_left=[]
    tail_cl_values_left=[]
    tail_c_cl_values_left=[]
    tail_cd_values_left=[]


    for item in values_list_right_wing:     
      wing_y_values_right.append(item[0][0][1])  # column , tuple place, value part of tuple (not the key)
      wing_chord_values.append(item[1][0][1])
      wing_cl_values_right.append(item[4][0][1])
      wing_c_cl_values_right.append(item[2][0][1])
      wing_cd_values_right.append(item[5][0][1])

    for item in values_list_left_wing:     
      wing_y_values_left.append(item[0][0][1])
      wing_cl_values_left.append(item[4][0][1]) 
      wing_c_cl_values_left.append(item[2][0][1])
      wing_cd_values_left.append(item[5][0][1]) 

    for item in values_list_right_tail:     
      tail_y_values_right.append(item[0][0][1])  # column , tuple place, value part of tuple (not the key)
      tail_chord_values.append(item[1][0][1])
      tail_cl_values_right.append(item[4][0][1])
      tail_c_cl_values_right.append(item[2][0][1])
      tail_cd_values_right.append(item[5][0][1])

    for item in values_list_left_tail:     
      tail_y_values_left.append(item[0][0][1])
      tail_cl_values_left.append(item[4][0][1]) 
      tail_c_cl_values_left.append(item[2][0][1])
      tail_cd_values_left.append(item[5][0][1])   

   
    if plots:
         

         #cl-wingspan distribution 
         plt.figure(figsize=(10, 6),facecolor='grey')
         plt.title('Coefficient of lift Distribution for main wing')
         plt.plot(wing_y_values_right,wing_cl_values_right, marker='o', linestyle='-', color='r')
         plt.plot(wing_y_values_left,wing_cl_values_left, marker='o', linestyle='-', color='r')
         plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))  
         plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.1))
         plt.xlabel("wingspan ")
         plt.ylabel("Cl")
         plt.grid(True)
         plt.show()    

         #Lift distribution (N/m)

         wing_c_cl_values_right=np.array(wing_c_cl_values_right)   # turn to np.array type to plot 
         wing_c_cl_values_left=np.array(wing_c_cl_values_left)
         wing_l_values_right=0.5*1.225*(self.velocity**2)*wing_c_cl_values_right     # lift=cl * q 
         wing_l_values_left=0.5*1.225*(self.velocity**2)*wing_c_cl_values_left
         plt.figure(figsize=(10,6),facecolor='lightskyblue')
         plt.title('Lift Distribution (N/m) for main wing')
         plt.plot(wing_y_values_right,wing_l_values_right,marker='o',linestyle='-',color='b')
         plt.plot(wing_y_values_left,wing_l_values_left,marker='o',linestyle='-',color='b') 
         plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))  
         plt.gca().yaxis.set_major_locator(tick.MultipleLocator(max(wing_l_values_right)/6))
         plt.xlabel('Wingspan')
         plt.ylabel('Lift (N/m)')
         plt.grid(True)
         plt.show()  


         #Normalized Lift distribution (dimensionless)

         
         wing_l_cref_values_right=0.5*1.225*(self.velocity**2)*wing_c_cl_values_right/self.cref     # normalized as of cref
         wing_l_cref_values_left=0.5*1.225*(self.velocity**2)*wing_c_cl_values_left/self.cref
         plt.figure(figsize=(10,6),facecolor='red')
         plt.title('Normalized Lift Distribution (dimensionless) for main wing')
         plt.plot(wing_y_values_right,wing_l_cref_values_right,marker='o',linestyle='-',color='b')
         plt.plot(wing_y_values_left,wing_l_cref_values_left,marker='o',linestyle='-',color='b') 
         plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))  
         plt.gca().yaxis.set_major_locator(tick.MultipleLocator(max(wing_l_cref_values_right)/6))
         plt.xlabel('Wingspan')
         plt.ylabel('Nomralized Lift (dimensionless)')
         plt.grid(True)
         plt.show()  

         #Induced drag distribution 
         
         wing_cd_values_right = np.array(wing_cd_values_right)
         wing_chord_values=np.array(wing_chord_values) 
         wing_cd_values_left = np.array(wing_cd_values_left)
         wing_d_values_right=0.5*1.225*(self.velocity**2)*wing_cd_values_right*wing_chord_values
         wing_d_values_left=0.5*1.225*(self.velocity**2)*wing_cd_values_left*wing_chord_values
         plt.figure(figsize=(8,6),facecolor='grey')
         plt.title('Induced Drag distribution for main wing')
         plt.plot(wing_y_values_right,wing_d_values_right,marker='o',linestyle='-',color='g')
         plt.plot(wing_y_values_left,wing_d_values_left,marker='o',linestyle='-',color='g')
         plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))  
         plt.gca().yaxis.set_major_locator(tick.MultipleLocator(max(wing_d_values_right)/6))
         plt.xlabel('Wingspan')
         plt.ylabel('Induced Drag (N/m)')
         plt.grid(True)
         plt.show()  

      #TAIL
        #cl-wingspan distribution 
         plt.figure(figsize=(10, 6),facecolor='grey')
         plt.title('Coefficient of lift Distribution for horizontal tail')
         plt.plot(tail_y_values_right,tail_cl_values_right, marker='o', linestyle='-', color='r')
         plt.plot(tail_y_values_left,tail_cl_values_left, marker='o', linestyle='-', color='r')
         plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))  
         plt.gca().yaxis.set_major_locator(tick.MultipleLocator(0.1))
         plt.xlabel("wingspan ")
         plt.ylabel("Cl")
         plt.grid(True)
         plt.show()    

         #Lift distribution (N/m)

         tail_c_cl_values_right=np.array(tail_c_cl_values_right)   # turn to np.array type to plot 
         tail_c_cl_values_left=np.array(tail_c_cl_values_left)
         tail_l_values_right=0.5*1.225*(self.velocity**2)*tail_c_cl_values_right     # lift=cl * q 
         tail_l_values_left=0.5*1.225*(self.velocity**2)*tail_c_cl_values_left
         plt.figure(figsize=(10,6),facecolor='lightskyblue')
         plt.title('Lift Distribution (N/m) for horizontal tail')
         plt.plot(tail_y_values_right,tail_l_values_right,marker='o',linestyle='-',color='b')
         plt.plot(tail_y_values_left,tail_l_values_left,marker='o',linestyle='-',color='b') 
         plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))  
         plt.gca().yaxis.set_major_locator(tick.MultipleLocator(max(tail_l_values_right)/6))
         plt.xlabel('Wingspan')
         plt.ylabel('Lift (N/m)')
         plt.grid(True)
         plt.show()  


         #Normalized Lift distribution (dimensionless)

         
         tail_l_cref_values_right=0.5*1.225*(self.velocity**2)*tail_c_cl_values_right/self.cref     # normalized as of cref
         tail_l_cref_values_left=0.5*1.225*(self.velocity**2)*tail_c_cl_values_left/self.cref
         plt.figure(figsize=(10,6),facecolor='red')
         plt.title('Normalized Lift Distribution (dimensionless) for horizontal tail')
         plt.plot(tail_y_values_right,tail_l_cref_values_right,marker='o',linestyle='-',color='b')
         plt.plot(tail_y_values_left,tail_l_cref_values_left,marker='o',linestyle='-',color='b') 
         plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))  
         plt.gca().yaxis.set_major_locator(tick.MultipleLocator(max(tail_l_cref_values_right)/6))
         plt.xlabel('Wingspan')
         plt.ylabel('Nomralized Lift (dimensionless)')
         plt.grid(True)
         plt.show()  

         #Induced drag distribution 
         
         tail_cd_values_right = np.array(tail_cd_values_right)
         tail_chord_values=np.array(tail_chord_values) 
         tail_cd_values_left = np.array(tail_cd_values_left)
         tail_d_values_right=0.5*1.225*(self.velocity**2)*tail_cd_values_right*tail_chord_values
         tail_d_values_left=0.5*1.225*(self.velocity**2)*tail_cd_values_left*tail_chord_values
         plt.figure(figsize=(8,6),facecolor='grey')
         plt.title('Induced Drag distribution for horizontal tail')
         plt.plot(tail_y_values_right,wing_d_values_right,marker='o',linestyle='-',color='g')
         plt.plot(tail_y_values_left,wing_d_values_left,marker='o',linestyle='-',color='g')
         plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))  
         plt.gca().yaxis.set_major_locator(tick.MultipleLocator(max(tail_d_values_right)/6))
         plt.xlabel('Wingspan')
         plt.ylabel('Induced Drag (N/m)')
         plt.grid(True)
         plt.show()  


       #COMBINED 
       #cl
         plt.figure(figsize=(11,8),facecolor='white')
         plt.title('Sectional Coefficient of Lift distribution')
         plt.plot(wing_y_values_right,wing_cl_values_right,label='Main wing',marker='o',linestyle='-',color='g')
         plt.plot(wing_y_values_left,wing_cl_values_left,marker='o',linestyle='-',color='g')
         plt.plot(tail_y_values_right,tail_cl_values_right,label='Horizontal Tail', marker='o', linestyle='-', color='r')
         plt.plot(tail_y_values_left,tail_cl_values_left, marker='o', linestyle='-', color='r')
         plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))  
         plt.gca().yaxis.set_major_locator(tick.MultipleLocator(max(wing_cl_values_right)/8))
         plt.legend()
         plt.xlabel('Wingspan')
         plt.ylabel('Cl ')
         plt.grid(True)
         plt.show()  

       # lift 
         plt.figure(figsize=(11,8),facecolor='white')
         plt.title(' Lift distribution (N/m)')
         plt.plot(wing_y_values_right,wing_l_values_right,label='Main wing',marker='o',linestyle='-',color='g')
         plt.plot(wing_y_values_left,wing_l_values_left,marker='o',linestyle='-',color='g')
         plt.plot(tail_y_values_right,tail_l_values_right,label='Horizontal Tail', marker='o', linestyle='-', color='r')
         plt.plot(tail_y_values_left,tail_l_values_left, marker='o', linestyle='-', color='r')
         plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))  
         plt.gca().yaxis.set_major_locator(tick.MultipleLocator(max(wing_l_values_right)/10))
         plt.legend()
         plt.xlabel('Wingspan')
         plt.ylabel('Lift (N/m)')
         plt.grid(True)
         plt.show() 
         
       # Normalized lift
         plt.figure(figsize=(11,8),facecolor='white')
         plt.title(' Normalized Lift distribution (dimensionless)')
         plt.plot(wing_y_values_right,wing_l_cref_values_right,label='Main wing',marker='o',linestyle='-',color='g')
         plt.plot(wing_y_values_left,wing_l_cref_values_left,marker='o',linestyle='-',color='g')
         plt.plot(tail_y_values_right,tail_l_cref_values_right,label='Horizontal Tail', marker='o', linestyle='-', color='r')
         plt.plot(tail_y_values_left,tail_l_cref_values_left, marker='o', linestyle='-', color='r')
         plt.gca().xaxis.set_major_locator(tick.MultipleLocator(0.2))  
         plt.gca().yaxis.set_major_locator(tick.MultipleLocator(max(wing_l_cref_values_right)/10))
         plt.legend()
         plt.xlabel('Wingspan')
         plt.ylabel('Normalized Lift')
         plt.grid(True)
         plt.show() 




    return wing_cl_values_right,wing_chord_values,wing_c_cl_values_right,wing_y_values_right,wing_cl_values_left,wing_c_cl_values_left,wing_cd_values_right

