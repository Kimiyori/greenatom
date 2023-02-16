# Tets tasks from greenatom


# What's done

:white_check_mark: Base 5 tasks

:white_check_mark: Task with SpaceX API and count number of publications


# How deploy

Run the following command:

```
docker-compose up --build
```
localhost will be on port 8000

# How use 

Data from SpaceX will be processed immediately after the first run of docker, 
so immediately after launch, you can go to the endpoints to check the count of publications

1. Navigate to following urls:

* localhost:8000/launch
* localhost:8000/mission
* localhost:8000/rocket

2. Check counts

#Diagram for SpaceX data structure

![Diagram](https://github.com/Kimiyori/greenatom/blob/main/data_scructure_spacex.drawio.png)
