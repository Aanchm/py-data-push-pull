# Introduction 
This contains some basic function blocks for working with data and python. This is updated as and when functions are needed and is focussed around working with using dataframes and dictionaries in python. It currently works with data stored either as csvs or json files locally, or in an InfluxDB database. 

# Requirements
- python 3
- All package requirements are in requirements.txt

# Build and Test
All functions are in the /src directory. To import the library: 
```
sys.path.append(rf"{Path(__file__).parent.parent}\src")
import push_pull_local as loc 
```
Tests are in the /tests directory



# Limitations
- Further tests need to be written against pushing and pulling from Influx
- More functions needed to be added for working with different data files
- The Influx data pull and push can be further optimised
