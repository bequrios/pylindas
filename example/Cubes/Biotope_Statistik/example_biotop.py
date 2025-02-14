import pandas as pd
import yaml

from  pylindas.pycube import Cube
from pylindas.lindas.upload import upload_ttl
from pylindas.lindas.query import cube_exists

biotope = pd.read_csv("example/Biotope_Statistik/biotope.csv", encoding="utf-8", sep=",")
with open("example/Biotope_Statistik/biotope.yml", encoding="utf-8") as file:
    cube_yaml = yaml.safe_load(file)

cube = Cube(dataframe=biotope, cube_yaml=cube_yaml, environment="TEST", local=True)
cube.prepare_data()
cube.write_cube()
cube.write_observations()
cube.write_shape()
valid, text = cube.validate()
if valid:
    print(text)
    cube.serialize("example/Biotope_Statistik/cube.ttl")
    upload_ttl(filename="./example/Biotope_Statistik/cube.ttl", db_file="lindas.ini", environment="TEST")
else:
    print(text)