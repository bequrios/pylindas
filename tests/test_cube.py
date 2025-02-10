from pylindas.pycube import Cube
from rdflib import Graph
import pandas as pd
import pytest
import yaml

class TestClass:

    def setup_method(self):
        with open("tests/test.yml") as file:
            cube_yaml = yaml.safe_load(file)
        test_df = pd.read_csv("tests/test_data.csv")
        self.cube = Cube(
            dataframe=test_df, cube_yaml=cube_yaml,
            environment="TEST", local=True
        )
        self.cube.prepare_data().write_cube(opendataswiss=True).write_observations().write_shape()
        self.cube.serialize("tests/test_cube.ttl")

    def test_standard_error(self):
        sparql = (
            "ASK"
            "{"
            "  ?shape a cube:Constraint ;"
            "    sh:property ?prop ."
            "  ?prop schema:name 'Standardfehler für Wert2'@de ;"
            "    schema:description 'Standardfehler der Schätzung Wert2'@de ;"
            "    sh:path mock:standardError ;"
            "    qudt:scaleType qudt:RatioScale ;"
            "    qudt:hasUnit unit:PERCENT ;"
            "    meta:dimensionRelation ["
            "      a relation:StandardError;"
            "      meta:relatesTo mock:value2 ;"
            "    ] ."
            "}"
        )

        result = self.cube._graph.query(sparql)
        assert bool(result)

    def test_upper_uncertainty(self):
        sparql = (
            "ASK"
            "{"
            "  ?shape a cube:Constraint ;"
            "    sh:property ?prop ."
            "  ?prop sh:path mock:upperUncertainty ;"
            "    schema:name 'Upper Unsicherheit'@de ;"
            "    sh:maxCount 1 ;"
            "    qudt:scaleType qudt:RatioScale ;"
            "    meta:dimensionRelation ["
            "      a relation:ConfidenceUpperBound ;"
            '      dct:type "Confidence interval" ;'
            "      meta:relatesTo mock:value ;"
            "    ] ."
            "}"
        )

        result = self.cube._graph.query(sparql)
        assert bool(result)

    def test_lower_uncertainty(self):
        sparql = (
            "ASK"
            "{"
            "  ?shape a cube:Constraint ;"
            "    sh:property ?prop ."
            "  ?prop schema:name 'Lower Unsicherheit'@de ;"
            "    schema:description 'Lower Unsicherheit'@de ;"
            "    sh:path mock:lowerUncertainty ;"
            "    qudt:scaleType qudt:RatioScale ;"
            "    qudt:hasUnit unit:PERCENT ;"
            "    meta:dimensionRelation ["
            "      a relation:ConfidenceLowerBound ;"
            "      dct:type 'Confidence interval' ;"
            "      meta:relatesTo mock:value ;"
            "    ] ."
            "}"
        )

        result = self.cube._graph.query(sparql)
        assert bool(result)

    def test_point_limit(self):
        sparql = (
            "ASK"
            "{"
            "  ?shape a cube:Constraint ;"
            "    sh:property ?prop ."
            "  ?prop sh:path mock:value2 ;"
            "    meta:annotation ?annotation ."
            "  ?annotation a meta:Limit ;"
            "    schema:value 11 ;"
            "    meta:annotationContext ["
            "      sh:path mock:year ;"
            "      sh:hasValue <https://ld.admin.ch/time/year/2020> ;"
            "    ] ; "
            "    meta:annotationContext [ "
            "      sh:path mock:station ;"
            "      sh:hasValue <https://mock.ld.admin.ch/station/02> ;"
            "  ]."
            "}"
        )
    
        result = self.cube._graph.query(sparql)
        assert bool(result)
    
    def test_range_limit(self):
        sparql = (
            "ASK"
            "{"
            "  ?shape a cube:Constraint ;"
            "    sh:property ?prop ."
            "  ?prop sh:path mock:value2 ;"
            "    meta:annotation ?annotation ."
            "  ?annotation a meta:Limit ;"
            "    schema:minValue 9 ;"
            "    schema:maxValue 13 ;"
            "    meta:annotationContext ["
            "      sh:path mock:year ;"
            "      sh:hasValue <https://ld.admin.ch/time/year/2021> ;"
            "    ] ; "
            "    meta:annotationContext [ "
            "      sh:path mock:station ;"
            "      sh:hasValue <https://mock.ld.admin.ch/station/02> ;"
            "    ] ."
            "}"
        )

        result = self.cube._graph.query(sparql)
        assert bool(result)

    def test_annotation_dimension(self):
        sparql = (
            "ASK"
            "{"
            "  ?shape a cube:Constraint ;"
            "    sh:property ?prop ."
            "  ?prop sh:path mock:status ;"
            "     schema:name 'Veröffentlichungsstatus'@de ;"
            "     qudt:scaleType qudt:NominalScale ."
            "   minus {"
            "     ?prop a cube:KeyDimension ."
            "   }"
            "   minus {"
            "     ?prop a cube:MeasureDimension ."
            "   }"
            "}"
        )

        result = self.cube._graph.query(sparql)
        assert bool(result)

    def test_validate_basic_valid(self):
        result_bool, result_massage = self.cube._validate_base()
        assert bool(result_bool)

    def test_validate_visualize_valid(self):
        result_bool, result_message = self.cube._validate_visualize_profile()
        assert bool(result_bool)

    def test_validate_opendata_valid(self):
        result_bool, result_message = self.cube._validate_opendata_profile()
        assert bool(result_bool)

    def test_validate_whole(self):
        result_bool, result_message = self.cube.validate()
        assert result_message == "Cube is valid."

    def test_hierarchies(self):
        sparql = (
            "ASK"
            "{"
            "  ?shape a cube:Constraint ;"
            "    sh:property ?prop ."
            "  ?prop sh:path mock:station ;"
            "    meta:inHierarchy ?hierarchy ."
            "  ?hierarchy a meta:Hierarchy ;"
            "    meta:hierarchyRoot <https://mock.ld.admin.ch/station/switzerland> ;"
            "    schema:name 'Schweiz' ;"
            "    meta:nextInHierarchy ?nextInHierarchy ."
            "  ?nextInHierarchy schema:name 'Stationen' ;"
            "    sh:path schema:hasPart ;"
            "}"
        )

        result = self.cube._graph.query(sparql)
        assert bool(result)