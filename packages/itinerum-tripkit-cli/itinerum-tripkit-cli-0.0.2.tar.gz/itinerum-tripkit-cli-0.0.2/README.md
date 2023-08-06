
# itinerum-tripkit-cli

[![Python Version](https://img.shields.io/badge/Python-3.6%7C3.7-blue.svg?style=flat-square)]()

The `itinerum-tripkit-cli` makes using the `itinerum-tripkit` library fast and simple:

1. Create an `./input` and `./output` directory. Copy source .csv data to `./input`.
2. Edit a `config.py` file with data filepaths and trip processing parameters.
3. Run the tripkit command-line tool:
	### Itinerum
	```bash
	$ pip install itinerum-tripkit-cli
	$ tripkit-cli -v -c config.py
	```

	### QStarz
	```bash
	$ pip install itinerum-tripkit-cli
	$ tripkit-cli -v -c config.py
	```

## Quick comands
*Show help:*
```bash
$ tripkit-cli --help
```

*Increase logging verbosity:*
```bash
$ tripkit-cli -v   # verbose
$ tripkit-cli -vv  # very verbose
```

*Supply config:*
```bash
$ tripkit-cli -c config.py
```

## Config
*Sample config:*

```python
SURVEY_NAME = 'itinerum_survey'

# path of raw data directory exported from Itinerum platform or Qstarz
INPUT_DATA_DIR = './input/csv-data-dir'
# types: "itinerum" or "qstarz"
INPUT_DATA_TYPE = 'itinerum'

# path of export data from itinerum-cli
OUTPUT_DATA_DIR = './output'

# path of subway station entrances .csv for trip detection
SUBWAY_STATIONS_FP = './input/subway_stations/stations.csv'

# trip detection parameters
TRIP_DETECTION_BREAK_INTERVAL_SECONDS = 300
TRIP_DETECTION_SUBWAY_BUFFER_METERS = 300
TRIP_DETECTION_COLD_START_DISTANCE_METERS = 750
TRIP_DETECTION_ACCURACY_CUTOFF_METERS = 50

# timezone of study area for calculating complete trip days
TIMEZONE = 'America/Montreal'

# semantic location radius for activity dwell tallies
SEMANTIC_LOCATION_PROXIMITY_METERS = 50

# OSRM map matcher API URLs
MAP_MATCHING_BIKING_API_URL = 'https://osrm.server.com/match/v1/biking/'
MAP_MATCHING_DRIVING_API_URL = 'https://osrm.server.com/match/v1/driving/'
MAP_MATCHING_WALKING_API_URL = 'https://osrm.server.com/match/v1/walking/'
```