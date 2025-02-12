from lib.external import parser, re
from lib.models import sqlData

# Similar to getBodyData except this method returns a dict with all the keys and values
# This is used for when an event has nested dicts and both the key and values are needed
def getBodyDict(bodyDataModel):

    bodyDict = {}

    for (key, value) in bodyDataModel.items():
        if type(value) is dict:
            for (nestedKey, nestedValue) in value.items():
                newKey = key + "-" + nestedKey
                bodyDict[newKey] = nestedValue
        else:
            if 'time' in key.lower():
                formattedValue = parser.parse(value)
                bodyDict[key] = formattedValue
            else:
                bodyDict[key] = value


    return bodyDict


# This method is for UPDATE sql type events.
# Since the UPDATE logs only provide the parameters that are being updated,
# this method will extract all of the table's parameters
def getDatabaseParameters(sql, sqlEventModels):
    additionalParameters = None
    dbName_sql = sql.getLogLine()['Database Name']
    objName_sql = sql.getLogLine()['Object Name']
    logFile_sql = sql.getLogFile()

    for event in sqlEventModels:
        dbName_event = event.getLogLine()['Database Name']
        objName_event = event.getLogLine()['Object Name']
        logFile_event = event.getLogFile()
        actionID_event = event.getLogLine()['Action ID']

        if dbName_sql == dbName_event and objName_sql == objName_event and logFile_sql == logFile_event and actionID_event == 'INSERT':
            additionalParameters = getSqlParameters(event)
            return additionalParameters

    return additionalParameters


# Helper method to get the parameters of a sql statement
# This is needed for calculating the certainty of matched sql/response events
def getSqlParameters(sql):

    parameters_sql = None
    statement = sql.getLogLine()["Statement"]

    if sql.getLogLine()["Action ID"] == 'INSERT':
        parameters_sql = re.findall(r'\(.*?\)', statement)[0][1:-1]
        parameters_sql = parameters_sql.replace("<c/>", "").replace("[", "").replace("]", "").split()
    elif sql.getLogLine()["Action ID"] == 'DELETE':
        parameters_sql = list(filter(lambda x: x[0] == '@', statement.split()))
        parameters_sql = [x.replace('@', '') for x in parameters_sql]
    elif sql.getLogLine()["Action ID"] == 'UPDATE':
        parameters_sql = list(filter(lambda x: x[0] == '@', statement.split()))
        parameters_sql = [x.replace('@', '').replace('<nl/>', '') for x in parameters_sql]

    return parameters_sql


# Returns a list of all Values in BodyDataModel
# This is used rather than just .values() because some dicts have nested dicts
def getBodyData(bodyDataModel):

    bodyData = []

    for (key, value) in bodyDataModel.items():

        if type(value) is dict:
            bodyData += list(value.values())
        else:
            if "time" in key.lower():
                formattedValue = parser.parse(value)
                bodyData.append(formattedValue)

            else:
                bodyData.append(value)

    return bodyData


def getSP(sql):
    parameters_sql = None
    statement = sql["Statement"]

    if sql["Action ID"] == 'INSERT':
        parameters_sql = re.findall(r'\(.*?\)', statement)[0][1:-1]
        parameters_sql = parameters_sql.replace("<c/>", "").replace("[", "").replace("]", "").split()
    elif sql["Action ID"] == 'DELETE':
        parameters_sql = list(filter(lambda x: x[0] == '@', statement.split()))
        parameters_sql = [x.replace('@', '') for x in parameters_sql]
    elif sql["Action ID"] == 'UPDATE':
        parameters_sql = list(filter(lambda x: x[0] == '@', statement.split()))
        parameters_sql = [x.replace('@', '').replace('<nl/>', '') for x in parameters_sql]

    return parameters_sql


# From the sqlEventCorpus extracts all the logs with Action ID 'INSERT'
# Debugging method
def getINSERT(sqlEventCorpus):
    insertCorpus = []

    for event in sqlEventCorpus:
        for log in event.getLogEvents():
            temp = log.get("Action ID")
            if temp == "DELETE":
                logSource = event.getFileName()
                action = log.get("Action ID")
                dbName = log.get("Database Name")
                tableName = log.get("Object Name")
                date = log.get("Date")
                statement = log.get("Statement")
                ip = log.get("Client IP")
                transactionID = log.get("Transaction ID")
                objectID = log.get("Object ID")
                insertCorpus.append(sqlData(logSource, action, dbName, tableName, date, statement, ip, transactionID, objectID))


    return insertCorpus


# Find the data corresponding to the attribute conflict
# modify the event data (select a synonym to replace the conflicting attribute name)
def modifyEvent(eventModels, conflictCorpus, dk):

    x = 0
    for conflictAttribute in conflictCorpus:
        for key, values in dk.items():
            if conflictAttribute in values:
                conflictData = key

            # Iterates all invoice events and find any occurance of the conflictAttribute:conflictData occurence
            # changes the attribute name to a new one
            for event in eventModels:
                bodyDataModel = event.getBodyDataModel()

                if (conflictAttribute, conflictData) in bodyDataModel.items():
                    x+=1
                    if x==2:
                        print()
                    newAttributeName = dk[conflictData][0]

                    # This will fix the bodydata
                    newBody = {}
                    for key, value in bodyDataModel.items():
                        if key == conflictAttribute:
                            newBody[newAttributeName] = conflictData
                        else:
                            newBody[key] = value

                    event.setBodyDataModel(newBody)

                    # This will fix the log line
                    newLog = {}
                    logLine = event.getLogLine()
                    for key, value in logLine.items():
                        if key == conflictAttribute:
                            newLog[newAttributeName] = conflictData
                        elif key == '@mt':
                            formattedConflictAtt = "{%s}" % conflictAttribute
                            formattedNewAtt = "{%s}" % newAttributeName
                            newMT = logLine['@mt'].replace(formattedConflictAtt, formattedNewAtt)
                            newLog[key] = newMT
                        else:
                            newLog[key] = value

                    event.setLogLine(newLog)