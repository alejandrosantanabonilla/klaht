import re
import json


class IncarParser:

    def __init__(self):
        self.pattern = r"^(\S+)\n"  # Matches non-empty lines starting with non-whitespace characters

    def find_non_empty_patterns(self, text):
        """Finds patterns that don't start with blank spaces.

        Args:
            text (str): The text to search through.

        Returns:
            A list of patterns found in the text.
        """

        matches = re.findall(self.pattern, text, flags=re.MULTILINE)
        return matches

    def read_and_parse_file(self, filename):
        """Reads a file and parses its content using the find_non_empty_patterns method.

        Args:
            filename (str): The name of the file to read.

        Returns:
            A list of valid patterns found in the file, or None if an error occurs.
        """

        try:
            with open(filename, "r") as f:
                text = f.read()
                return self.find_non_empty_patterns(text)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return None

    def parse_incar_file(self, filename, patterns):
        """Parses the INCAR file and returns a dictionary of sections based on provided patterns.

        Args:
            filename (str): The path to the INCAR file.
            patterns (list[str]): A list of regular expression patterns defining sections.

        Returns:
            A dictionary containing parsed sections, or None if an error occurs.
        """

        data = {}
        current_section = None

        try:
            with open(filename, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    for pattern in patterns:
                        if re.match(pattern, line):
                            current_section = pattern.strip()  # Use the matched pattern as the section key
                            data[current_section] = {}
                            break

                    if current_section and line:
                        try:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().split("!")[0].strip()  # Remove comments
                            data[current_section][key] = value
                        except ValueError:
                            pass  # Handle lines without an equal sign (optional)

            return data
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return None

    def incar_to_json(self, parsed_data, json_file_path):
        """Writes parsed INCAR data to a JSON file.

        Args:
            parsed_data (dict): The dictionary containing parsed INCAR data.
            json_file_path (str): The path to the JSON file to write to.
        """

        with open(json_file_path, "w") as f:
            json.dump(parsed_data, f, indent=4)

        print(f"Successfully wrote INCAR data to {json_file_path}")

    def txt_to_json_file(self, incar_file, json_file_path):
        """Reads and parses an INCAR file, converts to JSON, and writes it to a file.

        Args:
            incar_file (str): The path to the INCAR file.
            json_file_path (str): The path to the JSON file to write to.
        """

        print("\nReading and parsing example INCAR file:")
        patterns = self.read_and_parse_file(incar_file)

        if patterns is None:
            return

        parsed_data = self.parse_incar_file(incar_file, patterns)

        if parsed_data is None:
            return

        self.incar_to_json(parsed_data, json_file_path)
        print(f"{json_file_path} file has been created.")


# Example usage
#incar_parser = IncarParser()
#incar_parser.txt_to_json_file("INCAR_test", "parsed_incar.json")  # Replace "IN#CAR" with your file path
