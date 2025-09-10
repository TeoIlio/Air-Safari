# mass data for the GeometryFileData dataclass 
"""
Contains the values for an instance concerning all runcase properties required for runcasefileData dataclass
"""
from AVL_dataclasses.AVL_runcase_dataclass import RunCaseFileData

def runcase_data_func():
    runcase_data=RunCaseFileData(
    aircraft_name="Echo",
    runcase_name="forrest gump",
    runcase_number=1,
    AoA=3.0,                    
    sideslip=0.0,               
    pitch_rate=0.0,             
    yaw_rate=0.0,               
    roll_rate=0.0,              
    elevator_def=0.0,          
    rudder_def=0.0,             
    flap_def=0.0,               
    aileron_def=0.0,            
    bank_angle=0.0,             
    climb_angle=0.0,            
    heading_angle=0.0,          
    velocity=25.0,              
    density=1.225       
    )
    
    return runcase_data