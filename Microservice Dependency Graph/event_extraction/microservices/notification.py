from lib.models import notificationEvent
from lib.external import re, json

# This method will find all notification related logs and extract the ones that contain data dependencies
# Returns Obj containing Microservice, DataModel. and original log line (log line can be used to trace specifice data values)
def findNotificationEvents():

    notificationEventModels = []
    notificationEvents = []

    logFile = open(".\\Logs\\CorpusLog.txt", "r")
    lines = logFile.readlines()

    for line in lines:
        data = json.loads(line)
        if "notificationservice" in data['Application'].lower():
            temp = data["@mt"]
            if "{" and "}" in temp:
                notificationEvents.append(line)

    for event in notificationEvents:
        eventData = json.loads(event)

        mt = eventData["@mt"]
        notificationKeys = re.findall(r"\{([A-Za-z0-9_]+)\}", mt)
        notificationValues = []

        for attribute in notificationKeys:
            notificationValues.append(eventData[attribute])

        notificationDataModel = dict(zip(notificationKeys, notificationValues))
        notificationEventModels.append(notificationEvent("notificationservice", notificationDataModel, eventData))

    logFile.close()

    return notificationEventModels