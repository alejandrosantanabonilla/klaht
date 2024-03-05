import json
from jinja2 import Template


class JsonToTextFile:
    """
    This class parses, prints, and saves variables from a JSON file.

    Attributes:
        data (dict): The loaded JSON data.
        output_file (str, optional): The filename to save the output (default: None).

    Example: Read the filed parder_incar.json and print it as parsed_incar_variables.txt
        parser = IncarDataParser("parsed_incar.json", "parsed_incar_variables.txt")
        parser.save_variables() 
    """

    def __init__(self, filename, output_file=None):
        """
        Initializes the class with the filename of the JSON data and optional output filename.

        Args:
            filename (str): The filename of the JSON data.
            output_file (str, optional): The filename to save the output.
        """
        with open(filename, "r") as json_file:
            self.data = json.load(json_file)
        self.output_file = output_file

    def print_variables(self, data=None, indent=0, header_printed=False):
        """
        Prints all variables from the loaded JSON data with single space formatting and indentation.

        Args:
            data (dict, optional): The dictionary to print (default: None, uses self.data).
            indent (int, optional): The indentation level for printing (default: 0).
            header_printed (bool, optional): Flag indicating if the header has already been printed.

        Returns:
            str: The formatted string containing the printed variables with a header and extra space before each key.
        """
        if data is None:
            data = self.data

        output=""
        if not header_printed:
            output += f"SYSTEM = user_provided\n"  # Print header only once
            header_printed = True

        output += " "  # Initial whitespace
        for key, value in data.items():
            if isinstance(value, dict):
                output += f"\n{' '*indent}{key}:\n"
                output += self.print_variables(value, indent + 2, header_printed)
            else:
                output += f"{' '*indent}{key} = {value}\n"

        return output

    def save_variables(self, data=None):
        """
        Saves the printed variables from the data to a text file.

        Args:
            data (dict, optional): The dictionary to print (default: None, uses self.data).

        Raises:
            ValueError: If no output filename is provided.
        """
        if self.output_file is None:
            raise ValueError("Please provide an output filename to save the results.")

        output_data = self.print_variables(data)
        with open(self.output_file, "w") as text_file:
            text_file.write(output_data)
