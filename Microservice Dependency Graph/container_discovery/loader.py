from lib.models import containerData

# Reads the container data file and creates a list of container objects
def readContainerData():
    containerList = []

    containerCorpus = open("./Container Data/ContainerData.txt", "r")

    lines = containerCorpus.readlines()

    for line in lines:
        line = line.rstrip("\n")
        data = line.split("\t")
        containerList.append(containerData(data[1], data[2], data[0]))

    containerCorpus.close()

    return containerList