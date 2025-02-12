from lib.models import adjMatrix

# Extracts the Source (publisher) , EdgeType and Destinations (list) of dependencies from microservices (via dependencyList)
# The publisher contains a broker attribute to show if the event goes through one
def getDataMatrix(dependencyList):

    dataMatrix = []
    sqlMatrix = []

    x = 0
    for dependency in dependencyList:
        adjacencyList = []
        rabbit = dependency.getRabbit()
        rabbitSQL = dependency.getRabbitSQL()
        publisher = rabbitSQL.getMicroservice()
        messageBroker = "auditlogservice"
        dataType = dependency.getRabbit().getMessageType()
        if x == 4:
            print()
        invoice = dependency.getInvoice()
        notification = dependency.getNotification()
        workshop = dependency.getWorkshop()

        invoiceSQL = dependency.getInvoiceSQL()
        notificationSQL = dependency.getNotificationSQL()
        workshopSQL = dependency.getWorkshopSQL()

        if invoice != None:
            adjacencyList.append("invoiceservice")
        if notification != None:
            adjacencyList.append("notificationservice")
        if workshop != None:
            adjacencyList.append("workshopmanagementeventhandler")

        # Contains all the microservice adj matrix from the rabbit event
        dataMatrix.append(adjMatrix(publisher, adjacencyList, dataType, messageBroker))

        # Contains all the microservices that write to SQL server
        # based on their matching sql event
        if invoiceSQL != None:
            sqlMatrix.append(adjMatrix(invoice, 'sqlserver', dataType, None))
        if notificationSQL != None:
            sqlMatrix.append(adjMatrix(notification, 'sqlserver', dataType, None))
        if workshopSQL != None:
            sqlMatrix.append(adjMatrix(workshop, 'sqlserver', dataType, None))
        if rabbitSQL != None:
            sqlMatrix.append(adjMatrix(rabbit, 'sqlserver', dataType, None))
        x = x+1


    return dataMatrix, sqlMatrix


# Could extract the information from the SVG files, but for now hard code it lul
def getCallMatrix():

    callMatrix = []

    callMatrix.append(adjMatrix("webapp", ["workshopmanagementapi", "vehiclemanagementapi", "customermanagementapi"], "call", None ))
    callMatrix.append(adjMatrix("workshopmanagementapi", ["sqlserver", "rabbitmq"], "call", None))
    callMatrix.append(adjMatrix("workshopmanagementeventhandler", ["sqlserver", "rabbitmq"], "call", None))
    callMatrix.append(adjMatrix("vehiclemanagementapi", ["sqlserver", "rabbitmq"], "call", None))
    callMatrix.append(adjMatrix("customermanagementapi", ["sqlserver", "rabbitmq"], "call", None))
    callMatrix.append(adjMatrix("auditlogservice", ["rabbitmq"], "call", None))
    callMatrix.append(adjMatrix("timeservice", ["rabbitmq"], "call", None))
    callMatrix.append(adjMatrix("invoiceservice", ["sqlserver", "rabbitmq", "mailserver"], "call", None))
    callMatrix.append(adjMatrix("notificationservice", ["sqlserver", "rabbitmq", "mailserver"], "call", None))

    return callMatrix
