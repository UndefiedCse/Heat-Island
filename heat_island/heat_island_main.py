"""
Heat Island Start Page

This module is the starting python page for Heat Island. Users can run this page to
access maps and the related local temperatures to analyze local heat fluctuations.
"""

import time
import geopandas as gpd

from heat_island.getcoor import select_coordinate
from heat_island.data_process import input_file_from_data_dir
from heat_island.geo_process import create_hexagon
from heat_island.height_acquire import get_centroid, average_building_height_with_centroid
from heat_island.height_acquire import height_acquire

cities = {"seattle": (47.606, -122.333)}
EXISTING = False
NEW = False
# boundaryPath = 'data/seattle-city-limits.geojson'

# If users want to input another set of data (new city)
print("We currently have data for the following city/cities:")
print(*cities)
response = input("What city would you like to view? Type 'New' for a new city.")

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
weatherFileDir = input_file_from_data_dir(city + "_weather")
boundaryFileDir = input_file_from_data_dir(city + "_boundary")
buildingFileDir = input_file_from_data_dir(city + "_building")

MOREPOINTS = True
while MOREPOINTS:
    # Returns latitude/longitude coordinates.
    print("Please select the coordinate where you want to run the weather model.")
    x, y = select_coordinate(boundaryFileDir)
    hex = create_hexagon(x, y, radius)

    # Call hex -> height here
    if city == 'seattle':
        building = gpd.read_file(input_file_from_data_dir("seattle_building_footprints.geojson"))
    building = height_acquire(hex)
    new_building = get_centroid(building)
    building_stats = average_building_height_with_centroid(new_building, hex)

    # Cleans data
    data = clean_data(building_stats)
    #NEED TO FIX ABOVE

    # If new city (i.e. no model yet), train
    if NEW:
        print("Please wait as the model trains on the new data.")
        train(data, fname = city + "_model")
        NEW = False
        
    # Call the ML model here?
    modelFileDir = input_file_from_data_dir(city + "_model")
    model, scale = load_model(modelFileDir)

    # Call functions for applying ML here
    print('''Please hold on as the algorithm computes
    the expected temperature within the region.''')
    predictions = predict(model, scale, data)

    # Display data currently in code output thing
    # Display data - What will it look like? Will create a folium pop-up regardless; can be a graph
    # or (various heights with various temperature predictions), or just a line of text as popup
    # and a text here directly.
    # Chart visualization look here: https://python-visualization.github.io/folium/latest/user_guide/ui_elements/popups.html
    # Look at the Vega/Vega Lite Charts
    display(predictions.to_string())
    
    more = ''
    while more not in ('y', 'n'):
        more = input("Would you like to test more points? (y/n)")
        if more.lower() == 'y':
            break
        if more.lower() == 'n':
            MOREPOINTS = False
            break
