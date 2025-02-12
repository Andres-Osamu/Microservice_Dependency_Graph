class containerData:
    def __init__(self, name, ip, id):
        self.name = name
        self.ip = ip
        self.id = id

    def getName(self):
        return self.name

    def getIP(self):
        return self.ip

    def getID(self):
        return self.id


class sqlLog:
    def __init__(self, fileName, logEvents):
        self.fileName = fileName
        self.logEvents = logEvents

    def getFileName(self):
        return self.fileName

    def getLogEvents(self):
        return self.logEvents

class sqlData:
    def __init__(self, logSource, action, dbName, tableName, date, statement, ip, transactionID, objectID):
        self.logSource =logSource
        self.action = action
        self.dbName = dbName
        self.tableName = tableName
        self.date = date
        self.statement = statement
        self.ip = ip
        self.transactionID = transactionID
        self.objectID = objectID

class sqlDisplay:
    def __init__(self, logFile, timestamp, parameters, statement, logLine, type):
        self.logFile = logFile
        self.timestamp = timestamp
        self.parameters = parameters
        self.statement = statement
        self.logLine = logLine
        self.type = type

class sqlEvent:
    def __init__(self, microservice, logLine, logFile, timestamp):
        self.microservice = microservice
        self.logLine = logLine
        self.logFile = logFile
        self.timestamp = timestamp

    def getMicroservice(self):
        return self.microservice

    def getLogLine(self):
        return self.logLine

    def getLogFile(self):
        return self.logFile

    def getTimeStamp(self):
        return self.timestamp

    def setMicroservice(self, m):
        self.microservice = m


class rabbitEvent:
    def __init__(self, messageType, bodyDataModel, logLine, messageBroker, sourceMicroservice):
        self.messageType = messageType
        self.bodyDataModel = bodyDataModel
        self.logLine = logLine
        self.messageBroker = messageBroker
        self.sourceMicroservice = sourceMicroservice

    def getMessageType(self):
        return self.messageType

    def getBodyDataModel(self):
        return self.bodyDataModel

    def getLogLine(self):
        return self.logLine

    def getMessageBroker(self):
        return self.messageBroker

    def getSourceMicroservice(self):
        return self.sourceMicroservice

    def setSourceMicroservice(self, sourceMicroservice):
        self.sourceMicroservice = sourceMicroservice

    def setBodyDataModel(self, newBodyDataModel):
        self.bodyDataModel = newBodyDataModel

    def setLogLine(self, newLogLine):
        self.logLine = newLogLine


class publishedEvent:
    def __init__(self, publisher, rabbitEvent, sqlEvent, partialEvents):
        self.publisher = publisher
        self.rabbitEvent = rabbitEvent
        self.sqlEvent = sqlEvent
        self.partialEvents = partialEvents

    def getPublisher(self):
        return self.publisher

    def getRabbitEvent(self):
        return self.rabbitEvent

    def getSqlEvent(self):
        return self.sqlEvent

    def getPartialEvents(self):
        return self.partialEvents

    def setSqlEvent(self, event):
        self.sqlEvent = event

    def setPublisher(self, pub):
        self.publisher = pub

class subscribedEvent:
    def __init__(self, subscriber, responseEvent, sqlEvent, rippleEvent, timeOnlyEvents, certainty, xorSQL, xorResponse):
        self.subscriber = subscriber
        self.responseEvent = responseEvent
        self.sqlEvent = sqlEvent
        self.rippleEvents = rippleEvent
        self.timeOnlyEvents = timeOnlyEvents
        self.certainty = certainty
        self.xorSQL = xorSQL
        self.xorResponse = xorResponse

    def getResponseEvent(self):
        return self.responseEvent

    def getSqlEvent(self):
        return self.sqlEvent

# This class is used to match a sub event with the rabbit pub event
class matchedPubSubEvent:
    def __init__(self, publishedEvent, subscribedEvents):
        self.publishedEvent = publishedEvent
        self.subscribedEvents = subscribedEvents

    def getPublisher(self):
        return self.publishedEvent

    def getSubscriber(self):
        return self.subscribedEvents

    def setPublisher(self, publisher):
        self.publishedEvent = publisher

    def setSubscriber(self, subscriber):
        self.subscribedEvents = subscriber

class potentialPubSubEvent:
    def __init__(self, publisher, subscriber):
        self.publisher = publisher
        self.subscriber = subscriber

    def getPublisher(self):
        return self.publisher

    def getSubscriber(self):
        return self.subscriber

class workshopEvent:
    def __init__(self, microservice, bodyDataModel, logLine):
        self.microservice = microservice
        self.bodyDataModel = bodyDataModel
        self.logLine = logLine

    def getMicroservice(self):
        return self.microservice

    def getBodyDataModel(self):
        return self.bodyDataModel

    def getLogLine(self):
        return self.logLine

    def setBodyDataModel(self, newBodyDataModel):
        self.bodyDataModel = newBodyDataModel

    def setLogLine(self, newLogLine):
        self.logLine = newLogLine


class invoiceEvent:
    def __init__(self, microservice, bodyDataModel, logLine):
        self.microservice = microservice
        self.bodyDataModel = bodyDataModel
        self.logLine = logLine

    def getMicroservice(self):
        return self.microservice

    def getBodyDataModel(self):
        return self.bodyDataModel

    def getLogLine(self):
        return self.logLine

    def setBodyDataModel(self, newBodyDataModel):
        self.bodyDataModel = newBodyDataModel

    def setLogLine(self, newLogLine):
        self.logLine = newLogLine


class notificationEvent:
    def __init__(self, microservice, dataModel, logLine):
        self.microservice = microservice
        self.bodyDataModel = dataModel
        self.logLine = logLine

    def getMicroservice(self):
        return self.microservice

    def getBodyDataModel(self):
        return self.bodyDataModel

    def getLogLine(self):
        return self.logLine

    def setBodyDataModel(self, newBodyDataModel):
        self.bodyDataModel = newBodyDataModel

    def setLogLine(self, newLogLine):
        self.logLine = newLogLine

class matchedDependencyData:
    # def __init__(self, publisher, invoice, notification, workshop, messageBroker):

    def __init__(self, rabbit, invoice, notification, workshop, invoiceSQL, notificationSQL, workshopSQL, rabbitSQL):
        self.rabbit = rabbit
        self.invoice = invoice
        self.notification = notification
        self.workshop = workshop
        self.invoiceSQL = invoiceSQL
        self.notificationSQL = notificationSQL
        self.workshopSQL = workshopSQL
        self.rabbitSQL = rabbitSQL

    def getRabbit(self):
        return self.rabbit

    def getInvoice(self):
        return self.invoice

    def getNotification(self):
        return self.notification

    def getWorkshop(self):
        return self.workshop

    def getInvoiceSQL(self):
        return self.invoiceSQL

    def getNotificationSQL(self):
        return self.notificationSQL

    def getWorkshopSQL(self):
        return self.workshopSQL

    def getRabbitSQL(self):
        return self.rabbitSQL

class adjMatrix:
    def __init__(self, source, destinations, edgeType, messageBroker):
        self.source = source
        self.destinations = destinations
        self.edgeType = edgeType
        self.messageBroker = messageBroker

    def getSource(self):
        return self.source

    def getDestinations(self):
        return self.destinations

    def getEdgeType(self):
        return self.edgeType

    def getMessageBroker(self):
        return self.messageBroker