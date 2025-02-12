from lib import getBodyData

# This method goes through all the event occurrences, does not only go through unique bodyDataModels
# This may be useful for tracing specific BodyData
def removeFluff(auditEventModel, invoiceEventModels, notificationEventModels, workshopEventModels ):

    tempAuditEventModel = auditEventModel.copy()
    # # Deleting all Published Events that do not contain Data
    # # i.e. DayHasPassed
    for auditEvent in tempAuditEventModel:
        if len(auditEvent.getBodyDataModel()) == 0:
            tempAuditEventModel.remove(auditEvent)


    x = 0

    # Each while loop will loop through all of the invoice/notification/workshop events and find events
    # that contain data values that are also in the rabbitEvents
    while x < len(invoiceEventModels):
        fluff = True
        invoiceEvent = invoiceEventModels[x]

        for auditEvent in tempAuditEventModel:

            auditDataModel = auditEvent.getBodyDataModel()
            invoiceDataModel = invoiceEvent.getBodyDataModel()

            auditBodyData = getBodyData(auditDataModel)
            invoiceBodyData = getBodyData(invoiceDataModel)

            if not len(list(set(auditBodyData) & (set(invoiceBodyData)))) == 0:
                fluff = False
                break
        if fluff:
            invoiceEventModels.remove(invoiceEvent)
        else:
            x += 1


    for invoice in invoiceEventModels:
        print(invoice.getLogLine())

    x = 0
    while x < len(notificationEventModels):
        fluff = True
        notificationEvent = notificationEventModels[x]
        for auditEvent in tempAuditEventModel:
            # if "Id" in notificationEvent.getDataModel():
            #     print()

            auditDataModel = auditEvent.getBodyDataModel()
            notificationDataModel = notificationEvent.getBodyDataModel()

            auditBodyData = getBodyData(auditDataModel)
            notificationBodyData = getBodyData(notificationDataModel)

            # if not len(list(set(notificationEvent.getData())&(set(auditEvent.getBodyData())))) == 0:
            if not len(list(set(auditBodyData) & (set(notificationBodyData)))) == 0:
                fluff = False
                break
        if fluff:
            notificationEventModels.remove(notificationEvent)
        else:
            x += 1


    x = 0
    while x < len(workshopEventModels):
        fluff = True
        workshopEvent = workshopEventModels[x]
        for auditEvent in tempAuditEventModel:
            # if "Id" in workshopEvent.getDataModel():
            #     print()
            auditDataModel = auditEvent.getBodyDataModel()
            workshopDataModel = workshopEvent.getBodyDataModel()

            auditBodyData = getBodyData(auditDataModel)
            workshopBodyData = getBodyData(workshopDataModel)

            # if not len(list(set(workshopEvent.getData())&(set(auditEvent.getBodyData())))) == 0:
            if not len(list(set(auditBodyData) & (set(workshopBodyData)))) == 0:
                fluff = False
                break
        if fluff:
            workshopEventModels.remove(workshopEvent)
        else:
            x += 1



    return invoiceEventModels, notificationEventModels, workshopEventModels