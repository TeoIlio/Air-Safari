#AVL geometry properties calculations


import math

def compute_halfspan(Bref: float):
    return Bref/2

def compute_sweeped(sweep: float,wingspan: float):
   return math.tan(math.radians(sweep)) * (wingspan/2) 

def compute_tip_chord(taper_ratio: float,root_chord: float):
    return taper_ratio * root_chord

