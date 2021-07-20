[![Language](https://img.shields.io/badge/language-python-blue.svg)](https://www.python.org/)

# Google Maps & Open Street Map Screenshot Taker

## Installation

- Install Chrome Webdriver or Firefox Geckodriver
- Install Conda
- Create Conda environment ```conda env create```
- Modify _take_screenshot_ function inside **test.py**
- Run ```python test.py```

## Procedure

- If you want to have matching from OSM and GMaps, you need to run the test.py with ```osm=True```. This will create
  a **osm_output.txt** file which GMaps read this file to generate matched images. Then you should set ```osm=False```
  and set ```gmaps``` or ```gmaps_satellite``` to True, so that the matching will be done.
- If you don't want to read from OSM (just remove the **osm_ouput.txt** from the directory), the GMaps will not skip any
  row or cols.

## Parameters

- ```lat``` Latitude of the top left corner **(float)**
- ```long``` Longitude of the top left corner **(float)**
- ```row``` Row count **(int)**
- ```col``` Col count **(int)**
- ```file_name``` File name of the output images **(string)**
- ```number``` Number of the file name {file_name}-{number}.png **(int)**
- ```crop_status``` Determine whether crop the image (by crop_size) or not **(bool)**
- ```gmaps``` Take a screenshot from Google Maps Map View **(bool)**
- ```gmaps_satellite``` Take a screenshot from Google Maps Satellite View **(bool)**
- ```osm``` Generate an image from Open Street Maps **(bool)**
- ```zoom``` Zoom value only applicable for Google Maps **(int (between 0 and 21))**

## Notes

- Based on [OSMnx](https://github.com/gboeing/osmnx)
- The Chromedriver inside the repo is for **macOS**. The version: _ChromeDriver 90.0.4430.24_
- Download the latest or suitable version for Chrome from https://chromedriver.chromium.org/downloads
- Download the latest or suitable version for Firefox Geckodriver from https://github.com/mozilla/geckodriver/releases
