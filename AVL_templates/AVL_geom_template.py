# AVL geometry template 

import textwrap # needed for proper template definition 

def uav_geometry(uav_id: str,main_wing: dict, h_tail: dict, v_tail: dict):

  """uav_id---> string 
     main_wing--->dictionary that will map keys to specified values(concerning main wing variables)
     h_tail--->dictrionary        //                              (concerning horizontal tail variables)
     v_tail--->dictionary         //                              (concerning vertical tail variables)
  """
  aircraft_name=uav_id 
  geometry_file = textwrap.dedent(f"""
  {aircraft_name}
  # Aircraft name

  # Mach
  0.0
  # IYsym  IZsym   Zsym
  0        0       0
  # Sref    Bref    Cref
  {main_wing['Sref']}    {main_wing['Bref']}    {main_wing['Cref']}
  # Xref   Yref   Zref
  0.0     0.0    0.0

  # =====================================
  SURFACE
  Main Wing
  # Nchordwise    Cspace    Nspanwise    Sspace
  13            1.0         19           -2.0
  # Mirror geometry
  YDUPLICATE
  0.0
  ANGLE
  {main_wing['Wing_incidence_angle']}

  SECTION
  # Xle   Yle   Zle      chord     Ainc
  0.0    0.0   0.0     {main_wing['Wing_root_chord']}     {main_wing['Wing_root_twist']}

  AFILE
  {main_wing['Wing_airfoil']}.dat

  # ------------------------------------
  SECTION
  # Xle    Yle     Zle    chord     Ainc
  {main_wing['Wing_sweeped']}    {main_wing['Wing_halfspan']}    {main_wing['Wing_dih']}    {main_wing['Wing_tip_chord']}     {main_wing['Wing_tip_twist']}

  AFILE
  {main_wing['Wing_airfoil']}.dat
  # ====================================
  SURFACE 
  Horizontal tail 
  # Nchordwise    Cspace    Nspanwise    Sspace
  13            1.0        19           -2.0
  TRANSLATE
  {h_tail['X_pos_Htail']} 0.0 {h_tail['Z_pos_Htail']}

  YDUPLICATE
  0.0
  ANGLE
  {h_tail['Htail_incidence_angle']}

  COMPONENT 
  1

  #-------------------------------------
  SECTION
  # Xle   Yle   Zle      chord     Ainc
  0.0    0.0   0.0     {h_tail['Htail_root_chord']}     {h_tail['Htail_root_twist']}

  AFILE
  {h_tail['Htail_airfoil']}.dat
  # ------------------------------------
  SECTION
  # Xle    Yle     Zle    chord     Ainc
  {h_tail['Htail_sweeped']}    {h_tail['Htail_halfspan']}    0.0    {h_tail['Htail_tip_chord']}     {h_tail['Htail_tip_twist']}

  AFILE
  {h_tail['Htail_airfoil']}.dat

  # ====================================
  SURFACE
  Vertical tail
  #Nchordwise  Cspace    Nspanwise  Sspace
  13          1.0       19          -2.0
  TRANSLATE 
  {v_tail['X_pos_Vtail']} 0.0 0.0

  COMPONENT 
  1
  ANGLE
  0.0

  #-------------------------------------
  SECTION
  #Xle    Yle    Zle     Chord        Ainc  
  0.0     0.0     0.0    {v_tail['Vtail_root_chord']}     0.0   

  #-------------------------------------------------------------
  SECTION
  #Xle    Yle    Zle     Chord   Ainc  
  {v_tail['Vtail_sweeped']}    0.0  {v_tail['Vtail_span']} {v_tail['Vtail_tip_chord']}     0.0  

  AFILE
  {v_tail['Vtail_airfoil']}.dat



  """)
  return geometry_file


    

