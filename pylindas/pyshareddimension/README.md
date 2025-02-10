# Generation of shared dimension
This is a proposal implementation to generate a shared dimension, following an approach similar to pyCube, but to transform a .csv file to the corresponding RDF.  
I will abbreviate Shared Dimension by SD, for convenience.  

The pyCube generates two things: the cube's resource (with its specific URL and properties as the cube's name and meta-data), and a list of observations (each a resource with a specific URL and properties).  
Similarily, a SD is also composed of the SD's resource itself (with its specific URL and properties as the SD's name), and a list of terms (each a resource with a specific URL and properties).  

For this implementation, 

Here are the components of this solution:
- [sd_description.yml](sd_description.yml): the information about the SD itself (Identifier, Name in different languages, etc) and about the Terms generation
- [sd_terms.csv](sd_terms.csv): the data for the terms with an identifier and a name in different languages
To be noted that I took the terms from the BAFU's Red List, a use-case that I did work on
- [sd_example.py](sd_example.py): example code to run the transformation
- [shared_dimension.py](shared_dimension.py): the implementation, which is a copy and adaptation ofe cube.py, to reproduce code that matches the pyCube "approach".
  
## Hierarchies
A first implementation of hierarchies is available.
This currently handled hierarchy is in the data itself:
- [sd_terms.csv](sd_terms.csv): has an identifier for the term itself (the `code` field), and an identifier for its parent (the `parent_code` field)
- [sd_description.yml](sd_description.yml): has a `parent-field` set to `parent_code`, which indicates that each term has a parent in the current dataset  
`parent-field` is optional, just omit it if there is no hierarchy in the dataset
- The code will thus add a `skos:broader` link between two terms

Notes: 
- The root term does not have a parent, this is currently handled properly  
- The description of the hierarchy is not generated yet, this will be added in a coming version
