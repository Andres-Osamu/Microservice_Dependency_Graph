from lib.models import rabbitEvent, publishedEvent
from lib.external import re, json, parser, timedelta, pytz
from lib.utilities.helpers import getBodyDict, getDatabaseParameters, getSqlParameters

# Finds all published events from the AuditLog corpus
# Creates object containing MessageType, BodyDataModel, BodyData, the original event log line and a NONE publisher
# The publisher will be found in 'matchRabbitEvents'
def findRabbitEvents():

    rabbitEventList = []

    logFile = open(".\\Logs\\CorpusLog.txt", "r")
    lines = logFile.readlines()

    for line in lines:
        data = json.loads(line)
        if data['Application'] == "AuditlogService":
            if "{MessageType} - {Body}" in data["@mt"]:
                messageType = data["MessageType"]
                bodyData = json.loads(data["Body"])
                messageBroker = "rabbitmq"

                rabbitEventList.append(rabbitEvent(messageType, bodyData, data, messageBroker, None))

    logFile.close()

    return rabbitEventList


# Takes all the published events from the rabbitMQ and matches them with the original source microservice
# This is accomplished using the SQL events and their corresponding client IPs
# TODO: include sql UPDATES, workshopplanning not finding anything
# The issue is with the rabbitmq having subdictionary in the data dictionary, of which the keys dont have proper titles.
# Current solution is to look at the other system events and trace the specific values and obtain their proper keys
# ie Item1 : J. Cole
# ie CustomerName : J. Cole

# Need a method that will determine if an events keys are valid (ie they appear in sql as columns)
# if not then we need to scan the system logs of the invalid keys value in attempts to find a proper key

# OR match the system event with the  SQL event based on parameter values, then just take the column names to replace the invalid keys
# in this situation need to check that the order is correct

# NOTE
# publishedEvent and subscribedEvent are potentially the same class.
def matchRabbitEvents(rabbitEventModels, sqlEventModels):

    matchedRabbitEventModels = []

    # For every rabbit event, find the source sql event
    # Due to latency in the logging systems, rabbitMQ event can occurs AFTER the source sql event
    # as a result we cannot get the first sql event after rabbit event
    # Must collect the sql events that contain the same parameters as the rabbit event
    # the collection begins with the first occurence and ends when the sql parameters no longer match
    # since there will be multiple occurences of the same time of sql event, we can take advantage of the
    # linear timeline of the logs, once a different sql event (diff parameters) occur we know we are no
    # longer dealing with the same rabbit event

    for rabbit in rabbitEventModels:
        # parameters_rabbit = list(rabbit.getBodyDataModel().keys())[:-2]
        parameters_rabbit = list(getBodyDict(rabbit.getBodyDataModel()))[:-2]
        time_rabbit = parser.parse(rabbit.getLogLine()["@t"])


        rangeStart = time_rabbit - timedelta(milliseconds=500)
        rangeEnd = time_rabbit + timedelta(milliseconds=500)

        potentialEvents = []
        timeOnlyEvents = []

        for sql in sqlEventModels:
            tempDate = sql.getLogLine()['Date'].split()[0]
            tempTime = sql.getLogLine()["Event Time "]
            time_sql = parser.parse(tempDate + " " + tempTime)
            time_sql = pytz.utc.localize(time_sql)

            #Step 1 Check if sql event is within range of rabbit event (Range will be +/- 0.5second
            if rangeStart <= time_sql <= rangeEnd:
                # Step 2 checks to see if sql event type is INSERT or DELETE or UPDATE
                # different methods needed for extracting the parameters from the statement
                # Additionally, if the type is UPDATE, use separate method to find the tables parameters
                actionID = sql.getLogLine()['Action ID']
                if actionID == 'UPDATE':
                    parameters_sql = getDatabaseParameters(sql, sqlEventModels)
                else:
                    parameters_sql = getSqlParameters(sql)


                # Step 3 check if the parameters match. If there are matching parameters append to PotentialEvents
                # otherwise append to timeOnlyEvents
                intersection = set(parameters_rabbit).intersection(parameters_sql)

                if len(intersection) != 0:
                    potentialEvents.append(sql)
                # If there are no parameter matching, we will save the event for later comparisons
                else:
                    timeOnlyEvents.append(sql)

        # If no sql events with intersecting parameters events are found, store only time matching events
        if potentialEvents == []:
            # Get sql parameters, cross reference with DKs. If sql parameters are a complete subset of rabbit Parameters
            # Then this is the established sql event. Add data accordingly (publishedEvent class)
            matchedRabbitEventModels.append(publishedEvent(None, rabbit, None, timeOnlyEvents))
        # Intersecting parameters were found, find the best match
        else:
            matchFound = False

            for potential in potentialEvents:

                actionID = potential.getLogLine()['Action ID']
                if actionID == 'UPDATE':
                    parameters_sql = getDatabaseParameters(potential, sqlEventModels)
                else:
                    parameters_sql = getSqlParameters(potential)

                intersection_sql = set(parameters_rabbit).intersection(parameters_sql)
                # Scenario 1: Perfect Match
                if len(intersection_sql) == len(parameters_rabbit):
                    potentialEvents.remove(potential)
                    sqlEvent = potential
                    # publisher = sqlEvent.getMicroservice()
                    publisher = sqlEvent
                    rabbitEvent = rabbit
                    rippleEvents = potentialEvents
                    matchedRabbitEventModels.append(publishedEvent(publisher, rabbitEvent, sqlEvent, rippleEvents))
                    matchFound = True
                    break

            # If no perfect match is found, combine the potential and time only events for further analysis using DK
            if matchFound == False:
                sqlEvent = None
                publisher = None
                rabbitEvent = rabbit
                rippleEvents = potentialEvents + timeOnlyEvents
                matchedRabbitEventModels.append(publishedEvent(publisher, rabbitEvent, sqlEvent, rippleEvents))

    return matchedRabbitEventModels