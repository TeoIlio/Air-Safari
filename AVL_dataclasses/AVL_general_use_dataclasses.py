
import matplotlib.pyplot as plt 
import numpy as np 
from dataclasses import dataclass , field
from typing import Optional 
from numpy.typing import NDArray
from AVL_dataclasses.AVL_geometry_file_dataclass import GeometryFileData
from AVL_dataclasses.AVL_mass_file_dataclass import MassFileData
from AVL_dataclasses.AVL_runcase_dataclass import RunCaseFileData


@dataclass
class StabilityData:
    CLtot: float
    CDtot: float 
    Cmtot: float
    CLa: float
    Cma: float
    CYb: float
    Clb: float
    Cnb: float
    CYp: float
    Clp: float
    Cnp: float
    CLq: float
    Cmq: float
    CYr: float
    Clr: float
    Cnr: float
    

@dataclass 
class StripData: 
    strip_number: NDArray[np.float64]
    y_coords: NDArray[np.float64]
    strip_chord: NDArray[np.float64]
    strip_ccl: NDArray[np.float64]
    strip_cl: NDArray[np.float64]
    strip_ai: NDArray[np.float64]
    strip_cdi: NDArray[np.float64]
    strip_cp: NDArray[np.float64]
    strip_cdv: Optional[np.ndarray] = field(default=None)
    strip_cdf: Optional[np.ndarray] = field(default=None)  
    strip_cdp: Optional[np.ndarray] = field(default=None)
    strip_top_transition: Optional[np.ndarray] = field(default=None)
    strip_bot_transition: Optional[np.ndarray] = field(default=None)

@dataclass
class SurfaceResults:  # for half a surface
     surface_area : float
     avg_chord : float
     CLsurf : float
     CDisurf : float
     CDvsurf : Optional[float] = field(default=None)
     CDfsurf : Optional[float] = field(default=None)
     CDpsurf : Optional[float] = field(default=None)


@dataclass
class AeroSurfaces:
    name : str   # surface name/UAV ID 
    surface: str  # surface type
    section_relevant_right: SurfaceResults    #dataclass with relevant values (cl,cd,surface area etc)
    section_relevant_YDUP: SurfaceResults
    strip_data_right: StripData  #A StripData object with all the arrays needed
    strip_data_YDUP: StripData
    plot_lift: plt.Figure 
    plot_viscous: Optional[plt.figure] = field(default=None)

@dataclass 
class batch_data:
    AoA_range_total: Optional[np.ndarray] = field(default=None)
    AoA_range_wing: Optional[np.ndarray] = field(default=None)
    AoA_range_tail: Optional[np.ndarray] = field(default=None)
    batch_wing_CL: Optional[np.ndarray] = field(default=None)
    batch_wing_CDi: Optional[np.ndarray] = field(default=None)
    batch_tail_CL:  Optional[np.ndarray] = field(default=None)
    batch_tail_CDi: Optional[np.ndarray] = field(default=None)
    batch_total_CL: Optional[np.ndarray] = field(default=None)
    batch_total_CDi: Optional[np.ndarray] = field(default=None)
    plot_total_forces: Optional[plt.figure] = field(default=None)
    plot_wing_forces: Optional[plt.figure] = field(default=None)
    plot_tail_forces: Optional[plt.figure] = field(default=None)


@dataclass
class Aircraft:
    uav_id: Optional[str] = field(default=None)
    geometry_data: Optional[GeometryFileData] = field(default=None)
    mass_data: Optional[MassFileData] = field(default=None)
    runcase_data: Optional[RunCaseFileData] = field(default=None)
    main_wing_data: Optional[AeroSurfaces] = field(default=None)
    horizontal_tail_data: Optional[AeroSurfaces] = field(default=None)
    batched_data: Optional[batch_data] = field(default=None)
    stability_data: Optional[StabilityData] = field(default=None)

    



