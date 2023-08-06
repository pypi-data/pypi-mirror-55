# python-aio-geojson-geonetnz-volcano

[![Build Status](https://travis-ci.org/exxamalte/python-aio-geojson-geonetnz-volcano.svg)](https://travis-ci.org/exxamalte/python-aio-geojson-geonetnz-volcano)
[![Coverage Status](https://coveralls.io/repos/github/exxamalte/python-aio-geojson-geonetnz-volcano/badge.svg?branch=master)](https://coveralls.io/github/exxamalte/python-aio-geojson-geonetnz-volcano?branch=master)
[![PyPi](https://img.shields.io/pypi/v/aio-geojson-geonetnz-volcano.svg)](https://pypi.python.org/pypi/aio-geojson-geonetnz-volcano)
[![Version](https://img.shields.io/pypi/pyversions/aio-geojson-geonetnz-volcano.svg)](https://pypi.python.org/pypi/aio-geojson-geonetnz-volcano)

This library for convenient async access to 
[GeoNet NZ Volcanic Alert Level](https://api.geonet.org.nz/#val) feed.


## Installation
`pip install aio-geojson-geonetnz-volcano`

## Usage
See below for examples of how this library can be used. After instantiating a 
particular class - feed or feed manager - and supply the required parameters, 
you can call `update` to retrieve the feed data. The return value 
will be a tuple of a status code and the actual data in the form of a list of 
feed entries specific to the selected feed.

Status Codes
* _OK_: Update went fine and data was retrieved. The library may still 
  return empty data, for example because no entries fulfilled the filter 
  criteria.
* _OK_NO_DATA_: Update went fine but no data was retrieved, for example 
  because the server indicated that there was not update since the last request.
* _ERROR_: Something went wrong during the update

**Parameters**

| Parameter          | Description                               |
|--------------------|-------------------------------------------|
| `home_coordinates` | Coordinates (tuple of latitude/longitude) |

**Supported Filters**

| Filter |                 | Description |
|--------|-----------------|-------------|
| Radius | `filter_radius` | Radius in kilometers around the home coordinates in which events from feed are included. |

**Example**
```python
import asyncio
from aiohttp import ClientSession
from aio_geojson_geonetnz_volcano import GeonetnzVolcanoFeed
async def main() -> None:
    async with ClientSession() as websession:    
        # Home Coordinates: Latitude: -41.2, Longitude: 174.7
        # Filter radius: 200 km
        feed = GeonetnzVolcanoFeed(websession, 
                                   (-41.2, 174.7),
                                   filter_radius=200)
        status, entries = await feed.update()
        print(status)
        print(entries)
asyncio.get_event_loop().run_until_complete(main())
```

## Feed entry properties
Each feed entry is populated with the following properties:

| Name             | Description                                           | Feed attribute |
|------------------|-------------------------------------------------------|----------------|
| geometry         | All geometry details of this entry.                   | `geometry`     |
| coordinates      | Best coordinates (latitude, longitude) of this entry. | `geometry`     |
| external_id      | The unique public identifier for this volcano.        | `volcanoID`    |
| title            | Volcano title.                                        | `volcanoTitle` |
| attribution      | Attribution of the feed.                              | n/a            |
| distance_to_home | Distance in km of this entry to the home coordinates. | n/a            |
| alert_level      | Volcanic alert level (0-5).                           | `level`        |
| activity         | Volcanic activity.                                    | `activity`     |
| hazards          | Most likely hazards.                                  | `hazards`      |


## Feed Manager

The Feed Manager helps managing feed updates over time, by notifying the 
consumer of the feed about new feed entries, updates and removed entries 
compared to the last feed update.

* If the current feed update is the first one, then all feed entries will be 
  reported as new. The feed manager will keep track of all feed entries' 
  external IDs that it has successfully processed.
* If the current feed update is not the first one, then the feed manager will 
  produce three sets:
  * Feed entries that were not in the previous feed update but are in the 
    current feed update will be reported as new.
  * Feed entries that were in the previous feed update and are still in the 
    current feed update will be reported as to be updated.
  * Feed entries that were in the previous feed update but are not in the 
    current feed update will be reported to be removed.
* If the current update fails, then all feed entries processed in the previous
  feed update will be reported to be removed.

After a successful update from the feed, the feed manager provides two
different dates:

* `last_update` will be the timestamp of the last update from the feed 
  irrespective of whether it was successful or not.
* `last_update_successful` will be the timestamp of the last successful update 
  from the feed. This date may be useful if the consumer of this library wants 
  to treat intermittent errors from feed updates differently.
* `last_timestamp` is not available for this feed.
