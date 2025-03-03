# Generation of shared dimension
This is a first implementation to generate a shared dimension, following an approach similar to pyCube, but to transform a .csv file to the corresponding RDF.  
I will abbreviate Shared Dimension by SD, for convenience.  

The pyCube generates two things: the cube's resource (with its specific URL and properties as the cube's name and meta-data), and a list of observations (each a resource with a specific URL and properties).  
Similarily, a SD is also composed of the SD's resource itself (with its specific URL and properties as the SD's name), and a list of terms (each a resource with a specific URL and properties).  

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

## Links between terms: hierarchy example
A first implementation is available, and the current example demonstrates how to build a hierarchy with `skos:broader` links from child to parent.

The links (hierarchy) must be provided in the data itself:  
- [sd_terms.csv](sd_terms.csv): has an identifier for the term itself (the `code` field), and an identifier for its parent (the `parent_code` field)
- [sd_description.yml](sd_description.yml): defines a link between terms with the `links-to-other-terms key`. The sub-key `parent_code` is the name of the column that contains the identifier of the other term. The value of `property` is the URL of the property to use to link the current term to its related term, the parent in this example.
`links-to-other-terms key` is optional, just omit it if there is no links between terms in the dataset

Notes about the hierarchy example: 
- The root term does not have a parent, this is currently handled properly  
- The description of the hierarchy is not generated yet, this could be added in a coming version

This current implementation allows to create links between two terms and can thus be configured to link the term to its parent with the `skos:broader` property.  
Multiple links can be defined under the `links-to-other-terms key` key.  
One current "limitation" is that it links one term to another (not to multiple others).  

## About hierarchies "description" or "template"
When a hierarchy exists in a Shared Dimension, the Cube Creator allows to describe that hierarchy under the "Hierarchy" tab.  

The goal is to describe the existing hierarchy by defining the root(s) node(s), the levels, and the property that links the terms to build that hierarchy (as `skos:broader` for instance). When linking a cube's dimension to an existing Shared Dimension, the hierarchy description must be defined in the metadata, and it is then possible to copy an existing hierarchy description as explained in the [Cube Creator's User guide]](https://github.com/zazuko/cube-creator/wiki/3.-Cube-Designer#linking-to-shared-dimensions).  

In automn 2024, it was not yet possible to add, by code, a hiearchy description in LINDAS. The cause was that the Cube Creator was expecting the hiearchy description to be in a specific Named Graph (only available to the Cube Creator itself). The possibility to add hiearchies descriptions was requested [in this issue](https://gitlab.ldbar.ch/zazuko/misc/-/issues/197), and was first tested when creating this feature of Shared Dimension generation. At the time of writing (early March 2025), that possibility was not yet working properly (see the [comment](https://gitlab.ldbar.ch/zazuko/misc/-/issues/197#note_18273) in that feature request). 

**Currently proposed solution**: this step to add a hierarchy description to LINDAS, and then copy it when defining a cube's dimension, is just an option. It is not working yet with pyLindas. But it is also possible to directly add the hierarchy description to the metadata of the dimension while generating a cube with pyCube. This is a feature under development.   

For information, here is the RDF of the hierarchy description that was used to perform that test:
```
@prefix sd_md: <https://cube-creator.zazuko.com/shared-dimensions/vocab#> .
@prefix meta: <https://cube.link/meta/> .
@prefix hydra: <http://www.w3.org/ns/hydra/core#> .
@prefix schema1: <http://schema.org/> .
@prefix shacl: <http://www.w3.org/ns/shacl#> .

<https://ld.admin.ch/cube/dimension/hierarchy/pylindas_hierarchy_generation_example> a sd_md:Hierarchy, meta:Hierarchy, hydra:Resource ;
    schema1:name "PyLindas Hierarchy Description fo Shared Dimension generation example" ;
    sd_md:sharedDimension <https://ld.admin.ch/cube/dimension/pylindas_sd_generation_example> ;
    meta:hierarchyRoot ns1:1 ;
    meta:nextInHierarchy [ schema1:name "Level 1" ;
        shacl:path [shacl:inversePath skos:broader] ;
        meta:nextInHierarchy [ schema1:name "Level 2" ;
            shacl:path [shacl:inversePath skos:broader] ;
            meta:nextInHierarchy [ schema1:name "Level 3" ;
                shacl:path [shacl:inversePath skos:broader] ;
                meta:nextInHierarchy [ schema1:name "Level 4" ;
                    shacl:path [shacl:inversePath skos:broader] ;
                    meta:nextInHierarchy [ schema1:name "Level 5" ;
                        shacl:path [shacl:inversePath skos:broader]
                        ]
                    ]
                ]
            ]
        ] .
```
Note: the links `nextInHierarchy` must be defined from parent to child. Therefore, if the link in the data is from child to parent, the `shacl:inversePath` must be used as in that example. If the link is already parent to child, it can be simply stated:
```
 meta:nextInHierarchy [ schema1:name "Level 1" ;
    shacl:path skos:narrower 	
    ]
```

## Generated Shared dimension's RDF validation with SHACL
As the SHACL validation has now been implemented in PyCube, with the `validate()` method, a first temporary version is proposed here.

**IMPORTANT Remark:**  
The code of the `validate()` method is copied from the cube.py validate() and adapted.  
However, no official SHACL file is available yet online to validate a Shared Dimension.  
During former talks with Zazuko, when writing the [page about Data Validation](https://gitlab.ldbar.ch/hevs/lindas-architecture-and-components/-/blob/main/DataValidation.md?ref_type=heads), they sent us an extract of their data validation process, specific to Shared Dimension.  
This extract is temporarily added in this project, in the [shared_dimension_shape.ttl](shared_dimension_shape.ttl) file, and used for that SHACL validation.  
It is currently not hard-coded in the `validate()` method, but passed as parameter. See [sd_example.py](/example/Shared_Dimensions/shared_dimension_generation/sd_example.py) for an example.

This code demonstrates the validation, but should be improved when that SHACL is finalized and saved online.

