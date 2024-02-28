import subprocess as sp
import os
from concurrent.futures import ThreadPoolExecutor

class VaspError(Exception):
    """Custom exception for VASP execution errors."""

    def __init__(self, message):
        super().__init__(message)

class VaspLuncher:
    """Class for executing VASP calculations with robust error handling."""

    def __init__(self, vasp_exe):
        """
        Initializes the VaspLuncher class.

        Args:
            vasp_exe (str): Path to the VASP executable.
        """
        self.vasp_exe = vasp_exe

    def run_calculation(self, init_dir, num_cores=1, out_file="output.log", use_mpi=False):
        """Executes a VASP calculation and handles errors gracefully.

        Args:
            init_dir (str): Directory containing the VASP input files.
            num_cores (int, optional): Number of cores to use. Defaults to 1.
            out_file (str, optional): File to write output and error (aside the OUTCAR). Defaults to "output.log".
            use_mpi (bool, optional): Whether to use MPI. Defaults to False.

        Raises:
            VaspError: If the VASP calculation fails or an unexpected error occurs.
        """

        cmd = [self.vasp_exe]
        if use_mpi:
            cmd.insert(0, "mpirun")
            cmd.insert(1, "-np")
            cmd.insert(2, str(num_cores))

        try:
            with open(os.path.join(init_dir, out_file), 'w') as result:
                process = sp.check_call(cmd, cwd=init_dir, stdout=result, stderr=sp.STDOUT)
                print("VASP calculation completed successfully.")

        except sp.CalledProcessError as e:
            # Handle expected failures from sp.check_call
            error_msg = f"VASP calculation failed: {e}"
            raise VaspError(error_msg)

        except Exception as e:
            # Handle unexpected errors
            error_msg = f"An unexpected error occurred: {e}"
            raise VaspError(error_msg)

class ConcurrentVaspLauncher:
    """Class for concurrently launching multiple VASP calculations."""

    def __init__(self, max_workers=4):
        """
        Initializes the ConcurrentVaspLauncher class.

        Args:
            max_workers (int, optional): Maximum number of concurrent workers. Defaults to 4.
        """
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def launch_calculations(self, calculations):
        """Launches multiple VASP calculations concurrently.

        Args:
            calculations (list): A list of tuples, where each tuple contains:
                - Path to the VASP executable
                - Directory containing the VASP input files
                - Optional keyword arguments for VaspLuncher.run_calculation

        Returns:
            list: A list of futures representing the running calculations.
        """
        futures = []
        for exe_path, init_dir, kwargs in calculations:
            vasp_launcher = VaspLuncher(exe_path)
            future = self.executor.submit(vasp_launcher.run_calculation, init_dir, **kwargs)
            futures.append(future)
        return futures

    def wait_for_completion(self, futures):
        """Waits for all calculations to complete and handles any errors.

        Args:
            futures (list): A list of futures returned by launch_calculations.

        Raises:
            VaspError: If any of the calculations fail.
        """
        for future in futures:
            try:
                future.result()
            except VaspError as e:
                print(f"Error in calculation: {e}")

# Example usage:
#launcher = ConcurrentVaspLauncher()
#calculations = [
#    ("vasp_gam", "my_folder_1", dict(num_cores=4, out_file="output1.log", use_mpi=True)),
#    ("vasp_gam", "my_folder_2", dict(num_cores=2, out_file="output2.log")),
#]

#futures = launcher.launch_calculations(calculations)
#launcher.wait_for_completion(futures)

