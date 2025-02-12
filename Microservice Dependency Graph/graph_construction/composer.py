from lib.models import matchedDependencyData


def combineEventData(partialRabbitEventModels, matchedInvoiceEvents, matchedNotificationEvents, matchedWorkshopEvents,invoiceSqlEventModels, notificationSqlEventModels, workshopSqlEventModels):

    dependencyList = []
    sqlMatrix = []

    for pubEvent in partialRabbitEventModels:
        rabbitEvent = pubEvent.getRabbitEvent()
        rabbitEventLog = rabbitEvent.getLogLine()
        rabbitSQL = pubEvent.getSqlEvent()
        publisher = rabbitSQL.getMicroservice()

        rabbitEvent.setSourceMicroservice(publisher)


        matchedInvoiceData = None
        matchedNotificationData = None
        matchedWorkshopData = None

        invoiceSQL = None
        notificationSQL = None
        workshopSQL = None


        # Cross reference pubEvent data with invoice data
        # ie does the invoice publisher data coincide with the pubEvent rabbit data
        for invoice in matchedInvoiceEvents:

            publishedEventLog = invoice.getPublisher().getLogLine()

            if publishedEventLog == rabbitEventLog:
                matchedInvoiceData = invoice.getSubscriber()

                # Cross reference the specific invoice event and the invoiceSQL data
                # ie does the invoice event coincide with an SQL event
                # if so add SQL to the adjMatrix
                invoiceEvent = invoice.getSubscriber().getLogLine()

                for sql in invoiceSqlEventModels:
                    responseEvent = sql.getResponseEvent().getLogLine()
                    sqlEvent = sql.getSqlEvent()
                    if responseEvent == invoiceEvent and sqlEvent != None:
                        invoiceSQL = sqlEvent

        for notification in matchedNotificationEvents:

            publishedEventLog = notification.getPublisher().getLogLine()

            if publishedEventLog == rabbitEventLog:
                matchedNotificationData = notification.getSubscriber()

                # There is an edge case where there are two notification events for a rabbit event (DayHasPassed)
                # This additional logic is used to acknowledge this
                if isinstance(notification.getSubscriber(), list):
                    for subscriber in notification.getSubscriber():
                        notificationSubscribedEvent = subscriber.getLogLine()

                        for sql in notificationSqlEventModels:
                            responseEvent = sql.getResponseEvent().getLogLine()
                            sqlEvent = sql.getSqlEvent()
                            if responseEvent == notificationSubscribedEvent and sqlEvent != None:
                                notificationSQL = sqlEvent

                else:
                    notificationEvent = notification.getSubscriber().getLogLine()
                    for sql in notificationSqlEventModels:
                        responseEvent = sql.getResponseEvent().getLogLine()
                        sqlEvent = sql.getSqlEvent()
                        if responseEvent == notificationEvent and sqlEvent != None:
                            notificationSQL = sqlEvent


        for workshop in matchedWorkshopEvents:

            publishedEventLog = workshop.getPublisher().getLogLine()

            if publishedEventLog == rabbitEventLog:
                matchedWorkshopData = workshop.getSubscriber()

                workshopEvent = workshop.getSubscriber().getLogLine()

                for sql in workshopSqlEventModels:
                    responseEvent = sql.getResponseEvent().getLogLine()
                    sqlEvent = sql.getSqlEvent()
                    if responseEvent == workshopEvent and sqlEvent != None:
                        workshopSQL = sqlEvent

        dependencyList.append(matchedDependencyData(rabbitEvent, matchedInvoiceData, matchedNotificationData, matchedWorkshopData, invoiceSQL, notificationSQL, workshopSQL, rabbitSQL))


    return dependencyList


# Hard coded, could look at the MicroDepGraph files and extract from there
# Look into lxml
def getMicroserviceList():
    microserviceList = ["webapp", "workshopmanagementapi", "customermanagementapi", "invoiceservice", "mailserver",
                        "rabbitmq", "sqlserver", "timeservice", "vehiclemanagementapi", "workshopmanagementeventhandler",
                        "auditlogservice", "notificationservice"]

    return microserviceList