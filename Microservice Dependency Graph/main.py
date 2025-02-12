# Import necessary modules and functions
from container_discovery import getContainerData, writeContainerData, readContainerData
from event_extraction import extractSqlEvents, matchSQLEventsIP, findRabbitEvents, findInvoiceEvents, findNotificationEvents, findWorkshopManagementEvents, matchRabbitEvents

from event_correlation import removeFluff, matchResponseSQL, matchPubSub, domainKnowledgeEventAnalysis

from knowledge_processing import extractDomainKnowledge, filterDkCorpus, filterDkUnique

from graph_construction import combineEventData,getCallMatrix, getDataMatrix, getMicroserviceList, makeMultiGraph, createGML
# from event_correlation.cleaner import removeFluff
# from event_correlation import removeFluff


# from knowledge_processing import extractDomainKnowledge, filterDkCorpus, filterDkUnique
# from graph_construction import combineEventData, getMicroserviceList, getDataMatrix, getCallMatrix, makeMultiGraph, createGML


# Step 1
# Get container IPs
# This needs to execute only once, since microservice IPs are dynamic upon each docker-compose, need to obtain all logs and ips
# during the same instance, otherwise information won't match
# containerData = getContainerData()
# writeContainerData(containerData)


# Step 2
# Get SQL events
# This will get all SQL events and match them with the container IP that it corresponds to
containerList = readContainerData()
sqlCorpus = extractSqlEvents(containerList)
# This is a debug method
# insertCorpus = getINSERT(sqlCorpus)
sqlEventModels, tempDisplay = matchSQLEventsIP(sqlCorpus, containerList)


# Step 3
# Get RabbitMQ events
rabbitEventModels = findRabbitEvents()


# Step 4
# Get Microservice events
invoiceEventModels = findInvoiceEvents()
notificationEventModels = findNotificationEvents()
workshopEventModels = findWorkshopManagementEvents()


# Step 5
# Clean microservice events (remove all none data containing events, ie non response events)
invoiceEventModels, notificationEventModels, workshopEventModels = removeFluff(rabbitEventModels, invoiceEventModels, notificationEventModels, workshopEventModels)


# Step 6
# Match the Response Events with the SQL Events
invoiceSqlEventModels = matchResponseSQL(invoiceEventModels, sqlEventModels)
notificationSqlEventModels = matchResponseSQL(notificationEventModels, sqlEventModels)
workshopSqlEventModels = matchResponseSQL(workshopEventModels, sqlEventModels)


# Step 7
# Match Response events with Published events
# Not going to match with sql matched events.
matchedInvoiceEvents, dkInvoice = matchPubSub(rabbitEventModels, invoiceEventModels)
matchedNotificationEvents, dkNotification = matchPubSub(rabbitEventModels, notificationEventModels)
matchedWorkshopEvents, dkWorkshop = matchPubSub(rabbitEventModels, workshopEventModels)


# Step 8 Combine domain knowledge of all response events
# domainKnowledge = combineDKs(dkInvoice, dkNotification, dkWorkshop)
# Better method of fully obtaining all domain knowledge
dk = extractDomainKnowledge({}, rabbitEventModels)
dk = extractDomainKnowledge(dk, invoiceEventModels)
dk = extractDomainKnowledge(dk, notificationEventModels)
dk = extractDomainKnowledge(dk, workshopEventModels)
sortedDK = filterDkUnique(dk)
filteredDK = filterDkCorpus(dk)

# Step 9
# Match RabbitMQ events with SQL events to obtain the publisher of the event, using the domainKnowledge to assist
# This is obtained through the use of the SQL events, matching the data parameters from the RabbitMQ events with the
# insert parameters of the SQL events. Finalized with the Client IP of the SQL event
partialRabbitEventModels = matchRabbitEvents(rabbitEventModels, sqlEventModels)


# Step 10
# All events have gone through prilimary matching. Most events have the correct match others only have potential matches
# Cross reference all events and delete established events from other events potential events
# At the end, check the list of potential events remaining for non matched events
# select best potential event (how to determine this?)
# Uhhh something went wrong here, this bottom method isnt needed NVM this just modifies partial rabbit event models
# Need to change it such that empty rabbit events dont get a match (hard code)
matchedRabbitEvents = domainKnowledgeEventAnalysis(partialRabbitEventModels, filteredDK, sqlEventModels)


# Step 11
# Dependency Graph Generation Preparation
# Mulitgraph needs DataMatrix, CallMatrix, SqlMatrix and MicroserviceList
dependencyList = combineEventData(matchedRabbitEvents, matchedInvoiceEvents, matchedNotificationEvents, matchedWorkshopEvents,invoiceSqlEventModels, notificationSqlEventModels, workshopSqlEventModels)
dataMatrix, sqlMatrix = getDataMatrix(dependencyList)
callMatrix = getCallMatrix()
microserviceList = getMicroserviceList()


# Step 12
# Generate the multigraph using the matrices and microservice list
# save it to a gml file
multiGraph = makeMultiGraph(dataMatrix, sqlMatrix, callMatrix, microserviceList)
createGML(multiGraph)