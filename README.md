# KLAHT
KL-LSU Ab-Initio High-Throughput (KLAHT)


# ConcurrentVaspLauncher: Run VASP Calculations in Parallel

This document describes the ConcurrentVaspLauncher class, which allows you to execute multiple VASP calculations concurrently on your machine. 
This can significantly speed up your workflow compared to running them sequentially.

## Functionality

Launches multiple VASP calculations simultaneously using thread-based concurrency.

Accepts a list of calculation details, including the VASP executable path, input directory, and optional arguments for individual calculations.

Returns a list of futures representing the running calculations.

Provides a wait_for_completion method to wait for all calculations to finish and handle any errors.

## Benefits
1. Faster calculations: Reduces overall execution time by utilizing multiple cores.
2. Improved efficiency: Enables simultaneous execution of multiple VASP tasks.
3. Organized workflow: Simplifies managing and monitoring multiple calculations.

## Usage

Import the module in Python:

```
from concurrent_vasp_launcher import ConcurrentVaspLauncher

#Create a Luncher Object
launcher = ConcurrentVaspLauncher(max_workers=4)  # Adjust max_workers if needed

#Define calculation details:

calculations = [
    ("vasp_gam", "my_folder_1", dict(num_cores=4, out_file="output1.log", use_mpi=True)),
    ("vasp_std", "my_folder_2", dict(num_cores=2, out_file="output2.log")),
]
```

Each tuple contains the VASP executable path, input directory, and optional keyword arguments for the run_calculation method of VaspLuncher.
Launch calculations:
Python
futures = launcher.launch_calculations(calculations)
Use code with caution.
Wait for completion and handle errors:
Python
launcher.wait_for_completion(futures)
Use code with caution.
Example
The provided code snippet demonstrates how to launch two VASP calculations concurrently using different executables and configurations.

Notes
Ensure you have the concurrent.futures module installed (pip install concurrent.futures).
Refer to the VaspLuncher documentation for details on supported arguments for the run_calculation method.
Adjust the max_workers parameter based on your system resources and desired performance
