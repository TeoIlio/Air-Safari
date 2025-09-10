#AeroSurface dictionary 

import numpy as np 
from dataclasses import dataclass


@dataclass
class AeroSurfaces:
    name : str
    section: str
    strips: list

@dataclass 
class StipData: 
    y_coords: np.ndarray 
    strip_chord: np.ndarray
    strip_ccl: np.ndarray
    strip_cl: np.ndarray 
    strip_ai: np.ndarray
    strip_cdi: np.ndarray
       

