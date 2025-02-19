# Shared dimensions queries
The goal of [shared_dimensions_queries.py](shared_dimensions_queries.py) is to become a tool for developers to find a useful shared dimension,
then get the URLs of the terms in order to configure the mapping for a cube's dimension.

This is a first implementation of:
- Basic queries to request shared dimensions information from LINDAS
- Display the results, line by line

## Example
See an example usage in [example_sd.py](example_sd.py)

List all the shared dimensions for a specific LINDAS environment and print them line by line: 
 ```
 result=list_shared_dimensions("INT")
 list_shared_dimensions_print(result)
 ```

The result is ordered alphabetically.

list_shared_dimensions() has a number of optional parameters, with default values except for the environment:
- environment: LINDAS environment, one of `TEST`, `INT`, `PROD`
- name_lng: the language of the label of the shared dimensions to retrieve (default "en")  
Note: a shared dimension with no label in that language will not be listed (no fall-back handled yet)
- offset/limit: stardard possibility to page through the result with offset/limit (default to 0)  
OFFSET: "skip this many rows from the total result set", 0 to skip no row and begin from start  
LIMIT: "only give me this many rows (starting after any OFFSET)"  
a limit of 0 = no limit, display all results starting from offset (LIMIT will not be added to the query)
- search_word: to limit the results to labels containing a specific word (default "" -> ignored)

List 10 Shared Dimensions that contains "Canton" in the french name
 ```
    result = list_shared_dimensions("INT", "fr", 0, 10, "Canton")
 ```

As the goal is to observe the URLs of the terms in a shared dimension, URL that will be used to define the mappings, a feature of list_shared_dimensions_print() is to print 2-3 terms for each listed shared dimension.  
To do this, pass a second 'environment' parameter to the function
```
 list_shared_dimensions_print(result, "INT")
```
This environment should of course match the one used for `list_shared_dimensions()`. While displaying each shared dimension, LINDAS environment will be queried to get 2 terms.
Example result:
```
Cantons <https://ld.admin.ch/dimension/canton> - validFrom 2021-01-01T00:00:00Z 
{ Terms sample:
Aargau <https://ld.admin.ch/canton/19> 
Appenzell Ausserrhoden <https://ld.admin.ch/canton/15> 
}
Cantons NFI <https://ld.admin.ch/dimension/bgdi/biota/cantonregions>  
{ Terms sample:
Aargau <https://ld.admin.ch/dimension/bgdi/biota/cantonregions/19> 
Appenzell Ausserrhoden <https://ld.admin.ch/dimension/bgdi/biota/cantonregions/15> 
}
```
Note: `list_shared_dimensions()` will also display validFrom and validTo values, when available, as some shared dimensions could be deprecated.

It is finally possible to list all the terms for a specific shared dimension.
Here is an example to list the Cantons shared dimension's terms, in french:  
```
result = list_shared_dimension_terms("INT", "https://ld.admin.ch/dimension/canton", "fr")
print_sparql_result(result, ["name", "sdTerm"])
```
`print_sparql_result()` prints line by line the JSON result of a SPARQL query, printing the specific expected fields of the query.  

## Next steps
All of this is a first proposal, and should be further improved according to the developers needs.  

It is not yet a class with methods, and contains code that could be more generic.  
For instance, query_lindas could be a very generic function as the one found in /lindas/query.py  
To be noted that the existing query_lindas() is specific for ASK queries (returns a bool value), and is maybe "wrongly" named currently.

A class could be created, passing for instance the environment in the constructor. Thus avoiding to pass the environment parameter to the different queries.   
Furthermore, the environment could be coming from a configuration file (or environment variables), to avoid hard-coding them.
