from lib.models import sqlLog, sqlEvent, sqlDisplay
from lib.external import datetime, os, parser, pytz
from lib.utilities.helpers import getSP

# Extracts all data from SQL audits. Data is stored in a sqlLog object that contains the fileName (dbName) and the dictionary
# containing all the key/value pairs of the event
def extractSqlEvents(containList):
    logs = ["Customer", "Invoice", "Notification", "Vehicle", "Workshop", "WorkshopEvent"]
    # logs = ["Workshop", "WorkshopEvent"]
    fileNames = []
    for log in logs:
        temp = log + ".log"
        fileLocation = os.path.join('Logs', temp)
        fileNames.append(fileLocation)


    dateFormat = "%m/%d/%Y %H:%M:%S"

    sqlEventCorpus = []

    for file in fileNames:
        outfile = open(file, 'r', encoding='utf-16')
        data = outfile.readlines()
        count = 0
        logEvents = []
        keys = []
        values = []
        currentLogLine = ""
        for line in data:
            count += 1
            line = line.strip("\n")
            tokens = line.split(",")

            if count == 1:
                keys = tokens
            else:
                try:
                    datetime.strptime(tokens[0], dateFormat)
                    if len(currentLogLine) != 0:
                        values = currentLogLine.split(",")
                        sqlEvent = dict(zip(keys, values))
                        logEvents.append(sqlEvent)
                    currentLogLine = ""
                    values = []
                except ValueError:
                   print()
                currentLogLine = currentLogLine + line

        if len(currentLogLine) != 0:
            values = currentLogLine.split(",")
            sqlEvent = dict(zip(keys, values))
            logEvents.append(sqlEvent)

        sqlEventCorpus.append(sqlLog(file, logEvents))

    return sqlEventCorpus


# This will match the sql events with the microservice source (via ip)
# Some events are missing. Look at SQL DB to see which tables are missing
# Only looking at actionID : INSERT, should also look at the other IDs see what is missing
def matchSQLEventsIP(sqlCorpus, containerList):
    logSchema = {}
    sqlEventModels = []
    microservices  = {}
    # temp line
    tempDisplay = []

    # Make a dictionary with Microservice:IP pairs
    for container in containerList:
        name = container.getName()
        ip = container.getIP()
        if "src_" in name:
            name = name[5:-2]
        if "/" in name:
            name = name[1:]

        microservices[name] = ip

    # Adds all INSERT events into a list
    for sqlLog in sqlCorpus:
        db = sqlLog.getFileName()
        logs = sqlLog.getLogEvents()
        for log in logs:
            actionID = log["Action ID"]
            # ip = log.get("Client IP")
            if actionID == 'INSERT' or actionID == 'DELETE' or actionID == 'UPDATE':
            # if actionID == 'UPDATE':
                tempDate = log['Date'].split()[0]
                tempTime = log["Event Time "]
                time_sql = parser.parse(tempDate + " " + tempTime)
                time_sql = pytz.utc.localize(time_sql)
                sqlEventModels.append(sqlEvent(None, log, sqlLog.getFileName(), time_sql))
                parameters = getSP(log)
                #Temp Line
                tempDisplay.append(sqlDisplay(sqlLog.getFileName(), time_sql, parameters, log["Statement"], log, actionID))

    # Matches all the INSERT events IPs with the corresponding microservice IPs
    for sql in sqlEventModels:
        clientIP = sql.getLogLine()["Client IP"]
        for microservice, ip in microservices.items():
            if ip == clientIP:
                sql.setMicroservice(microservice)

    # Problem:
    # rabbit event models are ordered in chronological order, FIFO
    # sql event models are ordered in reverse chronological order, FILO
    # except since the sql logs come from various dbs, the ordering is non-linear
    # it is only FIFO in sections (per sql log file)

    # Solution:
    # order list of sql events by time in chronological order, FIFO
    sqlEventModels.sort(key=lambda sqlEvent: sqlEvent.timestamp)

    return sqlEventModels, tempDisplay
