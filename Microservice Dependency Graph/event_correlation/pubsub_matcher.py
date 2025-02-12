from lib.utilities.helpers import getBodyDict
from lib.external import parser, timedelta
from lib.models import  matchedPubSubEvent, potentialPubSubEvent

# Matching the publish events (rabbit) with the response events (invoice, notification and workshop)
# Matching will occur similarily to matchResponseSQL
# Match base on time range and matching parameters
def matchPubSub(rabbitEventModels, responseEventModels):

    matchedPubSub = []
    potentialPubSub = []
    domainKnowledge = {}
    x = 0
    counter = 0
    # For each rabbit events, iterate all of the given response events to find a match based on time and parameter values
    for rabbit in rabbitEventModels:
        if x == 3:
            print()
        bodyDictRabbit = getBodyDict(rabbit.getBodyDataModel())
        keys_rabbit = list(bodyDictRabbit.keys())
        values_rabbit = list(bodyDictRabbit.values())

        time_rabbit = parser.parse(rabbit.getLogLine()["@t"])
        rangeStart = time_rabbit - timedelta(milliseconds=500)
        rangeEnd = time_rabbit + timedelta(milliseconds=500)

        # Potential match will be used to create a list of potential events for each event
        # this is required as some events cannot be matched due to zero values provided by the rabbit event (ie DayHasPassed)
        # in this case no value matching event will be added to potential match
        # once all rabbit events have been matched as much as possible
        # Go through all the matching response events and remove them from a rabbit's potential match
        # at the end if a rabbit event still has potential match, then it is the response
        potentialMatch = []
        matchFound = False
        for response in responseEventModels:
            time_response = parser.parse(response.getLogLine()["@t"])
            # Step 1: Confirm time range
            if rangeStart <= time_response <= rangeEnd:
                if x == 3:
                    print()
                bodyDictResponse = getBodyDict(response.getBodyDataModel())
                keys_response = list(bodyDictResponse.keys())
                values_response = list(bodyDictResponse.values())

                # Step 2: if response values are a subset of rabbit values
                if (set(values_response).issubset(set(values_rabbit))):
                    matchedPubSub.append(matchedPubSubEvent(rabbit, response))
                    matchFound = True
                    for value in values_response:
                        positionRabbit = values_rabbit.index(value)
                        positionResponse = values_response.index(value)
                        dkRabbit = keys_rabbit[positionRabbit]
                        dkResponse = keys_response[positionResponse]
                        if dkRabbit != dkResponse:
                            if dkRabbit not in domainKnowledge:
                                domainKnowledge[dkRabbit] = list()
                            if dkResponse not in domainKnowledge[dkRabbit]:
                                domainKnowledge[dkRabbit].append(dkResponse)
                # Edge case - DayHasPassed
                else:
                    potentialMatch.append(response)
        # If no direct match is found, save the potentialMatches if any
        if matchFound == False and potentialMatch != []:
            potentialPubSub.append(potentialPubSubEvent(rabbit, potentialMatch))

        x += 1
    # All rabbit events have been traversed
    # Cross reference all potential matches with established matches, delete ones that are already associated with another event
    for potentialMatch in potentialPubSub:
        potentialPub = potentialMatch.getPublisher()
        potentialSub = potentialMatch.getSubscriber()
        for pubsub in matchedPubSub:
            matchedSub = pubsub.getSubscriber()
            if matchedSub in potentialSub:
                potentialSub.remove(matchedSub)

    # Remaining potential matches are established matches
    for potentialMatch in potentialPubSub:
        potentialPub = potentialMatch.getPublisher()
        potentialSub = potentialMatch.getSubscriber()
        if potentialSub != []:
            if len(potentialSub) > 1:
                matchedPubSub.append(matchedPubSubEvent(potentialPub, potentialSub))
            elif len(potentialSub) == 1:
                matchedPubSub.append(matchedPubSubEvent(potentialPub, potentialSub[0]))


    return matchedPubSub, domainKnowledge