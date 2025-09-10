#AVL mass file template 

import textwrap

def uav_mass_properties(uav_id : str, main_wing_mass :dict,fuselage_mass: dict, h_tail_mass:dict, v_tail_mass:dict,sporia_mass:dict):
  """
  uav_id--->string 
  main_wng_mass---> dictionary that includes mass properties of the main wing (mass,cg coordinates,inertia)
  fuselage_mass---> dictionary          //
  h_tail_mass---> dictionary             //
  v_tail_mass--->dictionary             //
  sporia_mass--->dictionary that includes the mass properties of the  remaining components i.e. payload,battery,servos etc
  """

  aircraft_name=uav_id
  mass_file=textwrap.dedent(f"""
  Lunit = 1.0 
  Munit = 0.001 kg
  Tunit = 1.0 sec 
  g = 9.81 
  rho = 1.225 

  #  mass   x     y     z       Ixx   Iyy   Izz    Ixy  Ixz  Iyz
   {main_wing_mass['right_wing_mass']}   {main_wing_mass['right_wing_Xcg']}      {main_wing_mass['right_wing_Ycg']}      {main_wing_mass['right_wing_Zcg']}        {main_wing_mass['Ixx_right_wing']}   {main_wing_mass['Iyy_right_wing']}   {main_wing_mass['Izz_right_wing']}  !right wing 
   {main_wing_mass['right_wing_mass']}   {main_wing_mass['right_wing_Xcg']}      -{main_wing_mass['right_wing_Ycg']}      {main_wing_mass['right_wing_Zcg']}        {main_wing_mass['Ixx_right_wing']}   {main_wing_mass['Iyy_right_wing']}   {main_wing_mass['Izz_right_wing']}  !left wing 
   {fuselage_mass['fuselage_mass']}   {fuselage_mass['fuselage_Xcg']}      {fuselage_mass['fuselage_Ycg']}      {fuselage_mass['fuselage_Zcg']}        {fuselage_mass['Ixx_fuselage']}   {fuselage_mass['Iyy_fuselage']}   {fuselage_mass['Izz_fuselage']}  !Fuselage 
   {h_tail_mass['right_Hwing_mass']}   {h_tail_mass['right_Hwing_Xcg']}      {h_tail_mass['right_Hwing_Ycg']}      {h_tail_mass['right_Hwing_Zcg']}        {h_tail_mass['Ixx_right_Hwing']}   {h_tail_mass['Iyy_right_Hwing']}   {h_tail_mass['Izz_right_Hwing']}  !right HTAIL wing 
   {h_tail_mass['right_Hwing_mass']}   {h_tail_mass['right_Hwing_Xcg']}      -{h_tail_mass['right_Hwing_Ycg']}      {h_tail_mass['right_Hwing_Zcg']}        {h_tail_mass['Ixx_right_Hwing']}   {h_tail_mass['Iyy_right_Hwing']}   {h_tail_mass['Izz_right_Hwing']}  !left HTAIL wing  
   {v_tail_mass['Vtail_mass']}   {v_tail_mass['Vtail_Xcg']}      {v_tail_mass['Vtail_Ycg']}      {v_tail_mass['Vtail_Zcg']}        {v_tail_mass['Ixx_Vtail']}   {v_tail_mass['Iyy_Vtail']}   {v_tail_mass['Izz_Vtail']}  !Vtail 
   {sporia_mass['payload_mass']}   {sporia_mass['payload_Xcg']}      {sporia_mass['payload_Ycg']}      {sporia_mass['payload_Zcg']}        {sporia_mass['Ixx_payload']}   {sporia_mass['Iyy_payload']}   {sporia_mass['Izz_payload']}  !payload
   {sporia_mass['battery_mass']}   {sporia_mass['battery_Xcg']}      {sporia_mass['battery_Ycg']}      {sporia_mass['battery_Zcg']}        0.0   0.0   0.0  !battery  
 
 


  """)
  return mass_file