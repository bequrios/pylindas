import pandas as pd
import yaml

from pylindas.pyshareddimension import SharedDimension
from pylindas.lindas.upload import upload_ttl
from pylindas.lindas.query import cube_exists

terms_df = pd.read_csv("example/Shared_Dimensions/shared_dimension_generation/sd_terms.csv", sep=";")

with open("example/Shared_Dimensions/shared_dimension_generation/sd_description.yml") as file:
    sd_yaml = yaml.safe_load(file)

sd = SharedDimension(dataframe=terms_df, sd_yaml=sd_yaml, environment="TEST", local=True)
sd.prepare_data()
sd.write_sd()
sd.write_terms()
sd.serialize("example/Shared_Dimensions/shared_dimension_generation/sd_example.ttl")
print(sd)

# About the SHACL validation, please see the comment of the SharedDimension.validate() method
#   in order to understand the parameters
# This is work in progress as the SHACL file has to be passed as parameter instead of being downloaded from the Web behind the scene
resultBool, resultTxt = sd.validate("./pylindas/pyshareddimension/shared_dimension_shape.ttl", "./example/Shared_Dimensions/shared_dimension_generation/sd_example_SHACL_result.ttl")
print(f"Shared dimension validation result: {resultBool}, with message '{resultTxt}'")
