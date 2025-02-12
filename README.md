# Microservice Dependency Graph

Microservice architecture enables scalable and extensible systems by breaking down functionality into small, independent components. However, as these systems evolve, ensuring compliance with policies and design constraints becomes challenging. To address this, a technique for constructing a Microservices Dependency Graph (MDG). This graph models call and data dependencies between microservices, service buses, publish-subscribe frameworks, and databases.

The MDG is built using log analysis and probabilistic reasoning to associate logged events. It is a labeled, typed, directed multigraph where:

* Nodes represent microservices, service buses, and databases.

* Edges represent data exchanges and request interactions.

Currently the framework is only configured to work the "Pitstop - Garage Mangagement System" (https://github.com/EdwinVW/pitstop)application. Additional work needs to be done to handle different microservice and database logging standards.

## Project Structure
    ./
        │
        ├──Container_Data/                 # Contains docker container specific data 
        │   │
        │   ├── ContainerData.txt          # Obtained from Docker environment
        │   └── dockerData.txt             # Obtained from Docker environment
        │
        ├──Graph_Analysis/                 # Contains Multigraph 
        │   │
        │   └── DependencyMultiGraph.gml   # Dependency MultiGraph
        │ 
        ├──Logs/                           # Logs from the base application
        │   │
        │   ├── Corpus.clef                # Microservice logs
        │   ├── Invoice.log                # Database logs
        │   ├── Notification.log           # Database logs
        │   ├── Vehicle.log                # Database logs
        │   ├── Workshop.log               # Database logs
        │   └──  Workshopevent.log         # Database logs
        │
        ├──Microservice Dependency Graph/ # Novel Microservice Dependency Graphing Framework
        │   │
        │   ├── lib/                       # Shared models, externals, and utilities
        │   │   ├── models.py              # Data models (e.g., containerData)
        │   │   ├── externals.py           # External Libraries (e.g., Networkx)
        │   │   └── utilities/             # Helper functions
        │   │       └──  helpers.py        # Helper functions (e.g., getBodyData)
        │   │
        │   ├── pipeline/                  # Pipeline modules
        │   │   ├── container_discovery/   # Container discovery stage
        │   │   ├── event_extraction/      # Event extraction stage
        │   │   ├── event_correlation/     # Event correlation stage
        │   │   ├── knowledge_processing/  # Knowledge processing stage
        │   │   └── graph_construction/    # Graph construction stage
        │   │
        │   └── main.py                    # Main entry point for the pipeline
        │
        ├── LICENSE                        # Configuration settings
        ├── requirements.txt               # Required Libraries
        ├── README.md                      # Project documentation
        └── Thesis_AndresR.pdf/            # Published thesis

## Getting Started

### Prerequisites

* Python 3.10 or higher
* Docker
* Required Python Libraries (install via requirements.txt)


### Steps
1. Clone the repository:

```
git clone https://github.com/Andres-Osamu/Microservice_Dependency_Graph.git
cd microservice_Dependency_Graph
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Ensure Docker is running on your system
* [Currently the framework is only configured to work with Pitstop](https://github.com/EdwinVW/pitstop)

### Usage
1. Run the pipline
```
python main.py
```

2. The pipeline wil
    * Fetch container Data
    * Extract and process events
    * Correlate events and extract domain knowledge
    * Generate and export dependency graphs

3. Output files:
    * 

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc