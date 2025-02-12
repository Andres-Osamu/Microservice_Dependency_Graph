# Import functions from the composer module
# - combineEventData: Combines event data for graph construction.
from .composer import combineEventData, getMicroserviceList

# Import functions from the matrix_generator module
# - getDataMatrix: Extracts dependency relationships from event data.
# - getCallMatrix: Retrieves hard-coded service call relationships.
from .matrix_generator import getDataMatrix, getCallMatrix

# Import functions from the graph_builder module
# - makeMultiGraph: Creates a NetworkX multigraph using data and call matrices.
# - createGML: Exports the multigraph to a GML file.
from .graph_builder import makeMultiGraph, createGML

# Define the public API of the module
# This list specifies which functions are exposed when using `from graph_construction import *`
# - combineEventData: Function to combine event data for graph construction.
# - getDataMatrix: Function to extract dependency relationships.
# - getCallMatrix: Function to retrieve service call relationships.
# - makeMultiGraph: Function to create a multigraph.
# - createGML: Function to export the multigraph to a GML file.
__all__ = [
    "combineEventData",
    "getMicroserviceList",
    "getDataMatrix",
    "getCallMatrix",
    "makeMultiGraph",
    "createGML",
]