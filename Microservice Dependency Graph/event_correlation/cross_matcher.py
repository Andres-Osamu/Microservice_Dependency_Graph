from lib.utilities.helpers import getBodyDict,getDatabaseParameters, getSqlParameters

def domainKnowledgeEventAnalysis(partialRabbitEventModels, dk, sqlEventModels):

    x=0
    publishedEventModels = partialRabbitEventModels
    for published in publishedEventModels:
        if published.getSqlEvent() == None:

            partialEvents = published.getPartialEvents()
            y=0
            eventsCertainty = []
            for partial in partialEvents:
                # parameters_rabbit = rabbit.getRabbitEvent().getBodyDataModel()
                parameters_rabbit = list(getBodyDict(published.getRabbitEvent().getBodyDataModel()))[:-2]
                actionID = partial.getLogLine()['Action ID']
                if actionID == 'UPDATE':
                    parameters_partial = getDatabaseParameters(partial, sqlEventModels)
                else:
                    parameters_partial = getSqlParameters(partial)

                intersection = set(parameters_rabbit).intersection(parameters_partial)
                differences =  set(parameters_rabbit).difference(set(intersection))
                matchedDifferences = []
                if x == 4 and y==2:
                    print()
                for difference in differences:
                    if difference in dk.keys():
                        values = dk[difference]
                        for value in values:
                            for parameter in parameters_partial:
                                if value == parameter:
                                    matchedDifferences.append(difference)

                y+=1
                eventsCertainty.append(len(intersection) + len(matchedDifferences))
            x += 1
            if x == 5:
                print()
            maxValue = max(eventsCertainty)
            maxIndex = eventsCertainty.index(maxValue)
            published.setSqlEvent(partialEvents[maxIndex])
            microservice = partialEvents[maxIndex].getMicroservice()
            published.setPublisher(microservice)
            print()

    return publishedEventModels
