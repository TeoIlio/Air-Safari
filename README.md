# Air-Safari
 **All details of the **Air Safari** project can be found in the ipynb and html file named "Final Guide" .In this guide , the core ideas, utilities and processes are explained**. 

 
Air Safari is, in a few words, a framework for 3D aerodynamic analyses that includes calculation of 3D viscous drag .

*  It must be noted that the code is run only with the V2 versions and  OLD VERSION files cannot be implemented with the current structure. 
*  If you want to run this code , you need to check the **paths** file located in the **"AVL other"** folder. In this file, all the needed paths for system,avl,xfoil, output are given and are completely defined by the user. The paths are defined once in this file manually and no other hard coding of paths is required.
*  Errors might occur , especially for other users due to the dila pathing and naming nature of the code's modules.
* Full code with all processes should take about 1 minute to be fully complete, depending on the AoA range and strip number you select.

**Future Work** 
* Implement performance related modules
* Implement, in a broader scale, error handling techniques.
* Improve file-reading techniques.
* Implement changes for faster file-handling and faster AVL,xfoil execution
* Consider a better method of aircraft data parsing. Currently, three files are used but values are passed manually for each time.
* Create more prototype geometry templates for multiple aircraft types and create a variable-type template method in order to enable a more flexible aircraft definition.
  

