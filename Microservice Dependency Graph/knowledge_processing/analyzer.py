from lib.utilities.helpers import modifyEvent

def combineDKs(dkInvoice, dkNotification, dkWorkshop):
    dk = {}

    for key in dkInvoice.keys():
        if key not in dk.keys():
            dk[key] = dkInvoice[key]
        else:
            for value in dkInvoice[key]:
                if value not in dk[key]:
                    dk[key].append(value)

    for key in dkNotification.keys():
        if key not in dk.keys():
            dk[key] = dkNotification[key]
        else:
            for value in dkNotification[key]:
                if value not in dk[key]:
                    dk[key].append(value)

    for key in dkWorkshop.keys():
        if key not in dk.keys():
            dk[key] = dkWorkshop[key]
        else:
            for value in dkWorkshop[key]:
                if value not in dk[key]:
                    dk[key].append(value)

    return dk



# There exist duplicate attribute names that correspond to separate unrelated data
# This method will change the attribute name of one of the attributes to prevent this conflict
def removeDkConflicts(sortedDK, dk, rabbitEventModels, invoiceEventModels, notificationEventModels, workshopEventModels):

    valueCorpus = []
    conflictCorpus = []
    valueList = list(sortedDK.values())

    # This will find all the conflicting attribute names
    for values in valueList:
        for value in values:
            if value not in valueCorpus:
                valueCorpus.append(value)
            else:
                if value not in conflictCorpus:
                    conflictCorpus.append(value)

    # Replace conflicting data in events
    invoiceEventModels = modifyEvent(invoiceEventModels, conflictCorpus, dk)
    notificationEventModels = modifyEvent(notificationEventModels, conflictCorpus, dk)
    workshopEventModels = modifyEvent(workshopEventModels, conflictCorpus, dk)
    rabbitEventModels = modifyEvent(rabbitEventModels, conflictCorpus, dk)

    # Replace all conflicting data in DKs
    for conflict in conflictCorpus:
        for key,values in sortedDK.items():
            if conflict in values:
                if len(values) != 1:
                    values.remove(conflict)

        for key,values in dk.items():
            if conflict in values:
                if len(values) != 1:
                    values.remove(conflict)
