# Method will return a dictionary with each unique parameter (that has synonyms) as a key, and all the synonyms as its values
# This can be used to quickly search the synonyms of an attribute
def filterDkCorpus(dk):
    filteredDK = dk
    #Removes parameters without synonyms
    # for key in dk.keys():
    #     if len(dk[key]) > 1:
    #         filteredDK[key] = dk[key]

    uniqueDK = {}
    #Removes duplicate parameters
    for key, values in filteredDK.items():
        if values not in uniqueDK.values():
            uniqueDK[key] = values

    finalDK = {}
    #Each parameter is set as a key with all its matching keys as its values
    for key, values in uniqueDK.items():
        for value in values:
            if value == "JobId":
                print()
            if finalDK.get(value) == None:
                finalDK[value] = values
            else:
                for element in values:
                    if element not in finalDK[value]:
                        finalDK[value] = finalDK[value] + [element]


    return finalDK

# This will filter out the DK such that there will be one main key for a set of attributes
# The
def filterDkUnique(dk):
    uniqueDK = {}
    # Removes duplicate parameters
    for key, values in dk.items():
        if values not in uniqueDK.values():
            uniqueDK[key] = values

    # same as uniqueDK except it replaces the key with one of the values (ie parameter becomes a key not an actual data value)
    sortedDK = {}
    for key, values in uniqueDK.items():
        if "MessageId" not in values and "MessageType" not in values:
            if len(set(values).intersection(set(sortedDK.keys()))) == 0:
                sortedDK[values[0]] = values[0:]
            else:
               temp = sortedDK[values[0]]
               for value in values:
                   if value not in temp:
                       sortedDK[values[0]].append(value)

    return sortedDK