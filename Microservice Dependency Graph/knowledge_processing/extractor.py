from lib.external import parser

# Method will go through the event model and extract all the parameters and values
def extractDomainKnowledge(dk, eventModels):

    # Event values will be the keys
    # Event keys will be the values
    for event in eventModels:
        eventDict = getBodyDict(event.getBodyDataModel())
        parameters = list(eventDict.keys())
        datas = list(eventDict.values())

        for parameter in parameters:
            data = eventDict[parameter]
            if data not in dk.keys():
                dk[data] = [parameter]
            elif parameter not in dk[data]:
                dk[data].append(parameter)

    return dk


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