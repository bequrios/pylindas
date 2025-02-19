# Generation of shared dimension
This is a proposal implementation to generate a shared dimension, following an approach similar to pyCube, but to transform a .csv file to the corresponding RDF.  
I will abbreviate Shared Dimension by SD, for convenience.  

The pyCube generates two things: the cube's resource (with its specific URL and properties as the cube's name and meta-data), and a list of observations (each a resource with a specific URL and properties).  
Similarily, a SD is also composed of the SD's resource itself (with its specific URL and properties as the SD's name), and a list of terms (each a resource with a specific URL and properties).  

For this implementation, 

The implementation is done in [shared_dimension.py](shared_dimension.py), which is a copy and adaptation of cube.py, to reproduce code that matches the pyCube "approach".

An example is given in the [example/Shared_Dimensions/shared_dimension_generation](/example/Shared_Dimensions/shared_dimension_generation/) folder, which contains:

- [sd_description.yml](/example/Shared_Dimensions/shared_dimension_generation/sd_description.yml): the information about the SD itself (Identifier, Name in different languages, etc) and about the Terms generation
- [sd_terms.csv](/example/Shared_Dimensions/shared_dimension_generation/sd_terms.csv): the data for the terms with an identifier and a name in different languages
To be noted that I took the terms from the BAFU's Red List, a use-case that I did work on
- [sd_example.py](/example/Shared_Dimensions/shared_dimension_generation/sd_example.py): example code to run the transformation

## WARNING: Persistent URLs
It is to be noted that when publishing a SD, the goal is that other datasets will make links to that SD.  
This link is the basic principle of Linked Data, and it consist in the re-use of the identifier of the SD and its terms (their URLs) in other datasets, as Cube's dimensions for instance.  
Therefore, the basic requirement of Persistent URLs should be carefully applied when publishing Shared Dimensions, because removing an existing SD or one of its term could break another dataset (or hundreds, thousands of other datasets).  
When trying things out on LINDAS TEST, it might not really matter, but when publishing a SD on LINDAS INT it is already more important, and when publishing to LINDAS PROD it is of course vital.  

To handle this properly, a SD and each term have a `schema:validFrom` triple which indicates the starting date of validity.  
The value comes from the configuration .yml file and is a date/time value: 
```
Valid-from: 2025-02-05T00:00:00Z
```
When a SD or one term should no more to be used, it must still exist but become "deprecated". This is done by adding a `schema:validThrough` triple with an ending date/time.  
This mechanism allows to avoid breaking existing datasets.  

The generation of the `schema:validThrough` triple is not currently handled in this code, further thoughts might be needed to handle this properly and allow to deprecate a whole SD, or only one/some of its terms.

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

## Generated Shared dimension's RDF validation with SHACL
As the SHACL validation has now been implemented in PyCube, with the `validate()` method, a first temporary version is proposed here.

**IMPORTANT Remark:**  
The code of the `validate()` method is copied from the cube.py validate() and adapted.  
However, no official SHACL file is available online to validate a Shared Dimension.  
During former talks with Zazuko, when writing the [page about Data Validation](https://gitlab.ldbar.ch/hevs/lindas-architecture-and-components/-/blob/main/DataValidation.md?ref_type=heads), they sent us an extract of their data validation process, specific to Shared Dimension.  
This extract is temporarily added in this project, in the [shared_dimension_shape.ttl](shared_dimension_shape.ttl) file, and used for that SHACL validation.  
It is currently not hard-coded in the `validate()` method, but passed as parameter. See [sd_example.py](/example/Shared_Dimensions/shared_dimension_generation/sd_example.py) for an example.

This code demonstrates the validation, but should be improved when that SHACL is finalized and saved online.

