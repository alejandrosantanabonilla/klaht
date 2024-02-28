import os
import time

from klaht.vasp_calculator.vasp_run import *
from klaht.utils.utils_folder import FolderManager


#start_time = time.perf_counter()
manager = FolderManager("my_folder", "input", ["INCAR", "POSCAR", "POTCAR", "KPOINTS"])
manager.create_folders(8)

folders = [f"my_folder_{i}" for i in range(8)]


launcher = ConcurrentVaspLauncher()
calculations = [
    ("vasp_gam", "my_folder_1", dict(num_cores=4, out_file="output1.log", use_mpi=True)),
    ("vasp_gam", "my_folder_2", dict(num_cores=4, out_file="output2.log", use_mpi=True)),
]
futures = launcher.launch_calculations(calculations)
launcher.wait_for_completion(futures)
