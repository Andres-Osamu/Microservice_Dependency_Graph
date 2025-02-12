from lib.external import docker
from lib.models import containerData


# Gets the container information for each microservice
# Note, the IPs are dynamic and change upon each startup
# For consistency the Audit Logs and Container data extraction must be performed on the same docker instance
def getContainerData():
    containerList = []
    client = docker.from_env()
    for container in client.containers.list():
        data = container.attrs
        # ip = container.attrs['NetworkSettings']['Networks']['src_default']['IPAddress']
        containerList.append(containerData(data['Name'], data['NetworkSettings']['Networks']['src_default']['IPAddress'], data['Id']))
        print()



    return containerList


# Store the container data in a file
def writeContainerData(data):

    # Original Filename, commented out for safety
    f = open("./Container_Data/ContainerData.txt", "a")
    # f = open("ContainerData_SCRAP.txt", "a")

    for container in data:
        name = container.getName()
        id = container.getID()
        ip = container.getIP()

        f.write(id + "\t" + name + "\t" + ip + "\n")

    f.close()