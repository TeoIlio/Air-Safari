#Dictionary definition for the runcase file  properties
"""
Define the horizontal tail MASS dictionary used inside the MassFileData dataclass. Functions that compute  certain values are called.
Main idea is to define the dictionary and the computations that this dictionary needs, in different(external) modules . These 
will be called inside the .py that creates the dataclass. 

"""


def create_runcase_dict(self):   # input is mass_data which are the data inside the dataclass

    runcase_dict= {
        'runcase_number': self.runcase_number , 
        'runcase_name':self.runcase_name,
        'AoA':self.AoA,
        'sideslip':self.sideslip,
        'roll_rate':self.roll_rate, 
        'pitch_rate':self.pitch_rate,
        'yaw_rate':self.yaw_rate,
        'elevator_def': self.elevator_def , 
        'rudder_def':self.rudder_def,
        'flap_def':self.flap_def,
        'aileron_def':self.aileron_def,
        'bank_angle': self.bank_angle, 
        'climb_angle': self.climb_angle, 
        'heading_angle':self.heading_angle, 
        'velocity':self.velocity,
        'density': self.density
                }
    
    return runcase_dict