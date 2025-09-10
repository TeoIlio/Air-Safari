#dataclass defintion for the runcase file 

from dataclasses import dataclass
from AVL_dictionaries.runcase_dictionaries.AVL_runcase_dict_definition import create_runcase_dict

@dataclass
class RunCaseFileData:
 
    # Flight conditions 
    aircraft_name: str
    runcase_number: float
    runcase_name: str
    AoA: float
    sideslip: float 
    roll_rate: float
    pitch_rate: float
    yaw_rate: float
    elevator_def: float
    rudder_def: float
    flap_def: float
    aileron_def: float
    bank_angle: float
    climb_angle: float
    heading_angle: float
    velocity: float
    density: float

    def runcase_dict(self)->dict:
        return create_runcase_dict(self)