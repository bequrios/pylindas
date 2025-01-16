from pyshacl import validate
from rdflib import Graph

def main():
    r = validate(
        data_graph=Graph().parse("https://raw.githubusercontent.com/zazuko/cube-link/refs/heads/main/test/basic-cube-constraint/valid.minimal.ttl"), 
        shacl_graph=Graph().parse("https://raw.githubusercontent.com/zazuko/cube-link/refs/heads/main/test/basic-cube-constraint/valid.minimal.ttl"))
    conforms, results_graph, results_text = r

    print(conforms)

if __name__ == "__main__":
    main()
