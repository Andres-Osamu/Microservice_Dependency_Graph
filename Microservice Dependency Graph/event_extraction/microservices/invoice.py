from lib.models import invoiceEvent
from lib.external import re, json

# This method will find all invoice related logs and extract the ones that contain data dependencies.
# Returns Obj containing Microservice, DataModel. and original log line (log line can be used to trace specifice data values)
def findInvoiceEvents():

    invoiceEventModels = []
    invoiceEvents = []

    logFile = open(".\\Logs\\CorpusLog.txt", "r")
    lines = logFile.readlines()

    for line in lines:
        data = json.loads(line)
        if "invoiceservice" in data['Application'].lower():
            temp = data["@mt"]
            temp2 = data['@t']
            if temp2 == '2022-02-02T17:39:26.2140382Z':
                print()
            if "{" and "}" in temp:
                invoiceEvents.append(line)


    for event in invoiceEvents:
        eventData = json.loads(event)

        mt = eventData["@mt"]
        invoiceKeys = re.findall(r"\{([A-Za-z0-9_]+)\}", mt)
        invoiceValues = []

        for attribute in invoiceKeys:
            invoiceValues.append(eventData[attribute])

        invoiceDataModel = dict(zip(invoiceKeys, invoiceValues))
        invoiceEventModels.append(invoiceEvent("invoiceservice", invoiceDataModel, eventData))

    logFile.close()

    return invoiceEventModels