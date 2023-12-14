"""
Heat Island Start Page

This module is the starting python page for Heat Island. Users can run this page to
access maps and the related local temperatures to analyze local heat fluctuations.
"""

import time
import geopandas as gpd
import pandas as pd
from heat_island.getcoor import select_coordinate
from heat_island.data_process import input_file_from_data_dir
from heat_island.geo_process import create_hexagon
from heat_island.height_acquire import get_centroid, average_building_height_with_centroid
from heat_island.height_acquire import height_acquire
from heat_island.model import train, predict, clean_data, load_model

cities = {"seattle": (47.606, -122.333)}
EXISTING = False
NEW = False
# boundaryPath = 'data/seattle-city-limits.geojson'

# If users want to input another set of data (new city)
print("We currently have data for the following city/cities:")
print(*cities)
response = input("What city would you like to view? Type 'New' for a new city. \n")

while not EXISTING:
    if response.lower() in cities :
        city = response.lower()
        # How to get access to the info needed for using Seattle map + Weather?
        EXISTING = True
    elif response.lower() == 'new':
        # 3. Request city name, and append to above list, cities
        city = input("What is the name of the new city?").lower()
        coordNew = input("What is the latitude/longitude coordinates of this city?")
        cities[city] = coordNew

        # Requests required data for new model formation/new height info
        print('''Move your weather data into the 'data' directory, using the following
        format: 'city_weather'. e.g. 'seattle_weather'.''')
        filler = input("Press any key to continue")
        print('''Move your city boundary into the 'data' directory, using the following
        format: 'city_boundary'. e.g. 'seattle_boundary'.''')
        filler = input("Press any key to continue")
        print('''Move your building data into the 'data' directory, using the following
        format: 'city_building'. e.g. 'seattle_building'.''')
        filler = input("Press any key to continue")

        radius = input("Please set the radius used for ML Training. Enter 0 for default.")
        EXISTING = True
        NEW = True
    else:
        print("This is not a valid response. Please either type a city name or 'New'.")
        response = input("What city would you like to view? Type 'New' for a new city.")

#input_file_from_data_dir(file name)
print("Please display both this page, and the following map simultaneously.")
time.sleep(2)  #Pauses to allow readers to read the message above

# Finding necessary directories
weatherFileDir = input_file_from_data_dir(city + "_weather.csv")
boundaryFileDir = input_file_from_data_dir(city + "_boundary.geojson")
buildingFileDir = input_file_from_data_dir(city + "_building_footprints.geojson")

MOREPOINTS = True
while MOREPOINTS:
    # Returns latitude/longitude coordinates.
    try:
        print("Please select the coordinate where you want to run the weather model.")
        x, y = select_coordinate(boundaryFileDir)
        region = create_hexagon(y, x)

        # Call hex -> height here
        if city == 'seattle':
            building = gpd.read_file(input_file_from_data_dir("seattle_building_footprints.geojson"))
        building = height_acquire(region)
        new_building = get_centroid(building)
        building_stats = average_building_height_with_centroid(new_building, region)
    except:
        print("No building data found please change coordinate")
        continue


    # If new city (i.e. no model yet), train
    if NEW:
        print("Please wait as the model trains on the new data.")
        # Cleans data
        data = clean_data(building_stats)
        train(data, fname = city + "_model.bin")
        NEW = False

    # Call the ML model here?
    print("This will take time. Please wait.")
    modelFileDir = input_file_from_data_dir(city + "_model.bin")
    model, scale = load_model(modelFileDir)

    # Call functions for applying ML here
    building_stats['Lat'] = y
    building_stats['Lon'] = x
    data = pd.DataFrame.from_records([building_stats])
    predictions = predict(model, scale, data)[0]

    # Display data currently in code output thing
    # Display data - What will it look like? Will create a folium pop-up regardless; can be a graph
    # or (various heights with various temperature predictions), or just a line of text as popup
    # and a text here directly.
    # Chart visualization look here:
    # https://python-visualization.github.io/folium/latest/user_guide/ui_elements/popups.html
    # Look at the Vega/Vega Lite Charts
    print(f'Temperature prediction is {predictions}')

    more = ''
    while more not in ('y', 'n'):
        more = input("Would you like to test more points? (y/n) \n")
        if more.lower() == 'y':
            break
        if more.lower() == 'n':
            print("Thank you for choosing `heat_island`")
            MOREPOINTS = False
            break
