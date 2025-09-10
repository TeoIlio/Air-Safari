# paths

import os 
import shutil

sys_path=r"C:\Users\Lenovo\Desktop\grand line\MY ACC\python_projects\Air Safari"
AVL_path = r"C:\Users\Lenovo\Desktop\Avl\runs"
AVL_exe_path = os.path.join(AVL_path,"avl.exe")
base_output_path=os.path.join(AVL_path,"skypiea")
xfoil_exe_path=r"C:\Users\Lenovo\Desktop\Xfoil\xfoil.exe"
airfoil_path=r"C:\Users\Lenovo\Desktop\Avl\runs\skypiea\airfoils"

def pathing(filename: str): 
    if os.path.exists(os.path.join(base_output_path,filename)):  # if the folder already exists, then delete it and everything placed inside it 
        shutil.rmtree(os.path.join(base_output_path,filename))   # delete 
        
    Output_path = os.path.join(base_output_path,filename)  
    os.makedirs(Output_path,exist_ok=True)
    
    return Output_path

