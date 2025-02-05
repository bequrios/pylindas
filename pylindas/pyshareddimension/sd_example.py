import pandas as pd
import yaml

from pylindas.pyshareddimension import SharedDimension
from pylindas.lindas.upload import upload_ttl
from pylindas.lindas.query import cube_exists

terms_df = pd.read_csv("pylindas/pyshareddimension/sd_terms.csv", sep=";")

with open("pylindas/pyshareddimension/sd_description.yml") as file:
    sd_yaml = yaml.safe_load(file)

sd = SharedDimension(dataframe=terms_df, sd_yaml=sd_yaml, environment="TEST", local=True)
sd.prepare_data()
sd.write_sd()
sd.write_terms()
sd.serialize("pylindas/pyshareddimension/sd_example.ttl")
print(sd)
