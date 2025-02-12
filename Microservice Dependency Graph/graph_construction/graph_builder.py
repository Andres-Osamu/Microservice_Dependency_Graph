
# from lib.utilities import getBodyData
from lib.models import rabbitEvent
from lib.external import nx

# NetworkX library allows to add attributes for each node
# Create multigraph using the call and data matrices.
def makeMultiGraph(dataMatrix, sqlMatrix, callMatrix, microserviceList):

    G = nx.MultiDiGraph()

    # Add all the nodes
    for microservice in microserviceList:
        G.add_node(microservice)

    # Add the call edges
    for call in callMatrix:
        for destination in call.getDestinations():
            source = call.getSource().lower()
            destination = destination.lower()
            # if source == "mailserver":
            #     print("hello")
            G.add_edge(call.getSource(), destination, key=call.getEdgeType(),edge=call.getEdgeType())

    # Add the data edges
    for data in dataMatrix:

        source = data.getSource().lower()


        # Case Study specific logic, the messageBroker is "AuditLogService" however the actual message broker is rabbitMQ
        if data.getMessageBroker() != None:
            logger = data.getMessageBroker().lower()
            messageBroker = 'rabbitmq'
            G.add_edge(messageBroker, logger, key=data.getEdgeType(),edge=data.getEdgeType())
            G.add_edge(source, messageBroker, key=data.getEdgeType(),edge=data.getEdgeType())

            for destination in data.getDestinations():
                destination = destination.lower()
                G.add_edge(messageBroker, destination, key=data.getEdgeType(), edge=data.getEdgeType())

        # Although the case study doesn't reach this condition (all events go through broker)
        # the optional logic is applied
        else:
            for destination in data.getDestinations():
                destination = destination.lower()
                G.add_edge(source, destination, key=data.getEdgeType(),edge=data.getEdgeType())

    x = 0
    for sql in sqlMatrix:

        if x == 3:
            print()
        if isinstance(sql.getSource(), rabbitEvent):
            source = sql.getSource().getSourceMicroservice().lower()
        else:
            source = sql.getSource().getMicroservice().lower()

        destination = sql.getDestinations().lower()

        G.add_edge(source, destination, key=sql.getEdgeType(),edge=sql.getEdgeType())

            #
    #
    print("Total number of nodes: ", int(G.number_of_nodes()))
    print("Total number of edges: ", int(G.number_of_edges()))
    print("List of all nodes: ", list(G.nodes()))
    print("List of all edges: ", list(G.edges( keys=True)))
    print("List of in edges: ", list(G.in_edges()))
    print("Degree for all nodes: ", list(G.degree()))
    # print("Total number of self-loops: ", int(G.number_of_selfloops()))
    # print("List of all nodes with self-loops: ", list(G.nodes_with_selfloops()))
    # print("List of all nodes we can go to in a single step from node E: ", list(G.neighbors('sqlserver')))
    return G


def createGML(multiGraph):
    nx.write_gml(multiGraph, "GraphAnalysis\DependencyMultiGraph.gml")