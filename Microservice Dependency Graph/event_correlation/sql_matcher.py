from lib.external import timedelta, parser, pytz
from lib.utilities.helpers import getSqlParameters
from lib.models import subscribedEvent

# Matches all response events with their sql events
def matchResponseSQL(responseEventModels, sqlEventModels):
    matchedResponseSQL = []

    # Loops through all the events and cross references with sql events

    for response in responseEventModels:
        parameters_response = list(response.getBodyDataModel().keys())
        time_response = parser.parse(response.getLogLine()["@t"])


        rangeStart = time_response - timedelta(milliseconds=500)
        rangeEnd = time_response + timedelta(milliseconds=500)

        potentialEvents = [] # These events contain either a complete or partial match of the parameters
        timeOnlyEvents = [] # These events don't contain any match of the parameters, they simply occur within the time range

        for sql in sqlEventModels:
            tempDate = sql.getLogLine()['Date'].split()[0]
            tempTime = sql.getLogLine()["Event Time "]
            time_sql = parser.parse(tempDate + " " + tempTime)
            time_sql = pytz.utc.localize(time_sql)

            # Step 1 Check if sql event is within range of rabbit event (Range will be +/- 0.5second)
            if rangeStart <= time_sql <= rangeEnd:
                # Step 2 checks to see if sql event type is INSERT or DELETE or UPDATEE
                # different methods needed for extracting the parameters from the statement
                parameters_sql = getSqlParameters(sql)
                # Step 3 check if the parameters match. If there are matching parameters append to PotentialEvents
                # otherwise append to timeOnlyEvents
                intersection = set(parameters_response).intersection(parameters_sql)
                if len(intersection) != 0:
                    potentialEvents.append(sql)
                # If there are no parameter matching, we will save the event for later comparisons
                else:
                    timeOnlyEvents.append(sql)


        # If no potential events are found, store only time matching events
        if potentialEvents == []:
            matchedResponseSQL.append(subscribedEvent(None, response, None, None, timeOnlyEvents, None, None, None))
        # Otherwise find the best matching potential event
        # priority matching -> Matching Microservice -> FIFO (Time based)
        else:
            matchFound = False
            for potential in potentialEvents:
                # Finds the first occurring microservice matching event
                if potential.getMicroservice() == response.getMicroservice():
                    sqlEvent = potential
                    publisher = sqlEvent.getMicroservice()
                    responseEvent = response
                    timeOnlyEvents = []
                    parameters_sql = getSqlParameters(sqlEvent)
                    intersection = set(parameters_response).intersection(parameters_sql)
                    xor = set(parameters_response) ^ set(parameters_sql)
                    totalParameters = parameters_sql + parameters_response
                    potentialEvents.remove(sqlEvent)
                    certainty = (len(totalParameters) - (len(xor))) / len(totalParameters)
                    xorSQL = set(xor).intersection(parameters_sql)
                    xorResponse = set(xor).intersection(parameters_response)
                    matchedResponseSQL.append(subscribedEvent(publisher, responseEvent, sqlEvent, potentialEvents, timeOnlyEvents, certainty, xorSQL, xorResponse))
                    matchFound = True
                    break
            # If no microservice matching events are found
            # No primary event is matched instead stores parameter matching events under ripple events
            # and time matching events under timeOnlyEvents
            if matchFound == False:
                matchedResponseSQL.append(subscribedEvent(None, responseEvent, None, potentialEvents, timeOnlyEvents, None, None, None))

    return matchedResponseSQL