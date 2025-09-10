#run case template 


import textwrap

def uav_runcase(uav_id : str, flight_conditions: dict):
    """
    uav_id--->string 
    flight_conditions---> dictionary that includes mandatory flight conditions for the  runcase file of avl(AoA,sideslip, velocity etc)
    """
    runcase_file=textwrap.dedent(f"""
   Run case  {flight_conditions['runcase_number']}:{flight_conditions['runcase_name']}                                   

   alpha        ->  alpha       =   {flight_conditions['AoA']}    
   beta         ->  beta        =   {flight_conditions['sideslip']}    
   pb/2V        ->  pb/2V       =   {flight_conditions['roll_rate']}   
   qc/2V        ->  qc/2V       =   {flight_conditions['pitch_rate']}    
   rb/2V        ->  rb/2V       =   {flight_conditions['yaw_rate']}    
   elevator     ->  elevator    =   {flight_conditions['elevator_def']} deg    
   rudder       ->  rudder      =   {flight_conditions['rudder_def']} deg    
   flap         ->  flap        =   {flight_conditions['flap_def']} deg
   aileron      ->  aileron     =   {flight_conditions['aileron_def']} deg  

   alpha     =   0.00000     deg                             
   beta      =   0.00000     deg                             
   pb/2V     =   0.00000                                     
   qc/2V     =   0.00000                                     
   rb/2V     =   0.00000                                     
   CL        =   0.00000                                     
   CDo       =  0.200000E-01                                 
   bank      =   {flight_conditions['bank_angle']}     deg                             
   elevation =   {flight_conditions['climb_angle']}     deg                             
   heading   =   {flight_conditions['heading_angle']}     deg                             
   Mach      =   0.01                                 
   velocity  =   {flight_conditions['velocity']}     m/s                             
   density   =   {flight_conditions['density']}     kg/m^3                          
   grav.acc. =   9.81     m/s^2                           
   turn_rad. =   0.00000     m                               
   load_fac. =   0.00000                                     
   X_cg      =   0.00000     Lunit         #ignore                   
   Y_cg      =   0.00000     Lunit                           
   Z_cg      =   0.00000     Lunit                           
   mass      =   0.00000     kg                              
   Ixx       =   0.00000     kg-m^2                          
   Iyy       =   0.00000     kg-m^2                          
   Izz       =   0.00000     kg-m^2                          
   Ixy       =   0.00000     kg-m^2                          
   Iyz       =   0.00000     kg-m^2                          
   Izx       =   0.00000     kg-m^2                          
   visc CL_a =   0.00000                                     
   visc CL_u =   0.00000                                     
   visc CM_a =   0.00000                                     
   visc CM_u =   0.00000      

  """ )
    
    return runcase_file