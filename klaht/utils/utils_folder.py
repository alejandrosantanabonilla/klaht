import concurrent.futures
import os
import shutil

class FolderManager:
    """
    A class for managing folder creation and file copying in parallel.

    Args:
        folder_name (str): The base name for the folders to be created.
        input_folder (str): The folder containing the files to be copied.
        files_to_copy (list): A list of file names to copy from the input folder.

    Example: 
        manager = FolderManager("my_folder", "input", ["INCAR", "POSCAR", "POTCAR"])
        manager.create_folders(5)  # Create 5 folders with the name my folder and copy the files "INCAR",
        "POSCAR", and "POTCAR" from folder input to my_folder_{i}.
        
    """

    def __init__(self, folder_name, input_folder, files_to_copy):
        self.folder_name = folder_name
        self.input_folder = input_folder
        self.files_to_copy = files_to_copy

    def create_folders(self, num_folders):
        """
        Creates multiple folders in parallel and copies files to them.

        Args:
            num_folders (int): The number of folders to create.

        Raises:
            ValueError: If the number of folders is not a positive integer.
            OSError: If there's an error creating folders or copying files.
        """

        if not isinstance(num_folders, int) or num_folders <= 0:
            raise ValueError("Number of folders must be a positive integer.")

        folder_names = [f"{self.folder_name}_{i}" for i in range(num_folders)]

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self._create_folder_and_copy_files, folder_names)

        print(f"{num_folders} Folders created and files copied successfully!")

    def _create_folder_and_copy_files(self, folder_name):
        """
        Creates a single folder and copies files to it.

        Args:
            folder_name (str): The name of the folder to create.

        Raises:
            OSError: If there's an error creating the folder or copying files.
        """

        try:
            os.makedirs(folder_name)
            for filename in self.files_to_copy:
                src_file = os.path.join(self.input_folder, filename)
                dest_file = os.path.join(folder_name, filename)
                shutil.copy(src_file, dest_file)
                print(f"{filename} copied to {folder_name}")
        except OSError as error:
            raise
