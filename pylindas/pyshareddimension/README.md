# Generation of shared dimension
This is a proposal implementation to generate a shared dimension, following an approach similar to pyCube, but to transform a .csv file to the corresponding RDF.  
I will abbreviate Shared Dimension by SD, for convenience.  

The pyCube generates two things: the cube's resource (with its specific URL and properties as the cube's name and meta-data), and a list of observations (each a resource with a specific URL and properties).  
Similarily, a SD is also composed of the SD's resource itself (with its specific URL and properties as the SD's name), and a list of terms (each a resource with a specific URL and properties).  

For this first implementation, 

Here are the components of this solution:
- [sd_description.yml](sd_description.yml: the information about the SD itself (Identifier, Name in different languages, etc) and about the Terms generation
- [sd_terms.csv](sd_terms.csv): the data for the terms with an identifier and a name in different languages
To be noted that I took the terms from the BAFU's Red List, a use-case that I did work on
- [sd_example.py](sd_example.py): example code to run the transformation
- shared_dimension.py: the implementation, which is a copy the cube.py that was adapted.
  
## Hierarchies
This is not handeld yet, but the data is ready for that and it will be implemented soon.

## Questioning about pyCube performances
I take here the opportunity to ask if pyCube does scale ? how does pyCube handle a big .csv in input (as the Zefix dataset for instance), given that it creates first the full graph in memory, parse the data with pandas, and then serialize the output ?
I do not have the answer, but for the first implementation of the Zefix dataset a few years ago, tarql was choosen as the RDFizer because it was easy to configure and performant.
I remember that at that time, the library used by Barnard59 was taking much more time than tarql (here we talk about 30 minutes of transforation becoming hours), but now Barnard59 is very performant.
My question being: shouldn't we reuse an existing RDFizer, pyCube handling the configuration of the RDFizer and launching the process ? Just a questioning.
