from lib.models import workshopEvent
from lib.external import re, json

# This method will find all WorkshopManagementEventHandler related logs and extract the ones that contain data dependencies
# Returns Obj containing Microservice, DataModel. and original log line (log line can be used to trace specifice data values)
def findWorkshopManagementEvents():
    workshopEventModels = []
    workshopEvents = []

    logFile = open(".\\Logs\\CorpusLog.txt", "r")
    lines = logFile.readlines()

    for line in lines:
        data = json.loads(line)
        if "87f8ff9a" in data["@@i"]:
            print()
        if "workshopmanagementeventhandler" in data['Application'].lower():
            temp = data["@mt"]
            if "{" and "}" in temp:
                workshopEvents.append(line)


    for event in workshopEvents:
        eventData = json.loads(event)

        mt = eventData["@mt"]
        workshopKeys = re.findall(r"\{([A-Za-z0-9_]+)\}", mt)
        workshopValues = []

        for attribute in workshopKeys:
            workshopValues.append(eventData[attribute])


        if "CustomerId" in data["@mt"]:
            print()

        workshopDataModel = dict(zip(workshopKeys, workshopValues))

        workshopEventModels.append(workshopEvent("workshopmanagementeventhandler", workshopDataModel, eventData))

    logFile.close()

    return workshopEventModels