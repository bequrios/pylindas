import pandas as pd
import yaml

from pylindas.lindas.namespaces import SCHEMA
from pylindas.pycube import Cube
from pylindas.lindas.upload import upload_ttl
from pylindas.lindas.query import cube_exists

"""
Author: Fabian Cretton - HEVS

See the description in the README.

This example script only generates the .ttl file, the upload operations are not performed
"""

# data_with_dummy.csv contains an airport type identifier that doesn't exist in airportType.csv
# the goal is to demonstrate that the  check_dimension_object_property() called here under will detect that
data_df = pd.read_csv("example/Cubes/concept_table_airport/data_with_dummy.csv")

with open("example/Cubes/concept_table_airport/description.yml") as file:
    cube_yaml = yaml.safe_load(file)

cube = Cube(dataframe=data_df, cube_yaml=cube_yaml, environment="TEST", local=True)
cube.prepare_data()
cube.write_cube()
cube.write_observations()
cube.write_shape()

# Add the concept data
# The concept must be defined in the cube_yaml file, as a nested key under the "Concepts" key
#   "typeOfAirport" is the name of that nested key
airport_concept_df = pd.read_csv("example/Cubes/concept_table_airport/airportType.csv")
cube.write_concept("typeOfAirport", airport_concept_df)

# Check that all the generated URLs for the typeOfAirport are resources (concept) with a SCHEMA.name triple
# This allows to check if all the entries in data_with_dummy.csv correspond to an entry in airportType.csv 
# This check should identify the error of the 'dummy' airport type
allConceptsFound = cube.check_dimension_object_property("typeOfAirport", SCHEMA.name)

if not allConceptsFound:
    print("""\nCheck result - WARNING: It seems that some objects of the \"typeOfAirport\" dimension have no matching concept.
          See the log for details and check your data + cube dimension and concepts configuration""")
else:
    print("\nCheck result - SUCCESS: It seems that all objects of the \"typeOfAirport\" dimension have a matching concept.")

cube.serialize("example/Cubes/concept_table_airport/cube_with_concept.ttl")

# Just for testing the functionality: add the 'dummy' airport type
airport_concept_dummy_df = pd.read_csv("example/Cubes/concept_table_airport/airportType_dummy.csv")
cube.write_concept("typeOfAirport", airport_concept_dummy_df)
allConceptsFound = cube.check_dimension_object_property("typeOfAirport", SCHEMA.name)

if not allConceptsFound:
    print("""\nCheck result - WARNING: It seems that some objects of the \"typeOfAirport\" dimension have no matching concept.
          See the log for details and check your data + cube dimension and concepts configuration""")
else:
    print("\nCheck result - SUCCESS: It seems that all objects of the \"typeOfAirport\" dimension have a matching concept.")

print(cube)


