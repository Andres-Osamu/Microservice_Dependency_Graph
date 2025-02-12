# Import functions from the collector module
# - getContainerData: Retrieves container information (name, IP, ID) from Docker.
# - writeContainerData: Writes container data to a file for persistence.
from .collector import getContainerData, writeContainerData

# Import functions from the loader module
# - readContainerData: Reads container data from a file and creates container objects.
from .loader import readContainerData

# Define the public API of the module
# This list specifies which functions are exposed when using `from container_discovery import *`
# - getContainerData: Function to fetch container data from Docker.
# - writeContainerData: Function to save container data to a file.
# - readContainerData: Function to load container data from a file.
__all__ = [
    "getContainerData",
    "writeContainerData",
    "readContainerData",
]