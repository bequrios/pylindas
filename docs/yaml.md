# Introduction

`pylindas` works with dictionaries to describe meta data for the various constructs that are supported (namely `cube:Cube`, `meta:SharedDimension`). One way to construct these nested dictionaries is through a `yaml` file. They are flexible and easy to read and are currently the main way (as well as the only supported way) to provide the necessary metadata.

This page describes the structure needed for a valid `yaml` file.

## Namespaces 
| **PREFIX** | **IRI** | 
| --- | --- |
| `cube` | `<https://cube.link/>` |
| `dcat` | `<http://www.w3.org/ns/dcat#>`|
| `dcterms` | `<http://purl.org/dc/terms/>` |
| `meta` | `<https://cube.link/meta/>` |
| `schema` | `<http://schema.org/>` |
| `sh` | `<http://www.w3.org/ns/shacl#>` |

***

# `cube:Cube`

Below the table you'll find a working example. For additional examples, please refer to [the example directory](https://github.com/Kronmar-Bafu/lindas-pylindas/tree/main/example/Cubes).

| Key | Status | Expected Entry | Description | Target Predicate  |
| --- | --- | --- | --- | --- |
|**Name** | Required | Key-Value pairs, with key being a [ISO 639 language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes)) for the language in question and the corresponding value | Name of the dataset with corresponding language | `schema:name`, `dcterms:title` | 
**Description** | Required | Key-Value pairs, with key being a [ISO 639 language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes)) for the language in question and the corresponding value | Description of the data set with correspoing language | `schema:description`, `dcterms:description` |
|**Publisher** | Required | List of Key-Value pairs, with `key = IRI` and the correct IRI | Describes the publisher of the dataset with the correct IRI | `schema:publisher`, `dcterms:publisher` |
|**Creator** | Required | List of Key-Value pairs, with `key = IRI` and the correct IRI | Describes the creator of the dataset with the correct IRI | `schema:creator`, `dcterms:creator` |
|**Contributor** | Required | List of Key-Value pairs, with `key = IRI` and the correct IRI and `key = Name`| Describes the contributors of the dataset. with both, the correct IRI and name | `schema:contributor`, `dcterms:contributor` |
|**Date Created** | Required | Date of Publication, given in ISO Format xxxx, i.e. YYYY-MM-DD | Publication date of the dataset.  | 
|**Contact Point** | Required | Key-Value pairs, with keys `E-Mail` and `Name` for contact E-mail as well as name | Contact point of the data set | `schema:contactPoint`, `dcat:contactPoint` |
|**Base-URI** | Required | a valid URI | The Base-URI will be used to construct a URI for the cube as well as other parts of the cube. Please make sure to give something meaningful and contact the Federal Archive | |
|**Identifier** | Required | a *unique* identifier for the cube | The unique identifier under which a cube (or a family of cubes with differing versions) can be identified | `dcterms:identifier` |
|**Version** | Required | a numerical value | the version of the cube | `schema:version` |
|**Work Status** | Required | Either `Draft` or `Published` | the work status of the Cube. Either Published for final iterations of the given version or Draft for earlier versions. | `schema:creativeWorkStatus` |
|**Visualize** | optional | True or False | boolean describing whether the Cube should be displayed on `visualize.admin.ch`. Key-value pair can be ommited, which will be considered `False` | `schema:workExample` |
|**Accrual Periodicity** | optional | `daily`, `weekly`, `monthly`, `yearly` or `irregular` | The frequency with which the cube is expected to be updated | `dct:accrualPeriodicity` |
|**Namespace** | optional | a string | does not have a technical impact but instead improves readability if one serializes a cube | |
|**dimensions** | required | a key-value pair with key being the column name in the `pandas.DataFrame`. The value is a valid `dimension` as described 	in [dimension](#dimension) | Describes the meta data of a given dimension. | `cube:observationConstraint/sh:property` |

## `dimension`

| Key | Status | Expected Entry | Description | Target Predicate |
| --- | --- | --- | --- | --- |
|**name** | Required | Key-Value pairs, with key being a language short hand and the corresponding value | Name of the dimension with corresponding language | `schema:name` |
|**description** | Required | Key-Value pairs, with key being a language short hand and the corresponding value | Description of the dimension with corresponding language | `schema:description` |
|**dimension type** | Required | Either `Key Dimension`, `Measure Dimension` or `Standard Error` | Type of dimension, which either is a measure dimension, key dimension or a standard error. Can only be one | `rdf:type` |
|**scale type** | Required | Either `nominal`, `ordinal`, `interval`, or `ratio` | Ratio type of dimension. Please refer to [link einfügen] for further details. | `qudt:scaleType`|
|**path** | required | a per cube unique string `path`, describing the predicate used for the dimension. | `cube:Observation` are written with `<cube_uri/observation/[unique_identifier]> <base_uri/path> "Value"`. | `sh:path` | 
|**mapping** | required for dimensions using URI objects | key-value pairs, at least one key-value pair with key `type` and value being either `replace` or `additive` | a logic which should be employed when mapping values in the data frame to some URI | None | 
|**unit** | required for measure dimensions | a unit from the qudt:unit namespace. Refer to [these Units here](https://www.qudt.org/doc/DOC_VOCAB-UNITS.html) - namespace does not need to be provided, for example for kg, provide `KiloGM` | Unit in which the measure dimension is provided | `unit:hasUnit` | |
|**datatype** | Required | a datatype defined in [section 3](https://www.w3.org/TR/xmlschema-2/#built-in-datatypes), without namespace | the datatype of the column in question | `sh:datatype` | 

### Example
```yaml
Name:
  de: Mock Cube
  fr: Mock Cube
  it: Mock Cube
  en: Mock Cube
Description:
  de: Ein Beispiel Cube, der simulierte Daten enthält
  en: An example Cube containing some simulated data
Publisher: 
  - IRI: https://register.ld.admin.ch/opendataswiss/org/office_of_Mock
Creator:
  - IRI: https://register.ld.admin.ch/opendataswiss/org/office_of_Mock
Contributor:
  - IRI: https://register.ld.admin.ch/opendataswiss/org/bundesamt-fur-umwelt-bafu
    Name: Bundesamt für Mock Data
Date Created:
  2024-08-26
Contact Point:
  E-Mail: contact@mock.ld.admin.ch
  Name: Bundesamt für Mock Data
Base-URI: https://mock.ld.admin.ch/
Identifier: mock-example
Version: 1
Work Status: 
  Draft
Visualize:
  True
# Optional but recommended
Accrual Periodicity: yearly

# Optional
Namespace: mock

dimensions:
  # required
  Jahr:
    name:
      de: Jahr
      fr: An
      it: Anno
      en: Year
    description:
      de: Jahr der Erhebung
    dimension-type: Key Dimension
    datatype: URI
    scale-type: ordinal
    path: year
    data-kind: 
      type: temporal
      unit: year
    mapping:
      type: additive
      base: https://ld.admin.ch/time/year/
```

***

## New features: Shared dimension generation + Concept tables
Early March 2025, those two new features were added.  
As there might be some refactoring about the yaml configuration, you can currently find the explanations in the respective README and in the yaml examples as comments:
- Shared dimensions: [README](https://github.com/Kronmar-Bafu/lindas-pylindas/blob/main/pylindas/pyshareddimension/README.md) and [sd_description.yml](https://github.com/Kronmar-Bafu/lindas-pylindas/blob/main/example/Shared_Dimensions/shared_dimension_generation/sd_description.yml)  
- Concept tables: [README](https://github.com/Kronmar-Bafu/lindas-pylindas/blob/main/example/Cubes/concept_table_airport/README.md) and [description.yml](https://github.com/Kronmar-Bafu/lindas-pylindas/blob/main/example/Cubes/concept_table_airport/description.yml)

