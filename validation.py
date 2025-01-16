from rdflib import Graph
from pyshacl import validate

shacl_graph = Graph()
# TODO: choose profile according to the cubes metadata
# note: for API explanation see also https://github.com/zazuko/cube-link?tab=readme-ov-file#validation-shapes
shacl_graph.parse("https://cube.link/ref/main/shape/profile-opendataswiss-lindas", format="turtle") # check on `<cube> schema:workExample <https://ld.admin.ch/application/opendataswiss>`
#shacl_graph.parse("https://cube.link/ref/main/shape/profile-opendataswiss", format="turtle")
#shacl_graph.parse("https://cube.link/ref/main/shape/profile-visualize", format="turtle") # check on `<cube> schema:workExample <https://ld.admin.ch/application/visualize>`
#shacl_graph.parse("https://cube.link/ref/main/shape/profile-standalone-cube-constraint", format="turtle") # check for any cube

# TODO: apply `code:imports` i.e. `<./standalone-cube-constraint>` in above profiles and merge it to a combined shape graph

data_graph = Graph()
data_graph.parse("example/mock-cube.ttl", format="turtle")

conforms, results_graph, text = validate(data_graph, shacl_graph=shacl_graph, abort_on_first=True, inference="none", advanced=True)
print(text)
