# Air-Safari
 **All details of the **Air Safari** project can be found in the ipynb and html file named "Final Guide" .In this guide , the core ideas, utilities and processes are explained**. 

 
Air Safari is, in a few words, a framework for 3D aerodynamic analyses that includes calculation of 3D viscous drag .

**Notes before using.:**
*  It must be noted that the code is run only with the "V2" versions and  "OLD VERSION" files cannot be implemented with the current structure. 
*  If you want to run this code , you need to check the **paths** file located in the **"AVL other"** folder. In this file, all the needed paths for system,avl,xfoil, output are given and are fully defined by the user. The paths are defined once in this file manually and no other hard coding of paths is required.
*  Errors might occur if the path file contains false pathlines.
*  For more accuracy , more strips can be used. However ,this comes with an increase in run time.
*  Xfoil might fail to converge in specific analysis. This issue has been solved by refining airfoil data, increasing the panel density and increasing the iteration number. Despite these fixes, xfoil may still return an unconverged case. In this scenario, data will be passed as None and filtered out. Be aware of extreme cases where xfoil data are physically incorrect.


**Some more details about the processes** 


All analyses are facilitated from AVL.When AVL is run , the output will be saved in a file. This file will be read and valuable data and information will be extracted. Most processes work straightfoward. The strip data management and the viscous modules include multiple functions and are more complex. Strip data management will  essentially extract all  valuable data that correspond to half-surface strips. These data can be used to plot distributions along the surface,compute coefficients or even compute forces. The viscous module highlight is the computation of viscous drag. For this process, xfoil is utilized. Local reynolds numbers are calculated for each strip. Xfoil viscous analysis is run for each strip by forcing the local Re and cl values. From the viscous analysis, the strip viscous drag is calculated. This analysis is performed iteratively for all the strips of a surface. Since all strip viscous drag values are known , distributions of each surface can be plotted. **Total viscous drag for a surface can also be computed by numerically integrating the strip values.** Sometimes xfoil will return sparse data due to unconverged strip cases. For this reason, quadratic interpolations are applied. The interpolated data are then used to compute the total vscous values with numerical integrations. The method that was chosen was trapezoid integration which returns about 5% max error and performs similarly to simpson method. Apart from numerical integration, another method can be applied. This method will compute the integral as a sum and requires the sectional area(between two strips) to be calculated ( discrete type calculation). Both methods return similar results and it is up to the user to select. 

**Future Work** 
* Implement performance related modules
* Implement, in a broader scale, error handling techniques.
* Improve file-reading techniques.
* Implement changes for faster file-handling and faster AVL,xfoil execution
* Consider a better method of aircraft data parsing. Currently, three files are used but values are passed manually  each time.
* Create more prototype geometry templates for multiple aircraft types and create a variable-type template method in order to enable a more flexible aircraft definition.
  

