from klaht.input_gen.json_to_txt import *
from klaht.input_gen.txt_to_json import *

# Example usage Incar Parser to a json file.
incar_parser = IncarParser()
incar_parser.txt_to_json_file("INCAR_test", "parsed_incar.json")

# Example usage Json file to INPUT
parser = JsonToTextFile("parsed_incar.json", "INCAR.txt")
parser.save_variables()
