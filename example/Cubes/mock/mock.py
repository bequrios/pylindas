#!/usr/bin/env python

import pandas as pd
import yaml
import os

from pylindas.pycube import Cube
from pylindas.lindas.upload import upload_ttl
from pylindas.lindas.query import cube_exists

BASEDIR = os.path.dirname(__file__)
DATAFILE = os.path.join(BASEDIR, "data.csv")
CONFIGFILE = os.path.join(BASEDIR, "description.yml")
CUBEFILE = os.path.join(BASEDIR, "mock-cube.ttl")

mock_df = pd.read_csv(DATAFILE)

with open(CONFIGFILE) as file:
    config = yaml.safe_load(file)

cube = Cube(dataframe=mock_df, cube_yaml=config, environment="TEST", local=True)
cube.prepare_data()
cube.write_cube()
cube.write_observations()
cube.write_shape()
cube.serialize("example/Cubes/mock/cube.ttl")
print(cube)

if not cube_exists(cube_uri=cube.get_iri(), environment="TEST"):
    if os.path.isfile("lindas.ini"):   
         upload_ttl(filename=CUBEFILE, db_file="lindas.ini", environment="TEST", graph_uri="")

modk_df_two_sided = pd.read_csv("tests/test_data.csv")
with open("tests/test.yml") as file:
    two_sided_yaml = yaml.safe_load(file)
cube_two_sided = Cube(dataframe=modk_df_two_sided, cube_yaml=two_sided_yaml, environment="TEST", local=True)
cube_two_sided.prepare_data()
cube_two_sided.write_cube()
cube_two_sided.write_observations()
cube_two_sided.write_shape()

cube_two_sided.serialize("./example/Cubes/mock-cube-two-sided.ttl")
if os.path.isfile("lindas.ini"):
    upload_ttl(filename="mock/mock-cube-two-sided.ttl", db_file="lindas.ini", environment="TEST", graph_uri="")
