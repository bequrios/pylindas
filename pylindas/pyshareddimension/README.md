# Generation of shared dimension
This is a proposal implementation to generate a shared dimension, following an approach similar to pyCube, but to transform a .csv file to the corresponding RDF.  
I will abbreviate Shared Dimension by SD, for convenience.  

The pyCube generates two things: the cube's resource (with its specific URL and properties as the cube's name and meta-data), and a list of observations (each a resource with a specific URL and properties).  
Similarily, a SD is also composed of the SD's resource itself (with its specific URL and properties as the SD's name), and a list of terms (each a resource with a specific URL and properties).  

For this first implementation, 

Here are the components of this solution:
- [sd_description.yml](sd_description.yml): the information about the SD itself (Identifier, Name in different languages, etc) and about the Terms generation
- [sd_terms.csv](sd_terms.csv): the data for the terms with an identifier and a name in different languages
To be noted that I took the terms from the BAFU's Red List, a use-case that I did work on
- [sd_example.py](sd_example.py): example code to run the transformation
- [shared_dimension.py](shared_dimension.py): the implementation, which is a copy and adaptation ofe cube.py, to reproduce code that matches the pyCube "approach".
  
## Hierarchies
This is not handeld yet, but the data is ready for that and it will be implemented soon.